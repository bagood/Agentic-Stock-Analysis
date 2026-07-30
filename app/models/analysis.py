from pydantic import BaseModel, ConfigDict


class TickerList(BaseModel):
    """Response containing all tickers with generated reports."""

    model_config = ConfigDict(frozen=True)

    tickers: list[str]


class AnalysisReport(BaseModel):
    """Response containing a ticker's Markdown analysis."""

    model_config = ConfigDict(frozen=True)

    ticker: str
    report: str
