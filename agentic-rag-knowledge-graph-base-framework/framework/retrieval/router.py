"""Adaptive retrieval router."""

from __future__ import annotations

from typing import Sequence

from ..config.settings import Settings
from ..logging.setup import get_logger
from .strategies import (
    GraphRetrievalStrategy,
    HybridRetrievalStrategy,
    RetrievalResult,
    RetrievalStrategy,
    VectorRetrievalStrategy,
)

logger = get_logger(__name__)


class RetrievalRouter:
    """Routes user questions to the appropriate retrieval strategy."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.vector_strategy = VectorRetrievalStrategy(settings)
        self.graph_strategy = GraphRetrievalStrategy(settings)
        self.hybrid_strategy = HybridRetrievalStrategy(settings)

    async def route(self, query: str, *, use_graph: bool | None = None) -> Sequence[RetrievalResult]:
        logger.info("Routing query '%s'", query)
        if use_graph is None and self.settings.knowledge_graph.enabled:
            use_graph = "relationship" in query.lower()

        if not self.settings.knowledge_graph.enabled:
            return await self.vector_strategy.search(query)

        if use_graph is True:
            return await self.graph_strategy.search(query)

        if use_graph is False:
            return await self.vector_strategy.search(query)

        return await self.hybrid_strategy.search(query)


__all__ = ["RetrievalRouter"]
