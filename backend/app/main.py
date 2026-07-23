from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.models import create_tables

from app.core.logging_config import configure_logging
configure_logging()

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_tables()

app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.get("/")
def root():
    return {"message": "Media Sentinel Running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
