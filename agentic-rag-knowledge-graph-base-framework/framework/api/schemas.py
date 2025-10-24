"""Pydantic schemas for the FastAPI layer."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., description="User input for the agent")


class ChatResponse(BaseModel):
    message: str
    sources: list[str]


__all__ = ["ChatRequest", "ChatResponse"]
