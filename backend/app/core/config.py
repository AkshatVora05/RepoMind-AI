from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "RepoMind AI"
    API_V1_STR: str = "/api/v1"

    # Database (Postgres)
    DATABASE_URL: str = ""

    # Pinecone
    PINECONE_API_KEY: str = ""
    PINECONE_INDEX_NAME: str = ""
    PINECONE_ENVIRONMENT: str = ""

    # AI
    GEMINI_API_KEY: str = ""

    # GitHub
    GITHUB_PAT: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
