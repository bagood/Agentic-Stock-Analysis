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


def build_technical_url(ticker: str) -> str:
    """Add the ticker query parameter to the technical-data URL."""
    base_url = os.environ["TECHNICAL_URL"]

    parsed = urllib.parse.urlsplit(base_url)
    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    query.append(("ticker", ticker))
    
    return urllib.parse.urlunsplit(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            urllib.parse.urlencode(query),
            parsed.fragment,
        )
    )


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


def build_prompt(instructions: str, technical_data: str, ticker: str) -> str:
    """Assemble the instructions, request, and technical JSON for Codex."""
    analysis_request = (
        f"Analyze the IDX-listed stock with ticker {ticker} (IDX: {ticker}) "
        "over the next 10–20 calendar days. Use IDR, moderate risk tolerance, "
        "and no assumed entry price. Follow every instruction above."
    )
    return (
        f"{instructions.rstrip()}\n\n"
        f"{analysis_request}\n\n"
        "<TECHNICAL_DATA_JSON>\n"
        f"{technical_data.rstrip()}\n"
        "</TECHNICAL_DATA_JSON>\n"
    )
