from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .metrics import evaluate_selection
from .models import Scenario
from .selectors import (
    NodeImpactLearner,
    SelectionResult,
    select_r0_full,
    select_r1_history,
    select_r2_code_graph,
    select_r3_system_graph,
    select_r4_risk_aware,
    select_r5_ai_assisted,
)
from .simulator import build_graph, observe_graph, simulate_change


@dataclass
class ExperimentBundle:
    scenario: Scenario
    true_graph: object
    observed_graph: object
    current_outcome: object
    selections: dict[str, SelectionResult]
    results: pd.DataFrame
    learner: NodeImpactLearner


def run_comparison(
    scenario: Scenario,
    *,
    change_id: str,
    graph_seed: int = 11,
    propagation_seed: int = 17,
    detection_seed: int = 23,
    completeness: float = 0.78,
    false_edge_rate: float = 0.03,
    budget: float = 22.0,
    history_repetitions: int = 8,
    ai_threshold: float = 0.35,
) -> ExperimentBundle:
    """Run R0-R5 while keeping the current hidden outcome away from selectors."""
    true_graph = build_graph(scenario)
    observed_graph = observe_graph(
        true_graph,
        completeness=completeness,
        false_edge_rate=false_edge_rate,
        seed=graph_seed,
    )
    current_change = scenario.changes[change_id]
    current_outcome = simulate_change(
        scenario, true_graph, current_change, seed=propagation_seed)

    # Historical labels emulate past investigated incidents. The current change
    # is explicitly excluded, so its hidden result cannot leak into R5 training.
    history = []
    seed_cursor = propagation_seed + 100
    for other_change in scenario.changes.values():
        if other_change.id == current_change.id:
            continue
        for rep in range(history_repetitions):
            prior = simulate_change(
                scenario, true_graph, other_change, seed=seed_cursor + rep)
            history.append((other_change, prior.impacted_nodes))
        seed_cursor += 100

    learner = NodeImpactLearner().fit(scenario, observed_graph, history)
    selections = {
        "R0": select_r0_full(scenario),
        "R1": select_r1_history(scenario, current_change, budget=budget),
        "R2": select_r2_code_graph(
            scenario, observed_graph, current_change, budget=budget),
        "R3": select_r3_system_graph(
            scenario, observed_graph, current_change, budget=budget),
        "R4": select_r4_risk_aware(
            scenario, observed_graph, current_change, budget=budget),
        "R5": select_r5_ai_assisted(
            scenario, observed_graph, current_change, learner,
            budget=budget, probability_threshold=ai_threshold),
    }

    rows = []
    for idx, (label, selection) in enumerate(selections.items()):
        evaluation = evaluate_selection(
            scenario, current_outcome, selection, seed=detection_seed + idx)
        row = evaluation.as_dict()
        row["label"] = label
        row["selected_tests"] = ", ".join(selection.selected_tests)
        row["predicted_impacts"] = len(selection.predicted_impacts)
        rows.append(row)

    results = pd.DataFrame(rows).set_index("label")
    return ExperimentBundle(
        scenario, true_graph, observed_graph, current_outcome,
        selections, results, learner)


def monte_carlo_sweep(
    scenario: Scenario,
    *,
    change_id: str,
    completeness_values=(0.5, 0.65, 0.8, 0.95),
    repetitions: int = 10,
    budget: float = 22.0,
    false_edge_rate: float = 0.03,
) -> pd.DataFrame:
    """Sweep engineering-knowledge completeness without tuning to truth."""
    rows = []
    for completeness in completeness_values:
        for rep in range(repetitions):
            bundle = run_comparison(
                scenario,
                change_id=change_id,
                graph_seed=1000 + rep,
                propagation_seed=2000 + rep,
                detection_seed=3000 + rep,
                completeness=float(completeness),
                false_edge_rate=false_edge_rate,
                budget=budget,
            )
            for label, row in bundle.results.iterrows():
                record = row.to_dict()
                record["label"] = label
                record["completeness"] = float(completeness)
                record["rep"] = rep
                rows.append(record)
    return pd.DataFrame(rows)
