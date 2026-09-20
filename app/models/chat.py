from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.quota import PersistedChatMessage, QuotaStatus


class ChatRequest(BaseModel):
    """One stateless user message sent to Codex."""

    model_config = ConfigDict(extra="forbid")

    message: str = Field(min_length=1)


class ChatResponse(BaseModel):
    """The final Codex response released after quota consumption."""

    model_config = ConfigDict(frozen=True)

    reply: str
    conversation_id: UUID
    messages: tuple[PersistedChatMessage, PersistedChatMessage]
    quota: QuotaStatus


class HealthResponse(BaseModel):
    """Health state returned by the chat API."""

    model_config = ConfigDict(frozen=True)

    status: Literal["ok", "not_ready"]
