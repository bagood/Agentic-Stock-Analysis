import io
import os
from contextlib import redirect_stderr, redirect_stdout
import tempfile
import unittest
from pathlib import Path
from unittest.mock import call, patch
from unittest.mock import ANY

import run_detailed_analysis as runner

from run_detailed_analysis import (
    FORECAST_CONFIGS,
    combine_tickers,
    parse_args,
    parse_scored_recommendations,
    prepare_output_dir,
    select_top_tickers,
    select_stock_tickers,
)


def recommendations(*entries):
    return {"recommendations": [
        {"ticker": ticker, "score": score} for ticker, score in entries
    ]}


class SelectTopTickersTests(unittest.TestCase):
    def test_sorts_unsorted_candidates_and_caps_at_k(self):
        payload = recommendations(("FIVE", .5), ("ONE", .9), ("THREE", .7),
                                  ("TWO", .8), ("FOUR", .6))
        self.assertEqual(select_top_tickers(payload, 4), ["ONE", "TWO", "THREE", "FOUR"])
        self.assertEqual(select_top_tickers(payload, 2), ["ONE", "TWO"])

    def test_ties_zero_negative_scores_and_normalized_duplicates(self):
        payload = recommendations((" zzzz ", -1), ("BBBB", 0), ("aaaa", 0),
                                  ("ZZZZ", -2), ("bbbb", -3), ("CCCC", -4))
        self.assertEqual(select_top_tickers(payload, 4), ["AAAA", "BBBB", "ZZZZ", "CCCC"])
        self.assertEqual(parse_scored_recommendations(payload),
                         [("AAAA", 0.), ("BBBB", 0.), ("ZZZZ", -1.), ("CCCC", -4.)])

    def test_rejects_invalid_counts(self):
        for count in (True, False, 0, -1, 1.5, "4", None):
            with self.subTest(count=count), self.assertRaisesRegex(ValueError, "positive integer"):
                select_top_tickers(recommendations(("AAAA", 1)), count)

    def test_rejects_invalid_and_nonfinite_scores(self):
        for score in (float("nan"), float("inf"), float("-inf"), 10 ** 400, True, "1", None):
            with self.subTest(score=score), self.assertRaisesRegex(ValueError, "invalid score"):
                select_top_tickers(recommendations(("AAAA", score)), 1)

    def test_rejects_invalid_payloads_and_tickers(self):
        for payload in ([], {}, {"recommendations": {}}, {"recommendations": [None]},
                        recommendations(("ßaa", .9)), recommendations((" ", .9)),
                        recommendations((None, .9))):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                select_top_tickers(payload, 1)

    def test_reports_quota_shortage_after_normalization(self):
        for payload, available in ((recommendations(), 0),
                                   (recommendations(("aaaa", 1), (" AAAA ", 2)), 1)):
            with self.subTest(available=available), self.assertRaisesRegex(
                ValueError, f"requested 4.*available {available}"
            ):
                select_top_tickers(payload, 4)


class SelectStockTickersTests(unittest.TestCase):
    def test_rejects_unicode_before_uppercase_can_expand_it(self) -> None:
        with self.assertRaises(ValueError):
            select_stock_tickers(["ßaa"], "5dd")

    def test_accepts_stocks_object_and_deduplicates_tickers(self) -> None:
        selected = select_stock_tickers(
            {
                "stocks": [
                    {"ticker": "indy", "trading_window": "10dd"},
                    {"ticker": "BBCA"},
                    {"ticker": "INDY"},
                ]
            },
            "10dd",
        )

        self.assertEqual(selected, ["INDY", "BBCA"])

    def test_accepts_ticker_string_array(self) -> None:
        self.assertEqual(
            select_stock_tickers(["BNBR"], "10dd"),
            ["BNBR"],
        )

    def test_rejects_mismatched_trading_window(self) -> None:
        with self.assertRaisesRegex(ValueError, "expected 5dd"):
            select_stock_tickers(
                [{"ticker": "BBCA", "trading_window": "10dd"}],
                "5dd",
            )


class CombineTickerTests(unittest.TestCase):
    def test_combines_sources_and_deduplicates_in_source_order(self) -> None:
        combined = combine_tickers(
            ["MDIA", "BBCA", "TLKM"],
            ["bbca", "ASII", " tlkm "],
        )

        self.assertEqual(combined, ["MDIA", "BBCA", "TLKM", "ASII"])


class OutputDirectoryTests(unittest.TestCase):
    def test_clears_only_the_selected_rolling_window_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_root = Path(temporary_directory) / "detailedAnalysisResults"
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
    def setUp(self):
        self.preflight = patch.object(runner, "preflight").start()
        self.addCleanup(patch.stopall)

    def test_defaults_to_ten_sessions(self) -> None:
        self.assertEqual(parse_args([]).forecast_window, "10")

    def test_accepts_each_supported_forecast_window(self) -> None:
        for forecast_window in ("5", "10"):
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
            FORECAST_CONFIGS["5"],
            {
                "instructions_path": (
                    "instructions/stock-upside-analysis-5-instructions.md"
                ),
                "rolling_window": "5dd",
                "prompt_horizon": "5 trading sessions",
            },
        )
        self.assertEqual(
            FORECAST_CONFIGS["10"],
            {
                "instructions_path": (
                    "instructions/stock-upside-analysis-10-instructions.md"
                ),
                "rolling_window": "10dd",
                "prompt_horizon": "10 trading sessions",
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
                "5",
                "5dd",
                "stock-upside-analysis-5-instructions.md",
                "5 trading sessions",
            ),
            (
                "10",
                "10dd",
                "stock-upside-analysis-10-instructions.md",
                "10 trading sessions",
            ),
        ):
            with self.subTest(forecast_window=forecast_window), patch.dict(
                os.environ,
                {
                    "ML_BASE_URL": "https://data.example.test/",
                    "ORGANIZER_BASE_URL": "http://localhost:8000",
                    "DETAILED_ANALYSIS_RESULT": "unused-in-test",
                },
                clear=False,
            ), patch.object(runner, "load_env"), patch.object(
                runner,
                "prepare_output_dir",
                return_value=Path(f"/tmp/detailedAnalysisResults/{rolling_window}"),
            ) as prepare_output, patch.object(
                runner,
                "fetch_json",
                side_effect=[
                    recommendations(("BBCA", .9), ("BMRI", .8), ("ASII", 0), ("INDY", -1)),
                    {"stocks": [{"ticker": "TLKM"}]},
                ],
            ) as fetch_json, patch.object(
                runner, "run_detailed_analysis", return_value=0
            ) as analyze:
                result = runner.main(forecast_window, timeout=12.0)

                self.assertEqual(result, 0)
                prepare_output.assert_called_once_with(
                    f"unused-in-test/{rolling_window}"
                )
                self.assertEqual(
                    fetch_json.call_args_list,
                    [
                        call(
                            "https://data.example.test/analytics/"
                            f"daily_recommendations?rolling_window={rolling_window}",
                            12.0,
                        ),
                        call(
                            "http://localhost:8000/stocks?trading_window="
                            f"{rolling_window}",
                            12.0,
                        ),
                    ],
                )
                self.assertEqual(
                    analyze.call_args_list,
                    [
                        call(
                            ticker,
                            f"instructions/{instruction_name}",
                            horizon,
                            "https://data.example.test/",
                            f"/tmp/detailedAnalysisResults/{rolling_window}",
                            12.0,
                            forecast_type=rolling_window,
                            technical_config=ANY,
                            _preflight=ANY,
                        )
                        for ticker in (
                            "BBCA", "BMRI", "ASII", "INDY", "TLKM",
                        )
                    ],
                )


class BatchTests(unittest.TestCase):
    candidates = recommendations(("DDDD", -1), ("BBBB", .8), ("AAAA", .9),
                                ("EEEE", -2), ("CCCC", 0))

    def run_batch(self, payload=None, stocks=None, outcomes=None, target_count=4,
                  forecast_window="5", fetch_error=None, preflight_error=None):
        with patch.dict(os.environ, {
            "ML_BASE_URL": "https://data.example.test",
            "DETAILED_ANALYSIS_RESULT": "unused",
            "ORGANIZER_BASE_URL": "https://organizer.example.test",
        }, clear=True), patch.object(runner, "load_env"), patch.object(
            runner, "TARGET_COUNT", target_count
        ), patch.object(runner, "preflight", side_effect=preflight_error) as checked, patch.object(
            runner, "prepare_output_dir", return_value=Path("/tmp/unused")
        ) as prepare, patch.object(
            runner, "fetch_json", side_effect=fetch_error or [
                self.candidates if payload is None else payload,
                [] if stocks is None else stocks,
            ]
        ) as fetch, patch.object(
            runner, "run_detailed_analysis", side_effect=outcomes, return_value=0
        ) as analyze, redirect_stdout(io.StringIO()) as stdout, redirect_stderr(io.StringIO()) as stderr:
            result = runner.main(forecast_window)
        return result, analyze, prepare, fetch, checked, stdout.getvalue(), stderr.getvalue()

    def test_portfolio_shapes_holdings_and_service_order(self):
        cases = [
            ([], ["AAAA", "BBBB", "CCCC", "DDDD"]),
            (["BBBB"], ["AAAA", "BBBB", "CCCC", "DDDD"]),
            (["bbbb", " EEEE ", "FFFF", "eeee"],
             ["AAAA", "BBBB", "CCCC", "DDDD", "EEEE", "FFFF"]),
            ([{"ticker": "EEEE", "rolling_window": "5dd"}, {"ticker": "BBBB"}],
             ["AAAA", "BBBB", "CCCC", "DDDD", "EEEE"]),
        ]
        for stocks, expected in cases:
            for payload in (stocks, {"stocks": stocks}):
                with self.subTest(payload=payload):
                    result, analyze, prepare, _, checked, output, _ = self.run_batch(stocks=payload)
                    self.assertEqual(result, 0)
                    self.assertEqual([c.args[0] for c in analyze.call_args_list], expected)
                    prepare.assert_called_once_with("unused/5dd")
                    self.assertIn(f"total selected tickers: {len(expected)}", output)
                    self.assertIn(f"additional portfolio tickers: {len(expected) - 4}", output)
                    self.assertTrue(all(c.kwargs["_preflight"] is checked.return_value
                                        for c in analyze.call_args_list))

    def test_changed_target_count_controls_quota_and_diagnostics(self):
        for count in (1, 2, 5):
            with self.subTest(count=count):
                result, analyze, _, _, _, output, _ = self.run_batch(target_count=count)
                self.assertEqual(result, 0)
                self.assertEqual(analyze.call_count, count)
                self.assertIn(f"requested {count}, selected {count}", output)

    def test_shared_tickers_remain_selected_for_both_windows(self):
        for window in ("5", "10"):
            with self.subTest(window=window):
                result, analyze, _, fetch, _, _, _ = self.run_batch(forecast_window=window)
                self.assertEqual(result, 0)
                self.assertEqual([c.args[0] for c in analyze.call_args_list],
                                 ["AAAA", "BBBB", "CCCC", "DDDD"])
                self.assertEqual(fetch.call_args_list, [
                    call(f"https://data.example.test/analytics/daily_recommendations?rolling_window={window}dd", 30.),
                    call(f"https://organizer.example.test/stocks?trading_window={window}dd", 30.),
                ])

    def test_shortages_never_cleanup_or_analyze_even_with_holdings(self):
        for payload, available in ((recommendations(), 0),
                                   (recommendations(("aaaa", 1), (" AAAA ", 2)), 1)):
            with self.subTest(available=available):
                result, analyze, prepare, _, _, _, error = self.run_batch(
                    payload=payload, stocks=["BBBB", "CCCC", "DDDD", "EEEE"])
                self.assertEqual(result, 1)
                self.assertIn(f"requested 4 unique ML tickers, available {available}", error)
                analyze.assert_not_called()
                prepare.assert_not_called()

    def test_bad_portfolio_and_retrieval_failures_preserve_reports(self):
        for stocks in ({}, {"stocks": None}, [None], [""],
                       [{"ticker": "AAAA", "trading_window": "10dd"}]):
            with self.subTest(stocks=stocks):
                result, analyze, prepare, *_ = self.run_batch(stocks=stocks)
                self.assertEqual(result, 1)
                analyze.assert_not_called()
                prepare.assert_not_called()
        for failure in ([RuntimeError("recommendations unavailable")],
                        [self.candidates, RuntimeError("portfolio unavailable")]):
            with self.subTest(failure=failure):
                result, analyze, prepare, *_ = self.run_batch(fetch_error=failure)
                self.assertEqual(result, 1)
                analyze.assert_not_called()
                prepare.assert_not_called()

    def test_preflight_failure_prevents_fetch_cleanup_and_analysis(self):
        result, analyze, prepare, fetch, *_ = self.run_batch(preflight_error=RuntimeError("preflight failed"))
        self.assertEqual(result, 1)
        analyze.assert_not_called()
        prepare.assert_not_called()
        fetch.assert_not_called()

    def test_failed_ticker_does_not_stop_batch_or_return_success(self):
        result, analyze, _, _, _, _, error = self.run_batch(stocks=["FFFF"], outcomes=[1, 0, 0, 0, 0])
        self.assertEqual(result, 1)
        self.assertEqual([c.args[0] for c in analyze.call_args_list], ["AAAA", "BBBB", "CCCC", "DDDD", "FFFF"])
        self.assertIn("Analysis failed for: AAAA", error)
        self.assertTrue(all(c.kwargs["forecast_type"] == "5dd" for c in analyze.call_args_list))
        self.assertIs(analyze.call_args_list[0].kwargs["technical_config"],
                      analyze.call_args_list[-1].kwargs["technical_config"])

    def test_bad_client_configuration_fails_before_network_or_directory_cleanup(self):
        with patch.dict(os.environ, {"TECHNICAL_API_TIMEOUT_SECONDS": "nan"}, clear=True), patch.object(
            runner, "load_env"
        ), patch.object(runner, "fetch_json") as fetch, patch.object(runner, "prepare_output_dir") as prepare:
            self.assertEqual(runner.main("5"), 1)
        fetch.assert_not_called()
        prepare.assert_not_called()


if __name__ == "__main__":
    unittest.main()
