from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_fsse3_test", ROOT / "tools/v7_sync_lib.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FutureScaleHighFidelityValidationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.corpus = cls.lib.load_future_scale_scenario_corpus(root=ROOT)
        cls.by_id = {row["SCENARIO_ID"]: row for row in cls.corpus["scenarios"]}
        cls.exact = cls.lib.execute_future_scale_scenario("LEASE_CONFLICT", root=ROOT)
        cls.batch = cls.lib.execute_future_scale_high_fidelity_batch(root=ROOT, scenario_budget=2)

    def test_01_corpus_is_bounded_high_fidelity_size(self):
        self.assertEqual(self.corpus["final_verdict"], "PASS")
        self.assertGreaterEqual(self.corpus["corpus_count"], 25)
        self.assertLessEqual(self.corpus["corpus_count"], 64)

    def test_02_required_risk_scenarios_exist(self):
        required = {
            "HEALTHY_10K_100_REAL_CODE", "CAPACITY_COLLAPSE", "RECOVERY_STORM",
            "LEASE_CONFLICT", "REPLAY_ORDERING", "SINGLE_FLIGHT_CONTENTION",
            "ROLLBACK_REQUIRED", "ROLLBACK_UNAVAILABLE", "FINAL_STOP_SAFE",
        }
        self.assertTrue(required.issubset(self.by_id))

    def test_03_expanded_scenarios_have_full_contract(self):
        row = self.by_id["LEASE_CONFLICT"]
        for field in self.lib.FUTURE_SCALE_SCENARIO_REQUIRED_FIELDS:
            self.assertIn(field, row)
        self.assertTrue(row["RATIONALE"])

    def test_04_generator_is_bounded_and_deterministic(self):
        first = self.lib.generate_future_scale_cases(self.by_id["CAPACITY_COLLAPSE"])
        replay = self.lib.generate_future_scale_cases(copy.deepcopy(self.by_id["CAPACITY_COLLAPSE"]))
        self.assertEqual(first, replay)
        self.assertLessEqual(first["case_count"], self.lib.FUTURE_SCALE_GENERATOR_CASE_BUDGET)

    def test_05_generator_has_stable_reproduction_identities(self):
        generated = self.lib.generate_future_scale_cases(self.by_id["MIXED_FRESHNESS"])
        self.assertTrue(all(row["case_identity"].startswith("fsgencase_") for row in generated["cases"]))
        self.assertTrue(all(row["reproduction_identity"].startswith("fsgenrepro_") for row in generated["cases"]))

    def test_06_dependency_binding_is_machine_readable(self):
        binding = self.lib.future_scale_dependency_binding(self.by_id["LEASE_CONFLICT"], root=ROOT)
        self.assertEqual(binding["final_verdict"], "PASS")
        self.assertEqual(len(binding["dependency_fingerprint"]), 64)
        self.assertIn("LEASE_IDENTITY", binding["invariants"])

    def test_07_selective_invalidation_includes_relevant_scenario(self):
        result = self.lib.future_scale_affected_scenario_subset(["admin_core/operator_execution.py"], root=ROOT)
        self.assertEqual(result["affected_scenarios"], ["LEASE_CONFLICT"])

    def test_08_selective_invalidation_excludes_unrelated_scenario(self):
        result = self.lib.future_scale_affected_scenario_subset(["admin_core/operator_execution.py"], root=ROOT)
        self.assertIn("HEALTHY_BASELINE_SMALL", result["unrelated_scenarios"])

    def test_09_unresolved_dependency_fails_closed(self):
        result = self.lib.future_scale_affected_scenario_subset(["UNKNOWN_OWNER"], root=ROOT)
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertTrue(result["errors"])

    def test_10_nonsemantic_change_does_not_invalidate_corpus(self):
        result = self.lib.future_scale_affected_scenario_subset(
            ["docs/reports/engineering/note.md"], root=ROOT, semantic_change=False,
        )
        self.assertEqual(result["affected_scenarios"], [])
        self.assertFalse(result["full_corpus_replay_required"])

    def test_11_exact_scenario_invokes_real_planner(self):
        self.assertEqual(self.exact["final_verdict"], "PASS")
        self.assertIn("tools/v7-users-autoswitch:AutoswitchPlanner.plan", self.exact["executed_functions"])

    def test_12_exact_scenario_invokes_real_invariants(self):
        verdicts = {row["invariant_id"]: row["verdict"] for row in self.exact["invariant_verdicts"]}
        self.assertEqual(verdicts["LEASE_IDENTITY"], "PASS")
        self.assertEqual(verdicts["SINGLE_FLIGHT"], "PASS")

    def test_13_concurrency_lease_and_replay_owners_are_consumed(self):
        evidence = self.exact["produced_outputs"]["planner"]["concurrency_evidence"]
        self.assertTrue(evidence["active_lease"])
        self.assertTrue(evidence["lease_expiry_denied"])
        self.assertTrue(evidence["duplicate_event_suppressed"])

    def test_14_shadow_owner_is_read_only(self):
        evidence = self.exact["produced_outputs"]["planner"]["shadow_evidence"]
        self.assertEqual(evidence["mode"], "shadow_only")
        self.assertFalse(evidence["runtime_mutation"])

    def test_15_performance_envelope_is_present(self):
        performance = self.exact["performance"]
        self.assertGreaterEqual(performance["state_materialization_seconds"], 0)
        self.assertGreater(performance["serialized_result_bytes"], 0)
        self.assertIn("AutoswitchPlanner", performance["dominant_cost_center"])

    def test_16_network_lane_preserves_production_isolation(self):
        result = self.lib.future_scale_network_emulation_evidence()
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertFalse(result["production_network_touched"])
        self.assertTrue(result["cleanup_verified"])

    def test_17_bounded_batch_preserves_exact_continuation(self):
        self.assertEqual(self.batch["final_verdict"], "BOUNDED_CONTINUATION")
        self.assertEqual(self.batch["scenarios_executed"], 2)
        self.assertEqual(self.batch["next_output"], self.lib.FUTURE_SCALE_HIGH_FIDELITY_MISSION_ID)

    def test_18_bounded_batch_uses_real_consumer(self):
        consumer = self.batch["consumer_result"]
        self.assertEqual(consumer["consumer"], "OMP_PROGRAM_EXECUTION_RECONCILIATION")
        self.assertEqual(consumer["final_verdict"], "PASS")

    def test_19_no_real_source_mismatch_creates_no_candidate(self):
        self.assertEqual(self.batch["mismatch_classification"], "NO_REPRODUCIBLE_REAL_SOURCE_MISMATCH_FOUND")
        self.assertEqual(self.batch["bdp_candidate_mission_result"]["candidate_count"], 0)

    def test_20_forbidden_effects_are_all_false(self):
        self.assertFalse(any(self.batch["forbidden_effects"].values()))

    def test_21_evidence_boundary_is_engineering_only(self):
        self.assertEqual(self.batch["evidence_class"], "ENGINEERING_SCENARIO_EVIDENCE")
        self.assertFalse(self.batch["historical_shadow"]["production_credit"])

    def test_22_high_fidelity_cli_is_existing_entrypoint(self):
        source = (ROOT / "tools/v7-truth-check").read_text(encoding="utf-8")
        self.assertIn("--omp-high-fidelity-batch", source)
        self.assertIn("--high-fidelity-scenario", source)
        self.assertIn("execute_future_scale_high_fidelity_batch", source)

    def test_23_batch_budget_is_capped(self):
        self.assertEqual(self.lib.FUTURE_SCALE_HIGH_FIDELITY_MAX_SCENARIOS, 64)
        self.assertLessEqual(self.batch["scenario_budget"], 40)

    def test_24_result_consumption_is_not_file_persistence(self):
        self.assertIn("behavior_change", self.batch["consumer_result"])
        self.assertNotIn("result_file", self.batch["consumer_result"])

    def test_25_stop_safe_is_a_legal_scenario_terminal(self):
        result = self.lib.execute_future_scale_scenario("ROLLBACK_UNAVAILABLE", root=ROOT)
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertEqual(result["terminal_class"], "STOP_SAFE")


if __name__ == "__main__":
    unittest.main()
