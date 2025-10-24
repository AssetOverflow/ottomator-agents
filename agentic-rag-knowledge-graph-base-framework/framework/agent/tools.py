"""Tool definitions exposed to the conversational agent."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Awaitable, Callable, Protocol, Sequence

from ..logging.setup import get_logger
from ..retrieval.router import RetrievalRouter

logger = get_logger(__name__)


class ToolHandler(Protocol):
    """Callable protocol for agent tools."""

    def __call__(self, *args, **kwargs) -> Awaitable[str]:
        ...


@dataclass(slots=True)
class Tool:
    """Structured representation of a tool."""

    name: str
    description: str
    handler: ToolHandler


def build_retrieval_tools(router: RetrievalRouter) -> Sequence[Tool]:
    """Create a standard set of retrieval tools for the agent."""

    async def vector_search(query: str, limit: int = 5) -> str:
        results = await router.vector_strategy.search(query, limit=limit)
        return str([dict(item) for item in results])

    async def graph_search(query: str, limit: int = 5) -> str:
        results = await router.graph_strategy.search(query, limit=limit)
        return str([dict(item) for item in results])

    async def hybrid_search(query: str, limit: int = 5) -> str:
        results = await router.hybrid_strategy.search(query, limit=limit)
        return str([dict(item) for item in results])

    return [
        Tool(
            name="vector_search",
            description="Retrieve semantically similar chunks using the vector store",
            handler=vector_search,
        ),
        Tool(
            name="graph_search",
            description="Query the knowledge graph for entities and relationships",
            handler=graph_search,
        ),
        Tool(
            name="hybrid_search",
            description="Combine vector and graph signals for comprehensive recall",
            handler=hybrid_search,
        ),
    ]


__all__ = ["Tool", "build_retrieval_tools"]
