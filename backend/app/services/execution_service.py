from app.models.processing_step import ProcessingStep, StepStatus
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.processing_run import RunStatus
from app.models.upload import Upload, UploadStatus


import logging
logger = logging.getLogger(__name__)

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

def start_step(
    step: ProcessingStep,
    db: Session
):
    if step is None:
        raise ValueError("The process has not been stored as a step yet.")
    try:
        step.status = StepStatus.RUNNING
        step.started_at = datetime.now(timezone.utc).replace(tzinfo=None)
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
        step.completed_at =datetime.now(timezone.utc).replace(tzinfo=None)
        step.duration_ms =  int(
            (step.completed_at - step.started_at).total_seconds() * 1000
        )
        
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
        step.completed_at = datetime.now(timezone.utc).replace(tzinfo=None).replace(tzinfo=None)
        if step.started_at is not None:
            step.duration_ms =  int(
                (step.completed_at - step.started_at).total_seconds() * 1000
            )
        else:
            step.duration_ms  = 0
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


def complete_processing(upload, running, db: Session):

    running.status = RunStatus.COMPLETED
    running.completed_at = datetime.now(timezone.utc).replace(tzinfo=None)
    if running.started_at is None:
        raise ValueError(
            f"Processing run {running.id} has no started_at timestamp."
        )
    running.duration_ms = int(
        (running.completed_at - running.started_at).total_seconds() * 1000
    )

    upload.status = UploadStatus.COMPLETED

    db.commit()
    db.refresh(running)

    logger.info(
        "Processing run completed | run_id=%s duration=%sms",
        running.id,
        running.duration_ms,
    )

    return running


def fail_processing(
    upload_id,
    running,
    media_preprocessing_step,
    error,
    db,
):
    if media_preprocessing_step is not None:
        fail_step(media_preprocessing_step, str(error), db)

    upload = db.get(Upload, upload_id)
    if upload is not None:
        upload.status = UploadStatus.FAILED

    if running is not None:
        running.status = RunStatus.FAILED
        running.completed_at = datetime.now(timezone.utc).replace(tzinfo=None)
        if running.started_at is None:
            raise ValueError(
                f"Processing run {running.id} has no started_at timestamp."
            )
        running.duration_ms = int(
            (running.completed_at - running.started_at).total_seconds()
            * 1000
        )

    db.commit()