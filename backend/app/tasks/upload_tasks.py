from app.core.celery_app import celery_app
from app.database.session import SessionLocal
from sqlalchemy import select
from app.models.upload import Upload, UploadStatus
from app.services.analysis_service import save_analysis_result


def mock_analysis(upload):
    media_type = upload.media_type

    if media_type == "text":
        return {
            "upload_id": upload.id,
            "agent": "text",
            "risk_score": 0.84,
            "label": "misleading",
            "confidence": 0.88,
            "details": {
                "transcript": "…",
                "top_match_id": "kb_123",
                "model_version": "v1.0"
            },
            "evidence":[
                {
                "similarity_score": 0.84,
                }
            ],
            "explanation":"This is a mock analysis for text"
        }
    elif media_type == "audio":
        return {
            "upload_id": upload.id,
            "agent": "audio",
            "risk_score": 0.28,
            "label": "authentic",
            "confidence": 0.91,
            "details": {
                "duration_seconds": 14.7,
                "model_version": "v1.0"
            },
            "evidence":[
                {
                "synthetic_voice_probability": 0.28,
                }
            ],
            "explanation":"This is a mock analysis for audio"
        }
    
    elif media_type == "video":
        return {
            "upload_id": upload.id,
            "agent": "vision",
            "risk_score": 0.68,
            "label": "authentic",
            "confidence": 0.71,
            "details": {
                "duration_seconds": 30.7,
                "model_version": "v1.0"
            },
            "evidence":[
                {
                "synthetic_video_probability": 0.98,
                }
            ],
            "explanation":"This is a mock analysis for video"
        }
    
    return {
        "upload_id": upload.id,
        "agent": "vision",
        "risk_score": 0.18,
        "label": "authentic",
        "confidence": 0.91,
        "details": {
            "model_version": "v1.0"
        },
        "evidence":[
            {
            "synthetic_image_probability": 0.19,
            }
        ],
        "explanation":"This is a mock analysis for images"
     }

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
       
        result = mock_analysis(upload)
        
        analysis_row = save_analysis_result(result,db)

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