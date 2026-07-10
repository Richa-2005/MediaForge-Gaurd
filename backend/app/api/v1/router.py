from fastapi import APIRouter
from app.api.v1 import uploads
from app.api.v1 import status
from app.api.v1 import analysis

api_router = APIRouter()
api_router.include_router(status.router, tags=["status"])
api_router.include_router(uploads.router, tags=["upload"])
api_router.include_router(analysis.router, tags=["analysis"])