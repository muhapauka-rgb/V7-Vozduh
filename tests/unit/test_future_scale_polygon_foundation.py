from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_future_scale_test", ROOT / "tools/v7_sync_lib.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FutureScalePolygonFoundationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.cps = (ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text()
        cls.fsse02_cps = re.sub(
            r"(?m)^\| `CURRENT_PROGRAM_STAGE` \| `[^`]+` \|$",
            "| `CURRENT_PROGRAM_STAGE` | `FSSE_02_COMPLETE_FSSE_03_READY` |",
            cls.cps,
            count=1,
        )
        cls.corpus = cls.lib.load_future_scale_scenario_corpus()
        cls.scenario = cls.corpus["scenarios"][0]

    def test_01_existing_polygon_owner_is_reused(self):
        self.assertTrue(hasattr(self.lib, "bounded_proactive_engineering_polygon_run"))
        self.assertTrue(hasattr(self.lib, "current_engineering_polygon_scenario_supply"))

    def test_02_seed_corpus_has_bounded_high_fidelity_count(self):
        self.assertGreaterEqual(self.corpus["corpus_count"], 25)
        self.assertLessEqual(self.corpus["corpus_count"], 40)
        self.assertEqual(self.corpus["final_verdict"], "PASS")

    def test_03_all_required_invariants_resolve(self):
        self.assertGreaterEqual(len(self.lib.FUTURE_SCALE_INVARIANTS), 30)
        self.assertTrue(all(self.lib.resolve_invariant(item)["resolved"] for item in self.lib.FUTURE_SCALE_INVARIANTS))

    def test_04_unresolved_invariant_fails_closed(self):
        scenario = copy.deepcopy(self.scenario)
        scenario["INVARIANT_IDS"] = ["UNKNOWN_INVARIANT"]
        scenario["SCENARIO_FINGERPRINT"] = "DERIVED"
        result = self.lib.validate_future_scale_scenario(scenario)
        self.assertFalse(result["valid"])
        self.assertIn("unresolved_invariant:UNKNOWN_INVARIANT", result["errors"])

    def test_05_missing_identity_is_rejected(self):
        scenario = copy.deepcopy(self.scenario)
        del scenario["SCENARIO_ID"]
        scenario["SCENARIO_FINGERPRINT"] = "DERIVED"
        self.assertIn("scenario_field_missing:SCENARIO_ID", self.lib.validate_future_scale_scenario(scenario)["errors"])

    def test_06_fingerprint_is_deterministic(self):
        self.assertEqual(
            self.lib.future_scale_scenario_fingerprint(self.scenario),
            self.lib.future_scale_scenario_fingerprint(copy.deepcopy(self.scenario)),
        )

    def test_07_meaningful_change_changes_fingerprint(self):
        changed = copy.deepcopy(self.scenario)
        changed["USER_POPULATION_PROFILE"] = {"users": 11}
        self.assertNotEqual(
            self.lib.future_scale_scenario_fingerprint(self.scenario),
            self.lib.future_scale_scenario_fingerprint(changed),
        )

    def test_08_seed_reproduction_is_deterministic(self):
        replay = self.lib.load_future_scale_scenario_corpus()
        self.assertEqual(self.corpus["corpus_fingerprint"], replay["corpus_fingerprint"])

    def test_09_duplicate_id_version_is_rejected(self):
        payload = json.loads((ROOT / self.lib.FUTURE_SCALE_SCENARIO_CORPUS_PATH).read_text())
        payload["scenarios"].append(copy.deepcopy(payload["scenarios"][0]))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / self.lib.FUTURE_SCALE_SCENARIO_CORPUS_PATH
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(payload))
            result = self.lib.load_future_scale_scenario_corpus(root=root)
        self.assertIn("duplicate_scenario_id_version", result["errors"])

    def test_10_engineering_evidence_class_is_mandatory(self):
        scenario = copy.deepcopy(self.scenario)
        scenario["EVIDENCE_CLASS"] = "PRODUCTION_EVIDENCE"
        scenario["SCENARIO_FINGERPRINT"] = "DERIVED"
        self.assertIn("scenario_evidence_class_invalid", self.lib.validate_future_scale_scenario(scenario)["errors"])

    def test_11_authority_expansion_must_be_forbidden(self):
        scenario = copy.deepcopy(self.scenario)
        scenario["FORBIDDEN_EFFECTS"].remove("AUTHORITY_EXPANSION")
        scenario["SCENARIO_FINGERPRINT"] = "DERIVED"
        self.assertIn("scenario_forbidden_effect_boundary_incomplete", self.lib.validate_future_scale_scenario(scenario)["errors"])

    def test_12_production_maturity_credit_must_be_forbidden(self):
        scenario = copy.deepcopy(self.scenario)
        scenario["FORBIDDEN_EFFECTS"].remove("PRODUCTION_MATURITY_CREDIT")
        scenario["SCENARIO_FINGERPRINT"] = "DERIVED"
        self.assertIn("scenario_forbidden_effect_boundary_incomplete", self.lib.validate_future_scale_scenario(scenario)["errors"])

    def test_13_ordinary_frontier_preempts_scenario(self):
        result = self.lib.future_scale_scenario_frontier(self.fsse02_cps, ordinary_work_available=True)
        self.assertEqual(result["decision"], "ORDINARY_FRONTIER_SELECTED")
        self.assertEqual(result["NEXT_SCENARIO_ID"], "NONE")

    def test_14_scenario_frontier_opens_without_ordinary_work(self):
        result = self.lib.future_scale_scenario_frontier(self.fsse02_cps)
        self.assertEqual(result["decision"], "SCENARIO_READY")
        self.assertNotEqual(result["NEXT_SCENARIO_ID"], "NONE")

    def test_15_eligible_scenario_prevents_exhaustion(self):
        result = self.lib.future_scale_scenario_frontier(self.fsse02_cps)
        self.assertFalse(result["FRONTIER_EXHAUSTED"])
        self.assertEqual(result["EXHAUSTION_REASON"], "NOT_EXHAUSTED")

    def test_16_stale_result_is_reselected(self):
        target = self.corpus["scenarios"][-1]
        history = {target["SCENARIO_ID"]: {"result": "PASS", "scenario_fingerprint": "old"}}
        result = self.lib.future_scale_scenario_frontier(self.fsse02_cps, result_history=history)
        self.assertEqual(result["NEXT_SCENARIO_ID"], target["SCENARIO_ID"])

    def test_17_current_pass_is_covered(self):
        target = self.corpus["scenarios"][0]
        history = {target["SCENARIO_ID"]: {"result": "PASS", "scenario_fingerprint": target["SCENARIO_FINGERPRINT"]}}
        result = self.lib.future_scale_scenario_frontier(self.fsse02_cps, result_history=history)
        self.assertIn(target["SCENARIO_ID"], result["COVERED_SCENARIOS"])

    def test_18_priority_is_deterministic(self):
        first = self.lib.future_scale_scenario_frontier(self.fsse02_cps)
        second = self.lib.future_scale_scenario_frontier(self.fsse02_cps)
        self.assertEqual((first["NEXT_SCENARIO_ID"], first["FRONTIER_FINGERPRINT"]), (second["NEXT_SCENARIO_ID"], second["FRONTIER_FINGERPRINT"]))

    def test_19_active_scenario_duplicate_is_blocked(self):
        target = self.corpus["scenarios"][0]["SCENARIO_ID"]
        if "| `ACTIVE_SCENARIO_ID` |" in self.fsse02_cps:
            cps = self.fsse02_cps.replace("| `ACTIVE_SCENARIO_ID` | `NONE` |", f"| `ACTIVE_SCENARIO_ID` | `{target}` |")
        else:
            cps = self.fsse02_cps.replace("| `CURRENT_EXECUTION_MISSION_ID` |", f"| `ACTIVE_SCENARIO_ID` | `{target}` |\n| `CURRENT_EXECUTION_MISSION_ID` |", 1)
        result = self.lib.future_scale_scenario_frontier(cps)
        self.assertTrue(any(row["SCENARIO_ID"] == target and row["REASON"] == "ACTIVE_DUPLICATE" for row in result["BLOCKED_SCENARIOS"]))

    def test_20_frontier_has_no_runtime_or_production_impact(self):
        result = self.lib.future_scale_scenario_frontier(self.fsse02_cps)
        self.assertEqual(result["runtime_impact"], "NONE")
        self.assertEqual(result["production_impact"], "NONE")
        self.assertFalse(result["authority_expansion"])
        self.assertEqual(result["maturity_impact"], "NONE")

    def test_21_exact_fsse3_output_is_produced_after_harness_consumption(self):
        result = self.lib.future_scale_scenario_frontier(self.fsse02_cps)
        self.assertEqual(result["next_output"], "V7_FUTURE_SCALE_HIGH_FIDELITY_VALIDATION_V1")

    def test_22_program_reconciliation_consumes_scenario_frontier(self):
        sources = self.lib.load_program_execution_sources()
        sources["cps"] = sources["cps"].replace(
            "| `FSSE_00_EXTERNAL_REENTRY_STATUS` | `PRODUCTION_CERTIFIED_TWO_NATURAL_REENTRIES` |",
            "| `FSSE_00_EXTERNAL_REENTRY_STATUS` | `DEFERRED_PLATFORM_CERTIFICATION` |",
        )
        result = self.lib.program_execution_reconciliation(sources)
        self.assertTrue(result["scenario_frontier_consumer_invoked"])
        self.assertEqual(result["scenario_frontier_decision"], "SCENARIO_FRONTIER_EXHAUSTED")
        self.assertEqual(result["executable_program_frontier"], [self.lib.FUTURE_SCALE_FSSE_04_OUTPUT])

    def test_23_real_truth_check_entrypoint_exists(self):
        source = (ROOT / "tools/v7-truth-check").read_text()
        self.assertIn("--omp-program-reconciliation", source)
        self.assertIn("program_execution_reconciliation(sources", source)

    def test_24_cli_real_consumer_returns_machine_output(self):
        completed = subprocess.run(
            [str(ROOT / "tools/v7-truth-check"), "--omp-program-reconciliation", "--json"],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertTrue(payload["scenario_frontier_consumer_invoked"])

    def test_25_no_new_owner_program_queue_or_scheduler(self):
        rendered = json.dumps(self.lib.future_scale_scenario_frontier(self.cps), sort_keys=True).lower()
        self.assertNotIn("new_owner", rendered)
        self.assertNotIn("scheduler", rendered)
        self.assertNotIn("queue", rendered)


if __name__ == "__main__":
    unittest.main()
