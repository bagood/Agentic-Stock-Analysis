import json
import sys
from pathlib import Path

from app.errors import CodexExecutionError
from detailedAnalysis.helper import (
    build_prompt,
    build_technical_url,
    fetch_json,
    normalize_ticker,
)
from llm_runner.codex_runner import run_codex

PROJECT_DIR = Path(__file__).resolve().parent.parent


def main(
    ticker: str,
    instructions_value: str,
    forecast_horizon: str,
    base_url: str,
    output_dir_value: str,
    timeout: float = 30.0,
) -> int:
    try:
        ticker = normalize_ticker(ticker)
        instructions_path = Path(instructions_value)
        if not instructions_path.is_absolute():
            instructions_path = PROJECT_DIR / instructions_path

        output_dir = Path(output_dir_value)
        if not output_dir.is_absolute():
            output_dir = PROJECT_DIR / output_dir

        output_path = output_dir / f"{ticker}.md"

        technical_url = build_technical_url(base_url, ticker)
        technical_data = fetch_json(technical_url, timeout)
        technical_data_text = json.dumps(
            technical_data,
            ensure_ascii=False,
            indent=2,
        )

        instructions = instructions_path.read_text(encoding="utf-8")
        prompt = build_prompt(
            instructions,
            technical_data_text,
            ticker,
            forecast_horizon,
        )

        run_codex(
            prompt,
            output_path,
            PROJECT_DIR,
            enable_search=True,
        )
    except (
        KeyError,
        OSError,
        RuntimeError,
        ValueError,
        CodexExecutionError,
    ) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Analysis saved to {output_path}")
    return 0


if __name__ == "__main__":
    print(
        "Run individual analyses through run_detailed_analysis.py so the "
        "forecast window is selected consistently.",
        file=sys.stderr,
    )
    raise SystemExit(2)
