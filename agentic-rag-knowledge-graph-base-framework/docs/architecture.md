# Architecture Overview

This document captures the architectural principles behind the
`agentic-rag-knowledge-graph-base-framework`. The framework is intentionally
modular and favors composition over inheritance.

## Layers

1. **Configuration Layer** (`framework.config`)
   - Centralizes all configuration into typed `Settings` models
   - Supports `.env`, JSON, and TOML loading using nested keys
   - Prevents configuration drift by making runtime services depend on the
     settings object instead of hard-coded constants

2. **Ingestion Layer** (`framework.ingestion`)
   - Responsible for turning raw documents into vectorized chunks and graph
     entities
   - Exposes `IngestionPipeline` which orchestrates chunking, embeddings,
     vector store writes, and optional knowledge graph updates

3. **Retrieval Layer** (`framework.retrieval`)
   - Encapsulates vector, graph, and hybrid retrieval strategies
   - Provides an adaptive router that chooses the right strategy based on
     heuristics and configuration flags

4. **Agent Layer** (`framework.agent`)
   - Holds the runtime object used by interfaces
   - Combines prompts, tools, and retrieval router to produce responses
   - Designed to be swapped for other agent frameworks while preserving tool
     wiring and retrieval semantics

5. **Interface Layer** (`framework.api` & `framework.interfaces`)
   - FastAPI server exposes `/health` and `/chat`
   - Typer CLI offers a simple debugging experience

6. **Cross-cutting Concerns** (`framework.logging`)
   - Provides structured logging helpers consumed by every layer

## Data Flow

```text
Documents -> IngestionPipeline -> Vector Store + Knowledge Graph
                                         |
                                         v
                                   RetrievalRouter
                                         |
                                         v
                                   AgentRuntime -> API / CLI
```

## Guiding Principles

- **Explicit boundaries** – Each layer defines interfaces so that production
  implementations can replace the provided reference ones.
- **Configuration driven** – No environment-specific logic lives outside of the
  `Settings` models.
- **Observability ready** – Logging is centralized and can be swapped with
  structured or OTLP exporters without touching business logic.
- **Testability** – The in-memory vector store and null knowledge graph writer
  allow unit tests to run without external services.

Refer to [`docs/extensibility.md`](extensibility.md) for guidance on extending
individual components.
