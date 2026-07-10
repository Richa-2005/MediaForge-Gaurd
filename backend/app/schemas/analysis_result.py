from pydantic import BaseModel, AfterValidator
from typing import Any, Annotated
from app.models.analysis_result import AgentName, Labels

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




