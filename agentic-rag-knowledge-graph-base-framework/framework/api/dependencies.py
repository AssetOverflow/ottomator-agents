"""FastAPI dependency wiring."""

from __future__ import annotations

from fastapi import Depends

from ..agent.runtime import AgentRuntime
from ..config.settings import Settings, get_settings


def get_settings_dep() -> Settings:
    return get_settings()


def get_agent_runtime(settings: Settings = Depends(get_settings_dep)) -> AgentRuntime:
    return AgentRuntime(settings)


__all__ = ["get_agent_runtime"]
