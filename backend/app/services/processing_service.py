from app.services.processor_adapter import (
    process_video_adapter,process_image_adapter,
    process_audio_adapter
)
from app.services.artifact_service import save_artifacts
from sqlalchemy.orm import Session

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

    return None
