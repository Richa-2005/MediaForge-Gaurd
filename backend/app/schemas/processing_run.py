from pydantic import BaseModel
from app.models.processing_run import RunStatus, RunTrigger
from datetime import datetime

class ProcessingRunResponse(BaseModel):
    id: int
    upload_id: int
    status:RunStatus
    trigger: RunTrigger
    started_at: datetime
    completed_at: datetime | None
    created_at: datetime
    duration_ms: int | None