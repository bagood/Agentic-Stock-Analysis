from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from app.clients.organizer_quota_client import OrganizerQuotaClient
from app.controllers.chat_controller import ChatController
from app.integrations.codex_runner import CodexRunner
from app.routers.chat_router import router as chat_router
from app.services.chat_service import ChatService
from app.settings import ChatSettings


def create_app(settings: ChatSettings | None = None) -> FastAPI:
    """Build the dedicated chat API and its managed dependencies."""

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        resolved_settings = settings or ChatSettings.from_env()
        timeout = httpx.Timeout(resolved_settings.organizer_timeout_seconds)
        async with httpx.AsyncClient(
            timeout=timeout,
            follow_redirects=True,
        ) as http_client:
            quota_client = OrganizerQuotaClient(
                resolved_settings.organizer_base_url,
                http_client,
                retry_attempts=resolved_settings.organizer_retry_attempts,
                retry_backoff_seconds=(
                    resolved_settings.organizer_retry_backoff_seconds
                ),
            )
            codex_runner = CodexRunner(
                executable=resolved_settings.codex_executable,
                mcp_url=resolved_settings.mcp_url,
                timeout_seconds=resolved_settings.codex_timeout_seconds,
                max_concurrency=resolved_settings.max_concurrency,
                max_response_bytes=resolved_settings.max_response_bytes,
            )
            service = ChatService(
                quota_client,
                codex_runner,
                resolved_settings.max_message_chars,
            )
            app.state.chat_controller = ChatController(service)
            yield

    application = FastAPI(
        title="agentic-stock-analysis Chat API",
        description=(
            "Quota-controlled chat with Codex and the stock-analysis MCP server."
        ),
        version="1.0.0",
        lifespan=lifespan,
    )
    application.include_router(chat_router)
    return application


app = create_app()
