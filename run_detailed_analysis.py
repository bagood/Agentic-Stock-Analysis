"""Run forecasts using validated Technical API schema 2.1 historical data.

The shared dates align OHLCV and indicators for three historical sessions;
--forecast-window selects the future horizon and model metadata union.
"""

import argparse
import math
import os
import shutil
import sys
from pathlib import Path
from typing import Any

from detailedAnalysis.helper import build_api_url, fetch_json, load_env
from detailedAnalysis.main import main as run_detailed_analysis
from detailedAnalysis.technical_api import TechnicalConfig
from detailedAnalysis.preflight import preflight

PROJECT_DIR = Path(__file__).resolve().parent
ENV_PATH = PROJECT_DIR / ".env"
TARGET_COUNT = 4

FORECAST_CONFIGS = {
    "5": {
        "instructions_path": "instructions/stock-upside-analysis-5-instructions.md",
        "rolling_window": "5dd",
        "prompt_horizon": "5 trading sessions",
    },
    "10": {
        "instructions_path": "instructions/stock-upside-analysis-10-instructions.md",
        "rolling_window": "10dd",
        "prompt_horizon": "10 trading sessions",
    },
}


def parse_args(arguments: list[str] | None = None) -> argparse.Namespace:
    """Parse the supported forecast-window command-line option."""
    parser = argparse.ArgumentParser(
        description="Generate short-term stock analysis reports."
    )
    parser.add_argument(
        "--forecast-window",
        choices=tuple(FORECAST_CONFIGS),
        default="10",
        help="forecast horizon in trading sessions (default: 10)",
    )
    return parser.parse_args(arguments)


def prepare_output_dir(output_dir_value: str) -> Path:
    """Create the output directory and remove any existing contents."""
    output_dir = Path(output_dir_value)
    if not output_dir.is_absolute():
        output_dir = PROJECT_DIR / output_dir

    output_dir.mkdir(parents=True, exist_ok=True)
    for child in output_dir.iterdir():
        if child.is_dir() and not child.is_symlink():
            shutil.rmtree(child)
        else:
            child.unlink()

    return output_dir


def parse_scored_recommendations(payload: Any) -> list[tuple[str, float]]:
    """Return unique, normalized recommendations sorted by descending score."""
    if not isinstance(payload, dict):
        raise ValueError("Recommendations response must be a JSON object")

    recommendations = payload.get("recommendations")
    if not isinstance(recommendations, list):
        raise ValueError("Recommendations response is missing a recommendations list")

    ticker_scores: dict[str, float] = {}
    for index, recommendation in enumerate(recommendations):
        if not isinstance(recommendation, dict):
            raise ValueError(f"Recommendation at index {index} must be an object")

        ticker = recommendation.get("ticker")
        score = recommendation.get("score")
        if not isinstance(ticker, str) or not ticker.strip() or not ticker.isascii():
            raise ValueError(f"Recommendation at index {index} has an invalid ticker")
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise ValueError(f"Recommendation at index {index} has an invalid score")
        try:
            score = float(score)
        except OverflowError as exc:
            raise ValueError(
                f"Recommendation at index {index} has an invalid score"
            ) from exc
        if not math.isfinite(score):
            raise ValueError(f"Recommendation at index {index} has an invalid score")

        normalized_ticker = ticker.strip().upper()
        existing_score = ticker_scores.get(normalized_ticker)
        if existing_score is None or score > existing_score:
            ticker_scores[normalized_ticker] = score

    return sorted(
        ticker_scores.items(),
        key=lambda scored_ticker: (-scored_ticker[1], scored_ticker[0]),
    )


def select_top_tickers(payload: Any, target_count: int) -> list[str]:
    """Return exactly the highest-scoring K unique tickers or fail explicitly."""
    if (
        isinstance(target_count, bool)
        or not isinstance(target_count, int)
        or target_count < 1
    ):
        raise ValueError("Target count must be a positive integer")
    scored_tickers = parse_scored_recommendations(payload)
    if len(scored_tickers) < target_count:
        raise ValueError(
            f"Recommendation quota shortage: requested {target_count} unique ML "
            f"tickers, available {len(scored_tickers)}"
        )
    return [ticker for ticker, _ in scored_tickers[:target_count]]


def select_stock_tickers(payload: Any, trading_window: str) -> list[str]:
    """Return normalized tickers from the stocks API response."""
    if trading_window not in {"5dd", "10dd"}:
        raise ValueError("Trading window must be either 5dd or 10dd")

    stocks = payload.get("stocks") if isinstance(payload, dict) else payload
    if not isinstance(stocks, list):
        raise ValueError("Stocks response must be a JSON array or contain a stocks list")

    tickers: list[str] = []
    for index, stock in enumerate(stocks):
        if isinstance(stock, str):
            ticker = stock
            item_window = trading_window
        elif isinstance(stock, dict):
            ticker = stock.get("ticker")
            item_window = stock.get(
                "trading_window",
                stock.get("rolling_window", trading_window),
            )
        else:
            raise ValueError(f"Stock at index {index} must be a string or object")

        if not isinstance(ticker, str) or not ticker.strip() or not ticker.isascii():
            raise ValueError(f"Stock at index {index} has an invalid ticker")
        if item_window != trading_window:
            raise ValueError(
                f"Stock at index {index} has trading window {item_window!r}, "
                f"expected {trading_window}"
            )
        tickers.append(ticker.strip().upper())

    return list(dict.fromkeys(tickers))


def combine_tickers(*ticker_groups: list[str]) -> list[str]:
    """Combine ticker groups while preserving order and removing duplicates."""
    return list(
        dict.fromkeys(
            ticker.strip().upper()
            for ticker_group in ticker_groups
            for ticker in ticker_group
        )
    )


def main(forecast_window: str = "10", timeout: float = 30.0) -> int:
    try:
        load_env(ENV_PATH)
        forecast_config = FORECAST_CONFIGS[forecast_window]
        technical_config = TechnicalConfig.from_environment(timeout)
        checked = preflight(PROJECT_DIR, PROJECT_DIR / forecast_config["instructions_path"])
        output_dir_value = str(
            Path(os.environ["DETAILED_ANALYSIS_RESULT"])
            / forecast_config["rolling_window"]
        )
        base_url = os.environ["ML_BASE_URL"]
        recommendation_url = build_api_url(
            base_url,
            "analytics/daily_recommendations",
            [("rolling_window", forecast_config["rolling_window"])],
        )
        stocks_url = build_api_url(
            os.environ.get("ORGANIZER_BASE_URL", "http://localhost:8000"),
            "stocks",
            [("trading_window", forecast_config["rolling_window"])],
        )
        recommendations = fetch_json(recommendation_url, timeout)
        stocks = fetch_json(stocks_url, timeout)
        recommendation_tickers = select_top_tickers(
            recommendations, target_count=TARGET_COUNT
        )
        stock_tickers = select_stock_tickers(
            stocks,
            forecast_config["rolling_window"],
        )
        ticker_list = combine_tickers(
            recommendation_tickers,
            stock_tickers,
        )

        output_dir = prepare_output_dir(output_dir_value)
        print(
            f"ML recommendations: requested {TARGET_COUNT}, "
            f"selected {len(recommendation_tickers)}; "
            f"additional portfolio tickers: {len(ticker_list) - len(recommendation_tickers)}; "
            f"total selected tickers: {len(ticker_list)}"
        )
        print("Selected Tickers")
        print(ticker_list)

    except (KeyError, OSError, RuntimeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    failed_tickers: list[str] = []
    for ticker in ticker_list:
        print(f"Running detailed analysis for {ticker.upper()}...")
        if run_detailed_analysis(
            ticker,
            forecast_config["instructions_path"],
            forecast_config["prompt_horizon"],
            base_url,
            str(output_dir),
            timeout,
            forecast_type=forecast_config["rolling_window"],
            technical_config=technical_config,
            _preflight=checked,
        ) != 0:
            failed_tickers.append(ticker.upper())

    if failed_tickers:
        print(
            f"Analysis failed for: {', '.join(failed_tickers)}",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    arguments = parse_args()
    raise SystemExit(main(arguments.forecast_window))
