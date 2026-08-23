import unittest

from detailedAnalysis.helper import (
    build_api_url,
    build_prompt,
    build_technical_url,
)


class ApiUrlTests(unittest.TestCase):
    def test_builds_recommendation_url_for_each_rolling_window(self) -> None:
        for rolling_window in ("5dd", "10dd"):
            with self.subTest(rolling_window=rolling_window):
                url = build_api_url(
                    "https://data.example.test/api/",
                    "analytics/daily_recommendations",
                    [("rolling_window", rolling_window)],
                )
                self.assertEqual(
                    url,
                    "https://data.example.test/api/analytics/"
                    f"daily_recommendations?rolling_window={rolling_window}",
                )

    def test_preserves_base_query_parameters(self) -> None:
        url = build_api_url(
            "https://data.example.test/root?market=idx",
            "/technical",
            [("ticker", "BBCA")],
        )

        self.assertEqual(
            url,
            "https://data.example.test/root/technical?market=idx&ticker=BBCA",
        )

    def test_builds_technical_url_without_double_slashes(self) -> None:
        self.assertEqual(
            build_technical_url("http://localhost:8000/", "TLKM"),
            "http://localhost:8000/technical?ticker=TLKM",
        )

    def test_rejects_non_http_base_url(self) -> None:
        with self.assertRaisesRegex(ValueError, "absolute HTTP or HTTPS"):
            build_api_url("localhost:8000", "technical")


class PromptTests(unittest.TestCase):
    def test_uses_selected_trading_day_horizon(self) -> None:
        for horizon in ("5–10 trading days", "10–20 trading days"):
            with self.subTest(horizon=horizon):
                prompt = build_prompt("Instructions", "[]", "BBCA", horizon)
                self.assertIn(f"over the next {horizon}", prompt)
                self.assertNotIn("calendar days", prompt)


if __name__ == "__main__":
    unittest.main()
