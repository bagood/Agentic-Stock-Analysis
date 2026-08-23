from typing import Annotated, Literal

from fastapi import APIRouter, Depends

from app.controllers.analysis_controller import AnalysisController
from app.models.analysis import AnalysisReport, TickerList
from app.repositories.analysis_repository import AnalysisRepository
from app.services.analysis_service import AnalysisService

router = APIRouter(prefix="/analysis", tags=["Analysis"])

_repository = AnalysisRepository()
_service = AnalysisService(_repository)
_controller = AnalysisController(_service)


def get_analysis_controller() -> AnalysisController:
    """Provide the controller and allow dependency overrides in tests."""
    return _controller


AnalysisControllerDependency = Annotated[
    AnalysisController,
    Depends(get_analysis_controller),
]


@router.get("", response_model=TickerList)
def get_tickers(
    rolling_window: Literal["5dd", "10dd"],
    controller: AnalysisControllerDependency,
) -> TickerList:
    """Return tickers with reports in the selected rolling-window directory."""
    return controller.get_tickers(rolling_window)


@router.get("/report", response_model=AnalysisReport)
def get_report(
    ticker: str,
    rolling_window: str,
    controller: AnalysisControllerDependency,
) -> AnalysisReport:
    """Return a report selected by ticker and rolling-window query parameters."""
    return controller.get_report(ticker, rolling_window)
