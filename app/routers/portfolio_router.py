from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.controllers.portfolio_controller import PortfolioController
from app.models.portfolio import Portfolio, PortfolioMutation, PortfolioPosition
from app.repositories.portfolio_repository import PortfolioRepository
from app.services.portfolio_service import PortfolioService

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])

_repository = PortfolioRepository()
_service = PortfolioService(_repository)
_controller = PortfolioController(_service)


def get_portfolio_controller() -> PortfolioController:
    """Provide the controller and allow dependency overrides in tests."""
    return _controller


PortfolioControllerDependency = Annotated[
    PortfolioController,
    Depends(get_portfolio_controller),
]


@router.get("", response_model=Portfolio)
def list_portfolio(
    controller: PortfolioControllerDependency,
) -> Portfolio:
    """Return all positions in the portfolio."""
    return controller.list_positions()


@router.post(
    "",
    response_model=PortfolioMutation,
    status_code=status.HTTP_201_CREATED,
)
def add_portfolio_position(
    position: PortfolioPosition,
    controller: PortfolioControllerDependency,
) -> PortfolioMutation:
    """Add a ticker, price, and rolling window to the portfolio."""
    return controller.add(
        position.ticker,
        position.price,
        position.rolling_window,
    )


@router.put("", response_model=PortfolioMutation)
def update_portfolio_position(
    position: PortfolioPosition,
    controller: PortfolioControllerDependency,
) -> PortfolioMutation:
    """Replace the price for a ticker in a rolling window."""
    return controller.update(
        position.ticker,
        position.price,
        position.rolling_window,
    )


@router.delete("", response_model=PortfolioMutation)
def delete_portfolio_position(
    ticker: str,
    rolling_window: str,
    controller: PortfolioControllerDependency,
) -> PortfolioMutation:
    """Delete a ticker from a rolling window."""
    return controller.delete(ticker, rolling_window)
