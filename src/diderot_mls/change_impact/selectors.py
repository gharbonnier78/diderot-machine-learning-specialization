from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

import networkx as nx
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from .models import Change, Scenario, TestCase


@dataclass
class SelectionResult:
    strategy: str
    selected_tests: list[str]
    predicted_impacts: set[str] = field(default_factory=set)
    scores: dict[str, float] = field(default_factory=dict)
    explanations: dict[str, str] = field(default_factory=dict)

    def total_cost(self, scenario: Scenario) -> float:
        return sum(scenario.tests[t].cost for t in self.selected_tests)


def _reachable(graph, source, allowed=None, max_hops=5):
    if allowed is None:
        filtered = graph
    else:
        filtered = nx.MultiDiGraph()
        filtered.add_nodes_from(graph.nodes(data=True))
        for u, v, key, data in graph.edges(keys=True, data=True):
            if data.get("mechanism") in allowed:
                filtered.add_edge(u, v, key=key, **dict(data))
    return set(nx.single_source_shortest_path_length(filtered, source,
                                                      cutoff=max_hops))


def _greedy(scenario, utilities, budget):
    ranked = sorted(
        scenario.tests.values(),
        key=lambda t: (-(utilities.get(t.id, 0.0) / max(t.cost, 1e-9)),
                       -utilities.get(t.id, 0.0), t.cost, t.id),
    )
    out, spent = [], 0.0
    for test in ranked:
        if utilities.get(test.id, 0.0) <= 0:
            continue
        if budget is not None and spent + test.cost > budget + 1e-12:
            continue
        out.append(test.id)
        spent += test.cost
    return out


def _utility(scenario, test: TestCase, predicted, distances=None):
    generic = max(test.detects.values(), default=0.0)
    value = 0.0
    for node_id in set(test.covers) & predicted:
        node = scenario.nodes[node_id]
        proximity = 1.0 if distances is None else 1.0 / (
            1.0 + 0.25 * distances.get(node_id, 7)
        )
        value += node.criticality * generic * proximity
    return value


def select_r0_full(scenario):
    selected = sorted(scenario.tests)
    return SelectionResult("R0_full_suite", selected, set(scenario.nodes),
        explanations={t: "Full existing regression suite baseline." for t in selected})


def select_r1_history(scenario, change, *, budget=None):
    scores = {t.id: float(t.historical_relevance.get(change.category, 0.0))
              for t in scenario.tests.values()}
    selected = _greedy(scenario, scores, budget)
    implied = set()
    for test_id in selected:
        implied.update(scenario.tests[test_id].covers)
    return SelectionResult("R1_history", selected, implied, scores,
        {t: f"Historical relevance for '{change.category}' = {scores[t]:.3f}."
         for t in selected})


def _graph_selector(strategy, scenario, graph, change, *, budget,
                    allowed, max_hops, risk_weighted):
    predicted = _reachable(graph, change.target, allowed, max_hops)
    distances = nx.single_source_shortest_path_length(
        graph, change.target, cutoff=max_hops)
    utilities = {}
    for test in scenario.tests.values():
        if risk_weighted:
            value = _utility(scenario, test, predicted, distances)
        else:
            value = len(set(test.covers) & predicted) * max(
                test.detects.values(), default=0.0)
        utilities[test.id] = value
    selected = _greedy(scenario, utilities, budget)
    return SelectionResult(strategy, selected, predicted, utilities,
        {t: f"Predicted-impact evidence utility={utilities[t]:.3f}."
         for t in selected})


def select_r2_code_graph(scenario, graph, change, *, budget=None, max_hops=5):
    return _graph_selector("R2_code_graph", scenario, graph, change,
        budget=budget, allowed={"call", "control"}, max_hops=max_hops,
        risk_weighted=False)


def select_r3_system_graph(scenario, graph, change, *, budget=None, max_hops=5):
    return _graph_selector("R3_system_graph", scenario, graph, change,
        budget=budget, allowed=None, max_hops=max_hops, risk_weighted=False)


def select_r4_risk_aware(scenario, graph, change, *, budget=None, max_hops=5):
    return _graph_selector("R4_risk_aware", scenario, graph, change,
        budget=budget, allowed=None, max_hops=max_hops, risk_weighted=True)


class NodeImpactLearner:
    """Simple learned baseline using past labelled changes and G_observed only."""

    def __init__(self):
        self.model = make_pipeline(
            StandardScaler(),
            LogisticRegression(class_weight="balanced", max_iter=1000,
                               random_state=0),
        )
        self._is_fit = False

    @staticmethod
    def _features(scenario, graph, change, candidate):
        source, target = scenario.nodes[change.target], scenario.nodes[candidate]
        try:
            distance = nx.shortest_path_length(graph, change.target, candidate)
            reachable = 1.0
        except nx.NetworkXNoPath:
            distance, reachable = 12, 0.0
        return [
            reachable,
            float(min(distance, 12)),
            float(len(set(source.tags) & set(target.tags))),
            float(source.zone == target.zone),
            float(source.kind == target.kind),
            float(graph.has_edge(change.target, candidate)),
            float(graph.in_degree(candidate)),
            float(graph.out_degree(candidate)),
            float(target.criticality),
            float(change.category in target.tags),
        ]

    def fit(self, scenario, graph,
            history: Sequence[tuple[Change, set[str]]]):
        X, y = [], []
        for change, impacted in history:
            for candidate in scenario.nodes:
                X.append(self._features(scenario, graph, change, candidate))
                y.append(int(candidate in impacted))
        if len(set(y)) < 2:
            raise ValueError("History needs impacted and non-impacted examples.")
        self.model.fit(np.asarray(X, dtype=float), np.asarray(y, dtype=int))
        self._is_fit = True
        return self

    def predict_probabilities(self, scenario, graph, change):
        if not self._is_fit:
            raise RuntimeError("Fit NodeImpactLearner before prediction.")
        ids = list(scenario.nodes)
        X = np.asarray([self._features(scenario, graph, change, n) for n in ids],
                       dtype=float)
        return dict(zip(ids, map(float, self.model.predict_proba(X)[:, 1])))


def select_r5_ai_assisted(scenario, graph, change, learner, *, budget=None,
                          probability_threshold=0.35, max_hops=5):
    base = select_r4_risk_aware(scenario, graph, change, budget=None,
                                max_hops=max_hops)
    probabilities = learner.predict_probabilities(scenario, graph, change)
    learned = {n for n, p in probabilities.items() if p >= probability_threshold}
    predicted = base.predicted_impacts | learned
    distances = nx.single_source_shortest_path_length(
        graph, change.target, cutoff=max_hops)
    utilities = {}
    for test in scenario.tests.values():
        generic = max(test.detects.values(), default=0.0)
        value = 0.0
        for node_id in set(test.covers) & predicted:
            node = scenario.nodes[node_id]
            p = max(probabilities.get(node_id, 0.0),
                    0.55 if node_id in base.predicted_impacts else 0.0)
            proximity = 1.0 / (1.0 + 0.25 * distances.get(node_id, max_hops + 2))
            value += node.criticality * generic * p * proximity
        utilities[test.id] = value
    selected = _greedy(scenario, utilities, budget)
    return SelectionResult("R5_ai_assisted", selected, predicted, utilities,
        {t: f"Risk-aware utility + learned impact probability={utilities[t]:.3f}."
         for t in selected})
