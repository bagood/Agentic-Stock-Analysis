import unittest
from uuid import UUID

import httpx

from app.clients.organizer_quota_client import OrganizerQuotaClient
from app.errors import (
    ChatPersistenceRejectedError,
    OrganizerAuthorizationError,
    QuotaConsumptionRejectedError,
    QuotaServiceUnavailableError,
)

CLIENT_MESSAGE_ID = UUID("3fc82b96-3bd6-4b2e-b57d-30cc723ac784")


def consume_response() -> dict:
    return {
        "conversation_id": "87033aec-f74c-49ea-8812-37c15c9251e0",
        "messages": [
            {
                "id": "d54894fb-dce8-435a-9334-bc2a55571a91",
                "client_message_id": str(CLIENT_MESSAGE_ID),
                "role": "user",
                "content": "Analyze BBCA",
                "created_at": "2026-09-10T09:14:22+07:00",
            },
            {
                "id": "48cc11b6-7792-4220-bb29-1b41fd67e781",
                "client_message_id": None,
                "role": "assistant",
                "content": "Codex reply",
                "created_at": "2026-09-10T09:14:29+07:00",
            },
        ],
        "quota": {
            "allowed": True,
            "remaining": 4,
            "daily_limit": 5,
            "resets_at": "2026-09-11T00:00:00+07:00",
        },
    }


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

    async def test_consumes_with_completed_turn_and_parses_response(self) -> None:
        seen_requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            seen_requests.append(request)
            return httpx.Response(200, json=consume_response())

        async with httpx.AsyncClient(
            transport=httpx.MockTransport(handler)
        ) as http_client:
            client = OrganizerQuotaClient("http://organizer:8000", http_client)
            result = await client.consume(
                "Bearer token",
                "Analyze BBCA",
                "Codex reply",
                CLIENT_MESSAGE_ID,
            )

        self.assertEqual(seen_requests[0].method, "POST")
        self.assertEqual(
            str(seen_requests[0].url),
            "http://organizer:8000/chat-quota/consume",
        )
        self.assertEqual(seen_requests[0].headers["Authorization"], "Bearer token")
        self.assertEqual(seen_requests[0].headers["Content-Type"], "application/json")
        self.assertEqual(
            seen_requests[0].read().decode(),
            (
                '{"query":"Analyze BBCA","answer":"Codex reply",'
                '"client_message_id":"3fc82b96-3bd6-4b2e-b57d-30cc723ac784"}'
            ),
        )
        self.assertEqual(result.quota.remaining, 4)
        self.assertEqual(result.messages[1].content, "Codex reply")

    async def test_maps_concurrent_consume_rejection(self) -> None:
        transport = httpx.MockTransport(
            lambda _: httpx.Response(
                429,
                headers={"Retry-After": "120"},
                json={
                    "detail": {
                        "message": "Daily chat limit reached",
                        "remaining": 0,
                        "daily_limit": 5,
                        "resets_at": "2026-09-11T00:00:00+07:00",
                    }
                },
            )
        )
        async with httpx.AsyncClient(transport=transport) as http_client:
            client = OrganizerQuotaClient("http://organizer:8000", http_client)
            with self.assertRaises(QuotaConsumptionRejectedError) as caught:
                await client.consume(
                    "Bearer token",
                    "Analyze BBCA",
                    "Codex reply",
                    CLIENT_MESSAGE_ID,
                )

        self.assertEqual(caught.exception.quota.remaining, 0)
        self.assertEqual(caught.exception.retry_after, "120")

    async def test_rejects_invalid_success_response(self) -> None:
        transport = httpx.MockTransport(
            lambda _: httpx.Response(200, json={"quota": {"allowed": True}})
        )
        async with httpx.AsyncClient(transport=transport) as http_client:
            client = OrganizerQuotaClient("http://organizer:8000", http_client)
            with self.assertRaises(QuotaServiceUnavailableError):
                await client.consume(
                    "Bearer token",
                    "Analyze BBCA",
                    "Codex reply",
                    CLIENT_MESSAGE_ID,
                )

    async def test_does_not_retry_payload_rejection(self) -> None:
        requests = 0

        def handler(_: httpx.Request) -> httpx.Response:
            nonlocal requests
            requests += 1
            return httpx.Response(422)

        async with httpx.AsyncClient(
            transport=httpx.MockTransport(handler)
        ) as http_client:
            client = OrganizerQuotaClient("http://organizer:8000", http_client)
            with self.assertRaises(ChatPersistenceRejectedError):
                await client.consume(
                    "Bearer token",
                    "Analyze BBCA",
                    "Codex reply",
                    CLIENT_MESSAGE_ID,
                )

        self.assertEqual(requests, 1)

    async def test_retries_server_errors_with_the_same_payload(self) -> None:
        requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            if len(requests) < 3:
                return httpx.Response(503)
            return httpx.Response(200, json=consume_response())

        async with httpx.AsyncClient(
            transport=httpx.MockTransport(handler)
        ) as http_client:
            client = OrganizerQuotaClient(
                "http://organizer:8000",
                http_client,
                retry_attempts=3,
                retry_backoff_seconds=0.001,
            )
            await client.consume(
                "Bearer token",
                "Analyze BBCA",
                "Codex reply",
                CLIENT_MESSAGE_ID,
            )

        self.assertEqual(len(requests), 3)
        self.assertEqual(
            {request.read() for request in requests},
            {requests[0].read()},
        )

    async def test_maps_chat_history_unavailable_after_retries(self) -> None:
        transport = httpx.MockTransport(
            lambda _: httpx.Response(
                503,
                json={
                    "detail": {
                        "message": "Chat history is temporarily unavailable",
                        "error_code": "CHAT_HISTORY_UNAVAILABLE",
                    }
                },
            )
        )
        async with httpx.AsyncClient(transport=transport) as http_client:
            client = OrganizerQuotaClient(
                "http://organizer:8000",
                http_client,
                retry_attempts=1,
            )
            with self.assertRaises(QuotaServiceUnavailableError) as caught:
                await client.consume(
                    "Bearer token",
                    "Analyze BBCA",
                    "Codex reply",
                    CLIENT_MESSAGE_ID,
                )

        self.assertEqual(caught.exception.error_code, "CHAT_HISTORY_UNAVAILABLE")


if __name__ == "__main__":
    unittest.main()
