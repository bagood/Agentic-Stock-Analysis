from __future__ import annotations

import os
import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any
from pathlib import Path



def load_env(path: Path) -> None:
    """Load simple KEY=VALUE entries without overriding existing variables."""
    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"Invalid .env entry on line {line_number}")

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValueError(f"Empty .env key on line {line_number}")
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        value = os.path.expandvars(value)
        os.environ.setdefault(key, value)


def normalize_ticker(ticker: str) -> str:
    """Return a normalized ticker code or raise ValueError."""
    normalized = ticker.strip().upper()
    if not normalized:
        raise ValueError("Ticker code cannot be empty")
    if not all(character.isalnum() or character in ".-" for character in normalized):
        raise ValueError(f"Invalid ticker code: {ticker!r}")
    return normalized


def build_api_url(
    base_url: str,
    path: str,
    query_parameters: list[tuple[str, str]] | None = None,
) -> str:
    """Build an API URL from a configured base URL and endpoint path."""
    parsed = urllib.parse.urlsplit(base_url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("BASE_URL must be an absolute HTTP or HTTPS URL")

    base_path = parsed.path.rstrip("/")
    endpoint_path = path.strip("/")
    combined_path = f"{base_path}/{endpoint_path}" if endpoint_path else base_path
    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    query.extend(query_parameters or [])

    return urllib.parse.urlunsplit(
        (
            parsed.scheme,
            parsed.netloc,
            combined_path,
            urllib.parse.urlencode(query),
            parsed.fragment,
        )
    )


def build_technical_url(base_url: str, ticker: str) -> str:
    """Add the ticker query parameter to the technical-data URL."""
    return build_api_url(base_url, "technical", [("ticker", ticker)])


def fetch_json(url: str, timeout: float) -> Any:
    """Make a GET request and return the decoded JSON response."""
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json"},
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            body = response.read().decode(charset)
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace").strip()
        message = f"GET {url} returned HTTP {exc.code} {exc.reason}"
        if details:
            message = f"{message}: {details}"
        raise RuntimeError(message) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"GET {url} failed: {exc.reason}") from exc

    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"GET {url} did not return valid JSON: {exc}") from exc


def build_prompt(
    instructions: str,
    technical_data: str,
    ticker: str,
    forecast_horizon: str,
) -> str:
    """Assemble the instructions, request, and technical JSON for Codex."""
    analysis_request = (
        f"Analyze the IDX-listed stock with ticker {ticker} (IDX: {ticker}) "
        f"over the next {forecast_horizon}. Use IDR, moderate risk tolerance, "
        "and no assumed entry price. Follow every instruction above."
    )
    return (
        f"{instructions.rstrip()}\n\n"
        f"{analysis_request}\n\n"
        "<TECHNICAL_DATA_JSON>\n"
        f"{technical_data.rstrip()}\n"
        "</TECHNICAL_DATA_JSON>\n"
    )
