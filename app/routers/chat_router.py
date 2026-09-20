from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status

from app.controllers.chat_controller import ChatController
from app.models.chat import ChatRequest, ChatResponse, HealthResponse

router = APIRouter(tags=["Chat"])


def get_chat_controller(request: Request) -> ChatController:
    """Return the lifespan-created controller and allow test overrides."""
    controller = getattr(request.app.state, "chat_controller", None)
    if controller is None:
        raise RuntimeError("Chat service has not been initialized")
    return controller


ChatControllerDependency = Annotated[
    ChatController,
    Depends(get_chat_controller),
]
AuthorizationHeader = Annotated[str | None, Header(alias="Authorization")]


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    controller: ChatControllerDependency,
    authorization: AuthorizationHeader = None,
) -> ChatResponse:
    """Return a completed chat turn after atomic persistence and quota use."""
    return await controller.communicate(request.message, authorization)


@router.get("/health/live", response_model=HealthResponse)
def health_live() -> HealthResponse:
    """Report that the FastAPI process is serving requests."""
    return HealthResponse(status="ok")


@router.get("/health/ready", response_model=HealthResponse)
def health_ready(controller: ChatControllerDependency) -> HealthResponse:
    """Report whether the configured Codex executable is available."""
    if not controller.is_ready():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Codex executable is unavailable",
        )
    return HealthResponse(status="ok")
