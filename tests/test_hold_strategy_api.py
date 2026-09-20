import tempfile
import unittest
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.controllers.hold_strategy_controller import HoldStrategyController
from app.repositories.hold_strategy_repository import HoldStrategyRepository
from app.routers.hold_strategy_router import get_hold_strategy_controller, router
from app.services.hold_strategy_service import HoldStrategyService


class HoldStrategyApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        results_directory = Path(self.temporary_directory.name)
        window_directory = results_directory / "10dd"
        window_directory.mkdir()
        (window_directory / "INDY.md").write_text(
            "# INDY hold strategy",
            encoding="utf-8",
        )

        controller = HoldStrategyController(
            HoldStrategyService(HoldStrategyRepository(results_directory))
        )
        app = FastAPI()
        app.include_router(router)
        app.dependency_overrides[get_hold_strategy_controller] = lambda: controller
        self.client = TestClient(app)

    def tearDown(self) -> None:
        self.client.close()
        self.temporary_directory.cleanup()

    def test_lists_hold_strategy_tickers(self) -> None:
        response = self.client.get(
            "/hold_strategy",
            params={"rolling_window": "10dd"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"tickers": ["INDY"]})

    def test_gets_hold_strategy_report(self) -> None:
        response = self.client.get(
            "/hold_strategy/report",
            params={"ticker": "indy", "rolling_window": "10dd"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"ticker": "INDY", "report": "# INDY hold strategy"},
        )

    def test_returns_404_for_missing_report(self) -> None:
        response = self.client.get(
            "/hold_strategy/report",
            params={"ticker": "BBCA", "rolling_window": "10dd"},
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn("BBCA", response.json()["detail"])

    def test_rejects_invalid_window_and_ticker(self) -> None:
        invalid_window = self.client.get(
            "/hold_strategy",
            params={"rolling_window": "20dd"},
        )
        invalid_ticker = self.client.get(
            "/hold_strategy/report",
            params={"ticker": "../INDY", "rolling_window": "10dd"},
        )

        self.assertEqual(invalid_window.status_code, 422)
        self.assertEqual(invalid_ticker.status_code, 400)


if __name__ == "__main__":
    unittest.main()

