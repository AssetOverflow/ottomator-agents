"""Prompt templates used by the orchestrator."""

from __future__ import annotations

from textwrap import dedent

BASE_SYSTEM_PROMPT = dedent(
    """
    You are an autonomous analyst that can combine semantic retrieval with
    knowledge graph reasoning. Use the available tools to gather evidence and
    produce transparent answers. Always cite your sources.
    """
)


__all__ = ["BASE_SYSTEM_PROMPT"]
