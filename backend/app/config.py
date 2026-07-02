import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App Settings
    API_TITLE: str = "HelpOS API"
    API_VERSION: str = "1.0.0"
    
    # Ollama Settings
    OLLAMA_HOST: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"
    
    # CORS Settings
    ALLOWED_ORIGINS: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
