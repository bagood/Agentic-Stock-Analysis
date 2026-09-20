from pydantic import BaseModel, ConfigDict


class EntryStrategyTickerList(BaseModel):
    """Response containing tickers with generated entry strategies."""

    model_config = ConfigDict(frozen=True)

    tickers: list[str]


class EntryStrategyReport(BaseModel):
    """Response containing a ticker's Markdown entry strategy."""

    model_config = ConfigDict(frozen=True)

    ticker: str
    report: str

