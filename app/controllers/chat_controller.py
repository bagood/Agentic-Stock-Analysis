import math
from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.errors import (
    CodexExecutionError,
    CodexTimeoutError,
    InvalidChatMessageError,
    OrganizerAuthorizationError,
    QuotaConsumptionRejectedError,
    QuotaExceededError,
    QuotaServiceUnavailableError,
)
from app.models.chat import ChatResponse
from app.services.chat_service import ChatService


class ChatController:
    """Translate chat-domain outcomes into HTTP responses."""

    def __init__(self, service: ChatService) -> None:
        self._service = service

    async def communicate(
        self,
        message: str,
        authorization: str | None,
    ) -> ChatResponse:
        bearer_header = self._bearer_header(authorization)
        try:
            return await self._service.communicate(message, bearer_header)
        except InvalidChatMessageError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(exc),
            ) from exc
        except QuotaExceededError as exc:
            detail = {
                "code": "quota_exhausted",
                **exc.quota.model_dump(mode="json"),
            }
            headers: dict[str, str] = {}
            seconds = math.ceil(
                (exc.quota.resets_at - datetime.now(timezone.utc)).total_seconds()
            )
            if seconds > 0:
                headers["Retry-After"] = str(seconds)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=detail,
                headers=headers,
            ) from exc
        except OrganizerAuthorizationError as exc:
            raise HTTPException(
                status_code=exc.status_code,
                detail="Organizer rejected the authorization token",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc
        except QuotaConsumptionRejectedError as exc:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={"code": "quota_exhausted"},
            ) from exc
        except QuotaServiceUnavailableError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Chat quota service is unavailable",
            ) from exc
        except CodexTimeoutError as exc:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Codex execution timed out",
            ) from exc
        except CodexExecutionError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Codex could not produce a response",
            ) from exc

    def is_ready(self) -> bool:
        return self._service.is_ready()

    @staticmethod
    def _bearer_header(authorization: str | None) -> str:
        if authorization is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Bearer authorization is required",
                headers={"WWW-Authenticate": "Bearer"},
            )

        value = authorization.strip()
        scheme, separator, credentials = value.partition(" ")
        if (
            not separator
            or scheme.lower() != "bearer"
            or not credentials
            or any(character.isspace() for character in credentials)
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Bearer authorization is required",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return value
