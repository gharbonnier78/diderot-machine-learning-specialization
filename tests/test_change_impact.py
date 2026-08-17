from pathlib import Path
import unittest

from diderot_mls.change_impact import (
    build_graph,
    evaluate_selection,
    load_scenario,
    observe_graph,
    select_r0_full,
    select_r2_code_graph,
    simulate_change,
)
from diderot_mls.change_impact.experiment import run_comparison


SCENARIO = (
    Path(__file__).parents[1]
    / "labs"
    / "change-impact-regression"
    / "scenarios"
    / "identity_platform.yaml"
)


class ChangeImpactLabTests(unittest.TestCase):
    def test_scenario_loads_and_validates(self):
        scenario = load_scenario(SCENARIO)
        self.assertGreaterEqual(len(scenario.nodes), 15)
        self.assertGreaterEqual(len(scenario.edges), 25)
        self.assertGreaterEqual(len(scenario.tests), 12)
        self.assertGreaterEqual(len(scenario.changes), 4)

    def test_observed_graph_hides_explicit_hidden_edges(self):
        scenario = load_scenario(SCENARIO)
        true_graph = build_graph(scenario)
        observed = observe_graph(
            true_graph, completeness=1.0, false_edge_rate=0.0, seed=7)
        hidden = [edge for edge in scenario.edges if not edge.visible]
        self.assertTrue(hidden)
        for edge in hidden:
            matching = [
                data
                for u, v, data in observed.edges(data=True)
                if u == edge.source
                and v == edge.target
                and data.get("mechanism") == edge.mechanism
            ]
            self.assertFalse(matching)

    def test_propagation_is_reproducible_for_same_seed(self):
        scenario = load_scenario(SCENARIO)
        graph = build_graph(scenario)
        change = scenario.changes["CHG_CACHE_TTL"]
        a = simulate_change(scenario, graph, change, seed=123)
        b = simulate_change(scenario, graph, change, seed=123)
        self.assertEqual(a.impacted, b.impacted)
        self.assertEqual(a.traversed_edges, b.traversed_edges)

    def test_budgeted_selectors_respect_budget(self):
        scenario = load_scenario(SCENARIO)
        bundle = run_comparison(
            scenario, change_id="CHG_EVENTBUS_POOL", budget=18.0)
        for label, selection in bundle.selections.items():
            if label == "R0":
                continue
            self.assertLessEqual(selection.total_cost(scenario), 18.0 + 1e-9)

    def test_full_suite_pod_not_lower_than_subset_for_same_outcome(self):
        scenario = load_scenario(SCENARIO)
        true_graph = build_graph(scenario)
        observed = observe_graph(
            true_graph, completeness=0.7, false_edge_rate=0.0, seed=3)
        change = scenario.changes["CHG_SUPPLIER_SDK"]
        outcome = simulate_change(scenario, true_graph, change, seed=9)
        full = select_r0_full(scenario)
        subset = select_r2_code_graph(
            scenario, observed, change, budget=12.0)
        full_eval = evaluate_selection(scenario, outcome, full, seed=1)
        subset_eval = evaluate_selection(scenario, outcome, subset, seed=1)
        self.assertGreaterEqual(full_eval.mean_pod + 1e-12,
                                subset_eval.mean_pod)
        self.assertGreaterEqual(full_eval.critical_mean_pod + 1e-12,
                                subset_eval.critical_mean_pod)

    def test_ai_assisted_strategy_runs_from_historical_labels(self):
        scenario = load_scenario(SCENARIO)
        bundle = run_comparison(
            scenario,
            change_id="CHG_IDENTITY_EVENT_V2",
            history_repetitions=3,
        )
        self.assertTrue(bundle.learner._is_fit)
        self.assertIn("R5", bundle.selections)
        self.assertTrue(bundle.selections["R5"].selected_tests)


if __name__ == "__main__":
    unittest.main()
