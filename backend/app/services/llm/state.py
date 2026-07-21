from typing import NotRequired, TypedDict

from sqlalchemy.orm import Session

from app.models.analysis_result import ExplanationStatus
from app.schemas.analysis_result import AnalysisResultResponse
from app.services.llm.schemas import ExplanationReport


class ExplanationState(TypedDict):
    upload_id: int
    primary_analysis_id: int
    db: Session

    analysis_results: NotRequired[
        list[AnalysisResultResponse]
    ]
    primary_analysis: NotRequired[
        AnalysisResultResponse | None
    ]
    formatted_context: NotRequired[str | None]
    report: NotRequired[ExplanationReport | None]
    report_markdown: NotRequired[str | None]
    status: NotRequired[ExplanationStatus]