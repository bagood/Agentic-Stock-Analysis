import tempfile
import unittest
from pathlib import Path

from app.repositories.entry_strategy_repository import EntryStrategyRepository
from app.services.entry_strategy_service import EntryStrategyService


class EntryStrategyServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.results_directory = Path(self.temporary_directory.name)
        for rolling_window, reports in (
            ("5dd", {"FIVE": "five report", "SHARED": "five shared"}),
            ("10dd", {"TEN": "ten report", "SHARED": "ten shared"}),
        ):
            window_directory = self.results_directory / rolling_window
            window_directory.mkdir()
            for ticker, contents in reports.items():
                (window_directory / f"{ticker}.md").write_text(
                    contents,
                    encoding="utf-8",
                )
        self.service = EntryStrategyService(
            EntryStrategyRepository(self.results_directory)
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_lists_tickers_from_selected_window(self) -> None:
        self.assertEqual(
            self.service.get_tickers("5DD").tickers,
            ["FIVE", "SHARED"],
        )
        self.assertEqual(
            self.service.get_tickers("10dd").tickers,
            ["SHARED", "TEN"],
        )

    def test_reads_and_normalizes_requested_report(self) -> None:
        report = self.service.get_report(" shared ", "10DD")

        self.assertIsNotNone(report)
        self.assertEqual(report.ticker, "SHARED")
        self.assertEqual(report.report, "ten shared")

    def test_returns_none_for_missing_report(self) -> None:
        self.assertIsNone(self.service.get_report("MISSING", "5dd"))

    def test_rejects_invalid_ticker_and_window(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported characters"):
            self.service.get_report("../FIVE", "5dd")
        with self.assertRaisesRegex(ValueError, "must be 5dd or 10dd"):
            self.service.get_tickers("20dd")


if __name__ == "__main__":
    unittest.main()

