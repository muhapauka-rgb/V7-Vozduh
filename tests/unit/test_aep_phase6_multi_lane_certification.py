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
        self.assertEqual(lanes["PHASE_6A_STATUS"], "ACTIVE")
        self.assertEqual(lanes["PHASE_6_GLOBAL_STATUS"], "ACTIVE_MULTI_LANE_CERTIFICATION")
        self.assertNotEqual(lanes["PHASE_6_GLOBAL_STOP"], "REAL_WORLD_LIMIT")

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


if __name__ == "__main__":
    unittest.main()
