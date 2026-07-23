from fastapi import APIRouter
from app.api.v1 import uploads
from app.api.v1 import status
from app.api.v1 import analysis
from app.api.v1 import auth
from app.api.v1 import dashboard


api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(status.router, tags=["status"])
api_router.include_router(uploads.router, tags=["upload"])
api_router.include_router(analysis.router, tags=["analysis"])
api_router.include_router(dashboard.router)
