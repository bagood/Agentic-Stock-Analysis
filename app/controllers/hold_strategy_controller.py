from fastapi import HTTPException, status

from app.models.hold_strategy import HoldStrategyReport, HoldStrategyTickerList
from app.services.hold_strategy_service import HoldStrategyService


class HoldStrategyController:
    """Translate HTTP requests into hold-strategy service calls."""

    def __init__(self, service: HoldStrategyService) -> None:
        self._service = service

    def get_tickers(self, rolling_window: str) -> HoldStrategyTickerList:
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
    ) -> HoldStrategyReport:
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
                    f"Hold-strategy report for {ticker.upper()} was not found "
                    f"in {rolling_window}"
                ),
            )
        return report

