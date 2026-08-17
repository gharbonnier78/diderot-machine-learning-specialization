from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Node:
    id: str
    kind: str
    criticality: float = 1.0
    zone: str = "default"
    tags: tuple[str, ...] = ()
    failure_modes: tuple[str, ...] = ("functional",)


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    mechanism: str
    probability: float = 1.0
    weight: float = 1.0
    visible: bool = True


@dataclass(frozen=True)
class Change:
    id: str
    target: str
    category: str
    magnitude: float = 1.0
    description: str = ""


@dataclass(frozen=True)
class TestCase:
    id: str
    covers: tuple[str, ...]
    detects: dict[str, float]
    cost: float = 1.0
    tags: tuple[str, ...] = ()
    historical_relevance: dict[str, float] = field(default_factory=dict)


@dataclass
class Scenario:
    name: str
    nodes: dict[str, Node]
    edges: list[Edge]
    tests: dict[str, TestCase]
    changes: dict[str, Change]
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        missing = []
        for edge in self.edges:
            if edge.source not in self.nodes:
                missing.append(f"edge source {edge.source}")
            if edge.target not in self.nodes:
                missing.append(f"edge target {edge.target}")
        for change in self.changes.values():
            if change.target not in self.nodes:
                missing.append(f"change target {change.target}")
        for test in self.tests.values():
            for node_id in test.covers:
                if node_id not in self.nodes:
                    missing.append(f"test {test.id} cover {node_id}")
        if missing:
            raise ValueError("Invalid scenario references: " + ", ".join(missing))

    @property
    def node_ids(self) -> tuple[str, ...]:
        return tuple(self.nodes)
