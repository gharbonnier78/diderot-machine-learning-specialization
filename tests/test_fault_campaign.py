from pathlib import Path
import unittest

from diderot_mls.change_impact import (
    InjectedFault,
    evaluate_fault_campaign,
    load_scenario,
    select_r0_full,
)
from diderot_mls.change_impact.selectors import SelectionResult


SCENARIO = (
    Path(__file__).parents[1]
    / "labs"
    / "change-impact-regression"
    / "scenarios"
    / "identity_platform.yaml"
)


class FaultCampaignTests(unittest.TestCase):
    def test_covered_node_can_have_zero_detection_for_wrong_oracle(self):
        scenario = load_scenario(SCENARIO)
        selection = SelectionResult(
            strategy="oracle_gap_probe",
            selected_tests=["T_UNIT_IDENTITY"],
            predicted_impacts={"identity_service"},
        )
        fault = InjectedFault(
            id="F_identity_authorization",
            node="identity_service",
            failure_mode="authorization",
            criticality=5.0,
        )
        result = evaluate_fault_campaign(
            scenario, selection, [fault], seed=1).iloc[0]
        self.assertTrue(bool(result["covered"]))
        self.assertEqual(float(result["pod"]), 0.0)

    def test_full_suite_fault_campaign_is_nonempty(self):
        scenario = load_scenario(SCENARIO)
        full = select_r0_full(scenario)
        faults = [
            InjectedFault("F_cache_stale", "session_cache", "stale_state", 5.0),
            InjectedFault("F_event_schema", "event_bus", "schema_mismatch", 4.0),
        ]
        result = evaluate_fault_campaign(scenario, full, faults, seed=2)
        self.assertEqual(len(result), 2)
        self.assertTrue((result["pod"] > 0).all())


if __name__ == "__main__":
    unittest.main()
