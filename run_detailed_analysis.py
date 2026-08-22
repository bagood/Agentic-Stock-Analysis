import csv
import os
import shutil
import sys
from pathlib import Path
from typing import Any

from detailedAnalysis.helper import fetch_json, load_env
from detailedAnalysis.main import main as run_detailed_analysis

PROJECT_DIR = Path(__file__).resolve().parent
ENV_PATH = PROJECT_DIR / ".env"
PORTFOLIO_CSV_PATH = PROJECT_DIR / "data" / "portfolio.csv"


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


def select_positive_tickers(payload: Any, minimum_score: float) -> list[str]:
    """Return qualifying tickers, or the four highest-scoring tickers."""
    if not isinstance(payload, dict):
        raise ValueError("Recommendations response must be a JSON object")

    recommendations = payload.get("recommendations")
    if not isinstance(recommendations, list):
        raise ValueError("Recommendations response is missing a recommendations list")

    scored_tickers: list[tuple[str, float]] = []
    ticker_indexes: dict[str, int] = {}
    for index, recommendation in enumerate(recommendations):
        if not isinstance(recommendation, dict):
            raise ValueError(f"Recommendation at index {index} must be an object")

        ticker = recommendation.get("ticker")
        score = recommendation.get("score")
        if not isinstance(ticker, str) or not ticker.strip():
            raise ValueError(f"Recommendation at index {index} has an invalid ticker")
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise ValueError(f"Recommendation at index {index} has an invalid score")

        normalized_ticker = ticker.strip().upper()
        existing_index = ticker_indexes.get(normalized_ticker)
        if existing_index is None:
            ticker_indexes[normalized_ticker] = len(scored_tickers)
            scored_tickers.append((normalized_ticker, score))
        elif score > scored_tickers[existing_index][1]:
            scored_tickers[existing_index] = (normalized_ticker, score)

    tickers = [
        ticker for ticker, score in scored_tickers if score > minimum_score
    ]
    if len(tickers) < 4:
        tickers = [
            ticker
            for ticker, _ in sorted(
                scored_tickers,
                key=lambda scored_ticker: scored_ticker[1],
                reverse=True,
            )[:4]
        ]

    return tickers


def load_portfolio_tickers(csv_path: Path = PORTFOLIO_CSV_PATH) -> list[str]:
    """Load normalized ticker symbols from the portfolio CSV."""
    if not csv_path.is_file():
        return []

    with csv_path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames != ["ticker", "price"]:
            raise ValueError("Portfolio CSV must contain exactly: ticker,price")

        tickers: list[str] = []
        for row_number, row in enumerate(reader, start=2):
            ticker = row.get("ticker")
            if not isinstance(ticker, str) or not ticker.strip():
                raise ValueError(
                    f"Portfolio CSV row {row_number} has an invalid ticker"
                )
            tickers.append(ticker.strip().upper())
        return tickers


def combine_tickers(*ticker_groups: list[str]) -> list[str]:
    """Combine ticker groups while preserving order and removing duplicates."""
    return list(
        dict.fromkeys(
            ticker.strip().upper()
            for ticker_group in ticker_groups
            for ticker in ticker_group
        )
    )


def main(timeout: float = 30.0) -> int:
    try:
        load_env(ENV_PATH)
        prepare_output_dir(os.environ["OUTPUT_DIR"])
        recommendation_url = os.environ["RECOMMENDATION_URL"]
        minimum_score = float(os.environ["MINIMUM_SCORE"])
        recommendations = fetch_json(recommendation_url, timeout)
        recommendation_tickers = select_positive_tickers(
            recommendations, minimum_score
        )
        portfolio_tickers = load_portfolio_tickers()
        ticker_list = combine_tickers(recommendation_tickers, portfolio_tickers)

        print("Selected Tickers")
        print(ticker_list)

    except (KeyError, OSError, RuntimeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not ticker_list:
        print(f"No recommendations have a score above {minimum_score}.")
        return 0

    failed_tickers: list[str] = []
    for ticker in ticker_list:
        print(f"Running detailed analysis for {ticker.upper()}...")
        if run_detailed_analysis(ticker) != 0:
            failed_tickers.append(ticker.upper())

    if failed_tickers:
        print(
            f"Analysis failed for: {', '.join(failed_tickers)}",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
