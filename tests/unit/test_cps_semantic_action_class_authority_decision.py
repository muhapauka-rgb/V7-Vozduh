from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


def load_lib():
    spec = importlib.util.spec_from_file_location(
        "v7_cps_semantic_action_class_authority", ROOT / "tools/v7_sync_lib.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class CpsSemanticActionClassAuthorityDecisionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.cps = (ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text()
        cls.result = cls.lib.action_class_authority_decision_reconciliation(
            cls.cps, root=ROOT, consumer_proven=True,
        )

    def test_completed_scenario_frontier_cannot_remain_live(self):
        self.assertTrue(self.result["frontier_exhausted"])
        self.assertEqual(self.result["scenario_corpus_count"], 64)
        self.assertEqual(self.result["scenario_covered_count"], 64)
        self.assertEqual(self.result["stale_live_projections"], [])
        live = self.lib._markdown_field_table(self.lib._markdown_section(
            self.cps, "## 0. Authoritative Live Current State",
            "## Authoritative Unfinished Capability Closure Registry",
        ))
        self.assertEqual(
            live["PHASE_6_CERTIFICATION_FRONTIER"].strip("`"),
            "NONE",
        )
        self.assertFalse(live["PHASE_6_EXACT_NEXT_ACTION"].strip("`").startswith("EXECUTE PHASE6"))

    def test_phase6a_exhausted_semantics_have_no_next_scenario(self):
        self.assertEqual(
            self.result["phase6a_status"], "SCENARIO_FRONTIER_EXHAUSTED_CURRENT_GENERATION",
        )
        frontier = self.lib.future_scale_scenario_frontier(self.cps, root=ROOT)
        self.assertEqual(frontier["NEXT_SCENARIO_ID"], "NONE")

    def test_certification_recommendation_and_authority_are_separate(self):
        self.assertEqual(self.result["exact_action_class_state"], "GOVERNED_ONLY")
        self.assertEqual(self.result["action_class_certification_state"], "REVALIDATION_REQUIRED")
        self.assertEqual(
            self.result["authority_recommendation_state"],
            "AUTHORITY_RECOMMENDATION_BLOCKED_BY_REAL_WORLD_EVIDENCE",
        )
        self.assertIn("CLASS_AUTHORITY_NOT_GRANTED", self.result["granted_authority_state"])

    def test_no_current_candidate_packet_or_lease(self):
        self.assertTrue(self.result["active_identities_clear"])
        self.assertTrue(all(value == "NONE" for value in self.result["active_identities"].values()))

    def test_global_real_world_limit_is_legal_and_no_approval_is_requested(self):
        self.assertEqual(self.result["current_stop"], "REAL_WORLD_LIMIT")
        self.assertFalse(self.result["operator_approval_required_now"])
        self.assertEqual(self.result["operator_question"], "NONE")

    def test_u07_protected_wip_and_omp_terminal_are_preserved(self):
        live = self.lib._markdown_field_table(self.lib._markdown_section(
            self.cps, "## 0. Authoritative Live Current State",
            "## Authoritative Unfinished Capability Closure Registry",
        ))
        self.assertIn("CAP-U07", live["PROTECTED_CAPABILITY_WIP"])
        self.assertEqual(live["OMP_CONTINUATION_REQUIRED"].strip("`"), "FALSE")
        self.assertEqual(
            live["PROGRAM_TERMINAL_CLASS"].strip("`"),
            self.lib.PERMANENT_POLYGON_TARGET_LEVEL_TERMINAL,
        )

    def test_reentry_requires_fresh_owner_backed_input(self):
        self.assertEqual(self.result["exact_next_action"], "WAIT_FOR_FRESH_QUALIFYING_CONTROLLED_OR_NATURAL_OUTCOME")
        self.assertEqual(set(self.result["exact_reentry_conditions"]), {
            "FRESH_ELIGIBLE_CONTROLLED_WINDOW",
            "NEW_MATERIAL_NON_SYNTHETIC_OUTCOME_WITH_COMPLETE_TRACE_AND_LEARNING",
            "NEW_OWNER_BACKED_OBLIGATION",
        })
        self.assertNotIn("STALE_SCENARIO_FIELD", self.result["exact_reentry_conditions"])

    def test_criterion_audit_is_complete_and_non_interchangeable(self):
        rows = {row["criterion"]: row for row in self.result["criterion_audit"]}
        self.assertGreaterEqual(len(rows), 28)
        self.assertEqual(rows["scenario correctness"]["evidence_class"], "ENGINEERING_SCENARIO_EVIDENCE")
        self.assertEqual(rows["natural production evidence"]["state"], "INSUFFICIENT")
        self.assertEqual(rows["class Authority"]["state"], "NOT_GRANTED")

    def test_no_packet_policy_authority_or_production_mutation(self):
        self.assertEqual(self.result["packet_execution"], "NONE")
        self.assertEqual(self.result["authority_impact"], "NONE")
        self.assertEqual(self.result["policy_impact"], "NONE")
        self.assertEqual((self.result["runtime_impact"], self.result["routing_impact"], self.result["user_movement"]), ("NONE", "NONE", 0))

    def test_mission_completion_gate_passes_only_with_consumer(self):
        incomplete = self.lib.action_class_authority_decision_reconciliation(
            self.cps, root=ROOT, consumer_proven=False,
        )
        self.assertEqual(incomplete["completion_gate"]["completion_verdict"], "INTEGRATION_INCOMPLETE")
        self.assertEqual(self.result["completion_gate"]["completion_verdict"], "COMPLETE_CONSUMED")

    def test_reconciliation_is_deterministic(self):
        replay = self.lib.action_class_authority_decision_reconciliation(
            self.cps, root=ROOT, consumer_proven=True,
        )
        self.assertEqual(self.result, replay)


if __name__ == "__main__":
    unittest.main()
