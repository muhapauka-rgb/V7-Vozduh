from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


def load_lib():
    spec = importlib.util.spec_from_file_location(
        "v7_sync_lib_mission_integrity", ROOT / "tools/v7_sync_lib.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class OmpMissionIntegrityScenarioMatrixTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()

    def intent(self):
        return self.lib.mission_intent_contract(
            mission_id="V7_MISSION_INTEGRITY_SCENARIO_MATRIX_V1",
            objective="Complete the bounded optimization loop without changing its objective.",
            required_outcomes=["bridge", "second_domain", "anti_regrowth"],
            definition_of_done=["all_required_outcomes_proven", "reviews_bound", "same_mission"],
            authorized_effect_boundary=["ENGINEERING_READ_ONLY", "SOURCE_TESTS"],
            prohibited_effects=["RUNTIME", "PRODUCTION", "AUTHORITY_EXPANSION", "NEW_OWNER"],
            owner_authority_boundary=["OMP", "MISSION_COMPLETION_EVIDENCE_GATE"],
            required_reviews=["ARCHITECTURE", "SAFETY", "EVIDENCE", "MISSION_INTEGRITY"],
            legal_terminals=["FULL_COMPLETION", "MISSION_CLARIFICATION_REQUIRED", "STOP_SAFE_EXACT_GAP"],
            intermediate_non_terminals=["BRIDGE_IMPLEMENTED", "TESTS_PASS", "REPORT_CREATED"],
            continuation_policy="CONTINUE_SAME_MISSION_WHILE_AUTHORIZED_WORK_REMAINS",
            input_fingerprint="a" * 64,
            repo_fingerprint="b" * 64,
        )

    def adaptation(self, **overrides):
        values = {
            "adaptation_class": "LOCAL_EXECUTION_ADAPTATION",
            "discovered_fact": "existing owner already provides the required mapping",
            "original_proposed_method": "add a new mapping",
            "adapted_method": "reuse existing owner mapping",
            "objective_preserved": True,
            "definition_of_done_preserved": True,
            "effect_boundary_preserved_or_narrowed": True,
            "owner_boundary_preserved": True,
            "pending_required_outcomes": ["second_domain", "anti_regrowth"],
            "completed_required_outcomes": ["bridge"],
            "continuation_action": "execute second_domain",
            "evidence_references": ["tools/v7_sync_lib.py"],
        }
        values.update(overrides)
        return self.lib.mission_adaptation_record(self.intent(), **values)

    def bind(self, **overrides):
        contract = {
            "MISSION_INTENT_CONTRACT": self.intent(),
            "MISSION_ADAPTATION_RECORDS": [],
            "PROVEN_COMPLETED_OUTCOMES": ["bridge"],
            "REMAINING_AUTHORIZED_WORK": ["second_domain", "anti_regrowth"],
            "REQUESTED_MISSION_TERMINAL": "BRIDGE_IMPLEMENTED",
            "MISSION_TERMINAL_EVIDENCE": {},
            "NEXT_EXECUTABLE_ACTION": "execute second_domain",
        }
        contract.update(overrides)
        return self.lib.mission_integrity_completion_binding(contract)

    def test_01_reuse_existing_mechanism_is_local_adaptation_same_mission(self):
        result = self.bind(MISSION_ADAPTATION_RECORDS=[self.adaptation()])
        self.assertEqual(result["terminal_class"], "CONTINUE_SAME_MISSION")
        self.assertTrue(result["no_user_prompt_required"])

    def test_02_reorder_internal_steps_is_local_adaptation(self):
        record = self.adaptation(
            discovered_fact="dependency order differs",
            original_proposed_method="counterfactual before discovery",
            adapted_method="discovery before counterfactual",
        )
        result = self.bind(MISSION_ADAPTATION_RECORDS=[record])
        self.assertEqual(result["adaptation_status"][0]["final_verdict"], "PASS")

    def test_03_narrow_change_scope_preserves_effect_boundary(self):
        record = self.adaptation(adapted_method="change only the existing bridge owner")
        result = self.bind(MISSION_ADAPTATION_RECORDS=[record])
        self.assertEqual(result["terminal_class"], "CONTINUE_SAME_MISSION")

    def test_04_first_hypothesis_falsified_continues_to_remaining_candidate(self):
        result = self.bind(
            PROVEN_COMPLETED_OUTCOMES=["bridge"],
            REMAINING_AUTHORIZED_WORK=["second_domain", "anti_regrowth"],
            REQUESTED_MISSION_TERMINAL="FIRST_HYPOTHESIS_FALSIFIED",
        )
        self.assertEqual(result["terminal_class"], "CONTINUE_SAME_MISSION")

    def test_05_microstep_as_terminal_is_rejected(self):
        result = self.bind()
        self.assertEqual(result["terminal_class"], "CONTINUE_SAME_MISSION")
        self.assertIn("mission_intermediate_milestone_requested_as_terminal", result["errors"])

    def test_06_tests_pass_but_outcome_missing_is_rejected(self):
        result = self.bind(REQUESTED_MISSION_TERMINAL="TESTS_PASS")
        self.assertEqual(result["terminal_class"], "CONTINUE_SAME_MISSION")
        self.assertIn("anti_regrowth", result["unmet_outcomes"])

    def test_07_report_created_but_outcome_missing_is_rejected(self):
        result = self.bind(REQUESTED_MISSION_TERMINAL="REPORT_CREATED")
        self.assertEqual(result["terminal_class"], "CONTINUE_SAME_MISSION")

    def test_08_fake_stop_safe_for_unfinished_work_is_rejected(self):
        evidence = {
            "exact_blocking_fact": "anti-regrowth not implemented", "evidence": "current source",
            "violated_invariant_or_missing_authority": "none", "responsible_owner": "OMP",
            "last_proven_output": "bridge", "minimal_next_action": "implement anti-regrowth",
            "reentry_condition": "continue now", "blocker_class": "UNFINISHED_AUTHORIZED_WORK",
        }
        result = self.bind(
            REQUESTED_MISSION_TERMINAL="STOP_SAFE_EXACT_GAP",
            MISSION_TERMINAL_EVIDENCE=evidence,
        )
        self.assertEqual(result["terminal_class"], "CONTINUE_SAME_MISSION")
        self.assertIn("mission_fake_stop_safe_unfinished_authorized_work", result["errors"])

    def test_09_real_safety_gap_accepts_exact_stop_safe(self):
        evidence = {
            "exact_blocking_fact": "mutation requires unavailable Authority", "evidence": "authority record absent",
            "violated_invariant_or_missing_authority": "CURRENT_AUTHORITY_REQUIRED", "responsible_owner": "Authority",
            "last_proven_output": "read-only analysis", "minimal_next_action": "obtain Authority decision",
            "reentry_condition": "fresh exact Authority record", "blocker_class": "NEW_AUTHORITY_GAP",
        }
        result = self.bind(
            REQUESTED_MISSION_TERMINAL="STOP_SAFE_EXACT_GAP",
            MISSION_TERMINAL_EVIDENCE=evidence,
        )
        self.assertEqual(result["terminal_class"], "STOP_SAFE_EXACT_GAP_ACCEPTED")

    def test_10_real_owner_decision_accepts_clarification(self):
        evidence = {
            "exact_ambiguity": "two mutually exclusive product semantics",
            "exact_alternatives": ["A", "B"], "alternative_impacts": ["behavior A", "behavior B"],
            "canonical_owner_resolution_failure": "no current product rule", "exact_decision_requested": "choose A or B",
            "last_safe_proven_output": "read-only comparison", "reentry_condition": "owner decision received",
            "choice_class": "PRODUCT_SEMANTIC_CHOICE",
        }
        result = self.bind(
            REQUESTED_MISSION_TERMINAL="MISSION_CLARIFICATION_REQUIRED",
            MISSION_TERMINAL_EVIDENCE=evidence,
        )
        self.assertEqual(result["terminal_class"], "MISSION_CLARIFICATION_REQUIRED_ACCEPTED")

    def test_11_adaptation_expanding_authority_is_rejected(self):
        record = self.adaptation(effect_boundary_preserved_or_narrowed=False)
        result = self.bind(MISSION_ADAPTATION_RECORDS=[record])
        self.assertEqual(result["terminal_class"], "MISSION_INTEGRITY_REJECTED")
        self.assertIn("mission_local_adaptation_boundary_expanded", result["errors"])

    def test_12_definition_of_done_silent_narrowing_is_rejected(self):
        result = self.bind(CLAIMED_DEFINITION_OF_DONE=["bridge_only"])
        self.assertEqual(result["terminal_class"], "MISSION_INTEGRITY_REJECTED")

    def test_13_next_mission_cannot_carry_current_remainder(self):
        result = self.bind(NEXT_MISSION_REQUIRED_OUTCOMES=["anti_regrowth"])
        self.assertEqual(result["terminal_class"], "CONTINUE_SAME_MISSION")
        self.assertIn("next_mission_carries_current_remainder", result["errors"])
        self.assertFalse(result["no_new_mission"])

    def test_14_full_completion_after_adaptation_is_accepted(self):
        result = self.bind(
            MISSION_ADAPTATION_RECORDS=[self.adaptation(
                pending_required_outcomes=[],
                completed_required_outcomes=["bridge", "second_domain", "anti_regrowth"],
                continuation_action="consume final terminal",
            )],
            PROVEN_COMPLETED_OUTCOMES=["bridge", "second_domain", "anti_regrowth"],
            REMAINING_AUTHORIZED_WORK=[], REQUESTED_MISSION_TERMINAL="FULL_COMPLETION",
        )
        self.assertEqual(result["terminal_class"], "FULL_COMPLETION_ACCEPTED")
        self.assertEqual(result["final_verdict"], "PASS")

    def test_15_legacy_mission_without_intent_preserves_existing_behavior(self):
        result = self.lib.mission_completion_evidence_gate({
            "MISSION_TYPE": "ACCEPTANCE", "COMPLETION_CONTRACT": "ACCEPTANCE_COMPLETION",
            "INDEPENDENT_ACCEPTANCE_PROVEN": True, "NEXT_OUTPUT_PROVEN": True,
        })
        self.assertEqual(result["completion_verdict"], "COMPLETE_WITH_LEGAL_TERMINAL")
        self.assertFalse(result["mission_integrity_governed"])

    def test_16_stale_or_mismatched_intent_fails_closed(self):
        intent = copy.deepcopy(self.intent())
        intent["objective"] = "silently changed objective"
        result = self.bind(MISSION_INTENT_CONTRACT=intent)
        self.assertEqual(result["terminal_class"], "MISSION_INTEGRITY_REJECTED")
        self.assertIn("mission_intent_fingerprint_mismatch", result["errors"])

    def test_17_duplicate_adaptation_is_idempotent(self):
        record = self.adaptation()
        result = self.bind(MISSION_ADAPTATION_RECORDS=[record, copy.deepcopy(record)])
        self.assertTrue(result["adaptation_status"][1]["duplicate"])
        self.assertTrue(result["duplicate_adaptations_idempotent"])

    def test_18_changed_duplicate_adaptation_identity_is_rejected(self):
        first = self.adaptation()
        changed = copy.deepcopy(first)
        changed["adapted_method"] = "different method under same adaptation identity"
        changed["adaptation_fingerprint"] = self.lib._execution_contract_fingerprint({
            key: value for key, value in changed.items() if key != "adaptation_fingerprint"
        })
        result = self.bind(MISSION_ADAPTATION_RECORDS=[first, changed])
        self.assertIn("mission_adaptation_identity_conflict", result["errors"])

    def test_19_gpt_decision_review_reuses_same_intent_contract(self):
        intent = self.intent()
        profile = self.lib.gpt_decision_review_profile_contract(
            mission_id=intent["mission_id"], run_nonce="gpt-intent-review-v1",
            input_fingerprint=intent["input_fingerprint"], repo_fingerprint=intent["repo_fingerprint"],
            mission_intent_fingerprint=intent["mission_intent_fingerprint"],
        )
        admitted = self.lib.admit_execution_profile_contract(
            profile, mission_id=intent["mission_id"],
        )
        self.assertEqual(admitted["final_verdict"], "PASS")
        self.assertEqual(admitted["required_reviews"], [
            "ARCHITECTURE_REVIEW", "MISSION_INTEGRITY_REVIEW",
        ])

    def test_20_clarification_for_local_implementation_choice_is_rejected(self):
        evidence = {
            "exact_ambiguity": "which existing helper to reuse", "exact_alternatives": ["A", "B"],
            "alternative_impacts": ["same objective", "same objective"],
            "canonical_owner_resolution_failure": "none", "exact_decision_requested": "choose helper",
            "last_safe_proven_output": "discovery", "reentry_condition": "choice received",
            "choice_class": "LOCAL_IMPLEMENTATION_CHOICE",
        }
        result = self.bind(
            REQUESTED_MISSION_TERMINAL="MISSION_CLARIFICATION_REQUIRED",
            MISSION_TERMINAL_EVIDENCE=evidence,
        )
        self.assertEqual(result["terminal_class"], "CONTINUE_SAME_MISSION")
        self.assertIn("mission_clarification_used_for_local_choice", result["errors"])


if __name__ == "__main__":
    unittest.main()
