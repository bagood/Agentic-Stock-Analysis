from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict


class PortfolioPosition(BaseModel):
    """One ticker, tracked price, and assigned analysis window."""

    model_config = ConfigDict(frozen=True)

    ticker: str
    price: Decimal
    rolling_window: Literal["5dd", "10dd"]


class Portfolio(BaseModel):
    """All positions currently stored in the portfolio."""

    model_config = ConfigDict(frozen=True)

    positions: list[PortfolioPosition]


class PortfolioMutation(BaseModel):
    """Result of a successful portfolio mutation."""

    model_config = ConfigDict(frozen=True)

    action: str
    position: PortfolioPosition
