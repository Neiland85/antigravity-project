from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

    GOOGLE_API_KEY: str = Field(default="fake", alias="ANTIGRAVITY_API_KEY")
    GRAVITY_TOKEN: str = Field(default="zero-gravity-default-token", alias="GRAVITY_TOKEN")
    TESTING: bool = False
    IN_DOCKER: bool = False
    MOCK_AI: bool = False
    
    # Internal Service URLs
    SENTINEL_URL: str = Field(default="http://sentinel:9000", alias="SENTINEL_URL")
    BACKEND_URL: str = Field(default="http://oracle:8080", alias="BACKEND_URL")
    
    DB_URL: str = "sqlite:///./data/antigravity.db"

settings = Settings()
