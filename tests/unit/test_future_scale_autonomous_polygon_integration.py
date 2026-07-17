from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_fsse04_test", ROOT / "tools/v7_sync_lib.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FutureScaleAutonomousPolygonIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        dependencies = ["CERTIFICATION:FSSE04_LEASE_CONFLICT_INPUT_V1"]
        ordinary_exhausted = {"final_verdict": "PASS", "executable_program_frontier": []}
        with mock.patch.object(cls.lib, "program_execution_reconciliation", return_value=ordinary_exhausted):
            cls.result = cls.lib.continue_omp_engineering_control_loop(root=ROOT, changed_dependencies=dependencies)
            cls.replay = cls.lib.continue_omp_engineering_control_loop(root=ROOT, changed_dependencies=dependencies)

    def test_01_standard_trigger(self):
        self.assertEqual(self.result["trigger"], "Continue OMP")

    def test_02_existing_entrypoint(self):
        self.assertEqual(self.result["entrypoint"], "tools/v7-truth-check --continue-omp")

    def test_03_real_non_test_caller(self):
        self.assertEqual(self.result["real_caller"], "continue_omp_engineering_control_loop")

    def test_04_real_consumer(self):
        self.assertEqual(self.result["real_consumer"], "OMP_PROGRAM_EXECUTION_RECONCILIATION")

    def test_05_ordinary_frontier_is_evaluated_first(self):
        self.assertEqual(self.result["ordinary_frontier"], [])
        self.assertEqual(self.result["priority_decision"], "SCENARIO_FRONTIER_AFTER_ORDINARY_EXHAUSTION")

    def test_06_capability_wait_does_not_block_fsse(self):
        self.assertEqual(self.result["final_verdict"], "PASS")

    def test_07_multiple_internal_transitions(self):
        self.assertGreaterEqual(self.result["internal_iteration_count"], 3)

    def test_08_no_prompt_between_steps(self):
        self.assertTrue(all(row["no_user_prompt"] for row in self.result["transitions"]))

    def test_09_no_heartbeat_between_steps(self):
        self.assertTrue(all(not row["heartbeat_invoked"] for row in self.result["transitions"]))

    def test_10_selective_invalidation_exact_subset(self):
        self.assertEqual(self.result["selective_invalidation"]["affected_scenarios"], ["LEASE_CONFLICT"])

    def test_11_unrelated_scenarios_remain_current(self):
        self.assertEqual(len(self.result["selective_invalidation"]["unrelated_scenarios"]), 45)

    def test_12_coverage_transitions_46_45_46(self):
        self.assertEqual((self.result["coverage_before"], self.result["coverage_after_invalidation"], self.result["coverage_after"]), (46, 45, 46))

    def test_13_real_scenario_execution(self):
        self.assertEqual(self.result["scenario_result"]["scenario_id"], "LEASE_CONFLICT")
        self.assertEqual(self.result["scenario_result"]["final_verdict"], "PASS")

    def test_14_invariants_are_evaluated(self):
        self.assertTrue(self.result["scenario_result"]["invariant_verdicts"])
        self.assertTrue(all(row["verdict"] == "PASS" for row in self.result["scenario_result"]["invariant_verdicts"]))

    def test_15_result_identity_validation(self):
        self.assertEqual(self.result["consumer"]["identity_validation"], "PASS")
        self.assertTrue(all(self.result["consumer"]["identity_checks"].values()))

    def test_16_dependency_binding_validation(self):
        self.assertEqual(self.result["consumer"]["dependency_binding"]["final_verdict"], "PASS")

    def test_17_pass_changes_frontier(self):
        self.assertEqual(self.result["consumer"]["behavior_change"], "SCENARIO_COVERED_AND_NEXT_FRONTIER_MATERIALIZED")

    def test_18_duplicate_result_is_idempotent(self):
        duplicate = self.result["duplicate_result_consumption"]
        self.assertEqual(duplicate["behavior_change"], "DUPLICATE_RESULT_SUPPRESSED")
        self.assertFalse(duplicate["coverage_changed"])

    def test_19_certification_mismatch_is_not_product_defect(self):
        classification = self.result["mismatch_classification_evidence"]
        self.assertFalse(classification["product_candidate_allowed"])
        self.assertTrue(classification["certification_candidate_allowed"])

    def test_20_fixture_defect_excluded_from_bdp(self):
        self.assertFalse(self.lib.classify_future_scale_mismatch("INVALID_FIXTURE")["bdp_eligible"])

    def test_21_harness_defect_excluded_from_bdp(self):
        self.assertFalse(self.lib.classify_future_scale_mismatch("HARNESS_DEFECT")["bdp_eligible"])

    def test_22_oracle_defect_excluded_from_bdp(self):
        self.assertFalse(self.lib.classify_future_scale_mismatch("ORACLE_DEFECT")["bdp_eligible"])

    def test_23_generator_defect_excluded_from_bdp(self):
        self.assertFalse(self.lib.classify_future_scale_mismatch("GENERATOR_DEFECT")["bdp_eligible"])

    def test_24_real_source_mismatch_routes_to_bdp(self):
        classification = self.lib.classify_future_scale_mismatch("REPRODUCIBLE_REAL_SOURCE_MISMATCH")
        self.assertTrue(classification["bdp_eligible"])
        self.assertTrue(classification["product_candidate_allowed"])

    def test_25_unknown_mismatch_fails_closed(self):
        self.assertEqual(self.lib.classify_future_scale_mismatch("UNKNOWN")["final_verdict"], "STOP_SAFE")

    def test_26_candidate_reality_gate_and_admission(self):
        bdp = self.result["bdp_candidate_mission_result"]
        self.assertEqual(bdp["admission_decision"], "MISSION_ACCEPTED")
        self.assertTrue(bdp["mission_created"])

    def test_27_candidate_identity_is_stable(self):
        first = self.result["bdp_candidate_mission_result"]["candidate"]["candidate_instance_id"]
        second = self.replay["bdp_candidate_mission_result"]["candidate"]["candidate_instance_id"]
        self.assertEqual(first, second)

    def test_28_duplicate_candidate_suppressed(self):
        self.assertEqual(self.result["duplicate_candidate_result"]["handoff_status"], "DUPLICATE_SUPPRESSED")

    def test_29_single_active_mission(self):
        self.assertTrue(self.result["single_active_mission"])

    def test_30_isolated_repair_executes(self):
        self.assertEqual(self.result["repair_result"], "CERTIFICATION_INPUT_REPAIRED")

    def test_31_target_rerun_passes(self):
        self.assertEqual(self.result["target_rerun"]["final_verdict"], "PASS")

    def test_32_affected_replay_matches_target(self):
        self.assertEqual(self.result["affected_replay"]["final_verdict"], "PASS")
        self.assertEqual(self.result["target_rerun"]["result_fingerprint"], self.result["affected_replay"]["result_fingerprint"])

    def test_33_engineering_intent_closes(self):
        self.assertEqual(self.result["engineering_intent_closure"], "INTENT_CLOSED")

    def test_34_budgets_are_bounded(self):
        self.assertLessEqual(self.result["budgets"]["iterations"], self.lib.OMP_CONTINUATION_MAX_ITERATIONS)
        self.assertLessEqual(self.result["budgets"]["scenarios"], self.lib.OMP_CONTINUATION_SCENARIO_BUDGET)
        self.assertLessEqual(self.result["budgets"]["repairs"], self.lib.OMP_CONTINUATION_REPAIR_BUDGET)

    def test_35_iteration_budget_preserves_continuation(self):
        ordinary_exhausted = {"final_verdict": "PASS", "executable_program_frontier": []}
        with mock.patch.object(self.lib, "program_execution_reconciliation", return_value=ordinary_exhausted):
            result = self.lib.continue_omp_engineering_control_loop(
                root=ROOT,
                changed_dependencies=["CERTIFICATION:FSSE04_LEASE_CONFLICT_INPUT_V1"],
                iteration_budget=1,
            )
        self.assertEqual(result["final_verdict"], "BOUNDED_CONTINUATION")
        self.assertEqual(result["program_terminal"], "BOUNDED_INVOCATION_BUDGET_REACHED")

    def test_36_unresolved_dependency_mapping_fails_closed(self):
        ordinary_exhausted = {"final_verdict": "PASS", "executable_program_frontier": []}
        with mock.patch.object(self.lib, "program_execution_reconciliation", return_value=ordinary_exhausted):
            result = self.lib.continue_omp_engineering_control_loop(root=ROOT, changed_dependencies=["UNKNOWN"])
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertEqual(result["program_terminal"], "SELECTIVE_INVALIDATION_UNRESOLVED")

    def test_37_recursion_is_denied(self):
        self.lib._CONTINUE_OMP_ACTIVE = True
        try:
            result = self.lib.continue_omp_engineering_control_loop(root=ROOT)
        finally:
            self.lib._CONTINUE_OMP_ACTIVE = False
        self.assertIn("recursive_continue_omp_denied", result["errors"])

    def test_38_decision_replay_is_deterministic(self):
        self.assertEqual(self.lib.verify_continue_omp_decision_replay(self.result, self.replay)["final_verdict"], "PASS")

    def test_39_different_decision_fails_non_deterministic(self):
        drift = copy.deepcopy(self.replay)
        drift["exact_next_operator_command"] = "OTHER"
        result = self.lib.verify_continue_omp_decision_replay(self.result, drift)
        self.assertEqual(result["decision"], "NON_DETERMINISTIC_DECISION")

    def test_40_no_progress_has_deterministic_fingerprint(self):
        self.assertEqual(self.result["result_fingerprint"], self.replay["result_fingerprint"])
        self.assertEqual(self.result["no_progress_handling"], "DETERMINISTIC_FINGERPRINT_AND_NO_BLIND_RETRY")

    def test_41_atomic_updates_have_post_write_reread(self):
        self.assertTrue(all(row["post_write_reread"] == "PASS" for row in self.result["atomic_updates"]))

    def test_42_atomic_owner_supports_expected_transient_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "CPS.md"
            path.write_text((ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text(encoding="utf-8"), encoding="utf-8")
            state = self.lib.normalized_cps_live_state({
                "current_state_generation": "cpsgen_FSSE04_TEST_TRANSITION",
                "current_transition_id": "FSSE04_TEST_TRANSITION",
                "no_progress_fingerprint": "a" * 64,
            })
            result = self.lib.atomic_reconcile_cps(path, state=state)
        self.assertTrue(result["ok"], result.get("errors"))
        self.assertEqual(result["post_write_reread"], "PASS")

    def test_43_stale_generation_is_rejected(self):
        cps = (ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text(encoding="utf-8")
        drift = self.lib._replace_section_field(cps, "## 0. Authoritative Live Current State", "## Authoritative Unfinished Capability Closure Registry", "CURRENT_STATE_GENERATION", "`stale`")
        self.assertEqual(self.lib.cps_live_state_consistency(drift)["final_verdict"], "NO-GO")

    def test_44_ordinary_frontier_preempts_scenario(self):
        ordinary = {"final_verdict": "PASS", "executable_program_frontier": ["ORDINARY_SAFE_WORK"]}
        with mock.patch.object(self.lib, "program_execution_reconciliation", return_value=ordinary):
            result = self.lib.continue_omp_engineering_control_loop(root=ROOT)
        self.assertEqual(result["priority_decision"], "ORDINARY_FRONTIER_SELECTED")

    def test_45_completion_gate_is_automation_complete(self):
        self.assertEqual(self.result["completion_gate"]["completion_contract"], "AUTOMATION_COMPLETION")
        self.assertEqual(self.result["completion_gate"]["completion_verdict"], "COMPLETE_CONSUMED")

    def test_46_bounded_terminal_and_next_command(self):
        self.assertEqual(self.result["program_terminal"], "BOUNDED_INVOCATION_BUDGET_REACHED")
        self.assertEqual(self.result["exact_next_operator_command"], "Continue OMP")

    def test_47_forbidden_effects_are_absent(self):
        self.assertFalse(any(self.result["forbidden_effects"].values()))

    def test_48_no_production_credit(self):
        self.assertFalse(self.result["forbidden_effects"]["production_maturity_credit"])

    def test_49_terminal_is_exact(self):
        self.assertEqual(self.result["terminal_class"], self.lib.FUTURE_SCALE_FSSE_04_TERMINAL)

    def test_50_cli_is_existing_truth_entrypoint(self):
        source = (ROOT / "tools/v7-truth-check").read_text(encoding="utf-8")
        self.assertIn("--continue-omp", source)
        self.assertIn("continue_omp_engineering_control_loop", source)

    def test_51_bounded_continue_omp_frontier_is_valid(self):
        cps = (ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text(encoding="utf-8")
        normalized = self.lib.build_normalized_cps_document(cps, self.lib.normalized_cps_live_state())
        result = self.lib.capability_dependency_consistency(normalized)
        self.assertEqual(result["final_verdict"], "PASS", result["errors"])

    def test_52_active_multi_lane_requires_a_nonempty_frontier(self):
        cps = (ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text(encoding="utf-8")
        state = self.lib.normalized_cps_live_state({"current_program_execution_frontier": "NONE"})
        normalized = self.lib.build_normalized_cps_document(cps, state)
        result = self.lib.capability_dependency_consistency(normalized)
        self.assertIn("empty_frontier_continuation_decision_invalid", result["errors"])


if __name__ == "__main__":
    unittest.main()
