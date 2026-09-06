from pathlib import Path

from app.models.entry_strategy import EntryStrategyReport

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENTRY_STRATEGY_RESULT = PROJECT_ROOT / "entryStrategyResults"


class EntryStrategyRepository:
    """Read generated entry-strategy reports from the filesystem."""

    def __init__(self, results_directory: Path = ENTRY_STRATEGY_RESULT) -> None:
        self._results_directory = results_directory

    def get_tickers(self, rolling_window: str) -> list[str]:
        window_directory = self._results_directory / rolling_window
        if not window_directory.is_dir():
            return []

        return sorted(
            report_path.stem.upper()
            for report_path in window_directory.glob("*.md")
            if report_path.is_file()
        )

    def get_report(
        self,
        ticker: str,
        rolling_window: str,
    ) -> EntryStrategyReport | None:
        report_path = self._results_directory / rolling_window / f"{ticker}.md"
        if not report_path.is_file():
            return None

        return EntryStrategyReport(
            ticker=ticker,
            report=report_path.read_text(encoding="utf-8"),
        )

