# Extensibility Guide

The base framework is designed for customization. This guide outlines common
extension points.

## Replacing the Vector Store

1. Implement `VectorStore` with your database of choice (pgvector, Qdrant,
   Milvus, Pinecone, etc.).
2. Update `create_vector_store` to detect configuration flags and return your
   implementation.
3. Inject additional configuration fields into `VectorStoreSettings` as needed.

## Integrating Graphiti / Neo4j

1. Subclass `KnowledgeGraphWriter` and implement `upsert_entities` and
   `upsert_relationships` using the Graphiti SDK.
2. Use `settings.knowledge_graph` to honor refresh policies or temporal merges.
3. Provide a background job that prunes outdated relationships if you set
   `refresh_policy="replace"`.

## Custom Chunking

- Subclass `Chunker` to integrate semantic segmentation models such as
  `nomic` or `smolagents`.
- Configure via `chunking.strategy="hybrid"` and adjust the factory to combine
  heuristics.

## Tooling

- Add more tools (e.g., `timeline_generation`, `graph_path_explorer`) by
  extending the list returned by `build_retrieval_tools`.
- Tools can call external APIs, query relational databases, or trigger custom
  workflows.

## Agent Orchestration

- Wrap `AgentRuntime` in your orchestrator of choice (LangGraph, LlamaIndex,
  CrewAI) while reusing the router and tools.
- Replace the runtime entirely but keep configuration and ingestion layers.

## Deployment Patterns

- Package the FastAPI app as a container using the provided `pyproject.toml`.
- Deploy ingestion as a separate worker that shares configuration via `.env`
  files or secrets managers.
- Enable observability integrations by swapping `configure_logging` with
  an OTLP handler or OpenTelemetry instrumentation.

## Testing

- Use the in-memory vector store and null graph writer for unit tests.
- Provide fixtures that inject stubbed embeddings to avoid network calls.
- For integration tests, spin up Docker containers for Postgres + pgvector and
  Neo4j using `docker-compose`.

By following these patterns you can evolve the framework into a
production-grade system tailored to your data and retrieval requirements.
