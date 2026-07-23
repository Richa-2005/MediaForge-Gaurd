import asyncio
import ipaddress
from unittest.mock import Mock

import httpx
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.api.v1 import uploads
from app.api.dependencies import get_current_user
from app.api.v1.router import api_router
from app.core.config import settings
from app.database.session import get_db
from app.models.base import Base
from app.models.processing_run import ProcessingRun
from app.models.upload import Upload
from app.models.user import User
from app.services import url_ingestion_service as service


JPEG_BYTES = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00" + b"\x00" * 100
MP4_BYTES = (
    b"\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00mp42isom"
    + b"\x00" * 100
)
WAV_BYTES = (
    b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00"
    b"\x40\x1f\x00\x00\x80\x3e\x00\x00\x02\x00\x10\x00data\x00\x00\x00\x00"
)
TEXT_BYTES = b"This is a plain text media file.\n"
PUBLIC_ADDRESSES = {ipaddress.ip_address("8.8.8.8")}
REAL_RESOLVER = service._resolve_host_addresses


@pytest.fixture(autouse=True)
def public_dns(monkeypatch):
    monkeypatch.setattr(
        service,
        "_resolve_host_addresses",
        lambda _hostname, _port: PUBLIC_ADDRESSES,
    )


def run(coroutine):
    return asyncio.run(coroutine)


async def ingest_with_handler(monkeypatch, url, handler):
    captured = {}

    async def fake_create_upload(upload, db, user=None):
        captured["bytes"] = await upload.read()
        captured["content_type"] = upload.content_type
        captured["filename"] = upload.filename
        captured["db"] = db
        captured["user"] = user
        return {
            "upload_id": 12,
            "status": "queued",
            "media_type": upload.content_type.split("/", 1)[0],
            "is_duplication": False,
        }

    monkeypatch.setattr(service, "create_upload", fake_create_upload)
    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(
        transport=transport,
        follow_redirects=False,
    ) as client:
        result = await service.ingest_media_url(
            url,
            Mock(),
            client=client,
        )
    return result, captured


@pytest.mark.parametrize(
    ("path", "content", "mime", "extension", "media_type"),
    [
        ("image.jpg", JPEG_BYTES, "image/jpeg", ".jpg", "image"),
        ("video.mp4", MP4_BYTES, "video/mp4", ".mp4", "video"),
        ("audio.wav", WAV_BYTES, "audio/x-wav", ".wav", "audio"),
        ("file.txt", TEXT_BYTES, "text/plain", ".txt", "text"),
    ],
)
def test_valid_direct_media_urls(
    monkeypatch,
    path,
    content,
    mime,
    extension,
    media_type,
):
    def handler(request):
        return httpx.Response(
            200,
            content=content,
            headers={
                # Deliberately untrusted and incorrect.
                "content-type": "application/octet-stream",
            },
            request=request,
        )

    result, captured = run(
        ingest_with_handler(
            monkeypatch,
            f"https://media.example/{path}",
            handler,
        )
    )

    assert result["media_type"] == media_type
    assert captured["bytes"] == content
    assert captured["content_type"] == mime
    assert captured["filename"].endswith(extension)


@pytest.mark.parametrize(
    "url",
    [
        "file:///tmp/media.mp4",
        "ftp://example.com/media.mp4",
        "data:text/plain,hello",
        "javascript:alert(1)",
    ],
)
def test_unsupported_url_schemes(url):
    with pytest.raises(service.URLIngestionError, match="http and https"):
        run(service.validate_remote_url(url))


def test_download_timeout(monkeypatch):
    def handler(request):
        raise httpx.ReadTimeout("timed out", request=request)

    with pytest.raises(service.DownloadTimeoutError, match="timed out"):
        run(
            ingest_with_handler(
                monkeypatch,
                "https://media.example/file.txt",
                handler,
            )
        )


def test_oversized_download(monkeypatch):
    monkeypatch.setattr(service.settings, "MAX_UPLOAD_SIZE_BYTES", 10)

    def handler(request):
        return httpx.Response(200, content=b"x" * 11, request=request)

    with pytest.raises(service.DownloadTooLargeError, match="maximum"):
        run(
            ingest_with_handler(
                monkeypatch,
                "https://media.example/file.txt",
                handler,
            )
        )


def test_invalid_media_ignores_url_extension(monkeypatch):
    def handler(request):
        return httpx.Response(
            200,
            content=b"\x00\x01\x02\x03" * 20,
            request=request,
        )

    with pytest.raises(service.MediaValidationError, match="Unsupported"):
        run(
            ingest_with_handler(
                monkeypatch,
                "https://media.example/looks-like-image.jpg",
                handler,
            )
        )


def test_redirect_is_validated_and_followed(monkeypatch):
    requested_paths = []

    def handler(request):
        requested_paths.append(request.url.path)
        if request.url.path == "/start":
            return httpx.Response(
                302,
                headers={"location": "/final.txt"},
                request=request,
            )
        return httpx.Response(200, content=TEXT_BYTES, request=request)

    result, _ = run(
        ingest_with_handler(
            monkeypatch,
            "https://media.example/start",
            handler,
        )
    )

    assert result["media_type"] == "text"
    assert requested_paths == ["/start", "/final.txt"]


def test_redirect_to_private_address_is_rejected(monkeypatch):
    monkeypatch.setattr(
        service,
        "_resolve_host_addresses",
        lambda hostname, port: (
            REAL_RESOLVER(hostname, port)
            if hostname == "127.0.0.1"
            else PUBLIC_ADDRESSES
        ),
    )

    def handler(request):
        return httpx.Response(
            302,
            headers={"location": "http://127.0.0.1/private.txt"},
            request=request,
        )

    transport = httpx.MockTransport(handler)

    async def execute():
        async with httpx.AsyncClient(transport=transport) as client:
            return await service.download_remote_media(
                "https://media.example/start",
                client=client,
            )

    with pytest.raises(service.URLIngestionError, match="private"):
        run(execute())


def test_too_many_redirects(monkeypatch):
    def handler(request):
        return httpx.Response(
            302,
            headers={"location": "/again"},
            request=request,
        )

    with pytest.raises(service.DownloadFailedError, match="maximum"):
        run(
            ingest_with_handler(
                monkeypatch,
                "https://media.example/start",
                handler,
            )
        )


def test_empty_download_is_rejected(monkeypatch):
    def handler(request):
        return httpx.Response(200, content=b"", request=request)

    with pytest.raises(service.MediaValidationError, match="empty"):
        run(
            ingest_with_handler(
                monkeypatch,
                "https://media.example/file.txt",
                handler,
            )
        )


def test_http_failure_is_reported(monkeypatch):
    def handler(request):
        return httpx.Response(404, request=request)

    with pytest.raises(service.DownloadFailedError, match="404"):
        run(
            ingest_with_handler(
                monkeypatch,
                "https://media.example/missing.mp4",
                handler,
            )
        )


def test_connected_private_peer_is_rejected(monkeypatch):
    class PrivateNetworkStream:
        def get_extra_info(self, name):
            assert name == "server_addr"
            return ("127.0.0.1", 443)

    def handler(request):
        return httpx.Response(
            200,
            content=TEXT_BYTES,
            extensions={"network_stream": PrivateNetworkStream()},
            request=request,
        )

    with pytest.raises(service.URLIngestionError, match="private"):
        run(
            ingest_with_handler(
                monkeypatch,
                "https://media.example/file.txt",
                handler,
            )
        )


@pytest.mark.parametrize(
    "url",
    [
        "http://localhost/file.txt",
        "http://127.0.0.1/file.txt",
        "http://10.0.0.1/file.txt",
        "http://169.254.169.254/latest/meta-data",
        "http://[::1]/file.txt",
    ],
)
def test_local_and_private_addresses_are_rejected(monkeypatch, url):
    monkeypatch.setattr(
        service,
        "_resolve_host_addresses",
        REAL_RESOLVER,
    )

    with pytest.raises(service.URLIngestionError, match="private"):
        run(service.validate_remote_url(url))


def test_endpoint_uses_url_ingestion_service(monkeypatch):
    current_user = User(id=7, email="analyst@example.com")

    async def fake_ingest(url, db, user):
        assert url == "https://media.example/image.jpg"
        assert user is current_user
        return {"upload_id": 3, "status": "queued"}

    monkeypatch.setattr(uploads, "ingest_media_url", fake_ingest)
    app = FastAPI()
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)
    app.dependency_overrides[get_db] = lambda: Mock()
    app.dependency_overrides[get_current_user] = lambda: current_user

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/uploads/url",
            json={"url": "https://media.example/image.jpg"},
        )

    assert response.status_code == 200
    assert response.json() == {"upload_id": 3, "status": "queued"}


def test_url_ingestion_uses_existing_upload_creation(
    monkeypatch,
    tmp_path,
):
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    monkeypatch.setattr(service.settings, "UPLOAD_DIR", tmp_path / "uploads")
    enqueue = Mock()
    monkeypatch.setattr(
        "app.services.upload_service.process_upload.delay",
        enqueue,
    )

    def handler(request):
        return httpx.Response(200, content=JPEG_BYTES, request=request)

    async def execute(db):
        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(transport=transport) as client:
            return await service.ingest_media_url(
                "https://media.example/misleading.txt",
                db,
                client=client,
            )

    with Session(engine) as db:
        response = run(execute(db))
        upload = db.scalar(select(Upload))
        processing_run = db.scalar(select(ProcessingRun))

        assert response["upload_id"] == upload.id
        assert upload.media_type == "image"
        assert upload.mime_type == "image/jpeg"
        assert upload.stored_filename.endswith(".jpg")
        assert processing_run.upload_id == upload.id
        enqueue.assert_called_once_with(upload.id, processing_run.id)
