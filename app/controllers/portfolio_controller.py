from decimal import Decimal

from fastapi import HTTPException, status

from app.models.portfolio import Portfolio, PortfolioMutation
from app.services.portfolio_service import PortfolioService


class PortfolioController:
    """Translate HTTP requests into portfolio service calls."""

    def __init__(self, service: PortfolioService) -> None:
        self._service = service

    def list_positions(self) -> Portfolio:
        return self._service.list_positions()

    def add(
        self,
        ticker: str,
        price: Decimal,
        rolling_window: str,
    ) -> PortfolioMutation:
        try:
            return self._service.add(ticker, price, rolling_window)
        except ValueError as exc:
            status_code = (
                status.HTTP_409_CONFLICT
                if "already exists" in str(exc)
                else status.HTTP_400_BAD_REQUEST
            )
            raise HTTPException(status_code=status_code, detail=str(exc)) from exc

    def update(
        self,
        ticker: str,
        price: Decimal,
        rolling_window: str,
    ) -> PortfolioMutation:
        try:
            return self._service.update(ticker, price, rolling_window)
        except ValueError as exc:
            status_code = (
                status.HTTP_404_NOT_FOUND
                if "was not found" in str(exc)
                else status.HTTP_400_BAD_REQUEST
            )
            raise HTTPException(status_code=status_code, detail=str(exc)) from exc

    def delete(self, ticker: str, rolling_window: str) -> PortfolioMutation:
        try:
            return self._service.delete(ticker, rolling_window)
        except ValueError as exc:
            status_code = (
                status.HTTP_404_NOT_FOUND
                if "was not found" in str(exc)
                else status.HTTP_400_BAD_REQUEST
            )
            raise HTTPException(status_code=status_code, detail=str(exc)) from exc
