import os
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

import run_hold_strategy as runner
from holdStrategy.helper import Holding, build_hold_strategy_prompt, parse_holdings
from run_hold_strategy import WINDOW_CONFIGS, parse_args, prepare_output_dir


class HoldStrategyHelperTests(unittest.TestCase):
    def test_parses_stocks_object_and_sorts_tickers(self) -> None:
        holdings = parse_holdings(
            {
                "stocks": [
                    {"ticker": "bbca", "price": "9250", "trading_window": "5dd"},
                    {"ticker": "ASII", "price": "5100.50"},
                ]
            },
            "5dd",
        )

        self.assertEqual([holding.ticker for holding in holdings], ["ASII", "BBCA"])
        self.assertEqual(holdings[0].average_price, Decimal("5100.50"))

    def test_parses_ticker_only_array_without_price(self) -> None:
        holdings = parse_holdings(["BNBR"], "10dd")

        self.assertEqual([holding.ticker for holding in holdings], ["BNBR"])
        self.assertIsNone(holdings[0].average_price)

    def test_rejects_non_positive_price(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalid price"):
            parse_holdings([{"ticker": "BBCA", "price": 0}], "5dd")

    def test_prompt_includes_position_and_delimited_analysis(self) -> None:
        holding = Holding("BBCA", Decimal("9250"), "5dd")
        prompt = build_hold_strategy_prompt(
            "Instructions", "# Analysis\nEvidence", holding, "5–10 sessions"
        )

        self.assertIn("Average acquisition price: IDR 9250", prompt)
        self.assertIn("Quantity: Not supplied", prompt)
        self.assertIn("<ANALYSIS_REPORT>\n# Analysis\nEvidence", prompt)
        self.assertTrue(prompt.endswith("</ANALYSIS_REPORT>\n"))

    def test_prompt_marks_missing_average_price(self) -> None:
        holding = Holding("BBCA", None, "5dd")
        prompt = build_hold_strategy_prompt(
            "Instructions", "Analysis", holding, "5–10 sessions"
        )

        self.assertIn("Average acquisition price: Not supplied", prompt)


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

    def test_main_fetches_stocks_api_for_selected_window(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            analysis_dir = root / "detailedAnalysisResults" / "10dd"
            analysis_dir.mkdir(parents=True)
            analysis_path = analysis_dir / "INDY.md"
            analysis_path.write_text("analysis", encoding="utf-8")
            output_root = root / "holdStrategyResults"

            with patch.dict(
                os.environ,
                {
                    "DETAILED_ANALYSIS_RESULT": str(root / "detailedAnalysisResults"),
                    "HOLD_STRATEGY_RESULT": str(output_root),
                    "ORGANIZER_BASE_URL": "http://localhost:8000",
                },
                clear=False,
            ), patch.object(runner, "load_env"), patch.object(
                runner,
                "fetch_json",
                return_value=["INDY"],
            ) as fetch_json, patch.object(
                runner, "generate_hold_strategy", return_value=0
            ) as generate:
                result = runner.main("10-20", timeout=12.0)

            self.assertEqual(result, 0)
            fetch_json.assert_called_once_with(
                "http://localhost:8000/stocks?trading_window=10dd",
                12.0,
            )
            holding = Holding("INDY", None, "10dd")
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

            with patch.dict(
                os.environ,
                {
                    "DETAILED_ANALYSIS_RESULT": str(root / "detailedAnalysisResults"),
                    "HOLD_STRATEGY_RESULT": str(root / "holdStrategyResults"),
                    "ORGANIZER_BASE_URL": "http://localhost:8000",
                },
                clear=False,
            ), patch.object(runner, "load_env"), patch.object(
                runner,
                "fetch_json",
                return_value=["BBCA"],
            ), patch.object(
                runner, "generate_hold_strategy", return_value=1
            ):
                self.assertEqual(runner.main("5-10"), 1)


if __name__ == "__main__":
    unittest.main()
