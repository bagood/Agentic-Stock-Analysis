import csv
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

from detailedAnalysis.helper import normalize_ticker


@dataclass(frozen=True)
class Holding:
    ticker: str
    average_price: Decimal
    rolling_window: str


def load_holdings(csv_path: Path, rolling_window: str) -> list[Holding]:
    """Load and validate portfolio holdings for one rolling window."""
    if rolling_window not in {"5dd", "10dd"}:
        raise ValueError("Rolling window must be either 5dd or 10dd")
    if not csv_path.is_file():
        raise ValueError(f"Portfolio CSV does not exist: {csv_path}")

    with csv_path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames != ["ticker", "price", "rolling_window"]:
            raise ValueError(
                "Portfolio CSV must contain exactly: ticker,price,rolling_window"
            )

        holdings: list[Holding] = []
        seen_tickers: set[str] = set()
        for row_number, row in enumerate(reader, start=2):
            ticker = normalize_ticker(row.get("ticker") or "")
            row_window = (row.get("rolling_window") or "").strip().lower()
            if row_window not in {"5dd", "10dd"}:
                raise ValueError(
                    f"Portfolio CSV row {row_number} has an invalid rolling_window"
                )
            try:
                average_price = Decimal(row.get("price") or "")
            except InvalidOperation:
                raise ValueError(
                    f"Portfolio CSV row {row_number} has an invalid price"
                ) from None
            if not average_price.is_finite() or average_price <= 0:
                raise ValueError(
                    f"Portfolio CSV row {row_number} has an invalid price"
                )

            if row_window != rolling_window:
                continue
            if ticker in seen_tickers:
                raise ValueError(
                    f"Portfolio CSV contains duplicate {ticker}/{rolling_window}"
                )
            seen_tickers.add(ticker)
            holdings.append(Holding(ticker, average_price, row_window))

    return sorted(holdings, key=lambda holding: holding.ticker)


def build_hold_strategy_prompt(
    instructions: str,
    analysis_report: str,
    holding: Holding,
    trading_window: str,
) -> str:
    """Assemble instructions, position context, and source analysis for Codex."""
    return (
        f"{instructions.rstrip()}\n\n"
        f"Generate a hold strategy for the existing IDX-listed {holding.ticker} "
        f"position over the next {trading_window}. The stored average acquisition "
        f"price is IDR {holding.average_price}. Holding quantity and portfolio "
        "weight were not supplied. Decide whether to hold, tighten risk, reduce, "
        "or sell immediately. Follow every instruction above and use only the "
        "supplied analysis report.\n\n"
        "<POSITION_CONTEXT>\n"
        f"Ticker: {holding.ticker}\n"
        f"Average acquisition price: IDR {holding.average_price}\n"
        f"Rolling window: {holding.rolling_window}\n"
        "Quantity: Not supplied\n"
        "</POSITION_CONTEXT>\n\n"
        "<ANALYSIS_REPORT>\n"
        f"{analysis_report.rstrip()}\n"
        "</ANALYSIS_REPORT>\n"
    )

