from app.models.processing_step import ProcessingStep, StepStatus
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.processing_run import RunStatus
from app.models.upload import Upload, UploadStatus
from app.models.analysis_result import AgentName, AnalysisResult

import logging
logger = logging.getLogger(__name__)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def elapsed_ms(started_at: datetime | None, completed_at: datetime) -> int:
    if started_at is None:
        return 0

    if started_at.tzinfo is None:
        started_at = started_at.replace(tzinfo=timezone.utc)
    if completed_at.tzinfo is None:
        completed_at = completed_at.replace(tzinfo=timezone.utc)

    return int((completed_at - started_at).total_seconds() * 1000)


def generate_upload_report(*, upload_id: int, primary_analysis_id: int, db):
    """Load the LLM stack only inside the task that needs it."""
    from app.services.llm.report_service import (
        generate_upload_report as generate_report,
    )

    return generate_report(
        upload_id=upload_id,
        primary_analysis_id=primary_analysis_id,
        db=db,
    )

def create_step(
    processing_run_id: int,
    step_name: str,
    db: Session
) -> ProcessingStep:

    try:
        row = ProcessingStep(
            processing_run_id=processing_run_id,
            step_name=step_name,
            status=StepStatus.PENDING,
        )
        db.add(row)
        db.commit()
        db.refresh(row)
    except Exception as e:
        db.rollback()
        raise

    return row


def get_or_create_step(
    processing_run_id: int,
    step_name: str,
    db: Session,
) -> ProcessingStep:
    existing = (
        db.query(ProcessingStep)
        .filter(
            ProcessingStep.processing_run_id == processing_run_id,
            ProcessingStep.step_name == step_name,
        )
        .first()
    )
    if existing is not None:
        return existing

    return create_step(processing_run_id, step_name, db)

def start_step(
    step: ProcessingStep,
    db: Session
):
    if step is None:
        raise ValueError("The process has not been stored as a step yet.")
    try:
        step.status = StepStatus.RUNNING
        step.started_at = utc_now()
        db.commit()
        db.refresh(step)
    except Exception as e:
        db.rollback()
        raise

def complete_step(
    step: ProcessingStep,
    db: Session
):
    if step is None:
        raise ValueError("The process has not been stored as a step yet.")
    try:
        step.status = StepStatus.COMPLETED
        step.completed_at = utc_now()
        step.duration_ms = elapsed_ms(step.started_at, step.completed_at)
        
        db.commit()
        db.refresh(step)
    except Exception as e:
        db.rollback()
        raise


def fail_step(
    step: ProcessingStep,
    error: str,
    db: Session
):
    if step is None:
        raise ValueError("The process has not been stored as a step yet.")
    try:
        step.status = StepStatus.FAILED
        step.completed_at = utc_now()
        step.duration_ms = elapsed_ms(step.started_at, step.completed_at)
        step.error_message = error
        db.commit()
        db.refresh(step)
    except Exception as e:
        db.rollback()
        raise

def skip_step(
    step: ProcessingStep,
    db: Session
):
    if step is None:
        raise ValueError("The process has not been stored as a step yet.")
    try:
        step.status = StepStatus.SKIPPED
        db.commit()
        db.refresh(step)
    except Exception as e:
        db.rollback()
        raise


def complete_processing(
    saved_analyses: list[AnalysisResult],
    upload,
    running,
    db: Session,
):
    if not saved_analyses:
        raise ValueError(
            f"No analysis results were produced "
            f"for upload {upload.id}."
    )
    running.status = RunStatus.COMPLETED
    running.completed_at = utc_now()
    if running.started_at is None:
        raise ValueError(
            f"Processing run {running.id} has no started_at timestamp."
        )
    running.duration_ms = elapsed_ms(running.started_at, running.completed_at)

    upload.status = UploadStatus.COMPLETED

    db.commit()
    db.refresh(running)

    logger.info(
        "Processing run completed | run_id=%s duration=%sms",
        running.id,
        running.duration_ms,
    )

    supervisor_result = next(
        (
            result
            for result in saved_analyses
            if result.agent == AgentName.SUPERVISOR
        ),
        None,
    )
    primary_result = supervisor_result or max(
        saved_analyses,
        key=lambda result: result.risk_score,
    )

    report_step = get_or_create_step(
        running.id,
        "report_generation",
        db,
    )

    if report_step.status == StepStatus.PENDING:
        start_step(report_step, db)

    try:
        generate_upload_report(
            upload_id=upload.id,
            primary_analysis_id=primary_result.id,
            db=db,
        )
        complete_step(report_step, db)
    except Exception:
        fail_step(report_step, "Report generation failed.", db)
        logger.exception(
            "Unable to generate LLM report "
            "for analysis_id=%s",
            primary_result.id,
        )

    return running


def fail_processing(
    upload_id,
    running,
    media_preprocessing_step,
    error,
    db,
):
    if (
        media_preprocessing_step is not None
        and media_preprocessing_step.status != StepStatus.COMPLETED
    ):
        fail_step(media_preprocessing_step, str(error), db)

    upload = db.get(Upload, upload_id)
    if upload is not None:
        upload.status = UploadStatus.FAILED

    if running is not None:
        running.status = RunStatus.FAILED
        running.completed_at = utc_now()
        if running.started_at is None:
            raise ValueError(
                f"Processing run {running.id} has no started_at timestamp."
            )
        running.duration_ms = elapsed_ms(running.started_at, running.completed_at)

    db.commit()
