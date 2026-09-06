import tempfile
import unittest
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.controllers.portfolio_controller import PortfolioController
from app.repositories.portfolio_repository import PortfolioRepository
from app.routers.portfolio_router import get_portfolio_controller, router
from app.services.portfolio_service import PortfolioService


class PortfolioApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        csv_path = Path(self.temporary_directory.name) / "portfolio.csv"
        controller = PortfolioController(
            PortfolioService(PortfolioRepository(csv_path))
        )

        app = FastAPI()
        app.include_router(router)
        app.dependency_overrides[get_portfolio_controller] = lambda: controller
        self.client = TestClient(app)

    def tearDown(self) -> None:
        self.client.close()
        self.temporary_directory.cleanup()

    def test_add_list_update_and_delete_portfolio_position(self) -> None:
        position = {
            "ticker": "bbca",
            "price": "9250.50",
            "rolling_window": "5dd",
        }
        response = self.client.post("/portfolio", json=position)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            "action": "added",
            "position": {
                "ticker": "BBCA",
                "price": "9250.50",
                "rolling_window": "5dd",
            },
        })

        response = self.client.get("/portfolio")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["positions"][0]["ticker"], "BBCA")

        position["price"] = "9300"
        response = self.client.put("/portfolio", json=position)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["action"], "updated")
        self.assertEqual(response.json()["position"]["price"], "9300")

        response = self.client.delete(
            "/portfolio",
            params={"ticker": "bbca", "rolling_window": "5dd"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["action"], "deleted")
        self.assertEqual(self.client.get("/portfolio").json(), {"positions": []})

    def test_returns_useful_status_codes_for_domain_errors(self) -> None:
        position = {
            "ticker": "AAPL",
            "price": 100,
            "rolling_window": "10dd",
        }
        self.assertEqual(self.client.post("/portfolio", json=position).status_code, 201)
        self.assertEqual(self.client.post("/portfolio", json=position).status_code, 409)

        missing = {**position, "ticker": "MSFT"}
        self.assertEqual(self.client.put("/portfolio", json=missing).status_code, 404)
        self.assertEqual(
            self.client.delete(
                "/portfolio",
                params={"ticker": "MSFT", "rolling_window": "10dd"},
            ).status_code,
            404,
        )

        invalid_price = {**position, "ticker": "MSFT", "price": 0}
        self.assertEqual(
            self.client.post("/portfolio", json=invalid_price).status_code,
            400,
        )
