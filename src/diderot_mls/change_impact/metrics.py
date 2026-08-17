from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np

from .models import Scenario
from .selectors import SelectionResult
from .simulator import SimulationOutcome


@dataclass
class Evaluation:
    strategy: str
    tests_executed: int
    execution_cost: float
    impact_recall: float
    critical_impact_recall: float
    impacted_node_coverage: float
    critical_node_coverage: float
    mean_pod: float
    critical_mean_pod: float
    critical_min_pod: float
    critical_regression_miss_rate: float
    realized_detection_rate: float
    realized_critical_detection_rate: float

    def as_dict(self):
        return asdict(self)


def _ratio(num, den, default=1.0):
    return default if den == 0 else num / den


def event_detection_probability(scenario: Scenario, selection: SelectionResult,
                                node_id: str, failure_mode: str) -> float:
    miss = 1.0
    for test_id in selection.selected_tests:
        test = scenario.tests[test_id]
        if node_id not in test.covers:
            continue
        p = min(1.0, max(0.0, float(
            test.detects.get(failure_mode, test.detects.get("*", 0.0)))))
        miss *= 1.0 - p
    return 1.0 - miss


def evaluate_selection(scenario: Scenario, outcome: SimulationOutcome,
                       selection: SelectionResult, *, seed: int = 0) -> Evaluation:
    true_nodes = outcome.impacted_nodes
    critical_nodes = outcome.critical_impacted_nodes
    predicted = selection.predicted_impacts
    impact_recall = _ratio(len(predicted & true_nodes), len(true_nodes), 0.0)
    critical_impact_recall = _ratio(
        len(predicted & critical_nodes), len(critical_nodes), 1.0)

    covered = set()
    for test_id in selection.selected_tests:
        covered.update(scenario.tests[test_id].covers)
    node_coverage = _ratio(len(covered & true_nodes), len(true_nodes), 1.0)
    critical_coverage = _ratio(
        len(covered & critical_nodes), len(critical_nodes), 1.0)

    pods = {
        node_id: event_detection_probability(
            scenario, selection, node_id, event.failure_mode)
        for node_id, event in outcome.impacted.items()
    }
    mean_pod = float(np.mean(list(pods.values()))) if pods else 1.0
    critical_pods = [pods[n] for n in critical_nodes]
    critical_mean = float(np.mean(critical_pods)) if critical_pods else 1.0
    critical_min = float(np.min(critical_pods)) if critical_pods else 1.0
    zero_miss = float(np.mean([p <= 0.0 for p in critical_pods])) \
        if critical_pods else 0.0

    rng = np.random.default_rng(seed)
    realized = {n: bool(rng.random() <= p) for n, p in pods.items()}
    realized_rate = _ratio(sum(realized.values()), len(realized), 1.0)
    realized_critical = _ratio(
        sum(realized[n] for n in critical_nodes), len(critical_nodes), 1.0)

    return Evaluation(
        selection.strategy, len(selection.selected_tests),
        selection.total_cost(scenario), impact_recall, critical_impact_recall,
        node_coverage, critical_coverage, mean_pod, critical_mean, critical_min,
        zero_miss, realized_rate, realized_critical)
