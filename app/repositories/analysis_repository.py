from pathlib import Path

from app.models.analysis import AnalysisReport

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ANALYSIS_RESULTS_DIR = PROJECT_ROOT / "analysisResults"


class AnalysisRepository:
    """Read generated analysis reports from the filesystem."""

    def __init__(self, results_directory: Path = ANALYSIS_RESULTS_DIR) -> None:
        self._results_directory = results_directory

    def get_tickers(self) -> list[str]:
        if not self._results_directory.is_dir():
            return []

        return sorted(
            report_path.stem.upper()
            for report_path in self._results_directory.glob("*.md")
            if report_path.is_file()
        )

    def get_report(self, ticker: str) -> AnalysisReport | None:
        report_path = self._results_directory / f"{ticker}.md"
        if not report_path.is_file():
            return None

        return AnalysisReport(
            ticker=ticker,
            report=report_path.read_text(encoding="utf-8"),
        )
