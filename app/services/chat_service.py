from typing import Protocol

from app.errors import InvalidChatMessageError, QuotaExceededError
from app.models.chat import ChatResponse
from app.models.quota import QuotaStatus


class QuotaGateway(Protocol):
    async def check(self, authorization: str) -> QuotaStatus: ...

    async def consume(self, authorization: str) -> None: ...


class ChatAgent(Protocol):
    async def run(self, message: str) -> str: ...

    def is_ready(self) -> bool: ...


class ChatService:
    """Orchestrate quota checks, Codex, and quota consumption."""

    def __init__(
        self,
        quota_gateway: QuotaGateway,
        chat_agent: ChatAgent,
        max_message_chars: int,
    ) -> None:
        self._quota_gateway = quota_gateway
        self._chat_agent = chat_agent
        self._max_message_chars = max_message_chars

    async def communicate(
        self,
        message: str,
        authorization: str,
    ) -> ChatResponse:
        normalized_message = message.strip()
        if not normalized_message:
            raise InvalidChatMessageError("Message must not be blank")
        if len(normalized_message) > self._max_message_chars:
            raise InvalidChatMessageError(
                f"Message must not exceed {self._max_message_chars} characters"
            )

        quota = await self._quota_gateway.check(authorization)
        if not quota.allowed:
            raise QuotaExceededError(quota)

        reply = await self._chat_agent.run(normalized_message)
        await self._quota_gateway.consume(authorization)
        return ChatResponse(reply=reply)

    def is_ready(self) -> bool:
        return self._chat_agent.is_ready()
