import csv
import os
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

import run_hold_strategy as runner
from holdStrategy.helper import Holding, build_hold_strategy_prompt, load_holdings
from run_hold_strategy import WINDOW_CONFIGS, parse_args, prepare_output_dir


class HoldStrategyHelperTests(unittest.TestCase):
    def test_loads_only_selected_window_and_sorts_tickers(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            csv_path = Path(temporary_directory) / "portfolio.csv"
            with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
                csv.writer(csv_file).writerows(
                    [
                        ["ticker", "price", "rolling_window"],
                        ["tlkm", "3000", "10dd"],
                        ["ASII", "5100.50", "5dd"],
                        ["bbca", "9250", "5dd"],
                    ]
                )

            holdings = load_holdings(csv_path, "5dd")

            self.assertEqual([holding.ticker for holding in holdings], ["ASII", "BBCA"])
            self.assertEqual(holdings[0].average_price, Decimal("5100.50"))

    def test_rejects_non_positive_price(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            csv_path = Path(temporary_directory) / "portfolio.csv"
            csv_path.write_text(
                "ticker,price,rolling_window\nBBCA,0,5dd\n", encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "invalid price"):
                load_holdings(csv_path, "5dd")

    def test_prompt_includes_position_and_delimited_analysis(self) -> None:
        holding = Holding("BBCA", Decimal("9250"), "5dd")
        prompt = build_hold_strategy_prompt(
            "Instructions", "# Analysis\nEvidence", holding, "5–10 sessions"
        )

        self.assertIn("Average acquisition price: IDR 9250", prompt)
        self.assertIn("Quantity: Not supplied", prompt)
        self.assertIn("<ANALYSIS_REPORT>\n# Analysis\nEvidence", prompt)
        self.assertTrue(prompt.endswith("</ANALYSIS_REPORT>\n"))


class HoldStrategyArgumentTests(unittest.TestCase):
    def test_defaults_to_ten_to_twenty(self) -> None:
        self.assertEqual(parse_args([]).forecast_window, "10-20")

    def test_accepts_both_windows(self) -> None:
        for window in ("5-10", "10-20"):
            self.assertEqual(
                parse_args(["--forecast-window", window]).forecast_window,
                window,
            )

    def test_configurations_reference_existing_instructions(self) -> None:
        project_dir = Path(__file__).resolve().parent.parent
        self.assertEqual(WINDOW_CONFIGS["5-10"]["rolling_window"], "5dd")
        self.assertEqual(WINDOW_CONFIGS["10-20"]["rolling_window"], "10dd")
        for config in WINDOW_CONFIGS.values():
            self.assertTrue((project_dir / config["instructions_path"]).is_file())


class HoldStrategyRunnerTests(unittest.TestCase):
    def test_clears_only_selected_output_window(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "holdStrategyResults"
            selected = root / "10dd"
            other = root / "5dd"
            selected.mkdir(parents=True)
            other.mkdir(parents=True)
            (selected / "OLD.md").write_text("old", encoding="utf-8")
            (other / "KEEP.md").write_text("keep", encoding="utf-8")

            self.assertEqual(prepare_output_dir(selected), selected)
            self.assertEqual(list(selected.iterdir()), [])
            self.assertTrue((other / "KEEP.md").is_file())

    def test_main_generates_only_for_matching_portfolio_window(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            analysis_dir = root / "detailedAnalysisResults" / "10dd"
            analysis_dir.mkdir(parents=True)
            analysis_path = analysis_dir / "INDY.md"
            analysis_path.write_text("analysis", encoding="utf-8")
            portfolio_path = root / "portfolio.csv"
            portfolio_path.write_text(
                "ticker,price,rolling_window\nINDY,2680,10dd\nBIPI,154,5dd\n",
                encoding="utf-8",
            )
            output_root = root / "holdStrategyResults"

            with patch.dict(
                os.environ,
                {
                    "DETAILED_ANALYSIS_RESULT": str(root / "detailedAnalysisResults"),
                    "PORTFOLIO_CSV_PATH": str(portfolio_path),
                    "HOLD_STRATEGY_RESULT": str(output_root),
                },
                clear=False,
            ), patch.object(runner, "load_env"), patch.object(
                runner, "generate_hold_strategy", return_value=0
            ) as generate:
                result = runner.main("10-20")

            self.assertEqual(result, 0)
            holding = Holding("INDY", Decimal("2680"), "10dd")
            generate.assert_called_once_with(
                holding,
                str(analysis_path),
                "instructions/stock-hold-strategy-10-20-instructions.md",
                "10–20 trading sessions",
                str(output_root / "10dd"),
            )

    def test_missing_analysis_is_reported_as_a_ticker_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            portfolio_path = root / "portfolio.csv"
            portfolio_path.write_text(
                "ticker,price,rolling_window\nBBCA,9250,5dd\n", encoding="utf-8"
            )

            with patch.dict(
                os.environ,
                {
                    "DETAILED_ANALYSIS_RESULT": str(root / "detailedAnalysisResults"),
                    "PORTFOLIO_CSV_PATH": str(portfolio_path),
                    "HOLD_STRATEGY_RESULT": str(root / "holdStrategyResults"),
                },
                clear=False,
            ), patch.object(runner, "load_env"), patch.object(
                runner, "generate_hold_strategy", return_value=1
            ):
                self.assertEqual(runner.main("5-10"), 1)


if __name__ == "__main__":
    unittest.main()
