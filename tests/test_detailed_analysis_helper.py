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
            build_technical_url("http://localhost:8000/", "TLKM", "5dd"),
            "http://localhost:8000/technical/?ticker=TLKM&forecast_type=5dd",
        )

    def test_technical_identity_cannot_be_duplicated_in_base_url(self) -> None:
        for query in ("ticker=BBCA", "forecast_type=10dd", "%74icker=BBCA"):
            with self.assertRaises(ValueError):
                build_technical_url(f"https://data.example.test?{query}", "AALI", "5dd")

    def test_technical_base_url_must_not_embed_credentials(self) -> None:
        with self.assertRaises(ValueError):
            build_technical_url("https://user:secret@data.example.test", "AALI", "5dd")

    def test_technical_url_retains_base_path_and_unrelated_query(self) -> None:
        self.assertEqual(
            build_technical_url("https://data.example.test/api/?market=idx", " aali ", "10dd"),
            "https://data.example.test/api/technical/?market=idx&ticker=AALI&forecast_type=10dd",
        )

    def test_rejects_non_http_base_url(self) -> None:
        with self.assertRaisesRegex(ValueError, "absolute HTTP or HTTPS"):
            build_api_url("localhost:8000", "technical")


class PromptTests(unittest.TestCase):
    def test_uses_selected_trading_day_horizon(self) -> None:
        for horizon in ("5 trading sessions", "10 trading sessions"):
            with self.subTest(horizon=horizon):
                prompt = build_prompt("Instructions", "[]", "BBCA", horizon)
                self.assertIn(f"over the next {horizon}", prompt)
                self.assertNotIn("calendar days", prompt)


if __name__ == "__main__":
    unittest.main()
