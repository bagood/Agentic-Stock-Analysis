from decimal import Decimal, InvalidOperation

from app.models.portfolio import Portfolio, PortfolioMutation, PortfolioPosition
from app.repositories.portfolio_repository import PortfolioRepository
from app.services.analysis_service import TICKER_PATTERN


class PortfolioService:
    """Validate portfolio requests and apply them to storage."""

    def __init__(self, repository: PortfolioRepository) -> None:
        self._repository = repository

    def list_positions(self) -> Portfolio:
        return Portfolio(positions=self._repository.list())

    VALID_ROLLING_WINDOWS = {"5dd", "10dd"}

    def add(
        self,
        ticker: str,
        price: Decimal | float | str,
        rolling_window: str,
    ) -> PortfolioMutation:
        position = self._position(ticker, price, rolling_window)
        self._repository.add(position)
        return PortfolioMutation(action="added", position=position)

    def update(
        self,
        ticker: str,
        price: Decimal | float | str,
        rolling_window: str,
    ) -> PortfolioMutation:
        position = self._position(ticker, price, rolling_window)
        self._repository.update(position)
        return PortfolioMutation(action="updated", position=position)

    def delete(self, ticker: str, rolling_window: str) -> PortfolioMutation:
        normalized_ticker = self._ticker(ticker)
        normalized_rolling_window = self._rolling_window(rolling_window)
        position = self._repository.delete(
            normalized_ticker, normalized_rolling_window
        )
        return PortfolioMutation(action="deleted", position=position)

    def _position(
        self,
        ticker: str,
        price: Decimal | float | str,
        rolling_window: str,
    ) -> PortfolioPosition:
        try:
            normalized_price = Decimal(str(price))
        except (InvalidOperation, ValueError):
            raise ValueError("Price must be a valid positive number") from None
        if not normalized_price.is_finite() or normalized_price <= 0:
            raise ValueError("Price must be a valid positive number")
        return PortfolioPosition(
            ticker=self._ticker(ticker),
            price=normalized_price,
            rolling_window=self._rolling_window(rolling_window),
        )

    @classmethod
    def _rolling_window(cls, rolling_window: str) -> str:
        normalized_rolling_window = rolling_window.strip().lower()
        if normalized_rolling_window not in cls.VALID_ROLLING_WINDOWS:
            raise ValueError("Rolling window must be either 5dd or 10dd")
        return normalized_rolling_window

    @staticmethod
    def _ticker(ticker: str) -> str:
        normalized_ticker = ticker.strip().upper()
        if not TICKER_PATTERN.fullmatch(normalized_ticker):
            raise ValueError("Ticker contains unsupported characters")
        return normalized_ticker
