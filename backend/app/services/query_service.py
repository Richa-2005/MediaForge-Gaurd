from sqlalchemy.orm import Session
from sqlalchemy import select, desc

from app.models.upload import Upload
from app.models.analysis_result import AnalysisResult
from app.models.processing_artifacts import ProcessingArtifact
from app.models.processing_run import ProcessingRun
from app.models.processing_step import ProcessingStep

import logging
logger = logging.getLogger(__name__)


def build_upload_view(upload_id: int, db: Session):
    """
    Returns the complete view of an upload.
    Used by the dashboard.
    """

    summary = {}

    upload = db.get(Upload, upload_id)

    if upload is None:
        return None

    summary["upload"] = upload

    # Latest processing run
    run = db.scalar(
        select(ProcessingRun)
        .where(ProcessingRun.upload_id == upload_id)
        .order_by(desc(ProcessingRun.created_at))
    )

    summary["processing_run"] = run

    # Processing steps
    if run:
        steps = db.scalars(
            select(ProcessingStep)
            .where(
                ProcessingStep.processing_run_id == run.id
            )
            .order_by(ProcessingStep.created_at)
        ).all()
    else:
        steps = []

    summary["processing_steps"] = steps

    # Analysis results
    analysis = db.scalars(
        select(AnalysisResult).where(
            AnalysisResult.upload_id == upload_id
        )
    ).all()

    summary["analysis_results"] = analysis

    # Processing artifacts
    artifacts = db.scalars(
        select(ProcessingArtifact).where(
            ProcessingArtifact.upload_id == upload_id
        )
    ).all()

    summary["artifacts"] = artifacts

    return summary


def get_processing_timeline(upload_id: int, db: Session):
    """
    Returns only the processing timeline.
    """

    run = db.scalar(
        select(ProcessingRun)
        .where(
            ProcessingRun.upload_id == upload_id
        )
        .order_by(desc(ProcessingRun.created_at))
    )

    if run is None:
        return None

    steps = db.scalars(
        select(ProcessingStep)
        .where(
            ProcessingStep.processing_run_id == run.id
        )
        .order_by(ProcessingStep.created_at)
    ).all()

    return {
        "processing_run": run,
        "processing_steps": steps,
    }


def get_analysis_summary(upload_id: int, db: Session):
    """
    Returns all AI analysis results for an upload.
    """

    return db.scalars(
        select(AnalysisResult)
        .where(
            AnalysisResult.upload_id == upload_id
        )
        .order_by(AnalysisResult.created_at)
    ).all()


def get_artifacts(upload_id: int, db: Session):
    """
    Returns all preprocessing artifacts.
    """

    return db.scalars(
        select(ProcessingArtifact)
        .where(
            ProcessingArtifact.upload_id == upload_id
        )
        .order_by(ProcessingArtifact.created_at)
    ).all()


def get_recent_uploads(db: Session, limit: int = 5):
    """
    Returns the most recent uploads.
    """

    return db.scalars(
        select(Upload)
        .order_by(desc(Upload.created_at))
        .limit(limit)
    ).all()