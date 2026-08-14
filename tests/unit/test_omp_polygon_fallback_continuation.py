import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "tools" / "v7_sync_lib.py"
CPS = ROOT / "docs" / "programs" / "V7_CURRENT_PROGRAM_STATE.md"


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_polygon_fallback_test", LIB)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class OmpPolygonFallbackContinuationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.cps = CPS.read_text(encoding="utf-8")
        cls.cps = cls.lib._replace_section_field(
            cls.cps, "## 0. Authoritative Live Current State",
            "## Authoritative Unfinished Capability Closure Registry",
            "CURRENT_STOP_CONDITION", "`REAL_WORLD_LIMIT`",
        )
        # This suite models the independent Polygon fallback condition.  The
        # checked-in CPS legitimately owns an active RS6 Mission, which must
        # preempt Polygon in production and is covered by the program-frontier
        # tests.  Clear only the fixture's active-Mission field so these tests
        # exercise the fallback contract rather than the live RS6 precedence.
        cls.cps = cls.lib._replace_section_field(
            cls.cps, "## 0. Authoritative Live Current State",
            "## Authoritative Unfinished Capability Closure Registry",
            "CURRENT_EXECUTION_MISSION_ID", "`NONE`",
        )
        cls.lib.current_engineering_polygon_scenario_supply = lambda *args, **kwargs: {"discovery": {"active_source_count": 0}}
        cls.discovery = cls.lib.discover_proactive_verification_inputs()

    def source(self, **overrides):
        value = {
            "source_owner": "EXISTING_TEST_OWNER",
            "execution_owner": "PYTHON_UNITTEST_EXISTING_VERIFICATION_OWNER",
            "source_evidence": "tests/unit/test_example.py",
            "target_contract": "example current contract",
            "contract_class": "STOP_SAFE_SAFETY",
            "engineering_intent": "Preserve example current contract.",
            "current_assumption": "The contract remains valid.",
            "expected_behavior": "The exact unittest passes.",
            "entrypoint": [sys.executable, "-m", "unittest", "tests.unit.test_example.ExampleTest.test_stop_safe"],
            "input_or_fixture": "tests.unit.test_example.ExampleTest.test_stop_safe",
            "preconditions": "isolated test-only execution",
            "observation_method": "unittest exit status",
            "pass_criteria": "zero exit",
            "fail_criteria": "reproducible nonzero exit",
            "result_consumer": "ENGINEERING_POLYGON_SCENARIO_SUPPLY",
            "rollback_or_stop_safe": "STOP_SAFE",
            "mutation_boundary": "ISOLATED_TEST_ONLY",
            "runtime_impact": "NONE",
            "production_impact": "NONE",
            "authority_impact": "NONE",
            "maturity_credit": "FORBIDDEN",
            "user_movement": False,
            "packet_apply": False,
            "restore_barrier_write": False,
            "revalidation_trigger": "contract fingerprint changes",
            "verification_class": "STOP_SAFE_SAFETY",
            "source_classification": "ACTIVE_EXECUTABLE_NOT_CONSUMED",
            "new_owner_required": False,
            "new_architecture_required": False,
            "revalidation_fingerprint": "fp-example-v1",
            "seed_input": False,
        }
        value.update(overrides)
        return value

    @staticmethod
    def pass_runner(cmd, cwd, timeout):
        return {"ok": True, "rc": 0, "stdout": "", "stderr": "OK", "cmd": cmd}

    @staticmethod
    def fail_runner(cmd, cwd, timeout):
        return {"ok": False, "rc": 1, "stdout": "", "stderr": "failed", "cmd": cmd}

    def instance(self, **overrides):
        return self.lib.proactive_verification_input(self.source(**overrides))["proactive_input"]

    def coverage(self, item, result="PASS_CURRENT", fingerprint=None):
        return {
            item["proactive_input_id"]: {
                "proactive_input_id": item["proactive_input_id"],
                "last_result": result,
                "last_evaluated_fingerprint": fingerprint or item.get("revalidation_fingerprint", item["deterministic_identity"]),
            }
        }

    def test_01_existing_six_seed_inputs_remain_discovered(self):
        self.assertEqual(self.discovery["seed_input_count"], 6)

    def test_02_additional_unittest_methods_are_discovered(self):
        self.assertGreater(self.discovery["automatic_input_count"], 0)

    def test_03_unsafe_mutation_capable_tests_are_excluded(self):
        reasons = {item["reason"] for item in self.discovery["excluded_inputs"]}
        self.assertTrue(any(reason.startswith("UNSAFE_OR_EXTERNAL_TOKEN") for reason in reasons))

    def test_04_external_access_tests_are_excluded(self):
        excluded = self.discovery["excluded_inputs"]
        self.assertTrue(any("EXTERNAL" in item["reason"] or "OWNER_NOT_MAPPED" == item["reason"] for item in excluded))

    def test_05_ambiguous_tests_are_excluded_with_reason(self):
        self.assertTrue(any(item["reason"] == "AMBIGUOUS_CONTRACT_SEMANTICS" for item in self.discovery["excluded_inputs"]))

    def test_06_corpus_ordering_is_deterministic(self):
        replay = self.lib.discover_proactive_verification_inputs()
        self.assertEqual(self.discovery["corpus_fingerprint"], replay["corpus_fingerprint"])

    def test_07_filesystem_order_does_not_change_selection(self):
        low = self.source(verification_class="ENGINEERING_QUALITY", contract_class="ENGINEERING_QUALITY", engineering_intent="Quality.")
        a = self.lib.select_proactive_verification_input([low, self.source()])["selected_input"]
        b = self.lib.select_proactive_verification_input([self.source(), low])["selected_input"]
        self.assertEqual(a["proactive_input_id"], b["proactive_input_id"])

    def test_08_same_corpus_has_same_fingerprint(self):
        items = [self.lib.proactive_verification_input(item)["proactive_input"] for item in self.discovery["proactive_inputs"]]
        self.assertEqual(self.lib.proactive_corpus_fingerprint(items), self.lib.proactive_corpus_fingerprint(reversed(items)))

    def test_09_new_eligible_test_changes_corpus_fingerprint(self):
        items = [self.lib.proactive_verification_input(item)["proactive_input"] for item in self.discovery["proactive_inputs"]]
        baseline = self.lib.proactive_corpus_fingerprint(items)
        items.append(self.instance(engineering_intent="New distinct contract.", input_or_fixture="tests.unit.test_example.ExampleTest.test_new_stop", entrypoint=[sys.executable, "-m", "unittest", "tests.unit.test_example.ExampleTest.test_new_stop"]))
        self.assertNotEqual(baseline, self.lib.proactive_corpus_fingerprint(items))

    def test_10_owner_change_marks_pass_stale(self):
        item = self.instance()
        selected = self.lib.select_proactive_verification_input([self.source()], coverage_records=self.coverage(item, fingerprint="old"))["selected_input"]
        self.assertEqual(selected["coverage_state"], "STALE_REVALIDATION_REQUIRED")

    def test_11_unchanged_pass_is_not_rerun(self):
        item = self.instance()
        result = self.lib.select_proactive_verification_input([self.source()], coverage_records=self.coverage(item))
        self.assertIsNone(result["selected_input"])

    def test_12_not_evaluated_precedes_current_pass(self):
        passed = self.instance()
        fresh_source = self.source(engineering_intent="Fresh contract.", input_or_fixture="tests.unit.test_example.ExampleTest.test_fresh_stop", entrypoint=[sys.executable, "-m", "unittest", "tests.unit.test_example.ExampleTest.test_fresh_stop"])
        result = self.lib.select_proactive_verification_input([self.source(), fresh_source], coverage_records=self.coverage(passed))
        self.assertIn("test_fresh_stop", result["selected_input"]["input_or_fixture"])

    def test_13_stop_safe_outranks_engineering_quality(self):
        quality = self.source(verification_class="ENGINEERING_QUALITY", contract_class="ENGINEERING_QUALITY", engineering_intent="Quality.")
        selected = self.lib.select_proactive_verification_input([quality, self.source()])["selected_input"]
        self.assertEqual(selected["verification_class"], "STOP_SAFE_SAFETY")

    def test_14_pass_continues_to_next_input(self):
        second = self.source(engineering_intent="Second.", input_or_fixture="tests.unit.test_example.ExampleTest.test_second_stop", entrypoint=[sys.executable, "-m", "unittest", "tests.unit.test_example.ExampleTest.test_second_stop"])
        run = self.lib.bounded_proactive_engineering_polygon_run(self.cps, sources=[self.source(), second], runner=self.pass_runner)
        self.assertEqual(run["inputs_executed"], 2)

    def test_15_budget_exhaustion_preserves_next_input(self):
        second = self.source(engineering_intent="Second.", input_or_fixture="tests.unit.test_example.ExampleTest.test_second_stop", entrypoint=[sys.executable, "-m", "unittest", "tests.unit.test_example.ExampleTest.test_second_stop"])
        run = self.lib.bounded_proactive_engineering_polygon_run(self.cps, sources=[self.source(), second], runner=self.pass_runner, max_inputs=1)
        self.assertEqual(run["stop_reason"], "PROACTIVE_INPUT_BUDGET_EXHAUSTED")
        self.assertNotEqual(run["next_corpus_input_id"], "NONE")

    def test_16_budget_exhaustion_is_not_real_world_limit(self):
        second = self.source(engineering_intent="Second.", input_or_fixture="tests.unit.test_example.ExampleTest.test_second_stop", entrypoint=[sys.executable, "-m", "unittest", "tests.unit.test_example.ExampleTest.test_second_stop"])
        run = self.lib.bounded_proactive_engineering_polygon_run(self.cps, sources=[self.source(), second], runner=self.pass_runner, max_inputs=1)
        self.assertNotIn("REAL_WORLD", run["stop_reason"])

    def test_17_current_reproducible_fail_creates_scenario(self):
        run = self.lib.bounded_proactive_engineering_polygon_run(self.cps, sources=[self.source()], runner=self.fail_runner)
        self.assertEqual(run["scenarios_created"], 1)

    def test_18_fail_cannot_bypass_bdp(self):
        run = self.lib.bounded_proactive_engineering_polygon_run(self.cps, sources=[self.source()], runner=self.fail_runner)
        self.assertEqual(run["trace"][0]["supply_status"], "SCENARIO_CONSUMED_BY_BDP")

    def test_19_fail_cannot_bypass_omp_admission(self):
        run = self.lib.bounded_proactive_engineering_polygon_run(self.cps, sources=[self.source()], runner=self.fail_runner)
        self.assertTrue(run["trace"][0]["mission_prepared"])

    def test_20_failed_input_is_rerun_for_reproducibility(self):
        calls = []
        def runner(cmd, cwd, timeout):
            calls.append(cmd)
            return self.fail_runner(cmd, cwd, timeout)
        self.lib.bounded_proactive_engineering_polygon_run(self.cps, sources=[self.source()], runner=runner)
        self.assertEqual(len(calls), 2)

    def test_21_flaky_result_stops_non_deterministic(self):
        calls = []
        def runner(cmd, cwd, timeout):
            calls.append(1)
            return {"ok": False, "rc": len(calls), "stdout": "", "stderr": str(len(calls)), "cmd": cmd}
        run = self.lib.bounded_proactive_engineering_polygon_run(self.cps, sources=[self.source()], runner=runner)
        self.assertEqual(run["stop_reason"], "NON_DETERMINISTIC_DECISION")

    def test_22_duplicate_inputs_are_suppressed(self):
        item = self.instance()
        result = self.lib.select_proactive_verification_input([self.source()], evaluated_inputs=[item])
        self.assertEqual(result["duplicate_input_count"], 1)

    def test_23_real_situation_preempts_polygon(self):
        run = self.lib.bounded_proactive_engineering_polygon_run(self.cps, sources=[self.source()], runner=self.pass_runner, fallback_context={"actionable_real_situation": True})
        self.assertFalse(run["polygon_fallback_activated"])

    def test_24_ready_capability_preempts_polygon(self):
        run = self.lib.bounded_proactive_engineering_polygon_run(self.cps, sources=[self.source()], runner=self.pass_runner, fallback_context={"ready_capabilities": "CAP-U99"})
        self.assertFalse(run["polygon_fallback_activated"])

    def test_25_active_candidate_preempts_polygon(self):
        run = self.lib.bounded_proactive_engineering_polygon_run(self.cps, sources=[self.source()], runner=self.pass_runner, fallback_context={"current_candidate_count": 1})
        self.assertFalse(run["polygon_fallback_activated"])

    def test_26_polygon_activates_without_real_work(self):
        run = self.lib.bounded_proactive_engineering_polygon_run(self.cps, sources=[self.source()], runner=self.pass_runner)
        self.assertTrue(run["polygon_fallback_activated"])

    def test_27_real_world_limit_forbidden_while_remaining(self):
        second = self.source(engineering_intent="Second.", input_or_fixture="tests.unit.test_example.ExampleTest.test_second_stop", entrypoint=[sys.executable, "-m", "unittest", "tests.unit.test_example.ExampleTest.test_second_stop"])
        run = self.lib.bounded_proactive_engineering_polygon_run(self.cps, sources=[self.source(), second], runner=self.pass_runner, max_inputs=1)
        self.assertEqual(run["corpus_remaining"], 1)
        self.assertEqual(run["stop_reason"], "PROACTIVE_INPUT_BUDGET_EXHAUSTED")

    def test_28_exhaustion_requires_full_current_corpus(self):
        run = self.lib.bounded_proactive_engineering_polygon_run(self.cps, sources=[self.source()], runner=self.pass_runner)
        self.assertTrue(run["exhaustion_proven"])

    def test_29_excluded_inputs_do_not_count_as_evaluated(self):
        result = self.lib.select_proactive_verification_input([self.source(source_classification="NOT_EXECUTABLE")])
        self.assertEqual(result["eligible_input_count"], 0)

    def test_30_stale_inputs_block_exhaustion(self):
        item = self.instance()
        selection = self.lib.select_proactive_verification_input([self.source()], coverage_records=self.coverage(item, fingerprint="old"))
        self.assertIsNotNone(selection["selected_input"])

    def test_31_runtime_impact_remains_none(self):
        run = self.lib.bounded_proactive_engineering_polygon_run(self.cps, sources=[self.source()], runner=self.pass_runner)
        self.assertEqual(run["runtime_impact"], "NONE")

    def test_32_production_impact_remains_none(self):
        run = self.lib.bounded_proactive_engineering_polygon_run(self.cps, sources=[self.source()], runner=self.pass_runner)
        self.assertEqual(run["production_impact"], "NONE")

    def test_33_authority_remains_unchanged(self):
        run = self.lib.bounded_proactive_engineering_polygon_run(self.cps, sources=[self.source()], runner=self.pass_runner)
        self.assertFalse(run["authority_expansion"])

    def test_34_maturity_credit_remains_none(self):
        run = self.lib.bounded_proactive_engineering_polygon_run(self.cps, sources=[self.source()], runner=self.pass_runner)
        self.assertEqual(run["maturity_impact"], "NONE")

    def test_35_protected_wip_remains_preserved(self):
        run = self.lib.bounded_proactive_engineering_polygon_run(self.cps, sources=[self.source()], runner=self.pass_runner)
        self.assertTrue(run["protected_wip_preserved"])

    def test_36_compact_continuation_projection_is_consistent(self):
        run = self.lib.bounded_proactive_engineering_polygon_run(self.cps, sources=[self.source()], runner=self.pass_runner)
        projection = run["continuation_projection"]
        self.assertEqual(projection["POLYGON_CORPUS_REMAINING"], 0)
        self.assertTrue(projection["POLYGON_EXHAUSTION_PROVEN"])

    def test_37_replay_reproduces_corpus_selection_and_stop(self):
        a = self.lib.bounded_proactive_engineering_polygon_run(self.cps, sources=[self.source()], runner=self.pass_runner)
        b = self.lib.bounded_proactive_engineering_polygon_run(self.cps, sources=[self.source()], runner=self.pass_runner)
        self.assertEqual((a["corpus_fingerprint"], a["trace"], a["stop_reason"]), (b["corpus_fingerprint"], b["trace"], b["stop_reason"]))

    def test_38_every_output_has_existing_consumer(self):
        self.assertTrue(all(item["result_consumer"] == "ENGINEERING_POLYGON_SCENARIO_SUPPLY" for item in self.discovery["proactive_inputs"]))

    def test_39_no_new_queue_owner_engine_or_lifecycle(self):
        run = self.lib.bounded_proactive_engineering_polygon_run(self.cps, sources=[self.source()], runner=self.pass_runner)
        self.assertNotIn("queue", str(run).lower())
        self.assertEqual(run["runtime_impact"], "NONE")

    def test_40_omp_continues_automatically_after_pass(self):
        second = self.source(engineering_intent="Second.", input_or_fixture="tests.unit.test_example.ExampleTest.test_second_stop", entrypoint=[sys.executable, "-m", "unittest", "tests.unit.test_example.ExampleTest.test_second_stop"])
        run = self.lib.bounded_proactive_engineering_polygon_run(self.cps, sources=[self.source(), second], runner=self.pass_runner)
        self.assertEqual([row["execution_result"] for row in run["trace"]], ["PROACTIVE_VERIFICATION_PASS", "PROACTIVE_VERIFICATION_PASS"])


if __name__ == "__main__":
    unittest.main()
