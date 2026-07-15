from pydantic import BaseModel
from app.models.processing_step import StepStatus
from datetime import datetime

class ProcessingStepResponse(BaseModel):
    id: int
    processing_run_id: int
    step_name: str
    status: StepStatus
    started_at: datetime | None
    completed_at: datetime | None
    error_message: str | None 
    created_at: datetime
    duration_ms: int | None