from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any

from detailedAnalysis.helper import normalize_ticker


@dataclass(frozen=True)
class Holding:
    ticker: str
    average_price: Decimal | None
    rolling_window: str


def parse_holdings(payload: Any, rolling_window: str) -> list[Holding]:
    """Parse and validate holdings returned by the stocks API."""
    if rolling_window not in {"5dd", "10dd"}:
        raise ValueError("Rolling window must be either 5dd or 10dd")

    stocks = payload.get("stocks") if isinstance(payload, dict) else payload
    if not isinstance(stocks, list):
        raise ValueError("Stocks response must be a JSON array or contain a stocks list")

    holdings: list[Holding] = []
    seen_tickers: set[str] = set()
    for index, stock in enumerate(stocks):
        if isinstance(stock, str):
            ticker_value = stock
            price_value = None
            item_window = rolling_window
        elif isinstance(stock, dict):
            ticker_value = stock.get("ticker")
            price_value = stock.get("price")
            item_window = stock.get(
                "trading_window",
                stock.get("rolling_window", rolling_window),
            )
        else:
            raise ValueError(f"Stock at index {index} must be a string or object")

        if not isinstance(ticker_value, str):
            raise ValueError(f"Stock at index {index} has an invalid ticker")
        ticker = normalize_ticker(ticker_value)
        if item_window != rolling_window:
            raise ValueError(
                f"Stock at index {index} has trading window {item_window!r}, "
                f"expected {rolling_window}"
            )
        if ticker in seen_tickers:
            raise ValueError(f"Stocks response contains duplicate ticker {ticker}")
        seen_tickers.add(ticker)

        average_price: Decimal | None = None
        if price_value is not None:
            try:
                average_price = Decimal(str(price_value))
            except (InvalidOperation, ValueError):
                raise ValueError(
                    f"Stock at index {index} has an invalid price"
                ) from None
            if not average_price.is_finite() or average_price <= 0:
                raise ValueError(f"Stock at index {index} has an invalid price")

        holdings.append(Holding(ticker, average_price, rolling_window))

    return sorted(holdings, key=lambda holding: holding.ticker)


def build_hold_strategy_prompt(
    instructions: str,
    analysis_report: str,
    holding: Holding,
    trading_window: str,
) -> str:
    """Assemble instructions, position context, and source analysis for Codex."""
    average_price = (
        f"IDR {holding.average_price}"
        if holding.average_price is not None
        else "Not supplied"
    )
    return (
        f"{instructions.rstrip()}\n\n"
        f"Generate a hold strategy for the existing IDX-listed {holding.ticker} "
        f"position over the next {trading_window}. The stored average acquisition "
        f"price is {average_price}. Holding quantity and portfolio "
        "weight were not supplied. Decide whether to hold, tighten risk, reduce, "
        "or sell immediately. Follow every instruction above and use only the "
        "supplied analysis report.\n\n"
        "<POSITION_CONTEXT>\n"
        f"Ticker: {holding.ticker}\n"
        f"Average acquisition price: {average_price}\n"
        f"Rolling window: {holding.rolling_window}\n"
        "Quantity: Not supplied\n"
        "</POSITION_CONTEXT>\n\n"
        "<ANALYSIS_REPORT>\n"
        f"{analysis_report.rstrip()}\n"
        "</ANALYSIS_REPORT>\n"
    )
