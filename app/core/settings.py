from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    GOOGLE_API_KEY: str = "NO_KEY"  # Valor por defecto para CI
    TESTING: bool = False
    DB_URL: str = "sqlite:///:memory:"  # DB en memoria para CI


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
