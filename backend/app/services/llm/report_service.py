from datetime import datetime, timezone
import logging

from sqlalchemy.orm import Session

from app.models.analysis_result import (
    AnalysisResult,
    ExplanationStatus,
)
from app.services.llm.graph import explanation_graph


logger = logging.getLogger(__name__)


def generate_upload_report(
    upload_id: int,
    primary_analysis_id: int,
    db: Session,
):
    try:
        return explanation_graph.invoke(
            {
                "upload_id": upload_id,
                "primary_analysis_id": (
                    primary_analysis_id
                ),
                "db": db,
                "status": ExplanationStatus.PENDING,
            }
        )

    except Exception:
        db.rollback()

        try:
            row = db.get(
                AnalysisResult,
                primary_analysis_id,
            )

            if row is not None:
                row.explanation_status = (
                    ExplanationStatus.FAILED
                )
                row.explanation_generated_at = (
                    datetime.now(timezone.utc)
                )

                db.commit()
                db.refresh(row)

            logger.exception(
                "Consolidated report generation failed | "
                "upload_id=%s primary_analysis_id=%s",
                upload_id,
                primary_analysis_id,
            )

        except Exception:
            db.rollback()
            logger.exception(
                "Failed to update report status | "
                "primary_analysis_id=%s",
                primary_analysis_id,
            )

        raise