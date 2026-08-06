import asyncio
import ipaddress
import re
import shutil
import socket
import subprocess
from pathlib import Path
from tempfile import SpooledTemporaryFile, TemporaryDirectory
from urllib.parse import unquote, urljoin, urlsplit

import httpx
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from starlette.datastructures import Headers

from app.core.config import settings
from app.models.user import User
from app.services.upload_service import (
    MIME_EXTENSIONS,
    create_upload,
    detect_media_mime,
    validate_media_mime,
)


REDIRECT_STATUSES = {301, 302, 303, 307, 308}
DOWNLOAD_CHUNK_SIZE = 64 * 1024
YOUTUBE_HOSTS = {
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "youtu.be",
}
REDDIT_HOSTS = {
    "reddit.com",
    "www.reddit.com",
    "old.reddit.com",
    "new.reddit.com",
    "redd.it",
}
UNSUPPORTED_SOCIAL_HOSTS = {
    "instagram": {"instagram.com", "www.instagram.com"},
    "x": {"x.com", "www.x.com", "twitter.com", "www.twitter.com"},
    "tiktok": {"tiktok.com", "www.tiktok.com"},
    "facebook": {"facebook.com", "www.facebook.com", "fb.watch"},
}


class URLIngestionError(Exception):
    status_code = 400

    def __init__(self, detail: str):
        super().__init__(detail)
        self.detail = detail


class DownloadTimeoutError(URLIngestionError):
    status_code = 504


class DownloadFailedError(URLIngestionError):
    status_code = 502


class DownloadTooLargeError(URLIngestionError):
    status_code = 413


class MediaValidationError(URLIngestionError):
    status_code = 415


class UnsupportedPlatformError(URLIngestionError):
    status_code = 422


class ExternalDownloaderUnavailableError(URLIngestionError):
    status_code = 503


async def ingest_media_url(
    url: str,
    db: Session,
    user: User | None = None,
    *,
    client: httpx.AsyncClient | None = None,
):
    adapter = adapter_for_url(url)
    temporary_file, size, final_url = await adapter.download(
        url,
        client=client,
    )

    return await create_upload_from_download(
        temporary_file,
        size,
        final_url,
        db,
        user,
    )


class DirectMediaURLAdapter:
    async def download(
        self,
        url: str,
        *,
        client: httpx.AsyncClient | None = None,
    ) -> tuple[SpooledTemporaryFile, int, str]:
        return await download_remote_media(url, client=client)


class YouTubeURLAdapter:
    async def download(
        self,
        url: str,
        *,
        client: httpx.AsyncClient | None = None,
    ) -> tuple[SpooledTemporaryFile, int, str]:
        if client is not None:
            raise UnsupportedPlatformError(
                "Mock HTTP clients are only supported for direct media URLs."
            )

        await validate_remote_url(url)

        if shutil.which("yt-dlp") is None:
            raise ExternalDownloaderUnavailableError(
                "YouTube URL ingestion requires yt-dlp to be installed."
            )

        return await asyncio.to_thread(_download_with_ytdlp, url)


class RedditURLAdapter:
    async def download(
        self,
        url: str,
        *,
        client: httpx.AsyncClient | None = None,
    ) -> tuple[SpooledTemporaryFile, int, str]:
        await validate_remote_url(url)
        media_url = await extract_reddit_media_url(url, client=client)
        return await download_remote_media(media_url, client=client)


def adapter_for_url(url: str):
    platform = detect_url_platform(url)
    if platform == "direct":
        return DirectMediaURLAdapter()
    if platform == "youtube":
        return YouTubeURLAdapter()
    if platform == "reddit":
        return RedditURLAdapter()
    raise UnsupportedPlatformError(
        f"{platform.title()} URL ingestion is not available yet. "
        "Use a direct media URL for now."
    )


def detect_url_platform(url: str) -> str:
    try:
        parsed = urlsplit(url)
    except ValueError as exc:
        raise URLIngestionError("URL is malformed.") from exc

    hostname = (parsed.hostname or "").rstrip(".").lower()
    if hostname in YOUTUBE_HOSTS or hostname.endswith(".youtube.com"):
        return "youtube"
    if hostname in REDDIT_HOSTS or hostname.endswith(".reddit.com"):
        return "reddit"

    for platform, hosts in UNSUPPORTED_SOCIAL_HOSTS.items():
        if any(hostname == host or hostname.endswith(f".{host}") for host in hosts):
            return platform

    return "direct"


async def create_upload_from_download(
    temporary_file: SpooledTemporaryFile,
    size: int,
    final_url: str,
    db: Session,
    user: User | None = None,
):

    try:
        header_bytes = temporary_file.read(8192)
        temporary_file.seek(0)
        detected_mime = detect_media_mime(header_bytes)

        try:
            validate_media_mime(detected_mime)
        except HTTPException as exc:
            raise MediaValidationError(exc.detail) from exc

        filename = _safe_filename(final_url, detected_mime)
        upload = UploadFile(
            file=temporary_file,
            size=size,
            filename=filename,
            headers=Headers({"content-type": detected_mime}),
        )
        return await create_upload(upload, db, user)
    finally:
        temporary_file.close()


def _download_with_ytdlp(url: str) -> tuple[SpooledTemporaryFile, int, str]:
    with TemporaryDirectory() as directory:
        output_template = str(Path(directory) / "%(id)s.%(ext)s")
        command = [
            "yt-dlp",
            "--no-playlist",
            "--max-filesize",
            str(settings.MAX_UPLOAD_SIZE_BYTES),
            "-f",
            "mp4/best[ext=mp4]/best",
            "-o",
            output_template,
            url,
        ]

        try:
            subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                timeout=settings.URL_SOCIAL_DOWNLOAD_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired as exc:
            raise DownloadTimeoutError("YouTube download timed out.") from exc
        except subprocess.CalledProcessError as exc:
            output = f"{exc.stdout}\n{exc.stderr}".lower()
            if "larger than max-filesize" in output:
                raise DownloadTooLargeError(
                    "Remote file exceeds the maximum size of "
                    f"{settings.MAX_UPLOAD_SIZE_BYTES} bytes."
                ) from exc
            raise DownloadFailedError("YouTube download failed.") from exc

        downloaded_files = [
            path
            for path in Path(directory).iterdir()
            if path.is_file() and not path.name.endswith(".part")
        ]
        if not downloaded_files:
            raise DownloadFailedError("YouTube download produced no media file.")

        media_path = max(downloaded_files, key=lambda path: path.stat().st_size)
        size = media_path.stat().st_size
        if size == 0:
            raise MediaValidationError("Downloaded file is empty or corrupted.")
        if size > settings.MAX_UPLOAD_SIZE_BYTES:
            raise DownloadTooLargeError(
                "Remote file exceeds the maximum size of "
                f"{settings.MAX_UPLOAD_SIZE_BYTES} bytes."
            )

        temporary_file = SpooledTemporaryFile(
            max_size=settings.MAX_UPLOAD_SIZE_BYTES,
            mode="w+b",
        )
        with media_path.open("rb") as source:
            shutil.copyfileobj(source, temporary_file)
        temporary_file.seek(0)

        return temporary_file, size, media_path.name


async def extract_reddit_media_url(
    url: str,
    *,
    client: httpx.AsyncClient | None = None,
) -> str:
    listing_url = _reddit_listing_url(url)
    owns_client = client is None
    active_client = client or httpx.AsyncClient(
        timeout=httpx.Timeout(settings.URL_SOCIAL_DOWNLOAD_TIMEOUT_SECONDS),
        follow_redirects=False,
        trust_env=False,
        headers={"User-Agent": "MediaForge-Guard/1.0"},
    )

    try:
        await validate_remote_url(listing_url)
        async with active_client.stream(
            "GET",
            listing_url,
            follow_redirects=False,
        ) as response:
            _validate_connected_peer(response)
            if response.status_code >= 300:
                raise DownloadFailedError(
                    "Reddit blocked this link or the post metadata could not be "
                    "loaded. Try a direct image/video URL from the post, a "
                    "YouTube link, or another direct media URL."
                )
            _validate_social_metadata_length(response.headers)
            payload = b""
            async for chunk in response.aiter_bytes(DOWNLOAD_CHUNK_SIZE):
                payload += chunk
                if len(payload) > settings.URL_SOCIAL_METADATA_MAX_BYTES:
                    raise DownloadTooLargeError(
                        "Remote metadata exceeds the maximum size of "
                        f"{settings.URL_SOCIAL_METADATA_MAX_BYTES} bytes."
                    )
    except httpx.TimeoutException as exc:
        raise DownloadTimeoutError("Reddit metadata download timed out.") from exc
    except httpx.HTTPError as exc:
        raise DownloadFailedError("Reddit metadata download failed.") from exc
    finally:
        if owns_client:
            await active_client.aclose()

    try:
        listing = httpx.Response(200, content=payload).json()
    except ValueError as exc:
        raise DownloadFailedError("Reddit metadata was not valid JSON.") from exc

    media_url = _extract_reddit_media_url_from_listing(listing)
    if media_url is None:
        raise UnsupportedPlatformError(
            "Reddit URL did not contain a direct media item. "
            "Use a Reddit image/video post or a direct media URL."
        )

    return media_url.replace("&amp;", "&")


def _reddit_listing_url(url: str) -> str:
    parsed = urlsplit(url)
    path = parsed.path.rstrip("/")
    if not path:
        raise URLIngestionError("URL is malformed.")
    if path.endswith(".json"):
        return url
    return f"{parsed.scheme}://{parsed.netloc}{path}.json"


def _extract_reddit_media_url_from_listing(listing) -> str | None:
    post = _first_reddit_post(listing)
    if not isinstance(post, dict):
        return None

    media = post.get("secure_media") or post.get("media") or {}
    reddit_video = media.get("reddit_video") if isinstance(media, dict) else None
    if isinstance(reddit_video, dict) and reddit_video.get("fallback_url"):
        return reddit_video["fallback_url"]

    url = post.get("url_overridden_by_dest") or post.get("url")
    if isinstance(url, str) and _looks_like_media_url(url):
        return url

    preview = post.get("preview")
    if isinstance(preview, dict):
        images = preview.get("images")
        if isinstance(images, list) and images:
            source = images[0].get("source") if isinstance(images[0], dict) else None
            if isinstance(source, dict) and isinstance(source.get("url"), str):
                return source["url"]

    return None


def _first_reddit_post(listing):
    if isinstance(listing, list) and listing:
        listing = listing[0]
    if not isinstance(listing, dict):
        return None
    data = listing.get("data")
    children = data.get("children") if isinstance(data, dict) else None
    if not isinstance(children, list) or not children:
        return None
    child_data = children[0].get("data") if isinstance(children[0], dict) else None
    return child_data if isinstance(child_data, dict) else None


def _looks_like_media_url(url: str) -> bool:
    path = urlsplit(url).path.lower()
    return any(path.endswith(extension) for extension in MIME_EXTENSIONS.values())


async def download_remote_media(
    url: str,
    *,
    client: httpx.AsyncClient | None = None,
) -> tuple[SpooledTemporaryFile, int, str]:
    owns_client = client is None
    active_client = client or httpx.AsyncClient(
        timeout=httpx.Timeout(settings.URL_DOWNLOAD_TIMEOUT_SECONDS),
        follow_redirects=False,
        trust_env=False,
        headers={"User-Agent": "MediaForge-Guard/1.0"},
    )
    current_url = url

    try:
        for redirect_count in range(settings.URL_MAX_REDIRECTS + 1):
            await validate_remote_url(current_url)

            try:
                async with active_client.stream(
                    "GET",
                    current_url,
                    follow_redirects=False,
                ) as response:
                    _validate_connected_peer(response)
                    if response.status_code in REDIRECT_STATUSES:
                        if redirect_count >= settings.URL_MAX_REDIRECTS:
                            raise DownloadFailedError(
                                "Remote URL exceeded the maximum of "
                                f"{settings.URL_MAX_REDIRECTS} redirects."
                            )
                        location = response.headers.get("location")
                        if not location:
                            raise DownloadFailedError(
                                "Remote server returned a redirect "
                                "without a Location header."
                            )
                        current_url = urljoin(current_url, location)
                        continue

                    if response.status_code >= 300:
                        raise DownloadFailedError(
                            "Remote download failed with HTTP status "
                            f"{response.status_code}."
                        )

                    _validate_content_length(response.headers)
                    temporary_file = SpooledTemporaryFile(
                        max_size=settings.MAX_UPLOAD_SIZE_BYTES,
                        mode="w+b",
                    )
                    size = 0
                    try:
                        async for chunk in response.aiter_bytes(
                            DOWNLOAD_CHUNK_SIZE
                        ):
                            size += len(chunk)
                            if size > settings.MAX_UPLOAD_SIZE_BYTES:
                                raise DownloadTooLargeError(
                                    "Remote file exceeds the maximum "
                                    f"size of {settings.MAX_UPLOAD_SIZE_BYTES} "
                                    "bytes."
                                )
                            temporary_file.write(chunk)
                    except Exception:
                        temporary_file.close()
                        raise

                    if size == 0:
                        temporary_file.close()
                        raise MediaValidationError(
                            "Downloaded file is empty or corrupted."
                        )

                    temporary_file.seek(0)
                    return temporary_file, size, current_url
            except httpx.TimeoutException as exc:
                raise DownloadTimeoutError(
                    "Remote download timed out."
                ) from exc
            except httpx.HTTPError as exc:
                raise DownloadFailedError(
                    "Remote download failed."
                ) from exc

        raise DownloadFailedError("Remote redirect handling failed.")
    finally:
        if owns_client:
            await active_client.aclose()


async def validate_remote_url(url: str) -> None:
    if not isinstance(url, str) or not url.strip():
        raise URLIngestionError("URL is required.")
    if any(character.isspace() for character in url):
        raise URLIngestionError("URL is malformed.")

    try:
        parsed = urlsplit(url)
        port = parsed.port
    except ValueError as exc:
        raise URLIngestionError("URL is malformed.") from exc

    if parsed.scheme.lower() not in {"http", "https"}:
        raise URLIngestionError(
            "Only http and https URLs are supported."
        )
    if not parsed.hostname:
        raise URLIngestionError("URL must include a valid host.")
    if parsed.username is not None or parsed.password is not None:
        raise URLIngestionError("URLs containing credentials are rejected.")

    hostname = parsed.hostname.rstrip(".").lower()
    if hostname == "localhost" or hostname.endswith(".localhost"):
        raise URLIngestionError("Local and private addresses are rejected.")

    effective_port = port or (443 if parsed.scheme.lower() == "https" else 80)
    addresses = await asyncio.to_thread(
        _resolve_host_addresses,
        hostname,
        effective_port,
    )
    if not addresses:
        raise URLIngestionError("URL host could not be resolved.")
    if any(not address.is_global for address in addresses):
        raise URLIngestionError("Local and private addresses are rejected.")


def _resolve_host_addresses(
    hostname: str,
    port: int,
) -> set[ipaddress.IPv4Address | ipaddress.IPv6Address]:
    try:
        literal = ipaddress.ip_address(hostname)
    except ValueError:
        try:
            records = socket.getaddrinfo(
                hostname,
                port,
                type=socket.SOCK_STREAM,
            )
        except socket.gaierror as exc:
            raise URLIngestionError(
                "URL host could not be resolved."
            ) from exc
        return {
            ipaddress.ip_address(record[4][0])
            for record in records
        }
    return {literal}


def _validate_content_length(headers: httpx.Headers) -> None:
    content_length = headers.get("content-length")
    if content_length is None:
        return
    try:
        declared_size = int(content_length)
    except ValueError:
        return
    if declared_size > settings.MAX_UPLOAD_SIZE_BYTES:
        raise DownloadTooLargeError(
            "Remote file exceeds the maximum size of "
            f"{settings.MAX_UPLOAD_SIZE_BYTES} bytes."
        )


def _validate_social_metadata_length(headers: httpx.Headers) -> None:
    content_length = headers.get("content-length")
    if content_length is None:
        return
    try:
        declared_size = int(content_length)
    except ValueError:
        return
    if declared_size > settings.URL_SOCIAL_METADATA_MAX_BYTES:
        raise DownloadTooLargeError(
            "Remote metadata exceeds the maximum size of "
            f"{settings.URL_SOCIAL_METADATA_MAX_BYTES} bytes."
        )


def _validate_connected_peer(response: httpx.Response) -> None:
    network_stream = response.extensions.get("network_stream")
    if network_stream is None:
        return
    peer = network_stream.get_extra_info("server_addr")
    if not peer:
        return
    try:
        address = ipaddress.ip_address(peer[0])
    except ValueError:
        return
    if not address.is_global:
        raise URLIngestionError(
            "Remote connection resolved to a local or private address."
        )


def _safe_filename(url: str, detected_mime: str) -> str:
    raw_name = Path(unquote(urlsplit(url).path)).name
    stem = Path(raw_name).stem if raw_name else "remote-media"
    safe_stem = re.sub(r"[^A-Za-z0-9._-]+", "_", stem).strip("._")
    safe_stem = safe_stem[:100] or "remote-media"
    return safe_stem + MIME_EXTENSIONS[detected_mime]
