from app.core.celery_app import celery_app
from app.database.session import SessionLocal
from sqlalchemy import select
from app.models.upload import Upload, UploadStatus

@celery_app.task(name="process_upload")
def process_upload(upload_id: int):
    db = SessionLocal()

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
        print("Processing complete!")

        upload.status = UploadStatus.COMPLETED
        db.commit()

        return {
            "status": "completed",
            "upload_id": upload_id,
        }

    except Exception as e:
        db.rollback()

        upload = db.get(Upload, upload_id)
        if upload is not None:
            upload.status = UploadStatus.FAILED
            db.commit()

        return {
            "status": "failed",
            "upload_id": upload_id,
            "error": str(e),
        }

    finally:
        db.close()