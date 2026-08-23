from fastapi import HTTPException, status

from app.models.analysis import AnalysisReport, TickerList
from app.services.analysis_service import AnalysisService


class AnalysisController:
    """Translate HTTP requests into analysis service calls."""

    def __init__(self, service: AnalysisService) -> None:
        self._service = service

    def get_tickers(self, rolling_window: str) -> TickerList:
        try:
            return self._service.get_tickers(rolling_window)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            ) from exc

    def get_report(self, ticker: str, rolling_window: str) -> AnalysisReport:
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
                    f"Analysis report for {ticker.upper()} was not found in "
                    f"{rolling_window}"
                ),
            )

        return report
