import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "tools" / "v7_sync_lib.py"
CPS = ROOT / "docs" / "programs" / "V7_CURRENT_PROGRAM_STATE.md"
OMP = ROOT / "docs" / "programs" / "OPERATIONAL_MATURITY_PROGRAM.md"


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_cps_atomic_test", LIB)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class CpsAtomicReconciliationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.cps = CPS.read_text(encoding="utf-8")
        cls.omp = OMP.read_text(encoding="utf-8")

    def validate(self, text):
        return self.lib.cps_live_state_consistency(text, root=ROOT, omp_text=self.omp)

    def test_01_binding_pass_with_binding_diagnosis_fails(self):
        drift = self.cps.replace("`AUTHORITY_REQUEST_ONLY;", "`READ_ONLY_BINDING_DIAGNOSIS_ONLY;", 1)
        self.assertNotEqual(self.validate(drift)["final_verdict"], "PASS")

    def test_02_operational_authority_with_stop_safe_projection_fails(self):
        drift = self.cps.replace("| `current_primary_stop` | `OPERATIONAL_AUTHORITY` |", "| `current_primary_stop` | `STOP_SAFE` |", 1)
        self.assertIn("cps_current_stop_divergence", self.validate(drift)["errors"])

    def test_03_operational_authority_with_authority_required_no_fails(self):
        drift = self.cps.replace("| `AUTHORITY_REQUIRED_NOW` | `YES;", "| `AUTHORITY_REQUIRED_NOW` | `NO;", 1)
        self.assertIn("cps_authority_required_not_yes", self.validate(drift)["errors"])

    def test_04_binding_certified_with_unresolved_cap_u01_drift_fails(self):
        drift = self.cps.replace("| `OPERATIONAL_AUTHORITY` | request one new exact Mission-scoped", "| `STOP_SAFE`; bundle drifted twice | diagnose existing binding", 1)
        result = self.validate(drift)
        self.assertIn("cps_cap_u01_unresolved_binding_drift", result["errors"])

    def test_05_fresh_scope_with_reusable_packet_fails(self):
        drift = self.cps.replace("| `OLD_PACKETS_REUSABLE` | `NO` |", "| `OLD_PACKETS_REUSABLE` | `YES` |", 1)
        self.assertIn("cps_old_packets_reusable", self.validate(drift)["errors"])

    def test_06_current_mission_report_identity_mismatch_fails(self):
        drift = self.cps.replace("2026-07-12_011049_atomic_cps_live_state_reconciliation_and_consistency_guard.md", "missing-report.md", 1)
        self.assertIn("cps_current_mission_report_identity_mismatch", self.validate(drift)["errors"])

    def test_07_registry_stop_differs_from_section_zero_fails(self):
        marker = "| `CURRENT_STOP_CONDITION` | `OPERATIONAL_AUTHORITY` |"
        first = self.cps.find(marker)
        second = self.cps.find(marker, first + 1)
        drift = self.cps[:second] + self.cps[second:].replace(marker, "| `CURRENT_STOP_CONDITION` | `STOP_SAFE` |", 1)
        self.assertIn("cps_current_stop_divergence", self.validate(drift)["errors"])

    def test_08_active_wip_next_action_differs_from_cap_u01_fails(self):
        drift = self.cps.replace(
            "| `smallest_existing_next_action` | request one new exact Mission-scoped Operational Authority; after approval generate a new fresh packet; never reuse old identities |",
            "| `smallest_existing_next_action` | diagnose binding owner |",
            1,
        )
        self.assertIn("cps_wip_cap_u01_next_action_divergence", self.validate(drift)["errors"])

    def test_09_sequence_position_one_stop_differs_fails(self):
        row = next(line for line in self.cps.splitlines() if line.startswith("| `1` | `U01` Controlled Run WIP"))
        drift = self.cps.replace(row, row.replace("`OPERATIONAL_AUTHORITY`", "`STOP_SAFE`"), 1)
        self.assertIn("cps_sequence_position_1_divergence", self.validate(drift)["errors"])

    def test_10_explicit_historical_stale_values_pass(self):
        drift = self.cps + "\n## Historical Test Snapshot\nREAD_ONLY_BINDING_DIAGNOSIS_ONLY\n"
        self.assertEqual(self.validate(drift)["final_verdict"], "PASS")

    def test_11_historical_binding_drift_does_not_affect_live_scheduling(self):
        self.assertIn("SUPERSEDED/HISTORICAL: SOURCE_SNAPSHOT_BUNDLE_DRIFT", self.cps)
        self.assertEqual(self.validate(self.cps)["current_stop"], "OPERATIONAL_AUTHORITY")

    def test_12_single_normalized_state_generates_all_live_projections(self):
        rendered = self.lib.build_normalized_cps_document(self.cps)
        result = self.validate(rendered)
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertEqual(result["contradiction_count"], 0)

    def test_13_atomic_write_failure_preserves_previous_valid_cps(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "CPS.md"
            path.write_text(self.cps, encoding="utf-8")
            before = path.read_text(encoding="utf-8")
            def fail_replace(source, target):
                raise OSError("injected replace failure")
            result = self.lib.atomic_reconcile_cps(path, replace_func=fail_replace)
            self.assertFalse(result["ok"])
            self.assertTrue(result["previous_state_preserved"])
            self.assertEqual(path.read_text(encoding="utf-8"), before)

    def test_14_post_write_reread_detects_partial_update_and_rolls_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "CPS.md"
            path.write_text(self.cps, encoding="utf-8")
            before = path.read_text(encoding="utf-8")
            def corrupt(written):
                text = written.read_text(encoding="utf-8")
                written.write_text(text.replace("| `current_primary_stop` | `OPERATIONAL_AUTHORITY` |", "| `current_primary_stop` | `STOP_SAFE` |", 1), encoding="utf-8")
            result = self.lib.atomic_reconcile_cps(path, post_write_hook=corrupt)
            self.assertEqual(result["status"], "CPS_POST_WRITE_REREAD_FAILED_ROLLED_BACK")
            self.assertTrue(result["previous_state_preserved"])
            self.assertEqual(path.read_text(encoding="utf-8"), before)

    def test_15_mission_identity_guard_remains_pass_for_current_report(self):
        self.assertEqual(self.validate(self.cps)["mission_identity_consistency"], "PASS")

    def test_16_omp_consumes_cps_pointer_not_historical_snapshot(self):
        omp = self.omp + "\nHistorical OMP snapshot: STOP_SAFE binding diagnosis\n"
        result = self.lib.cps_live_state_consistency(self.cps, root=ROOT, omp_text=omp)
        self.assertEqual(result["omp_pointer_consistency"], "PASS")

    def test_17_current_state_contradictions_are_zero(self):
        self.assertEqual(self.validate(self.cps)["contradiction_count"], 0)

    def test_18_registry_sequence_contradictions_are_zero(self):
        self.assertEqual(self.validate(self.cps)["registry_sequence_consistency"], "PASS")

    def test_19_stale_current_looking_fields_are_zero(self):
        self.assertEqual(self.validate(self.cps)["stale_live_projection_count"], 0)

    def test_20_no_packet_lease_barrier_apply_or_user_movement(self):
        live = self.lib._markdown_field_table(self.lib._markdown_section(
            self.cps, "## 0. Authoritative Live Current State", "## Authoritative Unfinished Capability Closure Registry"
        ))
        self.assertTrue(live["CONTROLLED_RUN_PACKET_PREVIEW"].strip("`").startswith("NONE_OPEN"))
        self.assertTrue(live["CONTROLLED_RUN_AUTHORITY_GENERATION"].strip("`").startswith("NONE_CURRENT"))
        self.assertTrue(live["CONTROLLED_RUN_ROLLBACK_MANIFEST"].strip("`").startswith("NONE_OPEN"))
        self.assertEqual(live["CONTROLLED_RUN_EXECUTION_AUTHORIZED"].strip("`"), "NO_CURRENT_AUTHORITY")
        self.assertTrue(live["PRODUCTION_RUNTIME_IMPACT"].strip("`").startswith("NONE"))
        self.assertEqual(live["USER_MOVEMENT"].strip("`"), "NO")
        self.assertIn("state=OPEN", live["ADMIN_SAFE_MODE_LIVE_STATE"])


if __name__ == "__main__":
    unittest.main()
