import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "tools" / "v7_sync_lib.py"
CPS = ROOT / "docs" / "programs" / "V7_CURRENT_PROGRAM_STATE.md"


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_proactive_polygon_test", LIB)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class OmpProactivePolygonVerificationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.cps = CPS.read_text(encoding="utf-8")

    def source(self, **overrides):
        value = {
            "source_owner": "EXISTING_STOP_SAFE_OWNER",
            "execution_owner": "PYTHON_UNITTEST_EXISTING_VERIFICATION_OWNER",
            "source_evidence": "tests/unit/test_example.py",
            "target_contract": "Snapshot mismatch stops before mutation.",
            "engineering_intent": "Preserve fail-closed snapshot validation.",
            "current_assumption": "Current implementation satisfies the contract.",
            "expected_behavior": "Mismatch is rejected before mutation.",
            "entrypoint": [sys.executable, "-m", "unittest", "tests.unit.test_example.ExampleTest.test_contract"],
            "input_or_fixture": "tests.unit.test_example.ExampleTest.test_contract",
            "preconditions": "clean repository and no Runtime mutation",
            "observation_method": "existing unittest assertion",
            "pass_criteria": "unittest exits zero",
            "fail_criteria": "unittest fails reproducibly",
            "result_consumer": "ENGINEERING_POLYGON_SCENARIO_SUPPLY",
            "rollback_or_stop_safe": "no mutation; STOP_SAFE",
            "runtime_impact": "NONE",
            "production_impact": "NONE",
            "authority_impact": "NONE",
            "maturity_credit": "FORBIDDEN",
            "user_movement": False,
            "packet_apply": False,
            "restore_barrier_write": False,
            "revalidation_trigger": "owner implementation or fixture changes",
            "verification_class": "STOP_SAFE_SAFETY_NEGATIVE",
            "source_classification": "ACTIVE_EXECUTABLE_NOT_CONSUMED",
            "new_owner_required": False,
            "new_architecture_required": False,
        }
        value.update(overrides)
        return value

    @staticmethod
    def passing_runner(cmd, cwd, timeout):
        return {"ok": True, "rc": 0, "stdout": "ok", "stderr": "", "cmd": cmd}

    @staticmethod
    def failing_runner(cmd, cwd, timeout):
        return {"ok": False, "rc": 1, "stdout": "", "stderr": "contract failed", "cmd": cmd}

    def materialized(self, **overrides):
        return self.lib.proactive_verification_input(self.source(**overrides))["proactive_input"]

    def test_01_existing_fixture_is_discovered_and_mapped(self):
        result = self.lib.discover_proactive_verification_inputs()
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertGreaterEqual(result["mapped_input_count"], 5)

    def test_02_historical_report_alone_is_not_executable(self):
        result = self.lib.select_proactive_verification_input([
            self.source(source_classification="HISTORICAL_CONTEXT_ONLY")
        ])
        self.assertIsNone(result["selected_input"])

    def test_03_production_only_evidence_is_excluded(self):
        result = self.lib.select_proactive_verification_input([
            self.source(source_classification="PRODUCTION_ONLY")
        ])
        self.assertEqual(result["selection_status"], "NO_ELIGIBLE_PROACTIVE_VERIFICATION_INPUT")

    def test_04_deterministic_input_receives_stable_identity(self):
        first = self.materialized()
        second = self.materialized(engineering_intent="  PRESERVE fail-closed snapshot validation. ")
        self.assertEqual(first["deterministic_identity"], second["deterministic_identity"])

    def test_05_duplicate_input_is_suppressed(self):
        first = self.materialized()
        result = self.lib.select_proactive_verification_input([self.source()], evaluated_inputs=[first])
        self.assertIsNone(result["selected_input"])
        self.assertEqual(result["duplicate_input_count"], 1)

    def test_06_priority_selection_is_deterministic(self):
        low = self.source(verification_class="ENGINEERING_QUALITY", engineering_intent="Low quality check.")
        first = self.lib.select_proactive_verification_input([low, self.source()])["selected_input"]
        replay = self.lib.select_proactive_verification_input([self.source(), low])["selected_input"]
        self.assertEqual(first["deterministic_identity"], replay["deterministic_identity"])

    def test_07_stop_safe_outranks_quality(self):
        low = self.source(verification_class="ENGINEERING_QUALITY", engineering_intent="Low quality check.")
        selected = self.lib.select_proactive_verification_input([low, self.source()])["selected_input"]
        self.assertEqual(selected["verification_class"], "STOP_SAFE_SAFETY_NEGATIVE")

    def test_08_pass_produces_no_scenario_or_candidate(self):
        run = self.lib.bounded_proactive_engineering_polygon_run(
            self.cps, sources=[self.source()], runner=self.passing_runner,
        )
        self.assertEqual(run["inputs_passed"], 1)
        self.assertEqual(run["scenarios_created"], 0)
        self.assertEqual(run["candidates_created"], 0)

    def test_09_current_reproducible_fail_produces_one_scenario(self):
        run = self.lib.bounded_proactive_engineering_polygon_run(
            self.cps, sources=[self.source()], runner=self.failing_runner,
        )
        self.assertEqual(run["inputs_failed"], 1)
        self.assertEqual(run["scenarios_created"], 1)

    def test_10_scenario_passes_through_bdp(self):
        run = self.lib.bounded_proactive_engineering_polygon_run(
            self.cps, sources=[self.source()], runner=self.failing_runner,
        )
        self.assertEqual(run["trace"][0]["supply_status"], "SCENARIO_CONSUMED_BY_BDP")
        self.assertTrue(run["trace"][0]["candidate_created"])

    def test_11_expected_failure_does_not_become_scenario(self):
        item = self.materialized()
        execution = self.lib.execute_proactive_verification_input(item, runner=self.passing_runner)
        conversion = self.lib.proactive_verification_failure_scenario_source(item, execution)
        self.assertEqual(conversion["final_verdict"], "STOP_SAFE")

    def test_12_non_deterministic_result_stops_safe(self):
        calls = []
        def flaky(cmd, cwd, timeout):
            calls.append(1)
            return {"ok": False, "rc": len(calls), "stdout": "", "stderr": str(len(calls)), "cmd": cmd}
        run = self.lib.bounded_proactive_engineering_polygon_run(
            self.cps, sources=[self.source()], runner=flaky,
        )
        self.assertEqual(run["stop_reason"], "NON_DETERMINISTIC_DECISION")

    def test_13_missing_owner_blocks_conversion(self):
        item = self.materialized()
        item["source_owner"] = ""
        execution = {"execution_result": "PROACTIVE_VERIFICATION_FAIL", "reproducible": True}
        result = self.lib.proactive_verification_failure_scenario_source(item, execution)
        self.assertIn("proactive_failure_owner_missing", result["errors"])

    def test_14_missing_consumer_blocks_conversion(self):
        item = self.materialized()
        item["result_consumer"] = ""
        execution = {"execution_result": "PROACTIVE_VERIFICATION_FAIL", "reproducible": True}
        result = self.lib.proactive_verification_failure_scenario_source(item, execution)
        self.assertIn("proactive_failure_consumer_missing", result["errors"])

    def test_15_runtime_impacting_input_is_excluded(self):
        result = self.lib.select_proactive_verification_input([self.source(runtime_impact="RUNTIME_APPLY")])
        self.assertEqual(result["final_verdict"], "STOP_SAFE")

    def test_16_production_impacting_input_is_excluded(self):
        result = self.lib.select_proactive_verification_input([self.source(production_impact="PRODUCTION_MUTATION")])
        self.assertEqual(result["final_verdict"], "STOP_SAFE")

    def test_17_authority_expanding_input_is_excluded(self):
        result = self.lib.select_proactive_verification_input([self.source(authority_impact="EXPANSION")])
        self.assertIn("proactive_input_authority_boundary", result["errors"])

    def test_18_user_movement_is_impossible(self):
        result = self.lib.proactive_verification_input(self.source(user_movement=True))
        self.assertIn("proactive_input_user_movement_boundary", result["errors"])

    def test_19_restore_barrier_write_is_impossible(self):
        result = self.lib.proactive_verification_input(self.source(restore_barrier_write=True))
        self.assertIn("proactive_input_restore_barrier_write_boundary", result["errors"])

    def test_20_packet_apply_is_impossible(self):
        result = self.lib.proactive_verification_input(self.source(packet_apply=True))
        self.assertIn("proactive_input_packet_apply_boundary", result["errors"])

    def test_21_production_maturity_remains_unchanged(self):
        result = self.lib.proactive_verification_input(self.source(maturity_credit="GRANTED"))
        self.assertIn("proactive_input_maturity_boundary", result["errors"])

    def test_22_real_world_limit_capabilities_remain_waiting(self):
        run = self.lib.bounded_proactive_engineering_polygon_run(
            self.cps, sources=[self.source()], runner=self.passing_runner,
        )
        self.assertEqual(run["maturity_impact"], "NONE")
        self.assertIn("REAL_WORLD_EVIDENCE", run["stop_reason"])

    def test_23_protected_wip_remains_preserved(self):
        run = self.lib.bounded_proactive_engineering_polygon_run(
            self.cps, sources=[self.source()], runner=self.passing_runner,
        )
        self.assertTrue(run["protected_wip_preserved"])

    def test_24_failure_mission_uses_existing_codex_owner(self):
        run = self.lib.bounded_proactive_engineering_polygon_run(
            self.cps, sources=[self.source()], runner=self.failing_runner,
        )
        self.assertTrue(run["trace"][0]["mission_prepared"])

    def test_25_verification_precedes_next_input(self):
        second = self.source(engineering_intent="Second contract check.")
        run = self.lib.bounded_proactive_engineering_polygon_run(
            self.cps, sources=[self.source(), second], runner=self.passing_runner,
        )
        self.assertEqual(run["inputs_executed"], 2)
        self.assertEqual(len(run["coverage"]), 2)

    def test_26_recalculation_selects_next_distinct_input(self):
        first = self.materialized()
        second_source = self.source(engineering_intent="Second contract check.")
        selected = self.lib.select_proactive_verification_input(
            [self.source(), second_source], evaluated_inputs=[first],
        )["selected_input"]
        self.assertNotEqual(selected["proactive_input_id"], first["proactive_input_id"])

    def test_27_budget_stops_correctly(self):
        sources = [self.source(engineering_intent=f"Contract check {index}.") for index in range(6)]
        run = self.lib.bounded_proactive_engineering_polygon_run(
            self.cps, sources=sources, runner=self.passing_runner, max_inputs=5,
        )
        self.assertEqual(run["inputs_executed"], 5)
        self.assertEqual(run["stop_reason"], "PROACTIVE_INPUT_BUDGET_EXHAUSTED")

    def test_28_replay_produces_identical_selection_and_result(self):
        first = self.lib.bounded_proactive_engineering_polygon_run(
            self.cps, sources=[self.source()], runner=self.passing_runner,
        )
        replay = self.lib.bounded_proactive_engineering_polygon_run(
            self.cps, sources=[self.source()], runner=self.passing_runner,
        )
        self.assertEqual(first["trace"], replay["trace"])

    def test_29_every_result_has_existing_consumer(self):
        discovered = self.lib.discover_proactive_verification_inputs()["proactive_inputs"]
        self.assertTrue(all(item["result_consumer"] == "ENGINEERING_POLYGON_SCENARIO_SUPPLY" for item in discovered))

    def test_30_coverage_state_is_recorded(self):
        run = self.lib.bounded_proactive_engineering_polygon_run(
            self.cps, sources=[self.source()], runner=self.passing_runner,
        )
        self.assertEqual(run["coverage"][0]["last_result"], "PROACTIVE_VERIFICATION_PASS")


if __name__ == "__main__":
    unittest.main()
