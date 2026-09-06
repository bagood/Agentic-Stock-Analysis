import argparse
import os
import shutil
import sys
from pathlib import Path

from detailedAnalysis.helper import load_env
from entryStrategy.helper import list_analysis_reports
from entryStrategy.main import main as generate_entry_strategy

PROJECT_DIR = Path(__file__).resolve().parent
ENV_PATH = PROJECT_DIR / ".env"

WINDOW_CONFIGS = {
    "5-10": {
        "instructions_path": "instructions/stock-entry-strategy-5-10-instructions.md",
        "rolling_window": "5dd",
        "trading_window": "5–10 trading sessions",
    },
    "10-20": {
        "instructions_path": "instructions/stock-entry-strategy-10-20-instructions.md",
        "rolling_window": "10dd",
        "trading_window": "10–20 trading sessions",
    },
}


def parse_args(arguments: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate entry strategies from stock-analysis reports."
    )
    parser.add_argument(
        "--forecast-window",
        choices=tuple(WINDOW_CONFIGS),
        default="10-20",
        help="entry-strategy horizon in trading days (default: 10-20)",
    )
    return parser.parse_args(arguments)


def resolve_project_path(path_value: str) -> Path:
    path = Path(path_value)
    return path if path.is_absolute() else PROJECT_DIR / path


def prepare_output_dir(output_dir: Path) -> Path:
    """Create and clear only the selected rolling-window directory."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for child in output_dir.iterdir():
        if child.is_dir() and not child.is_symlink():
            shutil.rmtree(child)
        else:
            child.unlink()
    return output_dir


def main(forecast_window: str = "10-20") -> int:
    try:
        load_env(ENV_PATH)
        config = WINDOW_CONFIGS[forecast_window]
        rolling_window = config["rolling_window"]
        analysis_root = resolve_project_path(
            os.environ.get("OUTPUT_DIR", "detailedAnalysisResults")
        )
        strategy_root = resolve_project_path(
            os.environ.get("ENTRY_STRATEGY_OUTPUT_DIR", "entryStrategyResults")
        )
        analysis_dir = analysis_root / rolling_window
        output_dir = prepare_output_dir(strategy_root / rolling_window)
        analysis_reports = list_analysis_reports(analysis_dir)
    except (KeyError, OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not analysis_reports:
        print(f"No analysis reports found in {analysis_dir}.")
        return 0

    print("Selected analysis reports")
    print([path.stem.upper() for path in analysis_reports])

    failed_tickers: list[str] = []
    for analysis_path in analysis_reports:
        ticker = analysis_path.stem.upper()
        print(f"Generating entry strategy for {ticker}...")
        if generate_entry_strategy(
            ticker,
            str(analysis_path),
            config["instructions_path"],
            config["trading_window"],
            str(output_dir),
        ) != 0:
            failed_tickers.append(ticker)

    if failed_tickers:
        print(
            f"Entry-strategy generation failed for: {', '.join(failed_tickers)}",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    arguments = parse_args()
    raise SystemExit(main(arguments.forecast_window))

