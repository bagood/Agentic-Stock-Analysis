from typing import Literal

from mcp.server import MCPServer
from mcp.types import ToolAnnotations
from starlette.applications import Starlette

from app.models.analysis import AnalysisReport, TickerList
from app.repositories.analysis_repository import AnalysisRepository
from app.services.analysis_service import AnalysisService

_service = AnalysisService(AnalysisRepository())

_read_only_annotations = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
)

mcp_server = MCPServer(
    name="agentic-stock-analysis",
    title="Agentic Stock Analysis",
    description="Read generated stock-analysis reports.",
    instructions=(
        "Use list_analysis_tickers with the requested rolling_window to discover "
        "available reports, then use "
        "get_analysis_report with one of those ticker symbols and the requested "
        "rolling_window: use 5dd for a 5-session recommendation and 10dd "
        "for a 10-session recommendation."
    ),
    version="2.0.0",
)


@mcp_server.tool(
    structured_output=True,
    annotations=_read_only_annotations,
)
def list_analysis_tickers(
    rolling_window: Literal["5dd", "10dd"],
) -> TickerList:
    """List report tickers from 5dd (5 trading sessions) or 10dd (10 trading sessions)."""
    return _service.get_tickers(rolling_window)


@mcp_server.tool(
    structured_output=True,
    annotations=_read_only_annotations,
)
def get_analysis_report(
    ticker: str,
    rolling_window: Literal["5dd", "10dd"],
) -> AnalysisReport:
    """Return a report from 5dd (5 trading sessions) or 10dd (10 trading sessions)."""
    try:
        report = _service.get_report(ticker, rolling_window)
    except ValueError as exc:
        raise ValueError(str(exc)) from exc

    if report is None:
        raise ValueError(
            f"Analysis report for {ticker.upper()} was not found in {rolling_window}"
        )

    return report


mcp_http_app: Starlette = mcp_server.streamable_http_app(
    streamable_http_path="/",
    stateless_http=True,
    json_response=True,
    host="0.0.0.0",
)
