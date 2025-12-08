from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    GOOGLE_API_KEY: str = "fake"
    TESTING: bool = False
    IN_DOCKER: bool = False

settings = Settings()
