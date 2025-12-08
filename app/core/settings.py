from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "fake")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
