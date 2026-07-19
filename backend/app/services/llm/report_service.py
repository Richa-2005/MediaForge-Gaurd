from app.services.llm.graph import explanation_graph
from app.models.analysis_result import ExplanationStatus
from sqlalchemy.orm import Session
from app.models.analysis_result import AnalysisResult
from datetime import datetime, timezone

import logging
logger = logging.getLogger(__name__)

def generate_report(
    analysis_id: int,
    db: Session,
):
    try:
        explanation_graph.invoke(
            {
                "analysis_id": analysis_id,
                "db": db,
                "status": ExplanationStatus.PENDING,
            }
        )

    except Exception as e:
        db.rollback()
        try: 
            row = db.get(
                AnalysisResult,
                analysis_id,
            )
            if row is not None:
                row.explanation_status = ExplanationStatus.FAILED
                row.explanation_generated_at = datetime.now(timezone.utc)

                db.commit()
                db.refresh(row)
            
            logger.exception(
                "LLM report generation failed for analysis_id=%s",
                analysis_id,
            )
        
      
        except Exception:
            db.rollback()
            logger.exception(
                "Failed to update explanation status for analysis_id=%s",
                analysis_id,
            )
            raise
            
        raise