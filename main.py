import os
import sys
from pathlib import Path
from typing import Any

from detailedAnalysis.helper import fetch_json, load_env
from detailedAnalysis.main import main as run_detailed_analysis


PROJECT_DIR = Path(__file__).resolve().parent
ENV_PATH = PROJECT_DIR / ".env"


def select_positive_tickers(payload: Any) -> list[str]:
    """Return unique tickers whose recommendation score is above zero."""
    if not isinstance(payload, dict):
        raise ValueError("Recommendations response must be a JSON object")

    recommendations = payload.get("recommendations")
    if not isinstance(recommendations, list):
        raise ValueError("Recommendations response is missing a recommendations list")

    tickers: list[str] = []
    seen: set[str] = set()
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
        if score > 0.5 and normalized_ticker not in seen:
            tickers.append(normalized_ticker)
            seen.add(normalized_ticker)

    return tickers


def main(timeout: float = 30.0) -> int:
    try:
        load_env(ENV_PATH)
        recommendation_url = os.environ["RECOMMENDATION_URL"]
        recommendations = fetch_json(recommendation_url, timeout)
        ticker_list = select_positive_tickers(recommendations)

    except (KeyError, OSError, RuntimeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not ticker_list:
        print("No recommendations have a score above 0.")
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
