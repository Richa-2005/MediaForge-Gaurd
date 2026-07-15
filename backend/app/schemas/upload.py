from pydantic import BaseModel
from app.models.upload import UploadStatus
from datetime import datetime

class UploadResponse(BaseModel):
    id: int
    status: UploadStatus
    media_type: str
    file_path: str
    original_filename: str
    stored_filename: str
    sha256_hash: str
    created_at: datetime