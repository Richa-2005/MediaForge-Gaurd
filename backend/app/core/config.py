from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Media Sentinel"
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./media_sentinel.db"

    class Config:
        env_file = ".env"


settings = Settings()