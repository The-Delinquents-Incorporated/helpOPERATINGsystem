from pathlib import Path
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_BACKEND_DIR = Path(__file__).resolve().parents[1]


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
        env_file=(_PROJECT_ROOT / ".env", _BACKEND_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        populate_by_name=True,
    )

    @field_validator("OLLAMA_HOST", mode="before")
    @classmethod
    def normalize_ollama_host(cls, value: Any) -> str:
        host = str(value or "http://localhost:11434").strip().strip('"\'')
        if not host:
            return "http://localhost:11434"
        if not host.startswith(("http://", "https://")):
            host = f"http://{host}"
        return host.rstrip("/")

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value: Any) -> list[str]:
        if isinstance(value, str):
            value = value.strip()
            if not value:
                return ["*"]
            if value.startswith("["):
                return value
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


settings = Settings()
