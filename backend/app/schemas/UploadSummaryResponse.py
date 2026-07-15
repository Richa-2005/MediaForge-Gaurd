from pydantic import BaseModel
from app.schemas.processing_artifact import ProcessingArtifactResponse
from app.schemas.processing_run import ProcessingRunResponse
from app.schemas.processing_step import ProcessingStepResponse
from app.schemas.upload import UploadResponse
from app.schemas.analysis_result import AnalysisResultResponse

class UploadSummaryResponse(BaseModel):
    upload: UploadResponse
    processing_run: ProcessingRunResponse | None
    processing_steps: list[ProcessingStepResponse]
    analysis_results: list[AnalysisResultResponse]
    artifacts: list[ProcessingArtifactResponse]