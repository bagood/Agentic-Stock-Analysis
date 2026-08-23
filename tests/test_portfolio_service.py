import csv
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from app.repositories.portfolio_repository import PortfolioRepository
from app.services.portfolio_service import PortfolioService


class PortfolioServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.csv_path = Path(self.temporary_directory.name) / "portfolio.csv"
        self.service = PortfolioService(PortfolioRepository(self.csv_path))

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_add_modify_delete_and_list(self) -> None:
        added = self.service.add(" bbca ", "9250.50", "5DD")
        self.assertEqual(added.action, "added")
        self.assertEqual(added.position.ticker, "BBCA")
        self.assertEqual(added.position.price, Decimal("9250.50"))
        self.assertEqual(added.position.rolling_window, "5dd")

        updated = self.service.update("BBCA", 9300, "5dd")
        self.assertEqual(updated.action, "updated")
        self.assertEqual(self.service.list_positions().positions, [updated.position])

        deleted = self.service.delete("bbca", "5dd")
        self.assertEqual(deleted.action, "deleted")
        self.assertEqual(self.service.list_positions().positions, [])

        with self.csv_path.open(newline="", encoding="utf-8") as csv_file:
            self.assertEqual(
                list(csv.reader(csv_file)),
                [["ticker", "price", "rolling_window"]],
            )

    def test_rejects_duplicate_missing_and_invalid_values(self) -> None:
        self.service.add("AAPL", 100, "10dd")
        with self.assertRaisesRegex(ValueError, "already exists"):
            self.service.add("aapl", 101, "10dd")
        with self.assertRaisesRegex(ValueError, "was not found"):
            self.service.update("MSFT", 100, "10dd")
        with self.assertRaisesRegex(ValueError, "was not found"):
            self.service.delete("MSFT", "10dd")
        with self.assertRaisesRegex(ValueError, "positive number"):
            self.service.add("MSFT", 0, "10dd")
        with self.assertRaisesRegex(ValueError, "unsupported characters"):
            self.service.add("bad ticker", 1, "10dd")
        with self.assertRaisesRegex(ValueError, "either 5dd or 10dd"):
            self.service.add("MSFT", 100, "20dd")

    def test_same_ticker_can_exist_in_both_rolling_windows(self) -> None:
        short = self.service.add("BBCA", 9200, "5dd")
        long = self.service.add("BBCA", 9250, "10dd")

        self.assertEqual(
            self.service.list_positions().positions,
            [long.position, short.position],
        )

        self.service.delete("BBCA", "5dd")
        self.assertEqual(self.service.list_positions().positions, [long.position])

    def test_csv_has_exact_columns_and_sorted_tickers(self) -> None:
        self.service.add("MSFT", "200.25", "5dd")
        self.service.add("AAPL", "100.50", "10dd")

        with self.csv_path.open(newline="", encoding="utf-8") as csv_file:
            rows = list(csv.DictReader(csv_file))

        self.assertEqual(rows, [
            {"ticker": "AAPL", "price": "100.50", "rolling_window": "10dd"},
            {"ticker": "MSFT", "price": "200.25", "rolling_window": "5dd"},
        ])


if __name__ == "__main__":
    unittest.main()
