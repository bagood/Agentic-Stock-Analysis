from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.routing import Mount

from app.mcp_server import mcp_http_app, mcp_server


@asynccontextmanager
async def lifespan(_: Starlette) -> AsyncIterator[None]:
    """Run the MCP transport session manager with the MCP application."""
    async with mcp_server.session_manager.run():
        yield


app = Starlette(
    routes=[Mount("/mcp", app=mcp_http_app, name="mcp")],
    lifespan=lifespan,
)

