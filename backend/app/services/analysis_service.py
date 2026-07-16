from fastapi import HTTPException, status
from app.schemas.analysis_result import AnalysisResultCreate
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.analysis_result import AnalysisResult
from pydantic import ValidationError

import logging
logger = logging.getLogger(__name__)

def persist_analysis_result(analysis: AnalysisResultCreate, db: Session):
    try:
        row = AnalysisResult(
            upload_id=analysis.upload_id,
            agent=analysis.agent,
            label=analysis.label,
            risk_score=analysis.risk_score,
            confidence=analysis.confidence,
            explanation=analysis.explanation,
            evidence=analysis.evidence,
            details=analysis.details
        )

        db.add(row)
        db.commit()
        db.refresh(row)

        logger.info(
            "Analysis stored | upload_id=%s agent=%s",
            analysis.upload_id,
            analysis.agent,
        )

        return row

    except Exception as e:
        db.rollback()
        logger.exception(
            "Failed to store analysis | upload_id=%s",
             analysis.upload_id,

        )
        raise

def save_analysis_result(analysis: dict, db: Session):
    #validate AI result
    try:
        validated_analysis = AnalysisResultCreate(**analysis)
        
    except ValidationError as val:
        print(f"\nCould not Store the analysis result.\n{val}")
        raise
    
    #create AnalysisResult database row
    analysis_row = persist_analysis_result(validated_analysis,db)

    return analysis_row


def get_upload_results(upload_id: int,db: Session):
    
    query = select(AnalysisResult).where(
        AnalysisResult.upload_id == upload_id
    )
    analysis_rows = db.scalars(query).all()

    return analysis_rows


def get_analysis_result(analysis_id: int, db: Session):
    query = select(AnalysisResult).where(
        AnalysisResult.id == analysis_id
    )
    analysis_row = db.scalar(query)
    return analysis_row

   
        