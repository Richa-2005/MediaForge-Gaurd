from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session

from app.services.upload_service import create_upload, get_upload_status
from app.database.session import get_db

router = APIRouter()


@router.get("/uploads/{upload_id}")
def upload_status(
    upload_id : int, 
    db: Session = Depends(get_db)
):
    upload = get_upload_status(upload_id, db)

    if upload is None:
        return {
            "message": "Upload not found",
            "upload_id": upload_id,
        }

    return {
        "upload_id": upload.id,
        "status": upload.status,
        "media_type": upload.media_type,
        "file_path": upload.file_path,
        "original_filename": upload.original_filename,
        "stored_filename": upload.stored_filename,
    }


@router.post("/uploads")
async def upload_media(
    uploaded_file: UploadFile,
    db: Session = Depends(get_db),
):
    created_upload = await create_upload(uploaded_file, db)
    return created_upload

