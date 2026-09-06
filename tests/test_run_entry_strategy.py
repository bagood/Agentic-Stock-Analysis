import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import run_entry_strategy as runner
from entryStrategy.helper import build_entry_strategy_prompt, list_analysis_reports
from run_entry_strategy import WINDOW_CONFIGS, parse_args, prepare_output_dir


class EntryStrategyHelperTests(unittest.TestCase):
    def test_lists_markdown_reports_in_ticker_order(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            analysis_dir = Path(temporary_directory)
            (analysis_dir / "TLKM.md").write_text("tlkm", encoding="utf-8")
            (analysis_dir / "BBCA.md").write_text("bbca", encoding="utf-8")
            (analysis_dir / "ignore.txt").write_text("x", encoding="utf-8")

            self.assertEqual(
                [path.name for path in list_analysis_reports(analysis_dir)],
                ["BBCA.md", "TLKM.md"],
            )

    def test_rejects_a_missing_analysis_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            missing = Path(temporary_directory) / "missing"
            with self.assertRaisesRegex(ValueError, "does not exist"):
                list_analysis_reports(missing)

    def test_builds_prompt_with_delimited_source_report(self) -> None:
        prompt = build_entry_strategy_prompt(
            "Instructions", "# Analysis\nEvidence", "bbca", "5–10 sessions"
        )

        self.assertIn("IDX-listed BBCA", prompt)
        self.assertIn("<ANALYSIS_REPORT>\n# Analysis\nEvidence", prompt)
        self.assertTrue(prompt.endswith("</ANALYSIS_REPORT>\n"))


class EntryStrategyArgumentTests(unittest.TestCase):
    def test_defaults_to_ten_to_twenty(self) -> None:
        self.assertEqual(parse_args([]).forecast_window, "10-20")

    def test_accepts_supported_windows(self) -> None:
        for window in ("5-10", "10-20"):
            self.assertEqual(
                parse_args(["--forecast-window", window]).forecast_window,
                window,
            )

    def test_window_configuration_points_to_existing_instructions(self) -> None:
        project_dir = Path(__file__).resolve().parent.parent
        self.assertEqual(WINDOW_CONFIGS["5-10"]["rolling_window"], "5dd")
        self.assertEqual(WINDOW_CONFIGS["10-20"]["rolling_window"], "10dd")
        for config in WINDOW_CONFIGS.values():
            self.assertTrue((project_dir / config["instructions_path"]).is_file())


class EntryStrategyOutputTests(unittest.TestCase):
    def test_clears_only_selected_window(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "entryStrategyResults"
            selected = root / "10dd"
            other = root / "5dd"
            selected.mkdir(parents=True)
            other.mkdir(parents=True)
            (selected / "OLD.md").write_text("old", encoding="utf-8")
            (other / "KEEP.md").write_text("keep", encoding="utf-8")

            self.assertEqual(prepare_output_dir(selected), selected)
            self.assertEqual(list(selected.iterdir()), [])
            self.assertTrue((other / "KEEP.md").is_file())

    def test_main_processes_matching_analysis_window(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            analysis_dir = root / "detailedAnalysisResults" / "5dd"
            analysis_dir.mkdir(parents=True)
            report = analysis_dir / "BBCA.md"
            report.write_text("analysis", encoding="utf-8")
            strategy_root = root / "entryStrategyResults"

            with patch.dict(
                os.environ,
                {
                    "OUTPUT_DIR": str(root / "detailedAnalysisResults"),
                    "ENTRY_STRATEGY_OUTPUT_DIR": str(strategy_root),
                },
                clear=False,
            ), patch.object(runner, "load_env"), patch.object(
                runner, "generate_entry_strategy", return_value=0
            ) as generate:
                result = runner.main("5-10")

            self.assertEqual(result, 0)
            generate.assert_called_once_with(
                "BBCA",
                str(report),
                "instructions/stock-entry-strategy-5-10-instructions.md",
                "5–10 trading sessions",
                str(strategy_root / "5dd"),
            )

    def test_main_returns_success_when_analysis_window_is_empty(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "detailedAnalysisResults" / "10dd").mkdir(parents=True)

            with patch.dict(
                os.environ,
                {
                    "OUTPUT_DIR": str(root / "detailedAnalysisResults"),
                    "ENTRY_STRATEGY_OUTPUT_DIR": str(
                        root / "entryStrategyResults"
                    ),
                },
                clear=False,
            ), patch.object(runner, "load_env"), patch.object(
                runner, "generate_entry_strategy"
            ) as generate:
                result = runner.main("10-20")

            self.assertEqual(result, 0)
            generate.assert_not_called()


if __name__ == "__main__":
    unittest.main()

