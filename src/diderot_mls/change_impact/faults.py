from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .metrics import event_detection_probability


@dataclass(frozen=True)
class InjectedFault:
    id: str
    node: str
    failure_mode: str
    criticality: float


def build_fault_catalogue(scenario, *, critical_only: bool = False):
    """Create explicit, reproducible fault hypotheses from declared node modes."""
    faults = []
    for node in scenario.nodes.values():
        if critical_only and node.criticality < 4.0:
            continue
        for mode in node.failure_modes:
            faults.append(InjectedFault(
                id=f"F_{node.id}_{mode}",
                node=node.id,
                failure_mode=mode,
                criticality=node.criticality,
            ))
    return faults


def evaluate_fault_campaign(scenario, selection, faults, *, seed: int = 0):
    """Inject declared failure modes independently and measure selected-test detection.

    The fault catalogue is separate from change propagation. This provides an
    explicit mutation/fault-injection plane for studying coverage versus oracle
    strength after a regression set has been selected.
    """
    rng = np.random.default_rng(seed)
    covered = set()
    for test_id in selection.selected_tests:
        covered.update(scenario.tests[test_id].covers)

    rows = []
    for fault in faults:
        pod = event_detection_probability(
            scenario, selection, fault.node, fault.failure_mode)
        rows.append({
            "fault_id": fault.id,
            "node": fault.node,
            "failure_mode": fault.failure_mode,
            "criticality": fault.criticality,
            "covered": fault.node in covered,
            "pod": pod,
            "detected": bool(rng.random() <= pod),
        })
    return pd.DataFrame(rows)


def summarize_fault_campaign(frame: pd.DataFrame):
    if frame.empty:
        return {
            "faults": 0,
            "node_coverage": 1.0,
            "mean_pod": 1.0,
            "realized_detection_score": 1.0,
            "critical_mean_pod": 1.0,
        }
    critical = frame[frame["criticality"] >= 4.0]
    return {
        "faults": int(len(frame)),
        "node_coverage": float(frame["covered"].mean()),
        "mean_pod": float(frame["pod"].mean()),
        "realized_detection_score": float(frame["detected"].mean()),
        "critical_mean_pod": float(critical["pod"].mean()) if len(critical) else 1.0,
    }
