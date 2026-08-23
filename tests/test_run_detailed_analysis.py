import csv
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import run_detailed_analysis as runner

from run_detailed_analysis import (
    FORECAST_CONFIGS,
    combine_tickers,
    load_portfolio_tickers,
    parse_args,
    prepare_output_dir,
    select_positive_tickers,
)


class SelectPositiveTickersTests(unittest.TestCase):
    def test_falls_back_to_top_four_when_only_two_clear_minimum(self) -> None:
        payload = {
            "score_date": "2026-08-07",
            "rolling_window": "10dd",
            "recommendations": [
                {
                    "ticker": "MDIA",
                    "score": 0.8599585269409312,
                    "target_buy_price": 212.0,
                    "target_sell_price": 267.0,
                },
                {
                    "ticker": "OASA",
                    "score": 0.5736330807047905,
                    "target_buy_price": 275.0,
                    "target_sell_price": 362.0,
                },
                {
                    "ticker": "BULL",
                    "score": 0.2157031614335893,
                    "target_buy_price": 365.0,
                    "target_sell_price": 481.0,
                },
                {
                    "ticker": "INDY",
                    "score": 0.1778875178227112,
                    "target_buy_price": 2244.0,
                    "target_sell_price": 2831.0,
                },
                {
                    "ticker": "BNBR",
                    "score": 0.1558037053441054,
                    "target_buy_price": 88.0,
                    "target_sell_price": 112.0,
                },
                {
                    "ticker": "MINA",
                    "score": 0.1414038307026853,
                    "target_buy_price": 231.0,
                    "target_sell_price": 292.0,
                },
                {
                    "ticker": "UNTR",
                    "score": 0.1292442781296986,
                    "target_buy_price": 19680.0,
                    "target_sell_price": 24815.0,
                },
                {
                    "ticker": "PADI",
                    "score": 0.0633433630397498,
                    "target_buy_price": 61.0,
                    "target_sell_price": 78.0,
                },
                {
                    "ticker": "ANTM",
                    "score": 0.0393221749179978,
                    "target_buy_price": 2626.0,
                    "target_sell_price": 3313.0,
                },
                {
                    "ticker": "EMTK",
                    "score": 0.0382674360882503,
                    "target_buy_price": 440.0,
                    "target_sell_price": 556.0,
                },
                {
                    "ticker": "SSMS",
                    "score": 0.0160040774695938,
                    "target_buy_price": 764.0,
                    "target_sell_price": 965.0,
                },
            ],
        }

        selected = select_positive_tickers(payload, minimum_score=0.5)

        self.assertEqual(selected, ["MDIA", "OASA", "BULL", "INDY"])


class PortfolioTickerTests(unittest.TestCase):
    def test_loads_normalized_portfolio_tickers(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            csv_path = Path(temporary_directory) / "portfolio.csv"
            with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(
                    [
                        ["ticker", "price", "rolling_window"],
                        ["bbca", "9250", "5dd"],
                        [" TLKM ", "3000", "10dd"],
                        ["asii", "5100", "5dd"],
                    ]
                )

            self.assertEqual(
                load_portfolio_tickers("5dd", csv_path), ["BBCA", "ASII"]
            )
            self.assertEqual(
                load_portfolio_tickers("10dd", csv_path), ["TLKM"]
            )

    def test_missing_portfolio_file_is_treated_as_empty(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            csv_path = Path(temporary_directory) / "missing.csv"
            self.assertEqual(load_portfolio_tickers("5dd", csv_path), [])

    def test_rejects_invalid_portfolio_rolling_window(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            csv_path = Path(temporary_directory) / "portfolio.csv"
            with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(
                    [
                        ["ticker", "price", "rolling_window"],
                        ["BBCA", "9250", "7dd"],
                    ]
                )

            with self.assertRaisesRegex(ValueError, "invalid rolling_window"):
                load_portfolio_tickers("5dd", csv_path)

    def test_rejects_unsupported_requested_rolling_window(self) -> None:
        with self.assertRaisesRegex(ValueError, "either 5dd or 10dd"):
            load_portfolio_tickers("7dd")

    def test_combines_sources_and_deduplicates_in_source_order(self) -> None:
        combined = combine_tickers(
            ["MDIA", "BBCA", "TLKM"],
            ["bbca", "ASII", " tlkm "],
        )

        self.assertEqual(combined, ["MDIA", "BBCA", "TLKM", "ASII"])


class OutputDirectoryTests(unittest.TestCase):
    def test_clears_only_the_selected_rolling_window_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_root = Path(temporary_directory) / "analysisResults"
            selected_dir = output_root / "10dd"
            other_dir = output_root / "5dd"
            selected_dir.mkdir(parents=True)
            other_dir.mkdir(parents=True)
            (selected_dir / "OLD.md").write_text("old", encoding="utf-8")
            (other_dir / "KEEP.md").write_text("keep", encoding="utf-8")

            prepared = prepare_output_dir(str(selected_dir))

            self.assertEqual(prepared, selected_dir)
            self.assertEqual(list(selected_dir.iterdir()), [])
            self.assertEqual(
                (other_dir / "KEEP.md").read_text(encoding="utf-8"),
                "keep",
            )


class ForecastArgumentTests(unittest.TestCase):
    def test_defaults_to_ten_to_twenty(self) -> None:
        self.assertEqual(parse_args([]).forecast_window, "10-20")

    def test_accepts_each_supported_forecast_window(self) -> None:
        for forecast_window in ("5-10", "10-20"):
            with self.subTest(forecast_window=forecast_window):
                arguments = parse_args(
                    ["--forecast-window", forecast_window]
                )
                self.assertEqual(arguments.forecast_window, forecast_window)

    def test_rejects_an_unsupported_forecast_window(self) -> None:
        with self.assertRaises(SystemExit) as raised:
            parse_args(["--forecast-window", "7-14"])

        self.assertEqual(raised.exception.code, 2)

    def test_each_window_has_distinct_complete_configuration(self) -> None:
        self.assertEqual(
            FORECAST_CONFIGS["5-10"],
            {
                "instructions_path": (
                    "instructions/stock-upside-analysis-5-10-instructions.md"
                ),
                "rolling_window": "5dd",
                "prompt_horizon": "5–10 trading days",
            },
        )
        self.assertEqual(
            FORECAST_CONFIGS["10-20"],
            {
                "instructions_path": (
                    "instructions/stock-upside-analysis-10-20-instructions.md"
                ),
                "rolling_window": "10dd",
                "prompt_horizon": "10–20 trading days",
            },
        )

        instruction_paths = {
            config["instructions_path"] for config in FORECAST_CONFIGS.values()
        }
        self.assertEqual(len(instruction_paths), 2)
        for instruction_path in instruction_paths:
            self.assertTrue(
                (Path(__file__).resolve().parent.parent / instruction_path).is_file()
            )

    def test_main_applies_the_selected_configuration_end_to_end(self) -> None:
        for forecast_window, rolling_window, instruction_name, horizon in (
            (
                "5-10",
                "5dd",
                "stock-upside-analysis-5-10-instructions.md",
                "5–10 trading days",
            ),
            (
                "10-20",
                "10dd",
                "stock-upside-analysis-10-20-instructions.md",
                "10–20 trading days",
            ),
        ):
            with self.subTest(forecast_window=forecast_window), patch.dict(
                os.environ,
                {
                    "BASE_URL": "https://data.example.test/",
                    "OUTPUT_DIR": "unused-in-test",
                    "MINIMUM_SCORE": "0.5",
                },
                clear=False,
            ), patch.object(runner, "load_env"), patch.object(
                runner,
                "prepare_output_dir",
                return_value=Path(f"/tmp/analysisResults/{rolling_window}"),
            ) as prepare_output, patch.object(
                runner,
                "fetch_json",
                return_value={
                    "recommendations": [{"ticker": "BBCA", "score": 0.9}]
                },
            ) as fetch_json, patch.object(
                runner, "load_portfolio_tickers", return_value=[]
            ) as load_portfolio, patch.object(
                runner, "run_detailed_analysis", return_value=0
            ) as analyze:
                result = runner.main(forecast_window, timeout=12.0)

                self.assertEqual(result, 0)
                prepare_output.assert_called_once_with(
                    f"unused-in-test/{rolling_window}"
                )
                fetch_json.assert_called_once_with(
                    "https://data.example.test/analytics/"
                    f"daily_recommendations?rolling_window={rolling_window}",
                    12.0,
                )
                load_portfolio.assert_called_once_with(rolling_window)
                analyze.assert_called_once_with(
                    "BBCA",
                    f"instructions/{instruction_name}",
                    horizon,
                    "https://data.example.test/",
                    f"/tmp/analysisResults/{rolling_window}",
                    12.0,
                )


if __name__ == "__main__":
    unittest.main()
