from app.models.hold_strategy import HoldStrategyReport, HoldStrategyTickerList
from app.repositories.hold_strategy_repository import HoldStrategyRepository
from app.services.analysis_service import TICKER_PATTERN, VALID_ROLLING_WINDOWS


class HoldStrategyService:
    """Apply validation and business rules for hold-strategy reports."""

    def __init__(self, repository: HoldStrategyRepository) -> None:
        self._repository = repository

    def get_tickers(self, rolling_window: str) -> HoldStrategyTickerList:
        normalized_window = self._rolling_window(rolling_window)
        return HoldStrategyTickerList(
            tickers=self._repository.get_tickers(normalized_window)
        )

    def get_report(
        self,
        ticker: str,
        rolling_window: str,
    ) -> HoldStrategyReport | None:
        normalized_ticker = ticker.strip().upper()
        if not TICKER_PATTERN.fullmatch(normalized_ticker):
            raise ValueError("Ticker contains unsupported characters")

        return self._repository.get_report(
            normalized_ticker,
            self._rolling_window(rolling_window),
        )

    @staticmethod
    def _rolling_window(rolling_window: str) -> str:
        normalized_window = rolling_window.strip().lower()
        if normalized_window not in VALID_ROLLING_WINDOWS:
            raise ValueError("Rolling window must be 5dd or 10dd")
        return normalized_window

