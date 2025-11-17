from dataclasses import dataclass
import os
from typing import Optional

from dotenv import load_dotenv


class ConfigError(Exception):
    """Raised when required configuration values are missing or invalid."""


@dataclass(frozen=True)
class Settings:
    api_id: int
    api_hash: str
    session_string: Optional[str]
    session_name: str


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ConfigError(f"Missing required environment variable: {name}")
    return value


def _require_int(name: str) -> int:
    raw = _require_env(name)
    try:
        return int(raw)
    except ValueError as exc:
        raise ConfigError(f"Environment variable {name} must be an integer") from exc


def load_settings() -> Settings:
    """
    Load and validate environment-driven settings for the Telegram MCP server.

    Returns:
        Settings: validated configuration dataclass.

    Raises:
        ConfigError: when required values are missing or malformed.
    """
    load_dotenv()
    api_id = _require_int("TELEGRAM_API_ID")
    api_hash = _require_env("TELEGRAM_API_HASH")
    session_string = os.getenv("TELEGRAM_SESSION_STRING")
    session_name = os.getenv("TELEGRAM_SESSION_NAME") or "anon"

    return Settings(
        api_id=api_id,
        api_hash=api_hash,
        session_string=session_string,
        session_name=session_name,
    )


__all__ = ["ConfigError", "Settings", "load_settings"]
