"""Shared models for algorithm traces."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SearchStep:
    """One visualizable step produced by a search algorithm."""

    title: str
    description: str
    state: Any
    frontier: list[Any] = field(default_factory=list)
    visited: set[Any] = field(default_factory=set)
    path: list[Any] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
