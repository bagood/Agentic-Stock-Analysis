from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    """One stateless user message sent to Codex."""

    model_config = ConfigDict(extra="forbid")

    message: str = Field(min_length=1)


class ChatResponse(BaseModel):
    """The final Codex response released after quota consumption."""

    model_config = ConfigDict(frozen=True)

    reply: str


class HealthResponse(BaseModel):
    """Health state returned by the chat API."""

    model_config = ConfigDict(frozen=True)

    status: Literal["ok", "not_ready"]
