import argparse
import os
import shutil
import sys
from pathlib import Path

from detailedAnalysis.helper import load_env
from holdStrategy.helper import load_holdings
from holdStrategy.main import main as generate_hold_strategy

PROJECT_DIR = Path(__file__).resolve().parent
ENV_PATH = PROJECT_DIR / ".env"

WINDOW_CONFIGS = {
    "5-10": {
        "instructions_path": "instructions/stock-hold-strategy-5-10-instructions.md",
        "rolling_window": "5dd",
        "trading_window": "5–10 trading sessions",
    },
    "10-20": {
        "instructions_path": "instructions/stock-hold-strategy-10-20-instructions.md",
        "rolling_window": "10dd",
        "trading_window": "10–20 trading sessions",
    },
}


def parse_args(arguments: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate hold strategies for portfolio positions."
    )
    parser.add_argument(
        "--forecast-window",
        choices=tuple(WINDOW_CONFIGS),
        default="10-20",
        help="hold-strategy horizon in trading days (default: 10-20)",
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
            os.environ.get("DETAILED_ANALYSIS_RESULT", "detailedAnalysisResults")
        )
        portfolio_path = resolve_project_path(
            os.environ.get("PORTFOLIO_CSV_PATH", "data/portfolio.csv")
        )
        output_root = resolve_project_path(
            os.environ.get("HOLD_STRATEGY_RESULT", "holdStrategyResults")
        )
        holdings = load_holdings(portfolio_path, rolling_window)
        output_dir = prepare_output_dir(output_root / rolling_window)
    except (KeyError, OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not holdings:
        print(f"No portfolio holdings found for {rolling_window}.")
        return 0

    print("Selected portfolio holdings")
    print([holding.ticker for holding in holdings])

    failed_tickers: list[str] = []
    for holding in holdings:
        analysis_path = analysis_root / rolling_window / f"{holding.ticker}.md"
        print(f"Generating hold strategy for {holding.ticker}...")
        if generate_hold_strategy(
            holding,
            str(analysis_path),
            config["instructions_path"],
            config["trading_window"],
            str(output_dir),
        ) != 0:
            failed_tickers.append(holding.ticker)

    if failed_tickers:
        print(
            f"Hold-strategy generation failed for: {', '.join(failed_tickers)}",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    arguments = parse_args()
    raise SystemExit(main(arguments.forecast_window))
