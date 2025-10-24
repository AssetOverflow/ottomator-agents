# Operations Playbook

This runbook outlines recommended operational practices for teams adopting the
framework.

## Environments

- **Development** – Use `.env` files, in-memory vector store, and dummy
  embedder.
- **Staging** – Mirror production configuration with smaller database instances;
  enable observability integrations.
- **Production** – Run ingestion workers separately from API pods to avoid
  blocking user requests.

## Deployment Checklist

1. Build and publish a Docker image using `uvicorn framework.api.server:app` as
   the entrypoint.
2. Mount configuration via secrets or environment variables.
3. Provision Postgres (with pgvector) and Neo4j; store credentials securely.
4. Configure health checks hitting `/health`.
5. Set resource requests/limits to accommodate ingestion spikes.

## Incident Response

- **API latency spikes** – Check vector store/graph connectivity, scale API pods
  horizontally, ensure ingestion jobs are not running on the same nodes.
- **Incomplete answers** – Verify ingestion freshness, review retrieval logs to
  ensure the router selects the expected strategy.
- **Graph drift** – Run reconciliation jobs using `KnowledgeGraphWriter` to prune
  stale relationships according to the chosen refresh policy.

## Continuous Improvement

- Instrument retrieval strategies to capture success metrics (hit rate, tool
  usage, fallback frequency).
- Periodically review prompt effectiveness and update the base prompt or add
  specialized tools for new scenarios.
- Automate ingestion via CI/CD pipelines triggered by document updates.

Maintaining clear runbooks ensures the framework remains reliable as it is
adapted across multiple projects and domains.
