"""Document chunking strategies."""

from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import Iterable, Sequence

from pydantic import BaseModel

from ..config.settings import ChunkingSettings


@dataclass(slots=True)
class Chunk:
    """Normalized representation of a document chunk."""

    document_id: str
    content: str
    order: int
    title: str | None = None
    metadata: dict[str, str] | None = None


class Chunker(abc.ABC):
    """Abstract base class for chunking strategies."""

    def __init__(self, settings: ChunkingSettings) -> None:
        self.settings = settings

    @abc.abstractmethod
    async def run(self, *, content: str, document_id: str, title: str | None) -> Sequence[Chunk]:
        """Split content into ordered chunks."""


class SemanticChunker(Chunker):
    """Semantic chunker leveraging LLM signals with fallbacks."""

    async def run(self, *, content: str, document_id: str, title: str | None) -> Sequence[Chunk]:
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        chunks: list[Chunk] = []
        for idx, paragraph in enumerate(paragraphs):
            if len(paragraph) > self.settings.max_chunk_size:
                sub_chunks = [
                    paragraph[i : i + self.settings.chunk_size]
                    for i in range(0, len(paragraph), self.settings.chunk_size)
                ]
            else:
                sub_chunks = [paragraph]

            for offset, piece in enumerate(sub_chunks):
                chunks.append(
                    Chunk(
                        document_id=document_id,
                        content=piece,
                        order=len(chunks),
                        title=title,
                        metadata={"source_paragraph": str(idx), "chunk_offset": str(offset)},
                    )
                )
        return chunks


class FixedChunker(Chunker):
    """Deterministic chunker that ignores semantic boundaries."""

    async def run(self, *, content: str, document_id: str, title: str | None) -> Sequence[Chunk]:
        tokens = content.split()
        chunks: list[Chunk] = []
        size = self.settings.chunk_size
        overlap = self.settings.chunk_overlap
        start = 0
        order = 0

        while start < len(tokens):
            end = min(start + size, len(tokens))
            chunk_tokens = tokens[start:end]
            chunks.append(
                Chunk(
                    document_id=document_id,
                    content=" ".join(chunk_tokens),
                    order=order,
                    title=title,
                    metadata={"strategy": "fixed", "start": str(start), "end": str(end)},
                )
            )
            if end == len(tokens):
                break
            start = end - overlap
            order += 1

        return chunks


def create_chunker(settings: ChunkingSettings) -> Chunker:
    """Factory for chunking strategies."""

    if settings.strategy == "semantic":
        return SemanticChunker(settings)
    if settings.strategy == "fixed":
        return FixedChunker(settings)
    # Hybrid currently defaults to semantic with deterministic fallback
    return SemanticChunker(settings)


class ChunkingResult(BaseModel):
    """Normalized chunk payload for downstream storage."""

    document_id: str
    chunk_id: str
    order: int
    content: str
    vector: list[float] | None = None
    metadata: dict[str, str] = {}


__all__ = ["Chunk", "Chunker", "create_chunker", "ChunkingResult"]
