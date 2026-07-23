from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.services.query_service import (
    build_upload_view,
    get_processing_timeline,
    get_analysis_summary,
    get_artifacts,
    get_recent_uploads,
)

from app.schemas.UploadSummaryResponse import UploadSummaryResponse
from app.schemas.analysis_result import AnalysisResultResponse
from app.schemas.processing_artifact import ProcessingArtifactResponse
from app.schemas.processing_run import ProcessingRunResponse
from app.schemas.processing_step import ProcessingStepResponse
from app.schemas.upload import UploadResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get(
    "/uploads/{upload_id}/summary",
    response_model=UploadSummaryResponse,
)
def upload_summary(
    upload_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    summary = build_upload_view(upload_id, db, current_user.id)

    if summary is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Upload not found",
        )

    return UploadSummaryResponse(
        upload=UploadResponse.model_validate(
            summary["upload"], from_attributes=True
        ),

        processing_run=ProcessingRunResponse.model_validate(
            summary["processing_run"], from_attributes=True
        ) if summary["processing_run"] else None,

        processing_steps=[
            ProcessingStepResponse.model_validate(
                step, from_attributes=True
            )for step in summary["processing_steps"]
        ],

        analysis_results=[
            AnalysisResultResponse.model_validate(
                r, from_attributes=True
            )for r in summary["analysis_results"]
        ],

        artifacts=[
            ProcessingArtifactResponse.model_validate(
                a, from_attributes=True
            )for a in summary["artifacts"]
        ],
    )


@router.get("/uploads/{upload_id}/timeline")
def upload_timeline(
    upload_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    timeline = get_processing_timeline(upload_id, db, current_user.id)

    if timeline is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Processing timeline not found",
        )
    
    
    return {
        "processing_run": ProcessingRunResponse.model_validate(
                timeline["processing_run"], from_attributes=True
        ),
        "processing_steps": [
            ProcessingStepResponse.model_validate(
                step,from_attributes=True
            )for step in timeline["processing_steps"]
        ]
    }


@router.get(
        "/uploads/{upload_id}/analysis",
        response_model=list[AnalysisResultResponse]
)
def upload_analysis(
    upload_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result =  get_analysis_summary(upload_id, db, current_user.id)
    return [
        AnalysisResultResponse.model_validate(
            analysis, from_attributes=True
        )for analysis in result
    ]


@router.get(
        "/uploads/{upload_id}/artifacts",
        response_model=list[ProcessingArtifactResponse]
)
def upload_artifacts(
    upload_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    artifacts= get_artifacts(upload_id, db, current_user.id)
    return [
        ProcessingArtifactResponse.model_validate(
            artifact, from_attributes=True
        )for artifact in artifacts
    ]


@router.get(
        "/uploads/recent",
        response_model=list[UploadResponse]
)
def recent_uploads(
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recent_upload= get_recent_uploads(db, limit, current_user.id)
    return [
        UploadResponse.model_validate(
            upload, from_attributes=True
        ) for upload in recent_upload
    ]
