from app.models.processing_artifacts import ProcessingArtifact
from sqlalchemy import delete
from sqlalchemy.orm import Session

import logging
logger = logging.getLogger(__name__)

def save_artifacts(artifacts , db:Session):
    if not artifacts:
        return []

    rows = []
    for arti in artifacts:
        obj = ProcessingArtifact(
            upload_id=arti["upload_id"],
            artifact_type=arti["artifact_type"],
            file_path=arti["file_path"],
            details=arti["details"]
        ) 
        rows.append(obj)
    try:
        # A retry replaces artifacts produced by the same preprocessing
        # route, including a complete set of video frames.
        upload_id = rows[0].upload_id
        artifact_types = {row.artifact_type for row in rows}
        db.execute(
            delete(ProcessingArtifact).where(
                ProcessingArtifact.upload_id == upload_id,
                ProcessingArtifact.artifact_type.in_(artifact_types),
            )
        )
        db.add_all(rows)
        db.commit()

        
        for row in rows:
            db.refresh(row)

        logger.info(
            "Saved %d artifacts | upload_id=%s",
            len(rows),
            upload_id,
        )

        return rows
    except Exception as e:
        db.rollback()
        logger.exception(
            "Artifact persistence failed"
        )
        raise


def save_artifact(arti , db:Session):
  
    obj = ProcessingArtifact(
        upload_id=arti["upload_id"],
        artifact_type=arti["artifact_type"],
        file_path=arti["file_path"],
        details=arti["details"]
    ) 

    try:
        db.add(obj)
        db.commit()
        db.refresh(obj)

        return obj

    except Exception as e:
        db.rollback()
        raise
