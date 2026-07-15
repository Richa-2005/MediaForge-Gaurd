from pydantic import BaseModel
from typing import Any
from datetime import datetime

class ProcessingArtifactResponse(BaseModel):
    id : int
    upload_id :int
    artifact_type: str
    file_path : str | None
    details : dict[str, Any] | None
    created_at : datetime
       