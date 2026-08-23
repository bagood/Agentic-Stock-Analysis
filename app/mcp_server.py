from mcp.server import MCPServer
from mcp.types import ToolAnnotations
from starlette.applications import Starlette

from app.models.analysis import AnalysisReport, TickerList
from app.models.portfolio import Portfolio, PortfolioMutation
from app.repositories.analysis_repository import AnalysisRepository
from app.repositories.portfolio_repository import PortfolioRepository
from app.services.analysis_service import AnalysisService
from app.services.portfolio_service import PortfolioService

_service = AnalysisService(AnalysisRepository())
_portfolio_service = PortfolioService(PortfolioRepository())

_read_only_annotations = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
)

_write_annotations = ToolAnnotations(
    readOnlyHint=False,
    destructiveHint=False,
    idempotentHint=False,
    openWorldHint=False,
)

_update_annotations = ToolAnnotations(
    readOnlyHint=False,
    destructiveHint=True,
    idempotentHint=True,
    openWorldHint=False,
)

mcp_server = MCPServer(
    name="agentic-stock-analysis",
    title="Agentic Stock Analysis",
    description=(
        "Read generated stock-analysis reports and manage a CSV-backed ticker portfolio."
    ),
    instructions=(
        "Use list_analysis_tickers to discover available reports, then use "
        "get_analysis_report with one of those ticker symbols. Use list_portfolio "
        "before adding, modifying, or deleting CSV-backed portfolio positions. "
        "Portfolio mutations require a rolling_window of 5dd or 10dd."
    ),
    version="1.2.0",
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


@mcp_server.tool(structured_output=True, annotations=_read_only_annotations)
def list_portfolio() -> Portfolio:
    """List every ticker, price, and rolling window in the portfolio."""
    return _portfolio_service.list_positions()


@mcp_server.tool(structured_output=True, annotations=_write_annotations)
def add_portfolio_ticker(
    ticker: str, price: float, rolling_window: str
) -> PortfolioMutation:
    """Add a ticker for rolling window 5dd or 10dd to the portfolio."""
    return _portfolio_service.add(ticker, price, rolling_window)


@mcp_server.tool(structured_output=True, annotations=_update_annotations)
def modify_portfolio_ticker(
    ticker: str, price: float, rolling_window: str
) -> PortfolioMutation:
    """Replace the price of a ticker in the specified rolling window."""
    return _portfolio_service.update(ticker, price, rolling_window)


@mcp_server.tool(structured_output=True, annotations=_update_annotations)
def delete_portfolio_ticker(ticker: str, rolling_window: str) -> PortfolioMutation:
    """Delete a ticker from the specified rolling window."""
    return _portfolio_service.delete(ticker, rolling_window)


mcp_http_app: Starlette = mcp_server.streamable_http_app(
    streamable_http_path="/",
    stateless_http=True,
    json_response=True,
    host="0.0.0.0",
)
