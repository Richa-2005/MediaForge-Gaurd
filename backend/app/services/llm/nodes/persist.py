from app.services.llm.state import ExplanationState
from app.models.analysis_result import AnalysisResult
from app.models.analysis_result import ExplanationStatus
from datetime import datetime, timezone

import logging
logger = logging.getLogger(__name__)
def persist(state : ExplanationState) -> ExplanationState:
    try:
        row = state["db"].get(AnalysisResult, state["analysis_id"])

        if row is None:
            raise ValueError(
                f"AnalysisResult {state['analysis_id']} not found."
            )
        
        row.report = state["report"].model_dump()
        row.report_markdown = state["report_markdown"]
        row.summary = state["report"].summary
        row.explanation_status = ExplanationStatus.COMPLETED
        row.explanation_generated_at = datetime.now(timezone.utc)

        state["db"].commit()
        state["db"].refresh(row)

        logger.info(
            "LLM report persisted for analysis_id=%s",
            state["analysis_id"],
        )
    except Exception as e:
        state["db"].rollback()
        logger.exception(
            "Unable to store in the database due to : %s",
            e
        )
        raise
    
    return state
