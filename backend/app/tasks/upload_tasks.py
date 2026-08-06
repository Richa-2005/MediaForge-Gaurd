from app.core.celery_app import celery_app
from app.database.session import SessionLocal
from datetime import datetime, timezone
from app.models.upload import Upload, UploadStatus
from app.models.processing_run import ProcessingRun, RunStatus
from app.models.processing_step import StepStatus
from app.services.execution_service import complete_processing, fail_processing
from app.services.execution_service import (
    complete_step,
    fail_step,
    get_or_create_step,
    start_step,
)
from app.services.analysis_service import run_analysis
from sqlalchemy.exc import OperationalError
import logging
from app.services.processing_service import run_preprocessing

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
    current_step = None
    saved = []

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

        saved, current_step = run_preprocessing(
            upload,
            running,
            db,
        )

        current_step = get_or_create_step(
            running.id,
            "analysis",
            db,
        )
        if current_step.status == StepStatus.PENDING:
            start_step(current_step, db)

        try:
            saved_results = run_analysis(
                upload,
                db,
            )
            complete_step(current_step, db)
        except Exception as e:
            fail_step(current_step, str(e), db)
            raise

        complete_processing(
            saved_results,
            upload,
            running,
            db,
        )


        return {
            "status": "completed",
            "upload_id": upload_id,
            "artifacts_saved": len(saved),
            "analysis_results_saved": len(saved_results),
        }

    except RETRYABLE_EXCEPTIONS as e:
        db.rollback()

        if self.request.retries >= self.max_retries:
            fail_processing(upload_id,running,current_step,e,db)

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

        fail_processing(upload_id,running,current_step,e,db)
        
        logger.exception(
            "Processing failed | upload_id=%s",
            upload_id,
        )
        raise

    finally:
        db.close()
