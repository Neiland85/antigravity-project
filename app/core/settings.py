from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

    GOOGLE_API_KEY: str = Field(default="fake", alias="ANTIGRAVITY_API_KEY")
    TESTING: bool = False
    IN_DOCKER: bool = False
    MOCK_AI: bool = False
    DB_URL: str = "sqlite:///./data/antigravity.db"

settings = Settings()
