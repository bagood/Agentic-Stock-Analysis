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
    description="List generated stock-analysis reports and retrieve them by ticker.",
    instructions=(
        "Use list_analysis_tickers to discover available reports, then use "
        "get_analysis_report with one of those ticker symbols."
    ),
    version="1.0.0",
)


@mcp_server.tool(
    structured_output=True,
    annotations=_read_only_annotations,
)
def list_analysis_tickers() -> TickerList:
    """List every ticker that has a generated Markdown analysis report."""
    return _service.get_tickers()


@mcp_server.tool(
    structured_output=True,
    annotations=_read_only_annotations,
)
def get_analysis_report(ticker: str) -> AnalysisReport:
    """Return the complete Markdown analysis report for one ticker."""
    try:
        report = _service.get_report(ticker)
    except ValueError as exc:
        raise ValueError(str(exc)) from exc

    if report is None:
        raise ValueError(f"Analysis report for {ticker.upper()} was not found")

    return report


mcp_http_app: Starlette = mcp_server.streamable_http_app(
    streamable_http_path="/",
    stateless_http=True,
    json_response=True,
    host="0.0.0.0",
)
