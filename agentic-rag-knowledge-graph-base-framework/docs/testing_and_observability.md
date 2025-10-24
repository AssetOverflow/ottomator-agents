# Testing & Observability

## Testing Strategy

1. **Unit Tests**
   - Mock the embedder to avoid network calls.
   - Use the in-memory vector store and null knowledge graph writer.
   - Validate chunking, routing, and agent response formatting.

2. **Integration Tests**
   - Spin up Postgres + pgvector and Neo4j containers.
   - Run the ingestion pipeline against a small corpus and verify results via
     SQL/Graph queries.
   - Exercise the FastAPI `/chat` endpoint to validate dependency injection.

3. **Contract Tests**
   - If integrating with Graphiti or other third-party services, create fixtures
     that assert schema expectations and temporal behaviors.

## Observability

- Logging is centralized through `framework.logging.setup.configure_logging`.
- Toggle log levels and structured logging via `observability` settings.
- For distributed tracing, wrap `configure_logging` with your preferred
  OpenTelemetry exporters. The code is intentionally minimal to avoid forcing a
  vendor.

## Recommended Tooling

- **pytest + pytest-asyncio** – Async-friendly testing out of the box.
- **coverage.py** – Ensure ingestion and retrieval paths are exercised.
- **Prometheus / Grafana** – Scrape metrics once you add instrumentation around
  ingestion throughput, latency, and tool usage.

## Runbook Tips

- Monitor ingestion jobs for stuck tasks (watch the semaphore concurrency).
- Alert on vector store or Neo4j connection errors; configure retries in your
  production implementations.
- Emit structured logs with document IDs and query IDs to trace the flow from
  ingestion to responses.
