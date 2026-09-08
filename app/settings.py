import os
from dataclasses import dataclass
from urllib.parse import urlparse


def _positive_float(name: str, default: str) -> float:
    raw_value = os.environ.get(name, default)
    try:
        value = float(raw_value)
    except ValueError as exc:
        raise ValueError(f"{name} must be a number") from exc
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return value


def _positive_int(name: str, default: str) -> int:
    raw_value = os.environ.get(name, default)
    try:
        value = int(raw_value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return value


def _http_url(name: str, value: str) -> str:
    normalized = value.strip().rstrip("/")
    parsed = urlparse(normalized)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"{name} must be an absolute HTTP(S) URL")
    return normalized


@dataclass(frozen=True)
class ChatSettings:
    """Runtime configuration for the dedicated chat API."""

    organizer_base_url: str
    mcp_url: str
    codex_executable: str
    codex_timeout_seconds: float
    organizer_timeout_seconds: float
    max_concurrency: int
    max_message_chars: int
    max_response_bytes: int

    @classmethod
    def from_env(cls) -> "ChatSettings":
        return cls(
            organizer_base_url=_http_url(
                "ORGANIZER_BASE_URL",
                os.environ.get("ORGANIZER_BASE_URL", "http://localhost:8001"),
            ),
            mcp_url=_http_url(
                "CHAT_MCP_URL",
                os.environ.get("CHAT_MCP_URL", "http://localhost:8004/mcp"),
            ),
            codex_executable=(
                os.environ.get("CHAT_CODEX_EXECUTABLE", "codex").strip() or "codex"
            ),
            codex_timeout_seconds=_positive_float(
                "CHAT_CODEX_TIMEOUT_SECONDS", "120"
            ),
            organizer_timeout_seconds=_positive_float(
                "CHAT_ORGANIZER_TIMEOUT_SECONDS", "5"
            ),
            max_concurrency=_positive_int("CHAT_MAX_CONCURRENCY", "2"),
            max_message_chars=_positive_int("CHAT_MAX_MESSAGE_CHARS", "10000"),
            max_response_bytes=_positive_int(
                "CHAT_MAX_RESPONSE_BYTES", "1000000"
            ),
        )
