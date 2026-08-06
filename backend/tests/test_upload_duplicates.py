from io import BytesIO
import ipaddress
from unittest.mock import Mock

import httpx
import pytest
from fastapi import UploadFile
from fastapi import HTTPException
from sqlalchemy import create_engine, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.base import Base
from app.models.upload import Upload, UploadStatus
from app.models.user import User
from app.services import upload_service
from app.services import url_ingestion_service


TEXT_BYTES = b"This is a plain text media file.\n"


@pytest.fixture()
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture()
def users(db):
    first = User(
        email="first@example.com",
        hashed_password="hash",
    )
    second = User(
        email="second@example.com",
        hashed_password="hash",
    )
    db.add_all([first, second])
    db.commit()
    db.refresh(first)
    db.refresh(second)
    return first, second


@pytest.fixture(autouse=True)
def upload_environment(monkeypatch, tmp_path):
    monkeypatch.setattr(upload_service.settings, "UPLOAD_DIR", tmp_path / "uploads")
    monkeypatch.setattr(
        url_ingestion_service.settings,
        "UPLOAD_DIR",
        tmp_path / "uploads",
    )
    monkeypatch.setattr(
        upload_service,
        "detect_media_mime",
        lambda _header: "text/plain",
    )
    enqueue = Mock()
    enqueue.return_value.id = "task-1"
    monkeypatch.setattr(upload_service.celery_app, "send_task", enqueue)
    return enqueue


def make_upload(filename="sample.txt"):
    return UploadFile(
        file=BytesIO(TEXT_BYTES),
        size=len(TEXT_BYTES),
        filename=filename,
    )


def make_video_upload(filename="sample.mp4"):
    return UploadFile(
        file=BytesIO(b"fake video bytes"),
        size=len(b"fake video bytes"),
        filename=filename,
    )


async def create_text_upload(db, user, filename="sample.txt"):
    return await upload_service.create_upload(
        make_upload(filename),
        db,
        user,
    )


@pytest.mark.anyio
async def test_same_user_uploads_same_file_twice(db, users, upload_environment):
    user, _ = users

    first = await create_text_upload(db, user)
    second = await create_text_upload(db, user)

    upload_count = db.scalar(select(func.count()).select_from(Upload))
    assert upload_count == 1
    assert second["upload_id"] == first["upload_id"]
    assert second["is_duplication"] is True
    assert upload_environment.call_count == 1


@pytest.mark.anyio
async def test_different_users_can_upload_same_file(db, users, upload_environment):
    first_user, second_user = users

    first = await create_text_upload(db, first_user)
    second = await create_text_upload(db, second_user)

    upload_count = db.scalar(select(func.count()).select_from(Upload))
    assert upload_count == 2
    assert second["upload_id"] != first["upload_id"]
    assert second["is_duplication"] is False
    assert upload_environment.call_count == 2


def test_processing_queue_for_media_type():
    assert upload_service.processing_queue_for_media_type("image") == "image_queue"
    assert upload_service.processing_queue_for_media_type("text") == "text_queue"
    assert upload_service.processing_queue_for_media_type("video") == "video_queue"
    assert upload_service.processing_queue_for_media_type("audio") == "audio_queue"
    assert upload_service.processing_queue_for_media_type("unknown") == "celery"


@pytest.mark.anyio
async def test_heavy_media_capacity_rejects_when_busy(
    db,
    users,
    monkeypatch,
    upload_environment,
):
    user, _ = users
    db.add(
        Upload(
            user_id=user.id,
            original_filename="busy.mp4",
            stored_filename="busy.mp4",
            file_path="/tmp/busy.mp4",
            media_type="video",
            mime_type="video/mp4",
            file_size=10,
            sha256_hash="b" * 64,
            status=UploadStatus.QUEUED,
        )
    )
    db.commit()
    monkeypatch.setattr(
        upload_service,
        "detect_media_mime",
        lambda _header: "video/mp4",
    )
    monkeypatch.setattr(upload_service.settings, "MAX_ACTIVE_HEAVY_JOBS", 1)

    with pytest.raises(HTTPException) as exc:
        await upload_service.create_upload(
            make_video_upload(),
            db,
            user,
        )

    assert exc.value.status_code == 429
    assert upload_environment.call_count == 0


@pytest.mark.anyio
async def test_url_upload_duplicate_uses_same_user_scope(
    db,
    users,
    monkeypatch,
    upload_environment,
):
    user, _ = users
    monkeypatch.setattr(
        url_ingestion_service,
        "detect_media_mime",
        lambda _header: "text/plain",
    )
    monkeypatch.setattr(
        url_ingestion_service,
        "_resolve_host_addresses",
        lambda _hostname, _port: {ipaddress.ip_address("8.8.8.8")},
    )

    def handler(request):
        return httpx.Response(200, content=TEXT_BYTES, request=request)

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        first = await url_ingestion_service.ingest_media_url(
            "https://media.example/sample.txt",
            db,
            user,
            client=client,
        )
        second = await url_ingestion_service.ingest_media_url(
            "https://media.example/sample.txt",
            db,
            user,
            client=client,
        )

    upload_count = db.scalar(select(func.count()).select_from(Upload))
    assert upload_count == 1
    assert second["upload_id"] == first["upload_id"]
    assert second["is_duplication"] is True
    assert upload_environment.call_count == 1


@pytest.mark.anyio
async def test_session_remains_usable_after_failed_persistence(
    db,
    users,
    monkeypatch,
):
    user, _ = users

    def fail_upload(*_args, **_kwargs):
        raise SQLAlchemyError("database unavailable")

    monkeypatch.setattr(upload_service, "upload_media", fail_upload)

    with pytest.raises(Exception):
        await create_text_upload(db, user)

    assert db.scalar(select(func.count()).select_from(Upload)) == 0


@pytest.mark.anyio
async def test_failed_persistence_removes_orphan_upload_directory(
    db,
    users,
    monkeypatch,
):
    user, _ = users
    upload_root = upload_service.settings.UPLOAD_DIR

    def fail_upload(*_args, **_kwargs):
        raise SQLAlchemyError("database unavailable")

    monkeypatch.setattr(upload_service, "upload_media", fail_upload)

    with pytest.raises(Exception):
        await create_text_upload(db, user)

    assert not upload_root.exists() or list(upload_root.iterdir()) == []


@pytest.mark.anyio
async def test_failed_file_write_removes_orphan_upload_directory(
    db,
    users,
    monkeypatch,
):
    user, _ = users
    upload_root = upload_service.settings.UPLOAD_DIR

    def fail_copy(*_args, **_kwargs):
        raise OSError("disk full")

    monkeypatch.setattr(upload_service.shutil, "copyfileobj", fail_copy)

    with pytest.raises(Exception):
        await create_text_upload(db, user)

    assert db.scalar(select(func.count()).select_from(Upload)) == 0
    assert not upload_root.exists() or list(upload_root.iterdir()) == []
