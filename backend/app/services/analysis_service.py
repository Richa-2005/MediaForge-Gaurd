from app.schemas.analysis_result import AnalysisResultCreate
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.analysis_result import AnalysisResult
from pydantic import ValidationError

from pathlib import Path

from app.models.processing_artifacts import ProcessingArtifact
from app.models.analysis_result import AgentName

from ai_workers.src.agents.analysis_agent import AnalysisAgent
from ai_workers.src.schemas.agent_result import AgentResult
from ai_workers.src.schemas.analysis_result import AnalysisResult as AIAnalysisResult

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
        logger.exception(
            "\nCould not Store the analysis result.\n %s",
            val
        )
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

   
        
def run_analysis(upload, db: Session):
    artifacts = db.scalars(
        select(ProcessingArtifact).where(
            ProcessingArtifact.upload_id == upload.id
        )
    ).all()

    analysis_agent = AnalysisAgent()

    if upload.media_type == "video":
        return run_video_analysis(upload,artifacts,analysis_agent,db)

    elif upload.media_type == "image":
        artifact_type = "processed_image"
        result_key = "vision"
        agent_name = AgentName.VISION

    elif upload.media_type == "audio":
        artifact_type = "processed_audio"
        result_key = "audio"
        agent_name = AgentName.AUDIO

    else:
        raise ValueError(
            f"Analysis is not implemented for media type: {upload.media_type}"
        )

    processed_artifact = next(
        (
            artifact
            for artifact in artifacts
            if artifact.artifact_type == artifact_type
            and artifact.file_path
        ),
        None,
    )

    if processed_artifact is None:
        raise ValueError(
            f"No {artifact_type} artifact found for upload {upload.id}."
        )

    media_path = Path(processed_artifact.file_path)

    if not media_path.exists():
        raise FileNotFoundError(
            f"Artifact file not found: {media_path}"
        )

    logger.info(
        "Analysis started | upload_id=%s media_type=%s",
        upload.id,
        upload.media_type,
    )

    result_output = analysis_agent.analyze(
        upload_id=upload.id,
        media_path=media_path,
        media_type=upload.media_type,
    )

    result: AgentResult | None = result_output.get(result_key)

    if result is None:
        raise ValueError(
            f"{result_key} agent returned no result for upload {upload.id}."
        )

    result_analysis: AIAnalysisResult = result.analysis

    extracted_analysis = {
        "upload_id": upload.id,
        "agent": agent_name,
        "label": result_analysis.label,
        "risk_score": result_analysis.risk_score,
        "confidence": result_analysis.confidence,
        "explanation": result_analysis.explanation,
        "evidence": [
            evidence.model_dump()
            for evidence in result_analysis.evidence
        ],
        "details": result.details,
    }

    saved_result = save_analysis_result(extracted_analysis, db)

    logger.info(
        "Analysis completed | upload_id=%s agent=%s",
        upload.id,
        agent_name,
    )

    return saved_result


def run_video_analysis(upload, artifacts, analysis_agent, db: Session):

        frame_artifacts = [
            artifact
            for artifact in artifacts
            if artifact.artifact_type == "frame"
            and artifact.file_path
        ]
        if not frame_artifacts:
            raise ValueError(
                f"No frame artifacts found for upload {upload.id}."
            )
        frame_results: list[tuple[ProcessingArtifact, AgentResult]] = []
        for frame_artifact in frame_artifacts:
            frame_path = Path(frame_artifact.file_path)
            if not frame_path.exists():
                logger.warning(
                    "Video frame missing; skipping | upload_id=%s path=%s",
                    upload.id,
                    frame_path,
                )
                continue
            result_output = analysis_agent.analyze(
                upload_id=upload.id,
                media_path=frame_path,
                media_type="image",
            )
            frame_result: AgentResult | None = result_output.get("vision")
            if frame_result is not None:
                frame_results.append(
                    (frame_artifact, frame_result)
                )
        if not frame_results:
            raise ValueError(
                f"Vision agent returned no frame results "
                f"for video upload {upload.id}."
            )
        # Select the frame with the highest risk score
        highest_risk_artifact, highest_risk_result = max(
            frame_results,
            key=lambda item: item[1].analysis.risk_score,
        )
        result_analysis: AIAnalysisResult = (
            highest_risk_result.analysis
        )
        per_frame_results = []
        for frame_artifact, frame_result in frame_results:
            frame_analysis = frame_result.analysis
            per_frame_results.append(
                {
                    "artifact_id": frame_artifact.id,
                    "file_path": frame_artifact.file_path,
                    "label": frame_analysis.label,
                    "risk_score": frame_analysis.risk_score,
                    "confidence": frame_analysis.confidence,
                }
            )
        extracted_analysis = {
            "upload_id": upload.id,
            "agent": AgentName.VIDEO,
            "label": result_analysis.label,
            "risk_score": result_analysis.risk_score,
            "confidence": result_analysis.confidence,
            "explanation": (
                f"Video analysis completed across "
                f"{len(frame_results)} frames. "
                f"The final result is based on the frame "
                f"with the highest risk score."
            ),
            "evidence": [
                evidence.model_dump()
                for evidence in result_analysis.evidence
            ],
            "details": {
                "total_frames": len(frame_artifacts),
                "analyzed_frames": len(frame_results),
                "highest_risk_frame": (
                    highest_risk_artifact.file_path
                ),
                "frame_results": per_frame_results,
            },
        }
        saved_result = save_analysis_result(
            extracted_analysis,
            db,
        )
        logger.info(
            "Video analysis completed | upload_id=%s frames=%s "
            "highest_risk=%s",
            upload.id,
            len(frame_results),
            result_analysis.risk_score,
        )
        return saved_result