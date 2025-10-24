"""Knowledge graph ingestion primitives."""

from __future__ import annotations

import abc
from typing import Iterable, Sequence

from ..config.settings import KnowledgeGraphSettings


class GraphEntity(dict):
    """Lightweight entity representation."""

    @property
    def label(self) -> str:
        return self.get("label", "Entity")


class GraphRelationship(dict):
    """Lightweight relationship representation."""

    @property
    def type(self) -> str:
        return self.get("type", "RELATED_TO")


class KnowledgeGraphWriter(abc.ABC):
    """Interface for persisting entities and relationships."""

    def __init__(self, settings: KnowledgeGraphSettings) -> None:
        self.settings = settings

    @abc.abstractmethod
    async def upsert_entities(self, entities: Sequence[GraphEntity]) -> None:
        """Persist nodes into the graph store."""

    @abc.abstractmethod
    async def upsert_relationships(self, relationships: Sequence[GraphRelationship]) -> None:
        """Persist relationships into the graph store."""

    async def cleanup_document(self, document_id: str) -> None:
        """Optional hook for removing outdated facts."""


class NullKnowledgeGraphWriter(KnowledgeGraphWriter):
    """No-op implementation used when the KG is disabled."""

    async def upsert_entities(self, entities: Sequence[GraphEntity]) -> None:  # noqa: D401
        return None

    async def upsert_relationships(self, relationships: Sequence[GraphRelationship]) -> None:
        return None


def create_knowledge_graph_writer(settings: KnowledgeGraphSettings) -> KnowledgeGraphWriter:
    """Factory that respects whether the knowledge graph is enabled."""

    if not settings.enabled:
        return NullKnowledgeGraphWriter(settings)

    return NullKnowledgeGraphWriter(settings)


__all__ = [
    "GraphEntity",
    "GraphRelationship",
    "KnowledgeGraphWriter",
    "create_knowledge_graph_writer",
]
