"""FastAPI application exposing the agent runtime."""

from __future__ import annotations

from fastapi import Depends, FastAPI

from ..agent.runtime import AgentRuntime
from ..config.settings import get_settings
from ..logging.setup import configure_logging
from .dependencies import get_agent_runtime
from .schemas import ChatRequest, ChatResponse

configure_logging()
settings = get_settings()
app = FastAPI(title=settings.project_name)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    agent: AgentRuntime = Depends(get_agent_runtime),
) -> ChatResponse:
    response = await agent.handle(request.message)
    return ChatResponse(message=response.message, sources=response.sources)


__all__ = ["app"]
