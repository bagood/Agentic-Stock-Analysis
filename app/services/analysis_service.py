import re

from app.models.analysis import AnalysisReport, TickerList
from app.repositories.analysis_repository import AnalysisRepository

TICKER_PATTERN = re.compile(r"[A-Z0-9][A-Z0-9.-]*")
VALID_ROLLING_WINDOWS = {"5dd", "10dd"}


class AnalysisService:
    """Apply validation and business rules for analysis reports."""

    def __init__(self, repository: AnalysisRepository) -> None:
        self._repository = repository

    def get_tickers(self) -> TickerList:
        return TickerList(tickers=self._repository.get_tickers())

    def get_report(self, ticker: str, rolling_window: str) -> AnalysisReport | None:
        normalized_ticker = ticker.strip().upper()
        if not TICKER_PATTERN.fullmatch(normalized_ticker):
            raise ValueError("Ticker contains unsupported characters")

        normalized_rolling_window = rolling_window.strip().lower()
        if normalized_rolling_window not in VALID_ROLLING_WINDOWS:
            raise ValueError("Rolling window must be 5dd or 10dd")

        return self._repository.get_report(
            normalized_ticker,
            normalized_rolling_window,
        )
