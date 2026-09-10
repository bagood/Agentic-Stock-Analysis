import sys
import unittest
from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.chat_main import create_app
from app.controllers.chat_controller import ChatController
from app.errors import (
    ChatPersistenceRejectedError,
    QuotaConsumptionRejectedError,
    QuotaServiceUnavailableError,
)
from app.models.quota import (
    ChatQuotaConsumeResponse,
    PersistedChatMessage,
    QuotaStatus,
)
from app.routers.chat_router import get_chat_controller, router
from app.services.chat_service import ChatService
from app.settings import ChatSettings


class FakeQuotaGateway:
    def __init__(
        self,
        allowed: bool = True,
        consume_error: Exception | None = None,
    ) -> None:
        self.allowed = allowed
        self.consumed = False
        self.consume_error = consume_error

    async def check(self, authorization: str) -> QuotaStatus:
        return QuotaStatus(
            allowed=self.allowed,
            remaining=1 if self.allowed else 0,
            daily_limit=20,
            resets_at=datetime.now(timezone.utc) + timedelta(hours=1),
        )

    async def consume(
        self,
        authorization: str,
        query: str,
        answer: str,
        client_message_id: UUID,
    ) -> ChatQuotaConsumeResponse:
        self.consumed = True
        if self.consume_error is not None:
            raise self.consume_error
        jakarta = timezone(timedelta(hours=7))
        created_at = datetime(2026, 9, 10, 9, 14, 22, tzinfo=jakarta)
        return ChatQuotaConsumeResponse(
            conversation_id=UUID("87033aec-f74c-49ea-8812-37c15c9251e0"),
            messages=(
                PersistedChatMessage(
                    id=UUID("d54894fb-dce8-435a-9334-bc2a55571a91"),
                    client_message_id=client_message_id,
                    role="user",
                    content=query,
                    created_at=created_at,
                ),
                PersistedChatMessage(
                    id=UUID("48cc11b6-7792-4220-bb29-1b41fd67e781"),
                    client_message_id=None,
                    role="assistant",
                    content=answer,
                    created_at=created_at + timedelta(seconds=7),
                ),
            ),
            quota=QuotaStatus(
                allowed=True,
                remaining=4,
                daily_limit=5,
                resets_at=datetime(2026, 9, 11, tzinfo=jakarta),
            ),
        )


class FakeChatAgent:
    async def run(self, message: str) -> str:
        return f"Reply to {message}"

    def is_ready(self) -> bool:
        return True


class ChatApiTests(unittest.TestCase):
    def build_client(
        self,
        allowed: bool = True,
        consume_error: Exception | None = None,
    ) -> tuple[TestClient, FakeQuotaGateway]:
        quota = FakeQuotaGateway(allowed, consume_error)
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
        body = response.json()
        self.assertEqual(body["reply"], "Reply to Analyze BBCA")
        self.assertEqual(
            body["conversation_id"],
            "87033aec-f74c-49ea-8812-37c15c9251e0",
        )
        self.assertEqual(
            [message["role"] for message in body["messages"]], ["user", "assistant"]
        )
        self.assertEqual(body["quota"]["remaining"], 4)
        self.assertTrue(body["quota"]["resets_at"].endswith("+07:00"))
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

    def test_returns_consume_time_quota_metadata(self) -> None:
        exhausted = QuotaStatus(
            allowed=False,
            remaining=0,
            daily_limit=5,
            resets_at=datetime.now(timezone.utc) + timedelta(hours=1),
        )
        client, quota = self.build_client(
            consume_error=QuotaConsumptionRejectedError(
                "race",
                quota=exhausted,
                retry_after="3600",
            )
        )

        with client:
            response = client.post(
                "/chat",
                headers={"Authorization": "Bearer token"},
                json={"message": "Analyze BBCA"},
            )

        self.assertEqual(response.status_code, 429)
        self.assertEqual(response.json()["detail"]["daily_limit"], 5)
        self.assertEqual(response.headers["Retry-After"], "3600")
        self.assertTrue(quota.consumed)

    def test_maps_consume_payload_rejection_to_bad_gateway(self) -> None:
        client, _ = self.build_client(
            consume_error=ChatPersistenceRejectedError("invalid payload")
        )

        with client:
            response = client.post(
                "/chat",
                headers={"Authorization": "Bearer token"},
                json={"message": "Analyze BBCA"},
            )

        self.assertEqual(response.status_code, 502)

    def test_maps_chat_history_outage_to_service_unavailable(self) -> None:
        client, _ = self.build_client(
            consume_error=QuotaServiceUnavailableError(
                "Chat history is temporarily unavailable",
                error_code="CHAT_HISTORY_UNAVAILABLE",
            )
        )

        with client:
            response = client.post(
                "/chat",
                headers={"Authorization": "Bearer token"},
                json={"message": "Analyze BBCA"},
            )

        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.json()["detail"]["error_code"],
            "CHAT_HISTORY_UNAVAILABLE",
        )

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
