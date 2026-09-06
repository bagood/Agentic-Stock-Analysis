from fastapi import HTTPException, status

from app.models.entry_strategy import EntryStrategyReport, EntryStrategyTickerList
from app.services.entry_strategy_service import EntryStrategyService


class EntryStrategyController:
    """Translate HTTP requests into entry-strategy service calls."""

    def __init__(self, service: EntryStrategyService) -> None:
        self._service = service

    def get_tickers(self, rolling_window: str) -> EntryStrategyTickerList:
        try:
            return self._service.get_tickers(rolling_window)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            ) from exc

    def get_report(
        self,
        ticker: str,
        rolling_window: str,
    ) -> EntryStrategyReport:
        try:
            report = self._service.get_report(ticker, rolling_window)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            ) from exc

        if report is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"Entry-strategy report for {ticker.upper()} was not found "
                    f"in {rolling_window}"
                ),
            )
        return report

