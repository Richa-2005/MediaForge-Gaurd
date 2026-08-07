from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from pydantic import SecretStr, model_validator


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
BACKEND_ROOT = REPOSITORY_ROOT / "backend"


class Settings(BaseSettings):
    PROJECT_NAME: str = "MediaForge-Gaurd"
    ENVIRONMENT: str = "development"
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str = f"sqlite:///{REPOSITORY_ROOT / 'mediaforge.db'}"
    BASE_DIR: Path = BACKEND_ROOT
    UPLOAD_DIR: Path = BACKEND_ROOT / "storage" / "uploads"
    MAX_UPLOAD_SIZE_BYTES : int = 50 * 1024 * 1024
    URL_DOWNLOAD_TIMEOUT_SECONDS: float = 15.0
    URL_SOCIAL_DOWNLOAD_TIMEOUT_SECONDS: float = 30.0
    URL_SOCIAL_METADATA_MAX_BYTES: int = 1024 * 1024
    URL_MAX_REDIRECTS: int = 5
    ALLOWED_MIME_TYPES : set[str] = {
        "image/jpg",
        "image/jpeg",
        "image/png",
        "image/webp",
        "video/mp4",
        "audio/mp3",
        "audio/mpeg",
        "audio/wav",
        "audio/x-wav",
        "text/plain"
    }
    MEDIA_PROCESSING_QUEUES : dict = {
        "image": "image_queue",
        "text": "text_queue",
        "video": "video_queue",
        "audio": "audio_queue",
    }
    DISABLED_MEDIA_TYPES: set[str] = set()
    HEAVY_MEDIA_TYPES: set[str] = {"video", "audio"}
    MAX_ACTIVE_HEAVY_JOBS: int = 1
    PROCESSING_TASK_SOFT_TIME_LIMIT_SECONDS: int = 15 * 60
    PROCESSING_TASK_TIME_LIMIT_SECONDS: int = 20 * 60

    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"

    PROCESSING_DIR: Path = BACKEND_ROOT / "storage" / "processing"
    SUPABASE_URL: str = ""
    SUPABASE_SERVICE_ROLE_KEY: SecretStr = SecretStr("")
    SUPABASE_STORAGE_BUCKET: str = ""

    LLM_PROVIDER: str = "OLLAMA"
    GROQ_API_KEY: SecretStr = SecretStr("")
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    JWT_SECRET_KEY: SecretStr = SecretStr("change-me-in-production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    @model_validator(mode="after")
    def validate_production_secrets(self):
        if (
            self.ENVIRONMENT.lower() == "production"
            and self.JWT_SECRET_KEY.get_secret_value()
            == "change-me-in-production"
        ):
            raise ValueError(
                "JWT_SECRET_KEY must be set to a secure value in production."
            )
        return self

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
