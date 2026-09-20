from typing import Annotated, Literal

from fastapi import APIRouter, Depends

from app.controllers.entry_strategy_controller import EntryStrategyController
from app.models.entry_strategy import EntryStrategyReport, EntryStrategyTickerList
from app.repositories.entry_strategy_repository import EntryStrategyRepository
from app.services.entry_strategy_service import EntryStrategyService

router = APIRouter(prefix="/entry_strategy", tags=["Entry Strategy"])

_repository = EntryStrategyRepository()
_service = EntryStrategyService(_repository)
_controller = EntryStrategyController(_service)


def get_entry_strategy_controller() -> EntryStrategyController:
    """Provide the controller and allow dependency overrides in tests."""
    return _controller


EntryStrategyControllerDependency = Annotated[
    EntryStrategyController,
    Depends(get_entry_strategy_controller),
]


@router.get("", response_model=EntryStrategyTickerList)
def get_tickers(
    rolling_window: Literal["5dd", "10dd"],
    controller: EntryStrategyControllerDependency,
) -> EntryStrategyTickerList:
    """Return tickers with entry strategies in the selected window."""
    return controller.get_tickers(rolling_window)


@router.get("/report", response_model=EntryStrategyReport)
def get_report(
    ticker: str,
    rolling_window: str,
    controller: EntryStrategyControllerDependency,
) -> EntryStrategyReport:
    """Return an entry strategy selected by ticker and rolling window."""
    return controller.get_report(ticker, rolling_window)

