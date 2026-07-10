from fastapi import APIRouter,Depends, HTTPException, status
from app.database.session import get_db
from app.services.analysis_service import get_analysis_result
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/api/v1/analysis/{result_id}")
def get_analysis(
    result_id: int, 
    db: Session = Depends(get_db)
):
    result = get_analysis_result(result_id,db)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analyis of this id not found"
        )
    
    return result
