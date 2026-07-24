from pathlib import Path

from fastapi import APIRouter, UploadFile, Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.dependencies import bearer_scheme, get_current_user
from app.models.user import User
from app.services.upload_service import create_upload, get_upload_status
from app.services.auth_service import decode_access_token
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

@router.get("/uploads/{upload_id}/media")
def uploaded_media_file(
    upload_id: int,
    token: str | None = Query(default=None),
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    if credentials is not None and credentials.scheme.lower() == "bearer":
        payload = decode_access_token(credentials.credentials)
    elif token:
        payload = decode_access_token(token)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not isinstance(user_id, str) or not user_id.isdigit():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    current_user = db.get(User, int(user_id))
    if current_user is None or not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User could not be authenticated.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    upload = get_upload_status(upload_id, db, current_user)

    if upload is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No uploads with this id found",
        )

    file_path = Path(upload.file_path)
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Uploaded media file is not available.",
        )

    return FileResponse(
        file_path,
        media_type=upload.mime_type,
        filename=upload.original_filename,
    )


@router.post("/uploads")
async def upload_media(
    uploaded_file: UploadFile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    created_upload = await create_upload(uploaded_file, db, current_user)
    return created_upload
