"""Structured logging helpers."""

from __future__ import annotations

import logging
from typing import Any

from ..config.settings import get_settings


def configure_logging() -> None:
    settings = get_settings().observability
    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def get_logger(name: str) -> logging.Logger:
    if not logging.getLogger().handlers:
        configure_logging()
    return logging.getLogger(name)


__all__ = ["configure_logging", "get_logger"]
