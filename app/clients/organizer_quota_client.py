import httpx
from pydantic import ValidationError

from app.errors import (
    OrganizerAuthorizationError,
    QuotaConsumptionRejectedError,
    QuotaServiceUnavailableError,
)
from app.models.quota import QuotaStatus


class OrganizerQuotaClient:
    """Check and consume chat quota through the Organizer API."""

    def __init__(self, base_url: str, client: httpx.AsyncClient) -> None:
        self._base_url = base_url.rstrip("/")
        self._client = client

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

    async def consume(self, authorization: str) -> None:
        response = await self._request(
            "POST", "/chat-quota/consume", authorization
        )
        if response.status_code in {401, 403}:
            raise OrganizerAuthorizationError(response.status_code)
        if response.status_code in {409, 429}:
            raise QuotaConsumptionRejectedError(
                "Chat quota was exhausted before it could be consumed"
            )
        if response.status_code < 200 or response.status_code >= 300:
            raise QuotaServiceUnavailableError("Unable to consume chat quota")
        if response.content:
            try:
                response_data = response.json()
            except ValueError:
                return
            if (
                isinstance(response_data, dict)
                and response_data.get("allowed") is False
            ):
                raise QuotaConsumptionRejectedError(
                    "Chat quota was exhausted before it could be consumed"
                )

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
