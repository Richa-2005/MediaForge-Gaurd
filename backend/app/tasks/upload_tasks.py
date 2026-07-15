from app.core.celery_app import celery_app
from app.database.session import SessionLocal
from datetime import datetime, timezone
from app.models.upload import Upload, UploadStatus
from app.models.processing_run import ProcessingRun, RunStatus, RunTrigger
from app.services.analysis_service import save_analysis_result
from app.services.processing_service import route_service
from app.services.execution_service import (
    create_step, start_step, complete_step, fail_step
)

@celery_app.task(name="process_upload")
def process_upload(upload_id: int):
    db = SessionLocal()
    running = None
    try:
        upload = db.get(Upload, upload_id)

        if not upload :
            return{
                "status": "failed",
                "reason": f"No media upload with id {upload_id} found.",
            }
        
        upload.status = UploadStatus.PROCESSING
        db.commit()

        print("Processing...")

        running = ProcessingRun(
            upload_id=upload_id,
            status=RunStatus.RUNNING,
            trigger=RunTrigger.UPLOAD,
            started_at=datetime.now(timezone.utc)
        )
        db.add(running)
        db.commit()
        db.refresh(running)

        media_preprocessing_step = create_step(
            running.id,
            "preprocessing",
            db,
        )

        start_step(media_preprocessing_step, db)
        
        saved = route_service(upload, db)

        complete_step(media_preprocessing_step, db)

        print("Processing complete!")
        
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

    except Exception as e:
        db.rollback()
        fail_step(media_preprocessing_step, str(e), db)
        upload = db.get(Upload, upload_id)
        if upload is not None:
            upload.status = UploadStatus.FAILED
            db.commit()
        
        if running is not None:
            running.status = RunStatus.FAILED
            running.completed_at = datetime.now(timezone.utc)
            db.commit()

        return {
            "status": "failed",
            "upload_id": upload_id,
            "error": str(e),
        }

    finally:
        db.close()