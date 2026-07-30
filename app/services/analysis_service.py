import re

from app.models.analysis import AnalysisReport, TickerList
from app.repositories.analysis_repository import AnalysisRepository

TICKER_PATTERN = re.compile(r"[A-Z0-9][A-Z0-9.-]*")


class AnalysisService:
    """Apply validation and business rules for analysis reports."""

    def __init__(self, repository: AnalysisRepository) -> None:
        self._repository = repository

    def get_tickers(self) -> TickerList:
        return TickerList(tickers=self._repository.get_tickers())

    def get_report(self, ticker: str) -> AnalysisReport | None:
        normalized_ticker = ticker.strip().upper()
        if not TICKER_PATTERN.fullmatch(normalized_ticker):
            raise ValueError("Ticker contains unsupported characters")

        return self._repository.get_report(normalized_ticker)
