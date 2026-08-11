from fastapi import UploadFile,HTTPException,status
from app.core.config import settings
from datetime import datetime, timezone
import magic
import os
import shutil
import hashlib
import logging
from pathlib import Path
from urllib.parse import urlparse
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models.upload import Upload, UploadStatus
from app.models.processing_run import ProcessingRun, RunStatus, RunTrigger
from app.models.processing_step import ProcessingStep, StepStatus
from app.models.user import User
from app.core.celery_app import celery_app
from app.services.storage_service import (
    build_storage_key,
    upload_to_supabase_storage,
)
from app.services.execution_service import (
    complete_step,
    get_or_create_step,
    start_step,
)

logger = logging.getLogger(__name__)


MIME_EXTENSIONS = {
    "image/jpg": ".jpg",
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "video/mp4": ".mp4",
    "audio/mp3": ".mp3",
    "audio/mpeg": ".mp3",
    "audio/wav": ".wav",
    "audio/x-wav": ".wav",
    "text/plain": ".txt",
}

EXTENSION_MIME_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".mp4": "video/mp4",
    ".mp3": "audio/mpeg",
    ".wav": "audio/x-wav",
    ".txt": "text/plain",
}


def processing_queue_for_media_type(media_type: str) -> str:
    return settings.MEDIA_PROCESSING_QUEUES.get(media_type, "celery")


def detect_media_mime(header_bytes: bytes) -> str:
    return magic.from_buffer(header_bytes, mime=True)


def normalize_detected_mime(
    detected_mime: str,
    filename: str | None = None,
) -> str:
    if detected_mime != "application/octet-stream" or not filename:
        return detected_mime

    extension = Path(filename).suffix.lower()
    return EXTENSION_MIME_TYPES.get(extension, detected_mime)


def validate_media_mime(
    detected_mime: str,
    filename: str | None = None,
) -> str:
    detected_mime = normalize_detected_mime(detected_mime, filename)

    if detected_mime not in settings.ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=(
                f"Unsupported file type: {detected_mime}. "
                "Only standard media files are allowed."
            ),
        )

    media_type = detected_mime.split("/", 1)[0]
    if media_type in settings.DISABLED_MEDIA_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=(
                f"{media_type.title()} submissions are disabled in this deployment. "
                "Choose another supported media type."
            ),
        )

    return detected_mime


def active_heavy_job_count(db: Session) -> int:
    recover_stale_processing_uploads(db)

    return db.scalar(
        select(func.count())
        .select_from(Upload)
        .where(
            Upload.media_type.in_(settings.HEAVY_MEDIA_TYPES),
            Upload.status.in_(
                [
                    UploadStatus.QUEUED,
                    UploadStatus.PROCESSING,
                ]
            ),
        )
    ) or 0


def enforce_heavy_media_capacity(media_type: str, db: Session) -> None:
    if media_type not in settings.HEAVY_MEDIA_TYPES:
        return

    recover_stale_processing_uploads(db)
    active_jobs = active_heavy_job_count(db)
    if active_jobs < settings.MAX_ACTIVE_HEAVY_JOBS:
        return

    raise HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail=(
            "Heavy media analysis is currently busy. "
            "Please try again shortly."
        ),
    )


async def validating_file(uploadedFile : UploadFile) -> str:
    #Validating the file
    if (
        uploadedFile.size is not None
        and uploadedFile.size > settings.MAX_UPLOAD_SIZE_BYTES
    ):
         raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum allowed size is {settings.MAX_UPLOAD_SIZE_BYTES / (1024*1024)}MB."
        )
    
    header_bytes = await uploadedFile.read(2048)
    await uploadedFile.seek(0) 

    detected_mime = validate_media_mime(
        detect_media_mime(header_bytes),
        uploadedFile.filename,
    )
    
    return detected_mime
    
async def store_file(uploadedFile : UploadFile, detected_mime: str):
    media_id = str(uuid4())
    folder_path = Path(settings.UPLOAD_DIR) / media_id
    folder_path.mkdir(parents=True, exist_ok=True)

    extension = Path(uploadedFile.filename).suffix.lower()

    stored_filename = f"{media_id}{extension}"
    file_path = folder_path / stored_filename
    object_key = build_storage_key(media_id, uploadedFile.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(uploadedFile.file, buffer)
    except OSError:
        shutil.rmtree(folder_path, ignore_errors=True)
        raise

    try:
        await upload_to_supabase_storage(uploadedFile, object_key, detected_mime)
    except HTTPException as exc:
        logger.warning(
            "Supabase upload skipped after failure | object_key=%s detail=%s",
            object_key,
            exc.detail,
        )

    return file_path, object_key
    

async def calculate_hash(uploadedFile : UploadFile) -> str:
    sha256_hash = hashlib.sha256()
    
    # Read chunks asynchronously
    while chunk := await uploadedFile.read(65536):
        sha256_hash.update(chunk)
        
    await uploadedFile.seek(0) # Reset pointer
    return sha256_hash.hexdigest()

def upload_media(
        db: Session,uploadedFile : UploadFile, 
        detected_mime : str,sha_hash : str,
        file_path : str,
        stored_filename: str,
        user: User | None = None,
    ):
    
    upload = Upload(
        user_id=user.id if user else None,
        original_filename=uploadedFile.filename,
        stored_filename=stored_filename,
        file_path=str(file_path),
        media_type=detected_mime.split('/', 1)[0],
        mime_type=detected_mime,
        file_size=uploadedFile.size,
        sha256_hash=sha_hash,
        status=UploadStatus.UPLOADED,
        language=None,
    )

    db.add(upload)
    db.flush()

    return upload

def file_exists(sha_hash: str, db: Session, user: User | None = None):
    query = select(Upload).where(Upload.sha256_hash == sha_hash)
    if user is not None:
        query = query.where(Upload.user_id == user.id)
    existing_file = db.scalar(query)
    return existing_file

async def create_upload(
        uploadedFile: UploadFile,
        db: Session,
        user: User | None = None,
):
        detected_mime = await validating_file(uploadedFile)
        sha_hash = await calculate_hash(uploadedFile)
        existing_file =  file_exists(sha_hash, db, user)
        
        if existing_file:
            return {
                "upload_id" : existing_file.id,
                "status" : existing_file.status,
                "media_type": existing_file.media_type,
                "file_path":existing_file.file_path,
                "is_duplication":True,
                "message":"File Already exists in the database."
            }

        media_type = detected_mime.split("/", 1)[0]
        enforce_heavy_media_capacity(media_type, db)

        file_path: Path | None = None
        try:
            file_path, storage_key = await store_file(uploadedFile, detected_mime)
            uploaded_file = upload_media(
                db,
                uploadedFile,
                detected_mime,
                sha_hash,
                file_path,
                storage_key,
                user,
            )

            #Queueing the file for processing
            uploaded_file.status = UploadStatus.QUEUED

            processing_run = ProcessingRun(
                upload_id=uploaded_file.id,
                status=RunStatus.RUNNING,
                trigger=RunTrigger.UPLOAD,
                started_at=datetime.now(timezone.utc),
            )
            db.add(processing_run)
            db.commit()
            db.refresh(uploaded_file)
            db.refresh(processing_run)

        except IntegrityError:
            db.rollback()
            cleanup_stored_file(file_path)
            existing_file = file_exists(sha_hash, db, user)
            if existing_file:
                return {
                    "upload_id" : existing_file.id,
                    "status" : existing_file.status,
                    "media_type": existing_file.media_type,
                    "file_path":existing_file.file_path,
                    "is_duplication":True,
                    "message":"File Already exists in the database."
                }
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A matching upload already exists.",
            )
        except (OSError, SQLAlchemyError) as exc:
            db.rollback()
            cleanup_stored_file(file_path)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="The media could not be stored. Please try again.",
            ) from exc

        try:
            queue_name = processing_queue_for_media_type(uploaded_file.media_type)
            task = celery_app.send_task(
                "process_upload",
                args=[uploaded_file.id, processing_run.id],
                queue=queue_name,
                ignore_result=True,
            )
            queue_step = get_or_create_step(
                processing_run.id,
                "queue_assigned",
                db,
            )
            if queue_step.status == StepStatus.RUNNING:
                complete_step(queue_step, db)
            elif queue_step.status != StepStatus.COMPLETED:
                start_step(queue_step, db)
                complete_step(queue_step, db)
            broker_url = urlparse(settings.CELERY_BROKER_URL)
            logger.info(
                "Queued Celery task | upload_id=%s run_id=%s task_id=%s broker=%s queue=%s",
                uploaded_file.id,
                processing_run.id,
                task.id,
                broker_url.hostname,
                queue_name,
            )
        except Exception as exc:
            logger.exception(
                "Failed to queue Celery task | upload_id=%s run_id=%s",
                uploaded_file.id,
                processing_run.id,
            )
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="The media was stored, but analysis could not be queued.",
            ) from exc

        return {
            "upload_id" : uploaded_file.id,
            "status" : uploaded_file.status,
            "media_type":uploaded_file.media_type,
            "file_path":uploaded_file.file_path,
            "is_duplication":False,
            "message":"File uploaded and stored successfully."
        }


def cleanup_stored_file(file_path: Path | None) -> None:
    if file_path is None:
        return

    upload_dir = file_path.parent
    try:
        if upload_dir.exists() and upload_dir.is_relative_to(settings.UPLOAD_DIR):
            shutil.rmtree(upload_dir)
    except OSError:
        pass
    
    
def get_upload_status(
    upload_id: int,
    db: Session,
    user: User | None = None,
):
    query = select(Upload).where(Upload.id== upload_id)
    if user is not None:
        query = query.where(Upload.user_id == user.id)
    response = db.scalar(query)
    recover_stale_processing_uploads(db, upload_id=upload_id)
    if response is not None:
        db.refresh(response)

    return response


def recover_stale_processing_uploads(
    db: Session,
    *,
    upload_id: int | None = None,
) -> int:
    """
    Mark abandoned queued/processing uploads as failed.

    A Celery worker SIGKILL or Railway redeploy can terminate the process before
    task exception handlers run. Without this recovery, stale heavy media rows
    permanently consume the heavy-media capacity slot.
    """

    stale_before = datetime.now(timezone.utc).timestamp() - (
        settings.PROCESSING_STALE_AFTER_SECONDS
    )
    upload_query = (
        select(Upload)
        .where(
            Upload.status.in_(
                [
                    UploadStatus.QUEUED,
                    UploadStatus.PROCESSING,
                ]
            ),
        )
    )
    if upload_id is not None:
        upload_query = upload_query.where(Upload.id == upload_id)

    recovered = 0
    now = datetime.now(timezone.utc)
    for upload in db.scalars(upload_query).all():
        run = db.scalar(
            select(ProcessingRun)
            .where(ProcessingRun.upload_id == upload.id)
            .order_by(ProcessingRun.started_at.desc())
        )
        if run is None or run.status != RunStatus.RUNNING:
            continue

        started_at = run.started_at
        if started_at.tzinfo is None:
            started_at = started_at.replace(tzinfo=timezone.utc)

        if started_at.timestamp() > stale_before:
            continue

        logger.warning(
            "Recovering stale processing upload | upload_id=%s run_id=%s status=%s",
            upload.id,
            run.id,
            upload.status,
        )
        upload.status = UploadStatus.FAILED
        run.status = RunStatus.FAILED
        run.completed_at = now
        run.duration_ms = int((now - started_at).total_seconds() * 1000)

        unfinished_steps = db.scalars(
            select(ProcessingStep).where(
                ProcessingStep.processing_run_id == run.id,
                ProcessingStep.status.in_(
                    [
                        StepStatus.PENDING,
                        StepStatus.RUNNING,
                    ]
                ),
            )
        ).all()
        for step in unfinished_steps:
            step.status = StepStatus.FAILED
            step.completed_at = now
            step.error_message = (
                "Processing worker stopped before this step completed."
            )
            step_started_at = step.started_at or run.started_at
            if step_started_at.tzinfo is None:
                step_started_at = step_started_at.replace(tzinfo=timezone.utc)
            step.duration_ms = int(
                (now - step_started_at).total_seconds() * 1000
            )

        recovered += 1

    if recovered:
        db.commit()

    return recovered
