from typing import TypedDict
from app.models.analysis_result import ExplanationStatus
from app.schemas.analysis_result import AnalysisResultResponse
from app.services.llm.schemas import ExplanationReport
from sqlalchemy.orm import Session

from typing import NotRequired, TypedDict

class ExplanationState(TypedDict):
    analysis_id: int
    db: Session

    analysis_result: NotRequired[AnalysisResultResponse | None]
    formatted_context: NotRequired[str | None]
    report: NotRequired[ExplanationReport | None]
    report_markdown: NotRequired[str | None]
    status: NotRequired[ExplanationStatus]