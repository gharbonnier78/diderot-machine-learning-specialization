from __future__ import annotations

from dataclasses import dataclass

import networkx as nx
import numpy as np

from .models import Change, Scenario

MECHANISM_TO_FAILURE = {
    "call": "functional",
    "control": "functional",
    "schema": "schema_mismatch",
    "message": "schema_mismatch",
    "state": "stale_state",
    "timing": "timeout",
    "synchronization": "race",
    "resource": "latency",
    "configuration": "misconfiguration",
    "security": "authorization",
    "topology": "availability",
    "supplier": "compatibility",
    "device": "acquisition",
    "sensor": "acquisition",
    "data": "data_shift",
    "ml": "model_shift",
}


@dataclass(frozen=True)
class ImpactEvent:
    node: str
    via_mechanism: str
    failure_mode: str
    depth: int
    criticality: float


@dataclass
class SimulationOutcome:
    change: Change
    impacted: dict[str, ImpactEvent]
    traversed_edges: list[tuple[str, str, str]]
    seed: int

    @property
    def impacted_nodes(self) -> set[str]:
        return set(self.impacted)

    @property
    def critical_impacted_nodes(self) -> set[str]:
        return {n for n, e in self.impacted.items() if e.criticality >= 4.0}


def build_graph(scenario: Scenario) -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph(name=scenario.name)
    for node in scenario.nodes.values():
        graph.add_node(node.id, kind=node.kind, criticality=node.criticality,
                       zone=node.zone, tags=node.tags,
                       failure_modes=node.failure_modes)
    for idx, edge in enumerate(scenario.edges):
        graph.add_edge(edge.source, edge.target, key=f"{edge.mechanism}:{idx}",
                       mechanism=edge.mechanism, probability=edge.probability,
                       weight=edge.weight, visible=edge.visible)
    return graph


def observe_graph(true_graph: nx.MultiDiGraph, *, completeness: float = 0.8,
                  false_edge_rate: float = 0.02, seed: int = 0,
                  mechanism_completeness: dict[str, float] | None = None) -> nx.MultiDiGraph:
    if not 0.0 <= completeness <= 1.0:
        raise ValueError("completeness must be in [0, 1]")
    rng = np.random.default_rng(seed)
    observed = nx.MultiDiGraph(name=f"{true_graph.graph.get('name', 'system')}:observed")
    observed.add_nodes_from(true_graph.nodes(data=True))
    for u, v, key, data in true_graph.edges(keys=True, data=True):
        if not data.get("visible", True):
            continue
        p_keep = completeness
        if mechanism_completeness:
            p_keep *= mechanism_completeness.get(data["mechanism"], 1.0)
        if rng.random() <= min(1.0, p_keep):
            observed.add_edge(u, v, key=key, **dict(data), observed=True)
    nodes = list(observed.nodes)
    candidate_pairs = [(u, v) for u in nodes for v in nodes
                       if u != v and not observed.has_edge(u, v)]
    n_false = int(round(false_edge_rate * max(1, true_graph.number_of_edges())))
    if n_false and candidate_pairs:
        choices = rng.choice(len(candidate_pairs),
                             size=min(n_false, len(candidate_pairs)),
                             replace=False)
        for pos, idx in enumerate(np.atleast_1d(choices)):
            u, v = candidate_pairs[int(idx)]
            observed.add_edge(u, v, key=f"noise:{pos}", mechanism="inferred_noise",
                              probability=0.25, weight=0.25, visible=True,
                              observed=True, synthetic_false_positive=True)
    observed.graph.update(completeness=completeness,
                          false_edge_rate=false_edge_rate, seed=seed)
    return observed


def simulate_change(scenario: Scenario, true_graph: nx.MultiDiGraph,
                    change: Change, *, seed: int = 0,
                    max_depth: int = 8) -> SimulationOutcome:
    if change.target not in true_graph:
        raise KeyError(change.target)
    rng = np.random.default_rng(seed)
    impacted: dict[str, ImpactEvent] = {}
    traversed: list[tuple[str, str, str]] = []
    target = scenario.nodes[change.target]
    seed_mode = target.failure_modes[0] if target.failure_modes else "functional"
    impacted[change.target] = ImpactEvent(change.target, "change", seed_mode, 0,
                                          target.criticality)
    queue: list[tuple[str, int]] = [(change.target, 0)]
    while queue:
        current, depth = queue.pop(0)
        if depth >= max_depth:
            continue
        outgoing = list(true_graph.out_edges(current, keys=True, data=True))
        outgoing.sort(key=lambda item: (item[1], item[2]))
        for u, v, _key, data in outgoing:
            mechanism = str(data.get("mechanism", "call"))
            p = min(1.0, max(0.0, float(data.get("probability", 1.0)) * change.magnitude))
            if rng.random() > p:
                continue
            traversed.append((u, v, mechanism))
            node = scenario.nodes[v]
            if v not in impacted:
                impacted[v] = ImpactEvent(v, mechanism,
                    MECHANISM_TO_FAILURE.get(mechanism, "functional"),
                    depth + 1, node.criticality)
                queue.append((v, depth + 1))
    return SimulationOutcome(change, impacted, traversed, seed)
