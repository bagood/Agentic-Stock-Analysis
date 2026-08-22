import csv
import tempfile
import unittest
from pathlib import Path

from run_detailed_analysis import (
    combine_tickers,
    load_portfolio_tickers,
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
                    [["ticker", "price"], ["bbca", "9250"], [" TLKM ", "3000"]]
                )

            self.assertEqual(load_portfolio_tickers(csv_path), ["BBCA", "TLKM"])

    def test_missing_portfolio_file_is_treated_as_empty(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            csv_path = Path(temporary_directory) / "missing.csv"
            self.assertEqual(load_portfolio_tickers(csv_path), [])

    def test_combines_sources_and_deduplicates_in_source_order(self) -> None:
        combined = combine_tickers(
            ["MDIA", "BBCA", "TLKM"],
            ["bbca", "ASII", " tlkm "],
        )

        self.assertEqual(combined, ["MDIA", "BBCA", "TLKM", "ASII"])


if __name__ == "__main__":
    unittest.main()
