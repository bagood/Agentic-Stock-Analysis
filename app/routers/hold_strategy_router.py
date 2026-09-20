from typing import Annotated, Literal

from fastapi import APIRouter, Depends

from app.controllers.hold_strategy_controller import HoldStrategyController
from app.models.hold_strategy import HoldStrategyReport, HoldStrategyTickerList
from app.repositories.hold_strategy_repository import HoldStrategyRepository
from app.services.hold_strategy_service import HoldStrategyService

router = APIRouter(prefix="/hold_strategy", tags=["Hold Strategy"])

_repository = HoldStrategyRepository()
_service = HoldStrategyService(_repository)
_controller = HoldStrategyController(_service)


def get_hold_strategy_controller() -> HoldStrategyController:
    """Provide the controller and allow dependency overrides in tests."""
    return _controller


HoldStrategyControllerDependency = Annotated[
    HoldStrategyController,
    Depends(get_hold_strategy_controller),
]


@router.get("", response_model=HoldStrategyTickerList)
def get_tickers(
    rolling_window: Literal["5dd", "10dd"],
    controller: HoldStrategyControllerDependency,
) -> HoldStrategyTickerList:
    """Return tickers with hold strategies in the selected window."""
    return controller.get_tickers(rolling_window)


@router.get("/report", response_model=HoldStrategyReport)
def get_report(
    ticker: str,
    rolling_window: str,
    controller: HoldStrategyControllerDependency,
) -> HoldStrategyReport:
    """Return a hold strategy selected by ticker and rolling window."""
    return controller.get_report(ticker, rolling_window)

