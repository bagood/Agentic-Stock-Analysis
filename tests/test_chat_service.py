import unittest
from datetime import datetime, timezone

from app.errors import (
    CodexExecutionError,
    InvalidChatMessageError,
    QuotaConsumptionRejectedError,
    QuotaExceededError,
)
from app.models.quota import QuotaStatus
from app.services.chat_service import ChatService


def quota_status(allowed: bool = True) -> QuotaStatus:
    return QuotaStatus(
        allowed=allowed,
        remaining=1 if allowed else 0,
        daily_limit=20,
        resets_at=datetime(2026, 9, 9, tzinfo=timezone.utc),
    )


class FakeQuotaGateway:
    def __init__(
        self,
        events: list[str],
        quota: QuotaStatus | None = None,
        consume_error: Exception | None = None,
    ) -> None:
        self.events = events
        self.quota = quota or quota_status()
        self.consume_error = consume_error

    async def check(self, authorization: str) -> QuotaStatus:
        self.events.append(f"check:{authorization}")
        return self.quota

    async def consume(self, authorization: str) -> None:
        self.events.append(f"consume:{authorization}")
        if self.consume_error:
            raise self.consume_error


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
        service = ChatService(
            FakeQuotaGateway(events),
            FakeChatAgent(events),
            max_message_chars=100,
        )

        response = await service.communicate("  Analyze BBCA  ", "Bearer token")

        self.assertEqual(response.reply, "Codex reply")
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
