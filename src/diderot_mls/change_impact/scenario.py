from __future__ import annotations

from pathlib import Path

import yaml

from .models import Change, Edge, Node, Scenario, TestCase


def load_scenario(path: str | Path) -> Scenario:
    path = Path(path)
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    nodes = {
        item["id"]: Node(
            id=item["id"],
            kind=item["kind"],
            criticality=float(item.get("criticality", 1.0)),
            zone=item.get("zone", "default"),
            tags=tuple(item.get("tags", [])),
            failure_modes=tuple(item.get("failure_modes", ["functional"])),
        )
        for item in raw["nodes"]
    }
    edges = [
        Edge(
            source=item["source"],
            target=item["target"],
            mechanism=item["mechanism"],
            probability=float(item.get("probability", 1.0)),
            weight=float(item.get("weight", 1.0)),
            visible=bool(item.get("visible", True)),
        )
        for item in raw["edges"]
    ]
    tests = {
        item["id"]: TestCase(
            id=item["id"],
            covers=tuple(item.get("covers", [])),
            detects={k: float(v) for k, v in item.get("detects", {}).items()},
            cost=float(item.get("cost", 1.0)),
            tags=tuple(item.get("tags", [])),
            historical_relevance={
                k: float(v) for k, v in item.get("historical_relevance", {}).items()
            },
        )
        for item in raw["tests"]
    }
    changes = {
        item["id"]: Change(
            id=item["id"],
            target=item["target"],
            category=item["category"],
            magnitude=float(item.get("magnitude", 1.0)),
            description=item.get("description", ""),
        )
        for item in raw["changes"]
    }
    scenario = Scenario(
        name=raw.get("name", path.stem),
        nodes=nodes,
        edges=edges,
        tests=tests,
        changes=changes,
        metadata=dict(raw.get("metadata", {})),
    )
    scenario.validate()
    return scenario
