from app.models.processing_step import ProcessingStep, StepStatus
from sqlalchemy.orm import Session
from datetime import datetime, timezone

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
        step.started_at = datetime.now(timezone.utc)
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
        step.completed_at = datetime.now(timezone.utc)
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
        step.completed_at = datetime.now(timezone.utc)
        step.duration_ms =  int(
            (step.completed_at - step.started_at).total_seconds() * 1000
        )
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

