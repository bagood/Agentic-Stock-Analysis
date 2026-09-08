from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


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
