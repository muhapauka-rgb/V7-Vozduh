from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_fsse_execution_test", ROOT / "tools/v7_sync_lib.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FutureScalePolygonExecutionHarnessTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        corpus = cls.lib.load_future_scale_scenario_corpus(root=ROOT)
        cls.scenario = next(row for row in corpus["scenarios"] if row["SCENARIO_ID"] == "CAPACITY_BOUNDARY")
        cls.state = cls.lib.materialize_future_scale_isolated_state(cls.scenario)
        cls.result = cls.lib.execute_future_scale_scenario("CAPACITY_BOUNDARY", root=ROOT)

    def test_01_capacity_scenario_binds_all_required_invariants(self):
        self.assertTrue(set(self.lib.FUTURE_SCALE_EXECUTION_REQUIRED_CAPACITY_INVARIANTS).issubset(self.scenario["INVARIANT_IDS"]))

    def test_02_isolated_state_materializes_full_scale(self):
        self.assertEqual((self.state["users_count"], self.state["channels_count"]), (10_000, 100))
        self.assertEqual((self.state["organizations_count"], self.state["cohorts_count"]), (30, 150))

    def test_03_isolated_state_identity_is_deterministic(self):
        replay = self.lib.materialize_future_scale_isolated_state(copy.deepcopy(self.scenario))
        self.assertEqual(self.state["state_fingerprint"], replay["state_fingerprint"])

    def test_04_isolated_state_rejects_over_bound_population(self):
        invalid = copy.deepcopy(self.scenario)
        invalid["USER_POPULATION_PROFILE"] = {"users": 10_001}
        result = self.lib.materialize_future_scale_isolated_state(invalid)
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertIn("isolated_state_user_bound", result["errors"])

    def test_05_real_scenario_execution_passes(self):
        self.assertEqual(self.result["final_verdict"], "PASS", self.result.get("errors"))
        self.assertEqual(self.result["failed_invariant"], "NONE")

    def test_06_real_planner_observes_full_population(self):
        planner = self.result["produced_outputs"]["planner"]
        self.assertEqual(planner["users_observed"], 10_000)
        self.assertEqual(planner["reachable_users"], 10_000)
        self.assertEqual(planner["representatives_evaluated"], 100)
        self.assertGreater(planner["candidate_moves"], 0)

    def test_07_real_planner_and_execution_owners_are_invoked(self):
        functions = set(self.result["executed_functions"])
        self.assertIn("tools/v7-users-autoswitch:AutoswitchPlanner.plan", functions)
        self.assertIn("admin_core/operator_execution_pipeline.py:autonomous_dry_run_model", functions)
        self.assertIn("admin_core/operator_execution_pipeline.py:verification_policy", functions)
        self.assertIn("admin_core/operator_execution_pipeline.py:rollback_policy", functions)

    def test_08_all_required_invariants_pass(self):
        verdicts = {row["invariant_id"]: row["verdict"] for row in self.result["invariant_verdicts"]}
        self.assertEqual(set(verdicts), set(self.lib.FUTURE_SCALE_EXECUTION_REQUIRED_CAPACITY_INVARIANTS))
        self.assertTrue(all(value == "PASS" for value in verdicts.values()))

    def test_09_replay_is_semantically_deterministic(self):
        self.assertTrue(self.result["produced_outputs"]["replay_semantic_match"])
        self.assertTrue(self.result["reproducibility_identity"].startswith("fsreplay_"))

    def test_10_forbidden_effects_are_absent(self):
        self.assertFalse(any(self.result["forbidden_effects"].values()))
        planner = self.result["produced_outputs"]["planner"]
        self.assertFalse(planner["apply_called"])
        self.assertEqual(planner["users_moved"], 0)

    def test_11_resource_bounds_are_enforced(self):
        self.assertLessEqual(self.result["execution_duration_seconds"], self.lib.FUTURE_SCALE_EXECUTION_MAX_SECONDS)
        self.assertEqual(self.result["resource_bounds"]["max_users"], 10_000)
        self.assertEqual(self.result["resource_bounds"]["max_channels"], 100)

    def test_12_real_consumer_covers_result_and_materializes_next_scenario(self):
        consumer = self.result["consumer_result"]
        self.assertEqual(consumer["final_verdict"], "PASS")
        self.assertTrue(consumer["consumed"])
        self.assertEqual(consumer["behavior_change"], "SCENARIO_COVERED_AND_NEXT_FRONTIER_MATERIALIZED")
        self.assertNotEqual(consumer["next_scenario_id"], "CAPACITY_BOUNDARY")
        self.assertNotEqual(consumer["next_scenario_id"], "NONE")

    def test_13_result_is_engineering_evidence_only(self):
        self.assertEqual(self.result["evidence_class"], "ENGINEERING_SCENARIO_EVIDENCE")
        self.assertFalse(self.result["forbidden_effects"]["production_maturity_credit"])

    def test_14_non_test_cli_entrypoint_is_wired(self):
        source = (ROOT / "tools/v7-truth-check").read_text(encoding="utf-8")
        self.assertIn("--omp-scenario-execution", source)
        self.assertIn("execute_future_scale_scenario", source)
        self.assertIn("V7_FSSE_SCENARIO_ROOT", source)
        self.assertIn("root=fsse_scenario_root()", source)


if __name__ == "__main__":
    unittest.main()
