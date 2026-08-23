import csv
import os
import tempfile
from decimal import Decimal
from pathlib import Path
from threading import Lock

from app.models.portfolio import PortfolioPosition

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PORTFOLIO_CSV = PROJECT_ROOT / "data" / "portfolio.csv"


class PortfolioRepository:
    """Persist portfolio positions in a three-column CSV file."""

    def __init__(self, csv_path: Path | None = None) -> None:
        configured_path = os.environ.get("PORTFOLIO_CSV_PATH")
        self._csv_path = csv_path or (
            Path(configured_path) if configured_path else DEFAULT_PORTFOLIO_CSV
        )
        self._lock = Lock()

    def list(self) -> list[PortfolioPosition]:
        with self._lock:
            return list(self._read().values())

    def add(self, position: PortfolioPosition) -> None:
        with self._lock:
            positions = self._read()
            key = (position.ticker, position.rolling_window)
            if key in positions:
                raise ValueError(
                    f"Ticker {position.ticker} already exists for "
                    f"{position.rolling_window}"
                )
            positions[key] = position
            self._write(positions)

    def update(self, position: PortfolioPosition) -> None:
        with self._lock:
            positions = self._read()
            key = (position.ticker, position.rolling_window)
            if key not in positions:
                raise ValueError(
                    f"Ticker {position.ticker} was not found for "
                    f"{position.rolling_window}"
                )
            positions[key] = position
            self._write(positions)

    def delete(self, ticker: str, rolling_window: str) -> PortfolioPosition:
        with self._lock:
            positions = self._read()
            key = (ticker, rolling_window)
            if key not in positions:
                raise ValueError(
                    f"Ticker {ticker} was not found for {rolling_window}"
                )
            deleted = positions.pop(key)
            self._write(positions)
            return deleted

    def _read(self) -> dict[tuple[str, str], PortfolioPosition]:
        if not self._csv_path.is_file():
            return {}

        with self._csv_path.open(newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            expected_fields = ["ticker", "price", "rolling_window"]
            if reader.fieldnames != expected_fields:
                raise ValueError(
                    "Portfolio CSV must contain exactly: "
                    "ticker,price,rolling_window"
                )

            positions: dict[tuple[str, str], PortfolioPosition] = {}
            for row in reader:
                position = PortfolioPosition(
                    ticker=row["ticker"],
                    price=Decimal(row["price"]),
                    rolling_window=row["rolling_window"],
                )
                positions[(position.ticker, position.rolling_window)] = position
            return dict(sorted(positions.items()))

    def _write(
        self, positions: dict[tuple[str, str], PortfolioPosition]
    ) -> None:
        self._csv_path.parent.mkdir(parents=True, exist_ok=True)
        file_descriptor, temporary_name = tempfile.mkstemp(
            dir=self._csv_path.parent, prefix=".portfolio-", suffix=".csv"
        )
        try:
            with os.fdopen(file_descriptor, "w", newline="", encoding="utf-8") as csv_file:
                writer = csv.DictWriter(
                    csv_file,
                    fieldnames=["ticker", "price", "rolling_window"],
                )
                writer.writeheader()
                for key in sorted(positions):
                    position = positions[key]
                    writer.writerow(
                        {
                            "ticker": position.ticker,
                            "price": str(position.price),
                            "rolling_window": position.rolling_window,
                        }
                    )
            os.replace(temporary_name, self._csv_path)
        except BaseException:
            Path(temporary_name).unlink(missing_ok=True)
            raise
