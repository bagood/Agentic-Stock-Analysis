import json
import sys
from pathlib import Path

from app.errors import CodexExecutionError
from detailedAnalysis.helper import (
    build_prompt,
    normalize_technical_ticker,
)
from detailedAnalysis.technical_api import TechnicalAPIClient, TechnicalConfig
from llm_runner.codex_runner import run_codex
from detailedAnalysis.preflight import PreflightResult, preflight, check_feature_cards

PROJECT_DIR = Path(__file__).resolve().parent.parent


def main(
    ticker: str,
    instructions_value: str,
    forecast_horizon: str,
    base_url: str,
    output_dir_value: str,
    timeout: float = 30.0,
    *,
    forecast_type: str,
    technical_config: TechnicalConfig | None = None,
    _preflight: PreflightResult | None = None,
) -> int:
    try:
        ticker = normalize_technical_ticker(ticker)
        instructions_path = Path(instructions_value)
        if not instructions_path.is_absolute():
            instructions_path = PROJECT_DIR / instructions_path

        output_dir = Path(output_dir_value)
        if not output_dir.is_absolute():
            output_dir = PROJECT_DIR / output_dir

        output_path = output_dir / f"{ticker}.md"
        checked = _preflight
        if checked is None:
            checked = preflight(PROJECT_DIR, instructions_path)
        elif checked.project != PROJECT_DIR.resolve() or checked.instructions != instructions_path.resolve():
            raise CodexExecutionError("Preflight handoff does not match the selected instructions/project")

        result = TechnicalAPIClient(
            base_url,
            technical_config if technical_config is not None else TechnicalConfig.from_environment(timeout),
        ).retrieve(ticker, forecast_type)
        check_feature_cards(PROJECT_DIR, result.indicators)
        technical_data_text = json.dumps(
            result.model_dump(),
            ensure_ascii=False,
            separators=(",", ":"),
            allow_nan=False,
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
            timeout_seconds=checked.generation_timeout,
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
