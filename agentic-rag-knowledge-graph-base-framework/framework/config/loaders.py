"""Configuration loading utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .settings import Settings


def load_settings_from_dict(data: Mapping[str, Any]) -> Settings:
    """Load settings from a mapping object."""

    return Settings(**data)


def load_settings_from_file(path: str | Path) -> Settings:
    """Load settings from a JSON or TOML file."""

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    if path.suffix.lower() == ".json":
        return load_settings_from_dict(json.loads(path.read_text()))

    if path.suffix.lower() in {".toml", ".tml"}:
        try:
            import tomllib  # Python 3.11+
        except ModuleNotFoundError:  # pragma: no cover - fallback for <3.11
            import tomli as tomllib  # type: ignore

        return load_settings_from_dict(tomllib.loads(path.read_text()))

    raise ValueError(f"Unsupported settings format: {path.suffix}")


__all__ = ["load_settings_from_dict", "load_settings_from_file"]
