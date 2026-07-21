from app.services.processor_adapter import (
    process_video_adapter,process_image_adapter,
    process_audio_adapter, process_text_adapter
)
from app.services.artifact_service import save_artifacts
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.processing_step import ProcessingStep, StepStatus
from app.services.execution_service import (
    create_step, start_step, complete_step
)

import logging
logger = logging.getLogger(__name__)

def route_service(upload, db: Session):
    media_type = upload.media_type

    logger.info(
        "Routing media | upload_id=%s media_type=%s",
        upload.id,
        upload.media_type,
    )

    if media_type == "video":
        artifacts = process_video_adapter(upload)
        saved = save_artifacts(artifacts, db)
        return saved

    elif media_type == "image":
        artifacts = process_image_adapter(upload)
        saved = save_artifacts(artifacts, db)
        return saved

    elif media_type == "audio" :
        artifacts = process_audio_adapter(upload)
        saved = save_artifacts(artifacts, db)
        return saved

    elif media_type == "text":
        artifacts = process_text_adapter(upload)
        saved = save_artifacts(artifacts, db)
        return saved

    raise ValueError(
        f"Preprocessing is not implemented for media type: {media_type}"
    )


def run_preprocessing(upload, run, db : Session):

        media_preprocessing_step = db.scalar(
            select(ProcessingStep).where(
                ProcessingStep.processing_run_id == run.id,
                ProcessingStep.step_name == "preprocessing",
            )
        )

        if media_preprocessing_step is None:
            media_preprocessing_step = create_step(
                run.id,
                "preprocessing",
                db,
            )

        if media_preprocessing_step.status == StepStatus.PENDING:
            start_step(media_preprocessing_step, db)

            logger.info(
                "Step started | run_id=%s step=%s",
                run.id,
                "media_preprocessing",
            )
        
        if media_preprocessing_step.status != StepStatus.COMPLETED:
            saved = route_service(upload, db)
            complete_step(media_preprocessing_step, db)

            logger.info(
                "Step completed | run_id=%s step=%s artifacts=%s",
                run.id,
                "preprocessing",
                len(saved),
            )

        else:
            logger.info(
                "Skipping completed preprocessing | run_id=%s",
                run.id,
            )

            saved = []

        return saved, media_preprocessing_step
