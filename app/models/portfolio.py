from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class PortfolioPosition(BaseModel):
    """One ticker and its tracked price."""

    model_config = ConfigDict(frozen=True)

    ticker: str
    price: Decimal


class Portfolio(BaseModel):
    """All positions currently stored in the portfolio."""

    model_config = ConfigDict(frozen=True)

    positions: list[PortfolioPosition]


class PortfolioMutation(BaseModel):
    """Result of a successful portfolio mutation."""

    model_config = ConfigDict(frozen=True)

    action: str
    position: PortfolioPosition
