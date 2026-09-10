from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class QuotaStatus(BaseModel):
    """Validated quota state returned by the Organizer API."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    allowed: bool
    remaining: int = Field(ge=0)
    daily_limit: int = Field(ge=0)
    resets_at: datetime

    @field_validator("resets_at")
    @classmethod
    def resets_at_must_include_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("resets_at must include a timezone")
        return value


class ChatQuotaConsumeRequest(BaseModel):
    """Completed chat turn submitted atomically to the Organizer API."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    query: str = Field(min_length=1, max_length=10_000)
    answer: str = Field(min_length=1, max_length=100_000)
    client_message_id: UUID


class PersistedChatMessage(BaseModel):
    """Authoritative message stored by the Organizer API."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    id: UUID
    client_message_id: UUID | None
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=100_000)
    created_at: datetime

    @field_validator("created_at")
    @classmethod
    def created_at_must_include_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("created_at must include a timezone")
        return value

    @model_validator(mode="after")
    def user_message_must_fit_query_limit(self) -> "PersistedChatMessage":
        if self.role == "user" and len(self.content) > 10_000:
            raise ValueError("user message must not exceed 10000 characters")
        return self


class ChatQuotaConsumeResponse(BaseModel):
    """Atomic chat persistence and quota result returned by Organizer."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    conversation_id: UUID
    messages: tuple[PersistedChatMessage, PersistedChatMessage]
    quota: QuotaStatus

    @model_validator(mode="after")
    def messages_must_be_an_authoritative_pair(self) -> "ChatQuotaConsumeResponse":
        user_message, assistant_message = self.messages
        if user_message.role != "user" or assistant_message.role != "assistant":
            raise ValueError("messages must be ordered user then assistant")
        if not self.quota.allowed:
            raise ValueError("successful consume response must be allowed")
        return self
