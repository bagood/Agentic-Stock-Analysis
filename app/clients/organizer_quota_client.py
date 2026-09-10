import asyncio
from uuid import UUID

import httpx
from pydantic import ValidationError

from app.errors import (
    ChatPersistenceRejectedError,
    OrganizerAuthorizationError,
    QuotaConsumptionRejectedError,
    QuotaServiceUnavailableError,
)
from app.models.quota import (
    ChatQuotaConsumeRequest,
    ChatQuotaConsumeResponse,
    QuotaStatus,
)

RETRYABLE_STATUS_CODES = {500, 502, 503, 504}


class OrganizerQuotaClient:
    """Check and consume chat quota through the Organizer API."""

    def __init__(
        self,
        base_url: str,
        client: httpx.AsyncClient,
        retry_attempts: int = 3,
        retry_backoff_seconds: float = 0.1,
    ) -> None:
        if retry_attempts <= 0:
            raise ValueError("retry_attempts must be greater than zero")
        if retry_backoff_seconds <= 0:
            raise ValueError("retry_backoff_seconds must be greater than zero")
        self._base_url = base_url.rstrip("/")
        self._client = client
        self._retry_attempts = retry_attempts
        self._retry_backoff_seconds = retry_backoff_seconds

    async def check(self, authorization: str) -> QuotaStatus:
        response = await self._request("GET", "/chat-quota", authorization)
        if response.status_code in {401, 403}:
            raise OrganizerAuthorizationError(response.status_code)
        if response.status_code != 200:
            raise QuotaServiceUnavailableError("Unable to check chat quota")

        try:
            return QuotaStatus.model_validate(response.json())
        except (ValueError, ValidationError) as exc:
            raise QuotaServiceUnavailableError(
                "Organizer returned an invalid quota response"
            ) from exc

    async def consume(
        self,
        authorization: str,
        query: str,
        answer: str,
        client_message_id: UUID,
    ) -> ChatQuotaConsumeResponse:
        payload = ChatQuotaConsumeRequest(
            query=query,
            answer=answer,
            client_message_id=client_message_id,
        )
        response = await self._consume_request(authorization, payload)
        if response.status_code in {401, 403}:
            raise OrganizerAuthorizationError(response.status_code)
        if response.status_code in {409, 429}:
            raise QuotaConsumptionRejectedError(
                "Chat quota was exhausted before it could be consumed",
                quota=self._rejected_quota(response),
                retry_after=response.headers.get("Retry-After"),
            )
        if response.status_code == 422:
            raise ChatPersistenceRejectedError(
                "Organizer rejected the completed chat payload"
            )
        if response.status_code != 200:
            if response.status_code == 503:
                error_code = self._error_code(response)
                if error_code == "CHAT_HISTORY_UNAVAILABLE":
                    raise QuotaServiceUnavailableError(
                        "Chat history is temporarily unavailable",
                        error_code=error_code,
                    )
            raise QuotaServiceUnavailableError("Unable to consume chat quota")

        try:
            result = ChatQuotaConsumeResponse.model_validate(response.json())
        except (ValueError, ValidationError) as exc:
            raise QuotaServiceUnavailableError(
                "Organizer returned an invalid consume response"
            ) from exc
        if result.messages[0].client_message_id != client_message_id:
            raise QuotaServiceUnavailableError(
                "Organizer returned a mismatched client message ID"
            )
        return result

    async def _consume_request(
        self,
        authorization: str,
        payload: ChatQuotaConsumeRequest,
    ) -> httpx.Response:
        for attempt in range(self._retry_attempts):
            try:
                response = await self._client.post(
                    f"{self._base_url}/chat-quota/consume",
                    headers={"Authorization": authorization},
                    json=payload.model_dump(mode="json"),
                )
            except httpx.RequestError as exc:
                if attempt + 1 == self._retry_attempts:
                    raise QuotaServiceUnavailableError(
                        "Organizer quota service is unavailable"
                    ) from exc
            else:
                if response.status_code not in RETRYABLE_STATUS_CODES:
                    return response
                if attempt + 1 == self._retry_attempts:
                    return response

            await asyncio.sleep(self._retry_backoff_seconds * (2**attempt))

        raise AssertionError("consume retry loop did not return")

    @staticmethod
    def _rejected_quota(response: httpx.Response) -> QuotaStatus | None:
        try:
            detail = response.json().get("detail")
            if not isinstance(detail, dict):
                return None
            return QuotaStatus.model_validate({"allowed": False, **detail})
        except (AttributeError, ValueError, ValidationError):
            return None

    @staticmethod
    def _error_code(response: httpx.Response) -> str | None:
        try:
            detail = response.json().get("detail")
        except (AttributeError, ValueError):
            return None
        if not isinstance(detail, dict):
            return None
        error_code = detail.get("error_code")
        return error_code if isinstance(error_code, str) else None

    async def _request(
        self,
        method: str,
        path: str,
        authorization: str,
    ) -> httpx.Response:
        try:
            return await self._client.request(
                method,
                f"{self._base_url}{path}",
                headers={"Authorization": authorization},
            )
        except httpx.RequestError as exc:
            raise QuotaServiceUnavailableError(
                "Organizer quota service is unavailable"
            ) from exc
