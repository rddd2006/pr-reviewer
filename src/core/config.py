import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parents[2] / ".env")


def _get_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(slots=True)
class Settings:
    max_tokens: int = 3000
    enable_compression: bool = True
    log_level: str = "INFO"
    llm_provider: str = "gemini"
    gemini_model: str = "gemini-2.5-flash"
    openai_model: str = "gpt-4o-mini"
    llm_timeout_seconds: int = 60
    gemini_retry_attempts: int = 3
    gemini_retry_backoff_seconds: int = 5

    @classmethod
    def from_env(cls):
        return cls(
            max_tokens=int(os.getenv("MAX_TOKENS", "3000")),
            enable_compression=_get_bool("ENABLE_COMPRESSION", True),
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
            llm_provider=os.getenv("LLM_PROVIDER", "gemini").strip().lower(),
            gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            llm_timeout_seconds=int(os.getenv("LLM_TIMEOUT_SECONDS", "60")),
            gemini_retry_attempts=int(os.getenv("GEMINI_RETRY_ATTEMPTS", "3")),
            gemini_retry_backoff_seconds=int(os.getenv("GEMINI_RETRY_BACKOFF_SECONDS", "5")),
        )
