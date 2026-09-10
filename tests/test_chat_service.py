import unittest
from datetime import datetime, timezone
from uuid import UUID

from app.errors import (
    CodexExecutionError,
    InvalidChatMessageError,
    QuotaConsumptionRejectedError,
    QuotaExceededError,
)
from app.models.quota import (
    ChatQuotaConsumeResponse,
    PersistedChatMessage,
    QuotaStatus,
)
from app.services.chat_service import ChatService


def quota_status(allowed: bool = True) -> QuotaStatus:
    return QuotaStatus(
        allowed=allowed,
        remaining=1 if allowed else 0,
        daily_limit=20,
        resets_at=datetime(2026, 9, 9, tzinfo=timezone.utc),
    )


CLIENT_MESSAGE_ID = UUID("3fc82b96-3bd6-4b2e-b57d-30cc723ac784")


def consume_response(
    query: str = "Analyze BBCA",
    answer: str = "Codex reply",
) -> ChatQuotaConsumeResponse:
    created_at = datetime(2026, 9, 10, tzinfo=timezone.utc)
    return ChatQuotaConsumeResponse(
        conversation_id=UUID("87033aec-f74c-49ea-8812-37c15c9251e0"),
        messages=(
            PersistedChatMessage(
                id=UUID("d54894fb-dce8-435a-9334-bc2a55571a91"),
                client_message_id=CLIENT_MESSAGE_ID,
                role="user",
                content=query,
                created_at=created_at,
            ),
            PersistedChatMessage(
                id=UUID("48cc11b6-7792-4220-bb29-1b41fd67e781"),
                client_message_id=None,
                role="assistant",
                content=answer,
                created_at=created_at,
            ),
        ),
        quota=quota_status(),
    )


class FakeQuotaGateway:
    def __init__(
        self,
        events: list[str],
        quota: QuotaStatus | None = None,
        consume_error: Exception | None = None,
        persisted: ChatQuotaConsumeResponse | None = None,
    ) -> None:
        self.events = events
        self.quota = quota or quota_status()
        self.consume_error = consume_error
        self.persisted = persisted or consume_response()
        self.consume_arguments: tuple[str, str, UUID] | None = None

    async def check(self, authorization: str) -> QuotaStatus:
        self.events.append(f"check:{authorization}")
        return self.quota

    async def consume(
        self,
        authorization: str,
        query: str,
        answer: str,
        client_message_id: UUID,
    ) -> ChatQuotaConsumeResponse:
        self.events.append(f"consume:{authorization}")
        self.consume_arguments = (query, answer, client_message_id)
        if self.consume_error:
            raise self.consume_error
        persisted = self.persisted.model_copy(
            update={
                "messages": (
                    self.persisted.messages[0].model_copy(
                        update={"client_message_id": client_message_id}
                    ),
                    self.persisted.messages[1],
                )
            }
        )
        return persisted


class FakeChatAgent:
    def __init__(
        self,
        events: list[str],
        reply: str = "Codex reply",
        error: Exception | None = None,
    ) -> None:
        self.events = events
        self.reply = reply
        self.error = error

    async def run(self, message: str) -> str:
        self.events.append(f"codex:{message}")
        if self.error:
            raise self.error
        return self.reply

    def is_ready(self) -> bool:
        return True


class ChatServiceTests(unittest.IsolatedAsyncioTestCase):
    async def test_checks_runs_consumes_then_returns(self) -> None:
        events: list[str] = []
        gateway = FakeQuotaGateway(events)
        service = ChatService(
            gateway,
            FakeChatAgent(events),
            max_message_chars=100,
        )

        response = await service.communicate("  Analyze BBCA  ", "Bearer token")

        self.assertEqual(response.reply, "Codex reply")
        self.assertEqual(response.quota.remaining, 1)
        self.assertEqual(gateway.consume_arguments[:2], ("Analyze BBCA", "Codex reply"))
        self.assertIsInstance(gateway.consume_arguments[2], UUID)
        self.assertEqual(
            events,
            [
                "check:Bearer token",
                "codex:Analyze BBCA",
                "consume:Bearer token",
            ],
        )

    async def test_denied_quota_stops_before_codex(self) -> None:
        events: list[str] = []
        service = ChatService(
            FakeQuotaGateway(events, quota_status(False)),
            FakeChatAgent(events),
            max_message_chars=100,
        )

        with self.assertRaises(QuotaExceededError):
            await service.communicate("Analyze BBCA", "Bearer token")

        self.assertEqual(events, ["check:Bearer token"])

    async def test_codex_failure_does_not_consume_quota(self) -> None:
        events: list[str] = []
        service = ChatService(
            FakeQuotaGateway(events),
            FakeChatAgent(events, error=CodexExecutionError("failed")),
            max_message_chars=100,
        )

        with self.assertRaises(CodexExecutionError):
            await service.communicate("Analyze BBCA", "Bearer token")

        self.assertEqual(
            events,
            ["check:Bearer token", "codex:Analyze BBCA"],
        )

    async def test_consume_rejection_suppresses_response(self) -> None:
        events: list[str] = []
        service = ChatService(
            FakeQuotaGateway(
                events,
                consume_error=QuotaConsumptionRejectedError("race"),
            ),
            FakeChatAgent(events),
            max_message_chars=100,
        )

        with self.assertRaises(QuotaConsumptionRejectedError):
            await service.communicate("Analyze BBCA", "Bearer token")

        self.assertEqual(events[-1], "consume:Bearer token")

    async def test_returns_authoritative_assistant_content(self) -> None:
        events: list[str] = []
        gateway = FakeQuotaGateway(
            events,
            persisted=consume_response(answer="Stored reply"),
        )
        service = ChatService(
            gateway,
            FakeChatAgent(events, reply="Generated reply"),
            max_message_chars=100,
        )

        response = await service.communicate("Analyze BBCA", "Bearer token")

        self.assertEqual(response.reply, "Stored reply")

    async def test_rejects_answer_above_organizer_limit(self) -> None:
        events: list[str] = []
        service = ChatService(
            FakeQuotaGateway(events),
            FakeChatAgent(events, reply="x" * 100_001),
            max_message_chars=100,
        )

        with self.assertRaises(CodexExecutionError):
            await service.communicate("Analyze BBCA", "Bearer token")

        self.assertNotIn("consume:Bearer token", events)

    async def test_rejects_blank_and_oversized_messages_before_quota(self) -> None:
        events: list[str] = []
        service = ChatService(
            FakeQuotaGateway(events),
            FakeChatAgent(events),
            max_message_chars=5,
        )

        with self.assertRaises(InvalidChatMessageError):
            await service.communicate("   ", "Bearer token")
        with self.assertRaises(InvalidChatMessageError):
            await service.communicate("123456", "Bearer token")

        self.assertEqual(events, [])


if __name__ == "__main__":
    unittest.main()
