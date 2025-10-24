"""Centralized configuration models for the base framework."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel, Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    """Settings for the relational/vector database layer."""

    url: str = Field(..., description="SQLAlchemy compatible database URL")
    schema: Optional[str] = Field(
        default=None,
        description="Optional schema name when using PostgreSQL compatible databases.",
    )
    pool_min_size: int = Field(default=1, ge=0)
    pool_max_size: int = Field(default=10, ge=1)
    timeout_seconds: float = Field(default=30.0, gt=0)


class VectorStoreSettings(BaseModel):
    """Settings related to pgvector or other vector stores."""

    collection_name: str = Field(default="documents")
    embedding_dimension: int = Field(default=1536, ge=1)
    similarity_metric: Literal["cosine", "dot", "euclidean"] = Field(default="cosine")
    chunk_table: str = Field(default="document_chunks")
    metadata_table: str = Field(default="document_metadata")


class GraphStoreSettings(BaseModel):
    """Settings for the graph database leveraged by Graphiti."""

    uri: str = Field(default="bolt://localhost:7687")
    user: str = Field(default="neo4j")
    password: str = Field(default="password")
    database: str = Field(default="neo4j")
    enable_temporal: bool = Field(
        default=True, description="Enable temporal modeling features for Graphiti."
    )


class ProviderSettings(BaseModel):
    """LLM and embedding provider configuration."""

    provider: Literal["openai", "ollama", "anthropic", "azure_openai", "custom"] = Field(
        default="openai"
    )
    base_url: str = Field(default="https://api.openai.com/v1")
    api_key: str = Field(default="", description="API key for the selected provider")
    model: str = Field(default="gpt-4.1-mini")
    request_timeout_seconds: float = Field(default=60, gt=0)


class EmbeddingSettings(ProviderSettings):
    """Embedding provider specific overrides."""

    model: str = Field(default="text-embedding-3-small")
    batch_size: int = Field(default=64, ge=1)


class ChunkingSettings(BaseModel):
    """Controls how documents are chunked prior to embedding."""

    strategy: Literal["semantic", "fixed", "hybrid"] = Field(default="semantic")
    chunk_size: int = Field(default=800, ge=50)
    chunk_overlap: int = Field(default=120, ge=0)
    max_chunk_size: int = Field(default=2000, ge=200)
    enable_title_inference: bool = Field(default=True)
    enable_metadata_extraction: bool = Field(default=True)


class KnowledgeGraphSettings(BaseModel):
    """Controls Graphiti powered knowledge graph construction."""

    enabled: bool = Field(default=True)
    relationship_confidence_threshold: float = Field(default=0.35, ge=0, le=1)
    entity_resolution_sensitivity: float = Field(default=0.6, ge=0, le=1)
    ingestion_batch_size: int = Field(default=100, ge=1)
    refresh_policy: Literal["replace", "append", "temporal_merge"] = Field(
        default="temporal_merge"
    )


class ObservabilitySettings(BaseModel):
    """Telemetry and logging configuration."""

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO"
    )
    structured_logging: bool = Field(default=True)
    enable_tracing: bool = Field(default=False)
    tracing_exporter: Literal["otlp", "console"] = Field(default="otlp")
    metrics_enabled: bool = Field(default=True)


class APISettings(BaseModel):
    """FastAPI server configuration."""

    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8058, ge=1, le=65535)
    reload: bool = Field(default=False)
    enable_cors: bool = Field(default=True)
    allowed_origins: list[str] = Field(default_factory=lambda: ["*"])


class RuntimeSettings(BaseModel):
    """Orchestrator level settings."""

    environment: Literal["development", "staging", "production", "test"] = Field(
        default="development"
    )
    conversation_history_limit: int = Field(default=25, ge=1)
    enable_tool_debug: bool = Field(default=False)
    default_tool_timeout_seconds: float = Field(default=45, gt=0)


class Settings(BaseSettings):
    """Top level configuration container."""

    model_config = SettingsConfigDict(
        env_file=Path(".env"),
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
    )

    runtime: RuntimeSettings = Field(default_factory=RuntimeSettings)
    database: DatabaseSettings = Field(
        default_factory=lambda: DatabaseSettings(url="postgresql://localhost/postgres")
    )
    vector_store: VectorStoreSettings = Field(default_factory=VectorStoreSettings)
    graph_store: GraphStoreSettings = Field(default_factory=GraphStoreSettings)
    llm: ProviderSettings = Field(default_factory=ProviderSettings)
    embeddings: EmbeddingSettings = Field(default_factory=EmbeddingSettings)
    chunking: ChunkingSettings = Field(default_factory=ChunkingSettings)
    knowledge_graph: KnowledgeGraphSettings = Field(default_factory=KnowledgeGraphSettings)
    observability: ObservabilitySettings = Field(default_factory=ObservabilitySettings)
    api: APISettings = Field(default_factory=APISettings)

    project_name: str = Field(default="Agentic RAG + Knowledge Graph Framework")
    workspace_dir: Path = Field(default=Path.cwd())

    @validator("workspace_dir", pre=True, always=True)
    def _expand_workspace_dir(cls, value: Path | str) -> Path:  # noqa: N805
        return Path(value).expanduser().resolve()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Cached settings loader for runtime usage."""

    return Settings()


__all__ = ["Settings", "get_settings"]
