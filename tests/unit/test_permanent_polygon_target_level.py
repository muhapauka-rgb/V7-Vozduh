from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_permanent_polygon_target_level_test", ROOT / "tools/v7_sync_lib.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PermanentPolygonTargetLevelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.cps = (ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text(encoding="utf-8")

    def test_mission0_rejects_stale_phase6_and_false_global_stop(self):
        live = self.lib._normalized_state_from_live_cps(self.cps)
        rendered = self.lib.build_normalized_cps_document(self.cps, live)
        stale = rendered.replace(
            f"| `PHASE_6_CERTIFICATION_FRONTIER` | `{live['current_next_action_id']}` |",
            "| `PHASE_6_CERTIFICATION_FRONTIER` | `STALE-CAP-U06` |",
            1,
        ).replace("| `PHASE_6_GLOBAL_STOP` | `NONE` |", "| `PHASE_6_GLOBAL_STOP` | `REAL_WORLD_LIMIT` |", 1)
        result = self.lib.cps_live_state_consistency(stale, verify_external=False, expected_state=live)
        self.assertEqual(result["final_verdict"], "NO-GO")
        self.assertIn("permanent_polygon_phase6_frontier_stale", result["errors"])
        self.assertIn("permanent_polygon_false_global_real_world_stop", result["errors"])

    def test_frontier_roles_and_consumed_rows_are_unambiguous(self):
        result = self.lib.cps_live_state_consistency(self.cps, root=ROOT, verify_external=False)
        self.assertEqual(result["final_verdict"], "PASS")
        for record in self.lib.permanent_polygon_criterion_registry(self.cps)["records"]:
            if record.get("lifecycle_state") == "CONSUMED":
                cap = record["capability_id"]
                row = next(line for line in self.cps.splitlines() if line.startswith(f"| `{cap}` |"))
                self.assertIn(record["criterion_id"].split(":", 1)[1], row)
                self.assertIn("whole capability remains PARTIAL", row)

    def test_gap_register_historical_lifecycle_annotation(self):
        register = (ROOT / "docs/reports/research/V7_CERTIFIED_AUTONOMOUS_BEHAVIOUR_GAP_REGISTER.md").read_text()
        self.assertIn("HISTORICAL_TERMINAL_SNAPSHOT", register)
        self.assertIn("Current live continuation, frontier and program status are owned only by CPS and OMP", register)

    def test_cap_u07_owner_chain_and_cleanup(self):
        supply = self.lib.permanent_polygon_obligation_supply(self.cps, root=ROOT)
        obligation = next(row for row in supply["obligations"] if row["capability_id"] == "CAP-U07")
        result = self.lib.execute_permanent_polygon_cap_u07_shadow_learning_matrix(obligation, root=ROOT)
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertTrue(result["checks"]["held_out_replay_consumed"])
        self.assertTrue(result["checks"]["reset_cleanup_proven"])
        self.assertFalse(result["whole_capability_complete"])

    def test_all_missing_owner_adapters_call_real_owners(self):
        supply = self.lib.permanent_polygon_obligation_supply(self.cps, root=ROOT)
        by_cap = {row["capability_id"]: row for row in supply["obligations"]}
        for cap in ("CAP-U12", "CAP-U13", "CAP-U14", "CAP-U16", "CAP-U20"):
            with self.subTest(capability=cap):
                executor = self.lib.PERMANENT_POLYGON_EXECUTOR_REGISTRY[by_cap[cap]["criterion_id"]]
                result = executor(by_cap[cap], root=ROOT)
                self.assertEqual(result["final_verdict"], "PASS")
                self.assertTrue(result["owner_outputs"])
                self.assertIn("OMP_PROGRAM_EXECUTION_RECONCILIATION", result["results"][0]["consumers"])

    def test_all_current_seed_criteria_consumed(self):
        consumed = set(self.lib.permanent_polygon_consumed_criterion_ids(self.cps))
        expected = {f"{cap}:{metadata[0]}" for cap, metadata in self.lib.PERMANENT_POLYGON_CURRENT_SEED.items()}
        self.assertEqual(expected - consumed, set())

    def test_proactive_multi_generation_and_cross_process_contracts(self):
        proactive = self.lib.synthesize_permanent_polygon_owner_backed_situations(root=ROOT)
        campaign = self.lib.run_permanent_polygon_multi_generation_campaign(root=ROOT)
        cross = self.lib.run_permanent_polygon_cross_process_stability_soak(root=ROOT)
        self.assertEqual(proactive["final_verdict"], "PASS")
        self.assertEqual(proactive["family_count"], 12)
        self.assertEqual(campaign["final_verdict"], "PASS")
        self.assertEqual(len(campaign["generations"]), 3)
        self.assertEqual(cross["final_verdict"], "PASS")
        self.assertEqual(cross["soak"]["iterations_executed"], 100)

    def test_stale_cas_preserves_original(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "V7_CURRENT_PROGRAM_STATE.md"
            path.write_text(self.cps, encoding="utf-8")
            result = self.lib.atomic_reconcile_cps(
                path, expected_generation="cpsgen_STALE", request_external_wake=False,
            )
            self.assertEqual(result["status"], "STALE_CPS_GENERATION_STOP_SAFE")
            self.assertEqual(path.read_text(encoding="utf-8"), self.cps)

    def test_direct_final_certification_frontier_suppresses_external_overlap(self):
        live = self.lib._markdown_field_table(self.lib._markdown_section(
            self.cps, "## 0. Authoritative Live Current State",
            "## Authoritative Unfinished Capability Closure Registry",
        ))
        result = self.lib._external_reentry_eligibility({
            key: value.strip("`") for key, value in live.items()
        })
        self.assertFalse(result["eligible"])
        self.assertEqual(result["outcome"], "REENTRY_ALREADY_ACTIVE")
        self.assertIn("active_execution_frontier", result["reason"])


if __name__ == "__main__":
    unittest.main()
