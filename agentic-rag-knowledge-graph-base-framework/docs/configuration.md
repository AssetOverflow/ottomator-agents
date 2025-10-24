# Configuration Guide

All runtime behavior is driven by the typed `Settings` models under
`framework.config.settings`. Configuration values can be supplied through:

1. Environment variables (recommended for deployments)
2. `.env` files (see `.env.example`)
3. JSON/TOML configuration files loaded via `framework.config.loaders`
4. Direct instantiation of the `Settings` class (useful for tests)

## Environment Variable Naming

Nested models use double underscores (`__`) to match Pydantic's
`env_nested_delimiter` setting. Examples:

- `DATABASE__URL`
- `VECTOR_STORE__EMBEDDING_DIMENSION`
- `KNOWLEDGE_GRAPH__ENABLED`
- `OBSERVABILITY__LOG_LEVEL`

## Key Sections

| Model | Description | Important Fields |
|-------|-------------|------------------|
| `runtime` | Core runtime behavior | `environment`, `conversation_history_limit` |
| `database` | Relational/vector database configuration | `url`, `pool_max_size` |
| `vector_store` | Vector storage behavior | `collection_name`, `similarity_metric` |
| `graph_store` | Neo4j / Graphiti connection details | `uri`, `user`, `password` |
| `llm` | LLM provider configuration | `provider`, `model`, `api_key` |
| `embeddings` | Embedding provider overrides | `model`, `batch_size` |
| `chunking` | Document chunking parameters | `strategy`, `chunk_size`, `max_chunk_size` |
| `knowledge_graph` | Graph ingestion controls | `enabled`, `refresh_policy` |
| `observability` | Logging and telemetry toggles | `log_level`, `enable_tracing` |
| `api` | HTTP server configuration | `host`, `port`, `enable_cors` |

## Loading Settings in Code

```python
from framework.config.settings import get_settings

settings = get_settings()
print(settings.vector_store.collection_name)
```

To load from a file instead of environment variables:

```python
from framework.config.loaders import load_settings_from_file

settings = load_settings_from_file("config/local.toml")
```

## Runtime Overrides

You can override specific fields at runtime when creating the agent:

```python
from framework.agent.runtime import AgentRuntime
from framework.config.settings import Settings

custom_settings = Settings(knowledge_graph={"enabled": False})
runtime = AgentRuntime(custom_settings)
```

The rest of the framework will automatically honor the updated configuration.
