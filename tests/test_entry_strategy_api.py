import tempfile
import unittest
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.controllers.entry_strategy_controller import EntryStrategyController
from app.repositories.entry_strategy_repository import EntryStrategyRepository
from app.routers.entry_strategy_router import (
    get_entry_strategy_controller,
    router,
)
from app.services.entry_strategy_service import EntryStrategyService


class EntryStrategyApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        results_directory = Path(self.temporary_directory.name)
        window_directory = results_directory / "5dd"
        window_directory.mkdir()
        (window_directory / "BBCA.md").write_text(
            "# BBCA entry strategy",
            encoding="utf-8",
        )

        controller = EntryStrategyController(
            EntryStrategyService(EntryStrategyRepository(results_directory))
        )
        app = FastAPI()
        app.include_router(router)
        app.dependency_overrides[get_entry_strategy_controller] = lambda: controller
        self.client = TestClient(app)

    def tearDown(self) -> None:
        self.client.close()
        self.temporary_directory.cleanup()

    def test_lists_entry_strategy_tickers(self) -> None:
        response = self.client.get(
            "/entry_strategy",
            params={"rolling_window": "5dd"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"tickers": ["BBCA"]})

    def test_gets_entry_strategy_report(self) -> None:
        response = self.client.get(
            "/entry_strategy/report",
            params={"ticker": "bbca", "rolling_window": "5dd"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"ticker": "BBCA", "report": "# BBCA entry strategy"},
        )

    def test_returns_404_for_missing_report(self) -> None:
        response = self.client.get(
            "/entry_strategy/report",
            params={"ticker": "TLKM", "rolling_window": "5dd"},
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn("TLKM", response.json()["detail"])

    def test_rejects_invalid_window_and_ticker(self) -> None:
        invalid_window = self.client.get(
            "/entry_strategy",
            params={"rolling_window": "20dd"},
        )
        invalid_ticker = self.client.get(
            "/entry_strategy/report",
            params={"ticker": "../BBCA", "rolling_window": "5dd"},
        )

        self.assertEqual(invalid_window.status_code, 422)
        self.assertEqual(invalid_ticker.status_code, 400)


if __name__ == "__main__":
    unittest.main()

