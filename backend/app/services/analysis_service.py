from app.schemas.analysis_result import AnalysisResultCreate
from sqlalchemy.orm import Session
from sqlalchemy import delete, select
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

def build_analysis_payload(
    upload_id: int,
    agent_name: AgentName,
    result: AgentResult,
) -> dict:
    """
    Convert an AI-worker AgentResult into the backend
    AnalysisResultCreate-compatible dictionary.
    """

    result_analysis: AIAnalysisResult = result.analysis

    return {
        "upload_id": upload_id,
        "agent": agent_name,
        "label": result_analysis.label,
        "risk_score": result_analysis.risk_score,
        "confidence": result_analysis.confidence,
        "explanation": result_analysis.explanation,
        "evidence": [
            evidence.model_dump()
            for evidence in result_analysis.evidence
        ],
        "details": result.details or {},
    }

def get_processed_artifact(
    upload_id: int,
    artifacts: list[ProcessingArtifact],
    artifact_type: str,
) -> ProcessingArtifact:
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
            f"No {artifact_type} artifact found "
            f"for upload {upload_id}."
        )

    artifact_path = Path(processed_artifact.file_path)

    if not artifact_path.exists():
        raise FileNotFoundError(
            f"Artifact file not found: {artifact_path}"
        )

    return processed_artifact

def run_analysis(
    upload,
    db: Session,
) -> list[AnalysisResult]:
    artifacts = db.scalars(
        select(ProcessingArtifact).where(
            ProcessingArtifact.upload_id == upload.id
        )
    ).all()

    analysis_agent = AnalysisAgent()

    logger.info(
        "Analysis started | upload_id=%s media_type=%s",
        upload.id,
        upload.media_type,
    )

    if upload.media_type == "image":
        analysis_payloads = dispatch_single_agent(
            upload,
            artifacts,
            analysis_agent,
            artifact_type="processed_image",
            result_key="vision",
            agent_name=AgentName.VISION,
        )

    elif upload.media_type == "audio":
        analysis_payloads = dispatch_single_agent(
            upload,
            artifacts,
            analysis_agent,
            artifact_type="processed_audio",
            result_key="audio",
            agent_name=AgentName.AUDIO,
        )

    elif upload.media_type == "video":
        analysis_payloads = run_video_analysis(
            upload,
            artifacts,
            analysis_agent,
        )
    elif upload.media_type == "text":
        analysis_payloads = dispatch_text_agents(
            upload,
            artifacts,
            analysis_agent,
        )

    else:
        raise ValueError(
            "Analysis is not implemented for media type: "
            f"{upload.media_type}"
        )

    # Validate every result before changing the database. Replacing the
    # same agents in one transaction makes Celery retries idempotent and
    # prevents a partially stored text/fact-check/fusion result set.
    validated_analyses = [
        AnalysisResultCreate(**payload)
        for payload in analysis_payloads
    ]
    agents = [analysis.agent for analysis in validated_analyses]
    saved_results = [
        AnalysisResult(
            upload_id=analysis.upload_id,
            agent=analysis.agent,
            label=analysis.label,
            risk_score=analysis.risk_score,
            confidence=analysis.confidence,
            explanation=analysis.explanation,
            evidence=analysis.evidence,
            details=analysis.details,
        )
        for analysis in validated_analyses
    ]

    try:
        db.execute(
            delete(AnalysisResult).where(
                AnalysisResult.upload_id == upload.id,
                AnalysisResult.agent.in_(agents),
            )
        )
        db.add_all(saved_results)
        db.commit()
        for saved_result in saved_results:
            db.refresh(saved_result)
    except Exception:
        db.rollback()
        logger.exception(
            "Failed to atomically store analyses | upload_id=%s",
            upload.id,
        )
        raise

    logger.info(
        "Analysis completed | upload_id=%s results=%s",
        upload.id,
        len(saved_results),
    )

    return saved_results

def run_video_analysis(
    upload,
    artifacts: list[ProcessingArtifact],
    analysis_agent: AnalysisAgent,
) -> list[dict]:

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
                "highest_risk_artifact_id": highest_risk_artifact.id,
                "frame_results": per_frame_results,
            },
        }
        logger.info(
            "Video analysis prepared | upload_id=%s frames=%s "
            "highest_risk=%s",
            upload.id,
            len(frame_results),
            result_analysis.risk_score,
        )

        return [extracted_analysis]


def dispatch_single_agent(
    upload,
    artifacts: list[ProcessingArtifact],
    analysis_agent: AnalysisAgent,
    *,
    artifact_type: str,
    result_key: str,
    agent_name: AgentName,
) -> list[dict]:
    processed_artifact = get_processed_artifact(
        upload_id=upload.id,
        artifacts=artifacts,
        artifact_type=artifact_type,
    )

    media_path = Path(processed_artifact.file_path)

    result_output = analysis_agent.analyze(
        upload_id=upload.id,
        media_path=media_path,
        media_type=upload.media_type,
    )

    result: AgentResult | None = result_output.get(
        result_key
    )

    if result is None:
        raise ValueError(
            f"{result_key} agent returned no result "
            f"for upload {upload.id}."
        )

    return [
        build_analysis_payload(
            upload_id=upload.id,
            agent_name=agent_name,
            result=result,
        )
    ]

def dispatch_text_agents(
    upload,
    artifacts: list[ProcessingArtifact],
    analysis_agent: AnalysisAgent,
) -> list[dict]:
    processed_artifact = get_processed_artifact(
        upload_id=upload.id,
        artifacts=artifacts,
        artifact_type="processed_text",
    )

    text_path = Path(processed_artifact.file_path)

    result_output = analysis_agent.analyze(
        upload_id=upload.id,
        media_path=text_path,
        media_type="text",
    )

    result_mappings = (
        (
            "text",
            AgentName.TEXT,
        ),
        (
            "factcheck",
            AgentName.FACTCHECK,
        ),
        (
            "fusion",
            AgentName.SUPERVISOR,
        ),
    )

    payloads: list[dict] = []

    for result_key, agent_name in result_mappings:
        result: AgentResult | None = result_output.get(
            result_key
        )

        if result is None:
            logger.warning(
                "%s agent returned no result | upload_id=%s",
                result_key,
                upload.id,
            )
            continue

        payloads.append(
            build_analysis_payload(
                upload_id=upload.id,
                agent_name=agent_name,
                result=result,
            )
        )

    if not payloads:
        raise ValueError(
            f"No text analysis results were produced "
            f"for upload {upload.id}."
        )

    return payloads
