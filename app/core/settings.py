from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    GOOGLE_API_KEY: str = ""
    TESTING: bool = False
    DB_URL: str = "sqlite:///:memory:"  # Default para CI y tests

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
