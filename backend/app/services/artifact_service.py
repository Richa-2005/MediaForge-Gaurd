from app.models.processing_artifacts import ProcessingArtifact
from sqlalchemy.orm import Session


def save_artifacts(artifacts , db:Session):
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
        db.add_all(rows)
        db.commit()
        
        for row in rows:
            db.refresh(row)

        return rows
    except Exception as e:
        db.rollback()
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

    