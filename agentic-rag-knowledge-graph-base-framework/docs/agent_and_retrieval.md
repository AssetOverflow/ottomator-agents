# Agent & Retrieval

The agent runtime orchestrates prompts, tools, and retrieval strategies to
produce answers.

## Retrieval Router

- `framework.retrieval.router.RetrievalRouter` encapsulates routing logic.
- Uses heuristics to decide between vector-only, graph-only, or hybrid.
- Honors `knowledge_graph.enabled` to automatically fallback to pure vector
  search.

## Retrieval Strategies

| Strategy | Module | Use Case |
|----------|--------|----------|
| `VectorRetrievalStrategy` | `framework.retrieval.strategies` | Semantic similarity search |
| `GraphRetrievalStrategy` | `framework.retrieval.strategies` | Relationship or temporal questions |
| `HybridRetrievalStrategy` | `framework.retrieval.strategies` | Combines both signals |

Each strategy returns lightweight `RetrievalResult` mappings, making it easy to
augment with scores, node IDs, or citations.

## Tools

`framework.agent.tools.build_retrieval_tools` produces a consistent set of tools
(`vector_search`, `graph_search`, `hybrid_search`). Each tool delegates to the
router and returns JSON-serializable payloads.

## Agent Runtime

- `framework.agent.runtime.AgentRuntime` wires the router, prompts, and tools.
- The `handle` method is intentionally lightweight so it can be wrapped by other
  agent frameworks such as Pydantic AI, LangGraph, or custom planners.
- Responses include the composed message and a list of source identifiers.

## Prompting

- Base system prompt lives in `framework.agent.prompts.BASE_SYSTEM_PROMPT`.
- Override it via configuration or subclassing to tailor behavior per project.

## Extending the Agent

1. Create new tools with the `Tool` dataclass and append them to the runtime's
   tool list.
2. Swap in a planning/execution framework while reusing the router and tools.
3. Extend `AgentResponse` to include citations or structured outputs.

See [`docs/extensibility.md`](extensibility.md) for concrete examples.
