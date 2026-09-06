from pydantic import BaseModel, ConfigDict


class HoldStrategyTickerList(BaseModel):
    """Response containing tickers with generated hold strategies."""

    model_config = ConfigDict(frozen=True)

    tickers: list[str]


class HoldStrategyReport(BaseModel):
    """Response containing a ticker's Markdown hold strategy."""

    model_config = ConfigDict(frozen=True)

    ticker: str
    report: str

