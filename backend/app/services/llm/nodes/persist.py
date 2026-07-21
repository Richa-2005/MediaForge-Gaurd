from datetime import datetime, timezone
import logging

from app.models.analysis_result import (
    AnalysisResult,
    ExplanationStatus,
)
from app.services.llm.state import ExplanationState


logger = logging.getLogger(__name__)


def persist(
    state: ExplanationState,
) -> ExplanationState:
    db = state["db"]
    primary_analysis_id = state[
        "primary_analysis_id"
    ]

    try:
        row = db.get(
            AnalysisResult,
            primary_analysis_id,
        )

        if row is None:
            raise ValueError(
                "Primary AnalysisResult "
                f"{primary_analysis_id} not found."
            )

        report = state.get("report")
        markdown = state.get("report_markdown")

        if report is None or markdown is None:
            raise ValueError(
                "Generated report content is missing."
            )

        row.report = report.model_dump()
        row.report_markdown = markdown
        row.summary = report.summary
        row.explanation_status = (
            ExplanationStatus.COMPLETED
        )
        row.explanation_generated_at = (
            datetime.now(timezone.utc)
        )

        db.commit()
        db.refresh(row)

        logger.info(
            "Consolidated report persisted | "
            "upload_id=%s primary_analysis_id=%s",
            state["upload_id"],
            primary_analysis_id,
        )

    except Exception:
        db.rollback()
        logger.exception(
            "Unable to persist consolidated report | "
            "upload_id=%s",
            state["upload_id"],
        )
        raise

    return state