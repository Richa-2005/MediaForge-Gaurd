from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = "Media Sentinel"
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./media_sentinel.db"
    BASE_DIR: str = "/Users/richagupta/Documents/MediaForge-Gaurd/backend"
    UPLOAD_DIR: str = BASE_DIR + "/storage/uploads"
    MAX_UPLOAD_SIZE_BYTES : int = 50 * 1024 * 1024
    ALLOWED_MIME_TYPES : set[str] = {
        "image/jpg",
        "image/jpeg", 
        "image/png",  
        "video/mp4", 
        "audio/mp3",
        "audio/mpeg",
        "text/plain"
    }

    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"

    PROCESSING_DIR: Path = Path(BASE_DIR) / "storage" / "processing"

    class Config:
        env_file = ".env"


settings = Settings()
