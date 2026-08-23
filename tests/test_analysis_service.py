import tempfile
import unittest
from pathlib import Path

from app.repositories.analysis_repository import AnalysisRepository
from app.services.analysis_service import AnalysisService


class AnalysisServiceTest(unittest.TestCase):
    def test_get_report_uses_requested_rolling_window_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            results_directory = Path(temporary_directory)
            for rolling_window, contents in (
                ("5dd", "five-day report"),
                ("10dd", "ten-day report"),
            ):
                window_directory = results_directory / rolling_window
                window_directory.mkdir()
                (window_directory / "TEST.md").write_text(
                    contents,
                    encoding="utf-8",
                )

            service = AnalysisService(AnalysisRepository(results_directory))

            self.assertEqual(
                service.get_report("test", "5dd").report,
                "five-day report",
            )
            self.assertEqual(
                service.get_report("test", "10dd").report,
                "ten-day report",
            )

    def test_get_report_rejects_unsupported_rolling_window(self) -> None:
        service = AnalysisService(AnalysisRepository())

        with self.assertRaisesRegex(ValueError, "must be 5dd or 10dd"):
            service.get_report("TEST", "20dd")


if __name__ == "__main__":
    unittest.main()
