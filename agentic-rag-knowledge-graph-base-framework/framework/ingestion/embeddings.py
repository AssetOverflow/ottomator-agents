"""Embedding abstractions for ingestion and retrieval."""

from __future__ import annotations

import abc
from typing import Iterable, Sequence

from ..config.settings import EmbeddingSettings


class Embedder(abc.ABC):
    """Abstract base class for embedding providers."""

    def __init__(self, settings: EmbeddingSettings) -> None:
        self.settings = settings

    @abc.abstractmethod
    async def embed_documents(self, texts: Sequence[str]) -> Sequence[list[float]]:
        """Generate embeddings for a list of texts."""

    @abc.abstractmethod
    async def embed_query(self, text: str) -> list[float]:
        """Generate a single embedding for query routing."""


class DummyEmbedder(Embedder):
    """Fallback embedder used in documentation/testing contexts."""

    async def embed_documents(self, texts: Sequence[str]) -> Sequence[list[float]]:
        return [await self.embed_query(text) for text in texts]

    async def embed_query(self, text: str) -> list[float]:
        return [float(len(text) % 10)] * self.settings.batch_size


def create_embedder(settings: EmbeddingSettings) -> Embedder:
    """Factory that yields the appropriate embedder implementation."""

    # Real implementation would branch on provider. Keeping simple for the base framework.
    return DummyEmbedder(settings)


__all__ = ["Embedder", "create_embedder"]
