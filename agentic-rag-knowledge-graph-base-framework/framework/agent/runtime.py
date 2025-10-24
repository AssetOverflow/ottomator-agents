"""Agent runtime orchestrating prompts, tools, and retrieval."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from ..config.settings import Settings, get_settings
from ..logging.setup import get_logger
from ..retrieval.router import RetrievalRouter
from .prompts import BASE_SYSTEM_PROMPT
from .tools import Tool, build_retrieval_tools

logger = get_logger(__name__)


@dataclass
class AgentResponse:
    """Simple response container."""

    message: str
    sources: list[str]


class AgentRuntime:
    """Composable agent runtime built on the framework primitives."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.router = RetrievalRouter(self.settings)
        self.tools: Sequence[Tool] = build_retrieval_tools(self.router)
        self.system_prompt = BASE_SYSTEM_PROMPT

    async def handle(self, query: str) -> AgentResponse:
        logger.info("Handling query '%s'", query)
        retrieval_results = await self.router.route(query)
        sources = [result["source"] for result in retrieval_results]
        message = (
            "System prompt: "
            + self.system_prompt.strip()
            + "\nQuery: "
            + query
            + "\nRetrieved sources: "
            + ", ".join(sources)
        )
        return AgentResponse(message=message, sources=sources)


__all__ = ["AgentRuntime", "AgentResponse"]
