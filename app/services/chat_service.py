from typing import Protocol
from uuid import UUID, uuid4

from app.errors import CodexExecutionError, InvalidChatMessageError, QuotaExceededError
from app.models.chat import ChatResponse
from app.models.quota import ChatQuotaConsumeResponse, QuotaStatus


class QuotaGateway(Protocol):
    async def check(self, authorization: str) -> QuotaStatus: ...

    async def consume(
        self,
        authorization: str,
        query: str,
        answer: str,
        client_message_id: UUID,
    ) -> ChatQuotaConsumeResponse: ...


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
        maximum_query_chars = min(self._max_message_chars, 10_000)
        if len(normalized_message) > maximum_query_chars:
            raise InvalidChatMessageError(
                f"Message must not exceed {maximum_query_chars} characters"
            )

        client_message_id = uuid4()
        quota = await self._quota_gateway.check(authorization)
        if not quota.allowed:
            raise QuotaExceededError(quota)

        reply = await self._chat_agent.run(normalized_message)
        if len(reply) > 100_000:
            raise CodexExecutionError(
                "Codex response exceeded the Organizer persistence limit"
            )
        result = await self._quota_gateway.consume(
            authorization,
            normalized_message,
            reply,
            client_message_id,
        )
        authoritative_reply = result.messages[1].content
        return ChatResponse(
            reply=authoritative_reply,
            conversation_id=result.conversation_id,
            messages=result.messages,
            quota=result.quota,
        )

    def is_ready(self) -> bool:
        return self._chat_agent.is_ready()
