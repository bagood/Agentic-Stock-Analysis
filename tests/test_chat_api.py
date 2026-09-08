import sys
import unittest
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.chat_main import create_app
from app.controllers.chat_controller import ChatController
from app.models.quota import QuotaStatus
from app.routers.chat_router import get_chat_controller, router
from app.services.chat_service import ChatService
from app.settings import ChatSettings


class FakeQuotaGateway:
    def __init__(self, allowed: bool = True) -> None:
        self.allowed = allowed
        self.consumed = False

    async def check(self, authorization: str) -> QuotaStatus:
        return QuotaStatus(
            allowed=self.allowed,
            remaining=1 if self.allowed else 0,
            daily_limit=20,
            resets_at=datetime.now(timezone.utc) + timedelta(hours=1),
        )

    async def consume(self, authorization: str) -> None:
        self.consumed = True


class FakeChatAgent:
    async def run(self, message: str) -> str:
        return f"Reply to {message}"

    def is_ready(self) -> bool:
        return True


class ChatApiTests(unittest.TestCase):
    def build_client(
        self, allowed: bool = True
    ) -> tuple[TestClient, FakeQuotaGateway]:
        quota = FakeQuotaGateway(allowed)
        controller = ChatController(
            ChatService(quota, FakeChatAgent(), max_message_chars=100)
        )
        app = FastAPI()
        app.include_router(router)
        app.dependency_overrides[get_chat_controller] = lambda: controller
        return TestClient(app), quota

    def test_returns_reply_after_consuming_quota(self) -> None:
        client, quota = self.build_client()
        with client:
            response = client.post(
                "/chat",
                headers={"Authorization": "Bearer token"},
                json={"message": "Analyze BBCA"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"reply": "Reply to Analyze BBCA"})
        self.assertTrue(quota.consumed)

    def test_requires_bearer_authorization(self) -> None:
        client, _ = self.build_client()
        with client:
            missing = client.post("/chat", json={"message": "Analyze BBCA"})
            malformed = client.post(
                "/chat",
                headers={"Authorization": "Basic token"},
                json={"message": "Analyze BBCA"},
            )

        self.assertEqual(missing.status_code, 401)
        self.assertEqual(malformed.status_code, 401)

    def test_returns_quota_metadata_and_retry_after(self) -> None:
        client, quota = self.build_client(allowed=False)
        with client:
            response = client.post(
                "/chat",
                headers={"Authorization": "Bearer token"},
                json={"message": "Analyze BBCA"},
            )

        self.assertEqual(response.status_code, 429)
        self.assertEqual(response.json()["detail"]["code"], "quota_exhausted")
        self.assertEqual(response.json()["detail"]["remaining"], 0)
        self.assertIn("Retry-After", response.headers)
        self.assertFalse(quota.consumed)

    def test_health_endpoints(self) -> None:
        client, _ = self.build_client()
        with client:
            live = client.get("/health/live")
            ready = client.get("/health/ready")

        self.assertEqual(live.json(), {"status": "ok"})
        self.assertEqual(ready.json(), {"status": "ok"})

    def test_application_factory_initializes_lifespan_dependencies(self) -> None:
        settings = ChatSettings(
            organizer_base_url="http://organizer:8000",
            mcp_url="http://agentic-mcp:8000/mcp",
            codex_executable=sys.executable,
            codex_timeout_seconds=1,
            organizer_timeout_seconds=1,
            max_concurrency=1,
            max_message_chars=100,
            max_response_bytes=1000,
        )

        with TestClient(create_app(settings)) as client:
            response = client.get("/health/ready")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})


if __name__ == "__main__":
    unittest.main()
