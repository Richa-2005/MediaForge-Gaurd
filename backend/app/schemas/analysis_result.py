from pydantic import BaseModel, AfterValidator, ConfigDict
from typing import Any, Annotated
from app.models.analysis_result import AgentName, Labels, ExplanationStatus
from datetime import datetime


def in_range(value: float)->float:
    if value < 0.0 or value > 1.0:
        raise ValueError(f"{value} is not within the range of 0.0 and 1.0.")
    return value
    
class AnalysisResultCreate(BaseModel):
    upload_id : int
    agent : AgentName
    label : Labels
    risk_score : Annotated[float,AfterValidator(in_range)]
    confidence : Annotated[float,AfterValidator(in_range)]
    explanation : str | None
    evidence : list[dict[str, Any]] | None
    details : dict[str, Any] | None
    
    report: dict[str, Any] | None = None
    report_markdown: str | None = None
    summary: str | None = None
    explanation_status: ExplanationStatus = ExplanationStatus.PENDING
    explanation_generated_at: datetime | None = None
    
class AnalysisResultResponse(BaseModel):
    id: int
    upload_id: int
    agent: AgentName
    label: Labels
    risk_score: float
    confidence: float
    explanation: str | None
    evidence: list[dict[str, Any]] | None
    details: dict[str, Any] | None
    created_at: datetime

    report: dict[str, Any] | None = None
    report_markdown: str | None
    summary: str | None
    explanation_status: ExplanationStatus
    explanation_generated_at: datetime | None
    model_config = ConfigDict(from_attributes=True)


