from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_phase6_multi_lane", ROOT / "tools/v7_sync_lib.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class AepPhase6MultiLaneCertificationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.cps = (ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text()

    def test_natural_wait_does_not_block_scenario_lane(self):
        frontier = self.lib.future_scale_scenario_frontier(self.cps, root=ROOT)
        lanes = self.lib.phase6_multi_lane_reconciliation(self.cps, frontier)
        self.assertEqual(lanes["PHASE_6C_STATUS"], "WAITING_NATURAL_PRODUCTION_EVIDENCE")
        self.assertEqual(lanes["PHASE_6A_STATUS"], "SCENARIO_FRONTIER_EXHAUSTED_CURRENT_GENERATION")
        self.assertEqual(lanes["PHASE_6_GLOBAL_STATUS"], "LANES_EXHAUSTED_WAITING_NATURAL_EVIDENCE")
        self.assertEqual(
            lanes["PHASE_6_GLOBAL_STOP"],
            "REAL_WORLD_LIMIT_AFTER_SCENARIO_AND_CONTROLLED_CERTIFICATION_EXHAUSTION",
        )

    def test_controlled_preparation_is_independent_and_no_action_selected(self):
        frontier = self.lib.future_scale_scenario_frontier(self.cps, root=ROOT)
        lanes = self.lib.phase6_multi_lane_reconciliation(self.cps, frontier, trace_capture_ready=False)
        self.assertEqual(lanes["PHASE_6B_STATUS"], "CONTROLLED_PRODUCTION_PREPARATION_READY")
        self.assertIn("PHASE6B_TRACE_COMPLETENESS_PREPARATION", lanes["PHASE_6_EXECUTABLE_FRONTIER"])
        self.assertIn("NO_ACTION_SELECTED", lanes["PHASE_6B_AUTHORITY_STATUS"])

    def test_evidence_classes_are_non_interchangeable(self):
        rejected = self.lib.phase6_evidence_classification(
            "ENGINEERING_SCENARIO_EVIDENCE", "NATURAL_REPRESENTATIVENESS",
        )
        accepted = self.lib.phase6_evidence_classification(
            "NATURAL_PRODUCTION_EVIDENCE", "NATURAL_REPRESENTATIVENESS",
        )
        self.assertFalse(rejected["accepted_for_criterion"])
        self.assertTrue(rejected["natural_representativeness_pending"])
        self.assertTrue(accepted["accepted_for_criterion"])

    def test_phase7_engineering_active_authority_locked(self):
        frontier = self.lib.future_scale_scenario_frontier(self.cps, root=ROOT)
        lanes = self.lib.phase6_multi_lane_reconciliation(self.cps, frontier)
        self.assertEqual(
            lanes["PHASE_7_ENGINEERING_EVOLUTION_STATUS"],
            "PHASE_7_ENGINEERING_CONTINUOUS_EVOLUTION_ACTIVE",
        )
        self.assertEqual(
            lanes["PHASE_7_PRODUCTION_AUTHORITY_STATUS"],
            "LOCKED_PENDING_NATURAL_AND_CONTROLLED_CERTIFICATION",
        )

    def test_new_obligation_generation_reuses_existing_corpus_and_consumer(self):
        corpus = self.lib.load_future_scale_scenario_corpus(root=ROOT)
        obligations = [
            row for row in corpus["scenarios"]
            if row.get("OBLIGATION_GENERATION") == "PHASE6_MULTI_LANE_V1"
        ]
        self.assertEqual(len(obligations), 6)
        result = self.lib.execute_future_scale_scenario(obligations[0]["SCENARIO_ID"], root=ROOT)
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertTrue(result["consumer_result"]["consumed"])
        self.assertEqual(result["situation_decision_trace"]["learning"]["natural_production_credit"], False)
        self.assertFalse(any(result["forbidden_effects"].values()))

    def test_v2_v3_v4_obligations_are_owner_ordered_and_frontier_is_exhausted(self):
        corpus = self.lib.load_future_scale_scenario_corpus(root=ROOT)
        for generation in (2, 3, 4):
            obligations = [
                row for row in corpus["scenarios"]
                if row.get("OBLIGATION_GENERATION") == f"PHASE6_MULTI_LANE_V{generation}"
            ]
            self.assertEqual(len(obligations), 6)
            self.assertEqual(
                [row["OBLIGATION_PRIORITY"] for row in obligations], list(range(6)),
            )
            self.assertTrue(all(row["OBLIGATION_SOURCE_CRITERIA"] for row in obligations))
            self.assertTrue(all(row["INVALIDATION_TRIGGERS"] for row in obligations))
        frontier = self.lib.future_scale_scenario_frontier(self.cps, root=ROOT)
        self.assertEqual(frontier["NEXT_SCENARIO_ID"], "NONE")
        self.assertEqual(len(frontier["COVERED_SCENARIOS"]), 64)
        self.assertEqual(len(frontier["ELIGIBLE_SCENARIOS"]), 0)

    def test_comprehensive_campaign_consumes_engineering_frontier_at_exact_boundary(self):
        result = self.lib.comprehensive_phase6_phase7_campaign_reconciliation(
            self.cps, root=ROOT,
        )
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertEqual(result["completion_gate"]["completion_contract"], "PROGRAM_COMPLETION")
        self.assertEqual(result["completion_gate"]["completion_verdict"], "COMPLETE_CONSUMED")
        self.assertEqual(result["scenario_covered_count"], 64)
        self.assertEqual(len(result["scenario_generations_closed"]), 4)
        self.assertEqual(
            result["action_class_certification"]["state"], "CERTIFIED_FOR_CLASS_APPROVAL",
        )
        self.assertFalse(any(row["whole_capability_complete"] for row in result["capability_reconciliation"]))
        self.assertEqual(result["runtime_impact"], "NONE")
        self.assertEqual(result["authority_impact"], "NONE")

    def test_exhausted_corpus_is_a_legal_bounded_continuation_not_missing_frontier(self):
        result = self.lib.continue_phase6a_obligation_corpus(root=ROOT)
        self.assertEqual(result["final_verdict"], "BOUNDED_CONTINUATION")
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["scenarios_executed"], 0)
        self.assertEqual(
            result["program_terminal"],
            "PHASE6A_CURRENT_GENERATION_CERTIFIED_OBLIGATION_DISCOVERY_REQUIRED",
        )

    def test_first_v2_scenario_has_complete_trace_and_no_forbidden_credit(self):
        result = self.lib.execute_future_scale_scenario(
            "PHASE6V2_MULTI_SIGNAL_INTERPRETATION_CONFLICT", root=ROOT,
        )
        self.assertEqual(result["final_verdict"], "PASS")
        trace = result["situation_decision_trace"]
        for key in (
            "scenario_id", "situation_id", "situation_class", "evidence_class",
            "source_context_fingerprint", "applicable_knowledge", "applicable_policies",
            "possible_decisions", "selected_decision", "rejected_alternatives",
            "expected_benefit", "state_change_cost", "decision_trace_id",
            "decision_fingerprint", "deterministic_replay_result", "expected_terminal",
            "actual_terminal", "verification", "rollback", "learning",
            "capability_criteria_affected", "production_maturity_impact",
            "authority_impact", "forbidden_claims",
        ):
            self.assertIn(key, trace)
        self.assertTrue(all(result["evidence_taxonomy_verification"].values()))
        self.assertFalse(any(result["forbidden_effects"].values()))


if __name__ == "__main__":
    unittest.main()
