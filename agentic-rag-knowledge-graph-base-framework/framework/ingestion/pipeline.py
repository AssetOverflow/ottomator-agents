"""High level ingestion pipeline coordinating chunking, embeddings, and storage."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from ..config.settings import Settings
from ..logging.setup import get_logger
from .chunking import Chunker, ChunkingResult, create_chunker
from .embeddings import Embedder, create_embedder
from .knowledge_graph import KnowledgeGraphWriter, create_knowledge_graph_writer
from .vector_store import VectorStore, create_vector_store

logger = get_logger(__name__)


@dataclass(slots=True)
class DocumentPayload:
    """In-memory representation of a document to ingest."""

    document_id: str
    content: str
    title: str | None = None
    metadata: dict[str, str] | None = None


class IngestionPipeline:
    """Coordinated ingestion pipeline with pluggable stages."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.chunker: Chunker = create_chunker(settings.chunking)
        self.embedder: Embedder = create_embedder(settings.embeddings)
        self.vector_store: VectorStore = create_vector_store(settings)
        self.graph_writer: KnowledgeGraphWriter = create_knowledge_graph_writer(
            settings.knowledge_graph
        )

    async def ingest_documents(self, documents: Sequence[DocumentPayload]) -> None:
        """Ingest a collection of documents concurrently."""

        semaphore = asyncio.Semaphore(self.settings.chunking.chunk_overlap or 4)

        async def _ingest(document: DocumentPayload) -> None:
            async with semaphore:
                await self._ingest_document(document)

        await asyncio.gather(*[_ingest(doc) for doc in documents])

    async def _ingest_document(self, document: DocumentPayload) -> None:
        logger.info("Ingesting document %s", document.document_id)
        chunks = await self.chunker.run(
            content=document.content,
            document_id=document.document_id,
            title=document.title,
        )
        vectors = await self.embedder.embed_documents([chunk.content for chunk in chunks])
        chunk_payloads = [
            ChunkingResult(
                document_id=document.document_id,
                chunk_id=f"{document.document_id}:{chunk.order}",
                order=chunk.order,
                content=chunk.content,
                vector=vector,
                metadata=chunk.metadata or {},
            )
            for chunk, vector in zip(chunks, vectors)
        ]
        await self.vector_store.upsert_chunks(chunk_payloads)
        if self.settings.knowledge_graph.enabled:
            await self.graph_writer.upsert_entities(
                [
                    {"id": document.document_id, "label": document.title or "Document"}
                ]
            )

    async def ingest_path(self, path: Path) -> None:
        """Convenience helper for ingesting all markdown files in a directory."""

        documents = []
        for file in path.glob("**/*.md"):
            documents.append(
                DocumentPayload(
                    document_id=file.stem,
                    content=file.read_text(),
                    title=file.stem.replace("_", " ").title(),
                    metadata={"source_path": str(file)},
                )
            )
        await self.ingest_documents(documents)


__all__ = ["IngestionPipeline", "DocumentPayload"]
