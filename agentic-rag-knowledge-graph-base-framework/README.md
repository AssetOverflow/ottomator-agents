# Agentic RAG + Knowledge Graph Base Framework

The `agentic-rag-knowledge-graph-base-framework` distills the lessons from the
original **agentic-rag-knowledge-graph** project into a reusable foundation that
any team can adopt. It standardizes configuration, ingestion, retrieval, and
agent orchestration while remaining intentionally extensible.

## Why a Base Framework?

The original project demonstrates the power of combining vector search with a
knowledge graph through Graphiti. However, the implementation is tightly bound
to a single use case (big tech research), mixes configuration concerns across
modules, and makes it difficult to swap components. This framework introduces a
layered architecture with explicit interfaces so you can:

- Plug in your own LLM, embedding, vector database, or graph database
- Configure deployments through environment variables, JSON, or TOML without
  editing code
- Start from a documented set of defaults while keeping production controls
  (observability, concurrency, prompt governance)
- Share ingestion, retrieval, and agent runtime primitives across many
  downstream projects

## Key Features

- **Configuration-first design** – Everything flows through typed Pydantic
  models with `.env`, JSON, and TOML loading helpers.
- **Pluggable ingestion pipeline** – Replace chunkers, embedders, and storage
  backends without touching orchestration code.
- **Hybrid retrieval router** – Route queries to vector, graph, or hybrid
  strategies with transparent heuristics.
- **Minimal FastAPI surface** – Ship a production-ready API with health checks
  and dependency-injected runtimes.
- **CLI tooling** – Interact with the agent from the terminal using Typer.
- **Extensive documentation** – Architecture, configuration, ingestion,
  retrieval, extensibility, and operations guides live under `docs/`.

## Getting Started

1. **Install dependencies**
   ```bash
   uv pip install -r requirements.txt  # or pip install -r requirements.txt
   ```

2. **Configure the environment**
   Copy `.env.example` to `.env` and update database credentials, LLM providers,
   and observability toggles.

3. **Run the FastAPI server**
   ```bash
   uvicorn framework.api.server:app --reload
   ```

4. **Use the CLI**
   ```bash
   python -m framework.interfaces.cli chat --message "What partnerships matter?"
   ```

## Repository Layout

```text
framework/
├── agent/          # Agent runtime, prompts, and tool wiring
├── api/            # FastAPI application & schemas
├── config/         # Typed configuration models and loaders
├── ingestion/      # Chunking, embeddings, vector + graph storage
├── interfaces/     # Command-line tooling
├── logging/        # Structured logging helpers
└── retrieval/      # Retrieval strategies and routing
```

## Documentation

| File | Description |
|------|-------------|
| [`docs/architecture.md`](docs/architecture.md) | High-level system design |
| [`docs/original_project_analysis.md`](docs/original_project_analysis.md) | Deep dive into the original project strengths and gaps |
| [`docs/configuration.md`](docs/configuration.md) | Environment variable and settings guide |
| [`docs/ingestion_pipeline.md`](docs/ingestion_pipeline.md) | Chunking, embeddings, and storage orchestration |
| [`docs/agent_and_retrieval.md`](docs/agent_and_retrieval.md) | Agent runtime, tools, and retrieval router |
| [`docs/extensibility.md`](docs/extensibility.md) | How to extend or replace components |
| [`docs/testing_and_observability.md`](docs/testing_and_observability.md) | Recommended testing + telemetry setup |
| [`docs/operations_playbook.md`](docs/operations_playbook.md) | Deployment and runbook tips |

This project is intentionally lightweight. Replace the provided in-memory
implementations with production backends, wire in your preferred LLM provider,
and adapt the prompts to your domain while keeping the architectural guardrails.
