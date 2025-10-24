"""Retrieval strategies for vector and knowledge graph search."""

from __future__ import annotations

import abc
from typing import Any, Mapping, Sequence

from ..config.settings import Settings
from ..logging.setup import get_logger

logger = get_logger(__name__)


class RetrievalResult(Mapping[str, Any]):
    """Minimal mapping used to expose retrieval payloads."""

    def __init__(self, data: Mapping[str, Any]):
        self._data = dict(data)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self) -> int:  # noqa: D401 - mapping requirement
        return len(self._data)


class RetrievalStrategy(abc.ABC):
    """Base interface for retrieval strategies."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @abc.abstractmethod
    async def search(self, query: str, *, limit: int = 5) -> Sequence[RetrievalResult]:
        """Execute a search."""


class VectorRetrievalStrategy(RetrievalStrategy):
    async def search(self, query: str, *, limit: int = 5) -> Sequence[RetrievalResult]:
        logger.debug("Vector search for query '%s'", query)
        return [RetrievalResult({"query": query, "source": "vector", "limit": limit})]


class GraphRetrievalStrategy(RetrievalStrategy):
    async def search(self, query: str, *, limit: int = 5) -> Sequence[RetrievalResult]:
        logger.debug("Graph search for query '%s'", query)
        return [RetrievalResult({"query": query, "source": "graph", "limit": limit})]


class HybridRetrievalStrategy(RetrievalStrategy):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings)
        self.vector_strategy = VectorRetrievalStrategy(settings)
        self.graph_strategy = GraphRetrievalStrategy(settings)

    async def search(self, query: str, *, limit: int = 5) -> Sequence[RetrievalResult]:
        logger.debug("Hybrid search for query '%s'", query)
        vector_results = await self.vector_strategy.search(query, limit=limit)
        graph_results = await self.graph_strategy.search(query, limit=limit)
        return list(vector_results) + list(graph_results)


__all__ = [
    "RetrievalStrategy",
    "VectorRetrievalStrategy",
    "GraphRetrievalStrategy",
    "HybridRetrievalStrategy",
    "RetrievalResult",
]
