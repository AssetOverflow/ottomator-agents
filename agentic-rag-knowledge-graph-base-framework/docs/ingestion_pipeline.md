# Ingestion Pipeline

The ingestion pipeline converts raw documents into the artifacts required for
agentic retrieval: vectorized chunks and knowledge graph entities.

## Components

1. **Chunker** (`framework.ingestion.chunking`)
   - Implements the `Chunker` abstract base class
   - Ships with `SemanticChunker` and `FixedChunker`
   - Factory method `create_chunker` selects the strategy based on settings

2. **Embedder** (`framework.ingestion.embeddings`)
   - Abstract `Embedder` interface normalizes how embeddings are generated
   - Default `DummyEmbedder` enables offline testing; replace with your preferred
     provider (OpenAI, Ollama, etc.)

3. **Vector Store** (`framework.ingestion.vector_store`)
   - `VectorStore` defines the persistence contract
   - `InMemoryVectorStore` serves as a drop-in fake for tests and demos
   - Swap with pgvector, Qdrant, or Pinecone implementations

4. **Knowledge Graph Writer** (`framework.ingestion.knowledge_graph`)
   - `KnowledgeGraphWriter` encapsulates Graphiti/Neo4j writes
   - `NullKnowledgeGraphWriter` respects the `enabled` flag without branching in
     your code

5. **Pipeline Orchestrator** (`framework.ingestion.pipeline`)
   - `IngestionPipeline` composes the components and provides `ingest_documents`
     plus `ingest_path`
   - Handles concurrency via semaphores to avoid overwhelming providers

## Implementing Production Backends

Create subclasses that satisfy the abstract interfaces. Example:

```python
from framework.ingestion.vector_store import VectorStore

class PgVectorStore(VectorStore):
    async def upsert_chunks(self, chunks):
        # Use asyncpg / SQLAlchemy to write embeddings
        ...

    async def delete_document(self, document_id: str):
        ...
```

Update `create_vector_store` to return your implementation when specific
settings are detected.

## End-to-End Usage

```python
from pathlib import Path
from framework.config.settings import get_settings
from framework.ingestion.pipeline import IngestionPipeline

settings = get_settings()
pipeline = IngestionPipeline(settings)
await pipeline.ingest_path(Path("documents"))
```

Because the pipeline only depends on abstract interfaces, you can write unit
tests that patch in-memory stores while integration tests validate external
systems.
