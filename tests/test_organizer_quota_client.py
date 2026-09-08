import unittest

import httpx

from app.clients.organizer_quota_client import OrganizerQuotaClient
from app.errors import (
    OrganizerAuthorizationError,
    QuotaConsumptionRejectedError,
    QuotaServiceUnavailableError,
)


class OrganizerQuotaClientTests(unittest.IsolatedAsyncioTestCase):
    async def test_checks_quota_and_forwards_authorization(self) -> None:
        seen_requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            seen_requests.append(request)
            return httpx.Response(
                200,
                json={
                    "allowed": True,
                    "remaining": 1,
                    "daily_limit": 20,
                    "resets_at": "2026-09-09T00:00:00Z",
                },
            )

        async with httpx.AsyncClient(
            transport=httpx.MockTransport(handler)
        ) as http_client:
            client = OrganizerQuotaClient("http://organizer:8000/", http_client)
            quota = await client.check("Bearer exact-token")

        self.assertTrue(quota.allowed)
        self.assertEqual(quota.remaining, 1)
        self.assertEqual(str(seen_requests[0].url), "http://organizer:8000/chat-quota")
        self.assertEqual(
            seen_requests[0].headers["Authorization"],
            "Bearer exact-token",
        )

    async def test_rejects_invalid_quota_response(self) -> None:
        transport = httpx.MockTransport(
            lambda _: httpx.Response(200, json={"allowed": True})
        )
        async with httpx.AsyncClient(transport=transport) as http_client:
            client = OrganizerQuotaClient("http://organizer:8000", http_client)
            with self.assertRaises(QuotaServiceUnavailableError):
                await client.check("Bearer token")

    async def test_maps_organizer_authorization_failure(self) -> None:
        transport = httpx.MockTransport(lambda _: httpx.Response(401))
        async with httpx.AsyncClient(transport=transport) as http_client:
            client = OrganizerQuotaClient("http://organizer:8000", http_client)
            with self.assertRaises(OrganizerAuthorizationError):
                await client.check("Bearer token")

    async def test_accepts_empty_successful_consume_response(self) -> None:
        seen_requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            seen_requests.append(request)
            return httpx.Response(204)

        async with httpx.AsyncClient(
            transport=httpx.MockTransport(handler)
        ) as http_client:
            client = OrganizerQuotaClient("http://organizer:8000", http_client)
            await client.consume("Bearer token")

        self.assertEqual(seen_requests[0].method, "POST")
        self.assertEqual(
            str(seen_requests[0].url),
            "http://organizer:8000/chat-quota/consume",
        )

    async def test_maps_concurrent_consume_rejection(self) -> None:
        transport = httpx.MockTransport(lambda _: httpx.Response(429))
        async with httpx.AsyncClient(transport=transport) as http_client:
            client = OrganizerQuotaClient("http://organizer:8000", http_client)
            with self.assertRaises(QuotaConsumptionRejectedError):
                await client.consume("Bearer token")

    async def test_maps_success_response_that_reports_disallowed(self) -> None:
        transport = httpx.MockTransport(
            lambda _: httpx.Response(200, json={"allowed": False})
        )
        async with httpx.AsyncClient(transport=transport) as http_client:
            client = OrganizerQuotaClient("http://organizer:8000", http_client)
            with self.assertRaises(QuotaConsumptionRejectedError):
                await client.consume("Bearer token")


if __name__ == "__main__":
    unittest.main()
