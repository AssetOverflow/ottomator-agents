"""Vector store storage abstraction."""

from __future__ import annotations

import abc
from typing import Sequence

from ..config.settings import Settings, VectorStoreSettings
from .chunking import ChunkingResult


class VectorStore(abc.ABC):
    """Interface for persisting and querying vectorized chunks."""

    def __init__(self, settings: VectorStoreSettings) -> None:
        self.settings = settings

    @abc.abstractmethod
    async def upsert_chunks(self, chunks: Sequence[ChunkingResult]) -> None:
        """Persist chunk vectors and metadata."""

    @abc.abstractmethod
    async def delete_document(self, document_id: str) -> None:
        """Remove all chunks for a document."""


class InMemoryVectorStore(VectorStore):
    """Simple in-memory implementation suitable for testing/documentation."""

    def __init__(self, settings: VectorStoreSettings) -> None:
        super().__init__(settings)
        self._store: dict[str, list[ChunkingResult]] = {}

    async def upsert_chunks(self, chunks: Sequence[ChunkingResult]) -> None:
        for chunk in chunks:
            self._store.setdefault(chunk.document_id, []).append(chunk)

    async def delete_document(self, document_id: str) -> None:
        self._store.pop(document_id, None)


def create_vector_store(settings: Settings) -> VectorStore:
    """Factory that returns a vector store implementation."""

    return InMemoryVectorStore(settings.vector_store)


__all__ = ["VectorStore", "create_vector_store", "InMemoryVectorStore"]
