import asyncio
import ipaddress
import re
import socket
from pathlib import Path
from tempfile import SpooledTemporaryFile
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


async def ingest_media_url(
    url: str,
    db: Session,
    user: User | None = None,
    *,
    client: httpx.AsyncClient | None = None,
):
    temporary_file, size, final_url = await download_remote_media(
        url,
        client=client,
    )

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
