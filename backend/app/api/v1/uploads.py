from fastapi import APIRouter, UploadFile, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.models.user import User
from app.services.upload_service import create_upload, get_upload_status
from app.services.analysis_service import get_upload_results
from app.services.url_ingestion_service import (
    URLIngestionError,
    ingest_media_url,
)
from app.database.session import get_db
from app.schemas.upload import URLUploadRequest


router = APIRouter()


@router.post("/uploads/url")
async def upload_media_from_url(
    request: URLUploadRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return await ingest_media_url(request.url, db, current_user)
    except URLIngestionError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        ) from exc

@router.get("/uploads/{upload_id}/results")
def upload_results(
    upload_id : int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    results = get_upload_results(upload_id, db, current_user.id)

    if results is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No analysis found"
        )
    
    return results

@router.get("/uploads/{upload_id}")
def upload_status(
    upload_id : int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    upload = get_upload_status(upload_id, db, current_user)

    if upload is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No uploads with this id found"
        )

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
    current_user: User = Depends(get_current_user),
):
    created_upload = await create_upload(uploaded_file, db, current_user)
    return created_upload
