from app.core.celery_app import celery_app
from app.database.session import SessionLocal
from datetime import datetime, timezone
from app.models.upload import Upload, UploadStatus
from app.models.processing_run import ProcessingRun, RunStatus
from app.models.processing_step import ProcessingStep, StepStatus
from app.services.processing_service import route_service
from app.services.execution_service import (
    create_step, start_step, complete_step, fail_step
)
from sqlalchemy import select
from sqlalchemy.exc import OperationalError

import logging

logger = logging.getLogger(__name__)

RETRYABLE_EXCEPTIONS = (
    OperationalError,
    ConnectionError,
    TimeoutError,
)


@celery_app.task(
    name="process_upload",
    bind=True,
    max_retries=3,
)
def process_upload(self, upload_id: int, run_id: int):
    db = SessionLocal()
    running = None
    media_preprocessing_step = None

    try:
        upload = db.get(Upload, upload_id)

        if upload is None:
            raise ValueError(f"No media upload with id {upload_id} found.")

        running = db.get(ProcessingRun, run_id)
        if running is None:
            raise ValueError(f"No processing run with id {run_id} found.")

        if running.upload_id != upload_id:
            raise ValueError(
                f"Processing run {run_id} does not belong to upload {upload_id}."
            )
        
        upload.status = UploadStatus.PROCESSING
        db.commit()

        logger.info(
            "Processing started | upload_id=%s media_type=%s",
            upload.id,
            upload.media_type,
        )

        media_preprocessing_step = db.scalar(
            select(ProcessingStep).where(
                ProcessingStep.processing_run_id == run_id,
                ProcessingStep.step_name == "preprocessing",
            )
        )

        if media_preprocessing_step is None:
            media_preprocessing_step = create_step(
                running.id,
                "preprocessing",
                db,
            )

        if media_preprocessing_step.status == StepStatus.PENDING:
            start_step(media_preprocessing_step, db)

        logger.info(
            "Step started | run_id=%s step=%s",
            running.id,
            "media_preprocessing",
        )
        
        if media_preprocessing_step.status != StepStatus.COMPLETED:
            saved = route_service(upload, db)
            complete_step(media_preprocessing_step, db)
            
        else:
            logger.info(
                "Skipping completed preprocessing | run_id=%s",
                run_id,
            )

        logger.info(
            "Processing completed | upload_id=%s artifacts=%s",
            upload.id,
            len(saved),
        )

        logger.info(
            "Processing run completed | run_id=%s duration=%sms",
            running.id,
            running.duration_ms,
        )
        
        running.status = RunStatus.COMPLETED
        running.completed_at = datetime.now(timezone.utc)
        running.duration_ms = int(
            (running.completed_at - running.started_at).total_seconds() * 1000
        )

        db.commit()
        db.refresh(running)


        upload.status = UploadStatus.COMPLETED
        db.commit()

        return {
            "status": "completed",
            "upload_id": upload_id,
            "artifacts_saved": len(saved)
        }

    except RETRYABLE_EXCEPTIONS as e:
        db.rollback()

        if self.request.retries >= self.max_retries:
            if media_preprocessing_step is not None:
                fail_step(media_preprocessing_step, str(e), db)

            upload = db.get(Upload, upload_id)
            if upload is not None:
                upload.status = UploadStatus.FAILED

            if running is not None:
                running.status = RunStatus.FAILED
                running.completed_at = datetime.now(timezone.utc)
                running.duration_ms = int(
                    (running.completed_at - running.started_at).total_seconds()
                    * 1000
                )

            db.commit()

            logger.exception(
                "Processing failed after retries exhausted | upload_id=%s attempts=%s",
                upload_id,
                self.request.retries + 1,
            )
            raise

        countdown = 2 ** (self.request.retries + 1)
        logger.warning(
            "Temporary processing failure; retrying | upload_id=%s retry=%s countdown=%ss error=%s",
            upload_id,
            self.request.retries + 1,
            countdown,
            e,
        )
        raise self.retry(exc=e, countdown=countdown)

    except Exception as e:
        db.rollback()

        if media_preprocessing_step is not None:
            fail_step(media_preprocessing_step, str(e), db)

        upload = db.get(Upload, upload_id)
        if upload is not None:
            upload.status = UploadStatus.FAILED
        
        if running is not None:
            running.status = RunStatus.FAILED
            running.completed_at = datetime.now(timezone.utc)
            running.duration_ms = int(
                (running.completed_at - running.started_at).total_seconds()
                * 1000
            )

        db.commit()
        
        logger.exception(
            "Processing failed | upload_id=%s",
            upload_id,
        )
        raise

    finally:
        db.close()
