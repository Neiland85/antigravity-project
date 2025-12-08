from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    GOOGLE_API_KEY: str = "test_mode_key"
    DB_URL: str = "sqlite:///./data/oracle.db"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    # En test: fuerzo config dummy y DB in-memory
    if os.getenv("TESTING") == "true":
        return Settings(
            GOOGLE_API_KEY="test_key",
            DB_URL="sqlite:///:memory:"
        )
    return Settings()


settings = get_settings()

