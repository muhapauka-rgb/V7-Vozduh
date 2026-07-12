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

    def delegated_validate(self, text):
        return self.lib.delegated_policy_live_state_consistency(text, self.omp)

    def test_01_binding_pass_with_binding_diagnosis_fails(self):
        drift = self.cps.replace("`NO_OUTSIDE_ACTIVE_POLICY;", "`READ_ONLY_BINDING_DIAGNOSIS_ONLY;", 1)
        self.assertNotEqual(self.validate(drift)["final_verdict"], "PASS")

    def test_02_operational_authority_with_stop_safe_projection_fails(self):
        drift = self.cps.replace("| `current_primary_stop` | `OPERATIONAL_AUTHORITY` |", "| `current_primary_stop` | `STOP_SAFE` |", 1)
        self.assertIn("cps_current_stop_divergence", self.validate(drift)["errors"])

    def test_03_operational_authority_with_authority_required_no_fails(self):
        drift = self.cps.replace("| `AUTHORITY_REQUIRED_NOW` | `YES_OUTSIDE_ACTIVE_POLICY;", "| `AUTHORITY_REQUIRED_NOW` | `NO_INSIDE_APPROVED_POLICY;", 1)
        self.assertIn("cps_authority_required_not_policy_bounded", self.validate(drift)["errors"])

    def test_04_binding_certified_with_unresolved_cap_u01_drift_fails(self):
        drift = self.cps.replace("bounded policy `APPROVED`", "bundle drifted twice", 1)
        result = self.validate(drift)
        self.assertIn("cps_cap_u01_unresolved_binding_drift", result["errors"])

    def test_05_fresh_scope_with_reusable_packet_fails(self):
        drift = self.cps.replace("| `OLD_PACKETS_REUSABLE` | `NO` |", "| `OLD_PACKETS_REUSABLE` | `YES` |", 1)
        self.assertIn("cps_old_packets_reusable", self.validate(drift)["errors"])

    def test_06_current_mission_report_identity_mismatch_fails(self):
        drift = self.lib._replace_section_field(
            self.cps,
            "## 0. Authoritative Live Current State",
            "## Authoritative Unfinished Capability Closure Registry",
            "CURRENT_MISSION_REPORT",
            "`missing-report.md`",
        )
        self.assertIn("MISSION_ROLE_AMBIGUITY_STOP_SAFE", self.validate(drift)["errors"])

    def test_07_registry_stop_differs_from_section_zero_fails(self):
        marker = "| `CURRENT_STOP_CONDITION` | `OPERATIONAL_AUTHORITY` |"
        first = self.cps.find(marker)
        second = self.cps.find(marker, first + 1)
        drift = self.cps[:second] + self.cps[second:].replace(marker, "| `CURRENT_STOP_CONDITION` | `STOP_SAFE` |", 1)
        self.assertIn("cps_current_stop_divergence", self.validate(drift)["errors"])

    def test_08_active_wip_next_action_differs_from_cap_u01_fails(self):
        drift = self.cps.replace(
            "| `smallest_existing_next_action` | `APPROVE_EXACT_TWO_USER_ROUTE_INTEGRITY_REPAIR`; one-time exact two-user serial repair only; no mutation before authority |",
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
        self.assertEqual(live["CONTROLLED_RUN_AUTHORITY_GENERATION"].strip("`"), "POLICY_SCOPED; NO_PACKET_SPECIFIC_AUTHORITY_REQUIRED")
        self.assertTrue(live["CONTROLLED_RUN_ROLLBACK_MANIFEST"].strip("`").startswith("NONE_OPEN"))
        self.assertTrue(live["CONTROLLED_RUN_EXECUTION_AUTHORIZED"].strip("`").startswith("NO_OUTSIDE_ACTIVE_POLICY"))
        self.assertTrue(live["PRODUCTION_RUNTIME_IMPACT"].strip("`").startswith("ONE_FORWARD_MUTATION_AND_CERTIFIED_ROLLBACK"))
        self.assertEqual(live["USER_MOVEMENT"].strip("`"), "NO")
        self.assertIn("state=OPEN", live["ADMIN_SAFE_MODE_LIVE_STATE"])

    def test_21_approved_policy_with_packet_approval_required_fails(self):
        drift = self.cps.replace("| `PACKET_APPROVAL_REQUIRED` | `NO` |", "| `PACKET_APPROVAL_REQUIRED` | `YES` |", 1)
        result = self.delegated_validate(drift)
        self.assertIn("delegated_policy_live_packet_approval_required", result["contradiction_ids"])

    def test_22_approved_policy_with_candidate_approval_required_fails(self):
        drift = self.cps.replace("| `CANDIDATE_APPROVAL_REQUIRED` | `NO` |", "| `CANDIDATE_APPROVAL_REQUIRED` | `YES` |", 1)
        result = self.delegated_validate(drift)
        self.assertIn("delegated_policy_live_candidate_approval_required", result["contradiction_ids"])

    def test_23_operational_authority_without_external_boundary_fails(self):
        drift = self.lib._replace_section_field(
            self.cps,
            "## 0. Authoritative Live Current State",
            "## Authoritative Unfinished Capability Closure Registry",
            "EXTERNAL_INPUT_REQUIRED",
            "`FALSE`",
        )
        result = self.delegated_validate(drift)
        self.assertIn("delegated_policy_current_stop_is_operational_authority", result["contradiction_ids"])

    def test_24_no_authority_required_with_exact_generation_request_fails(self):
        drift = self.cps.replace(
            "| `CONTROLLED_RUN_AUTHORITY_GENERATION` | `POLICY_SCOPED; NO_PACKET_SPECIFIC_AUTHORITY_REQUIRED` |",
            "| `CONTROLLED_RUN_AUTHORITY_GENERATION` | `NONE_CURRENT; request new exact authority generation` |",
            1,
        )
        result = self.delegated_validate(drift)
        self.assertIn("delegated_policy_stale_exact_authority_generation_request", result["contradiction_ids"])

    def test_25_sequence_explicit_approval_inside_policy_fails(self):
        drift = self.cps.replace("after delegated policy admission and all live gates", "only after explicit approval", 1)
        result = self.delegated_validate(drift)
        self.assertIn("delegated_policy_sequence_requires_explicit_approval", result["contradiction_ids"])

    def test_26_unclassified_historical_operational_authority_fails(self):
        drift = self.cps.replace(
            "Historical U01 stop: the old approval remains terminally invalid and cannot be reused.",
            "historical OPERATIONAL_AUTHORITY approval remains context",
            1,
        )
        result = self.delegated_validate(drift)
        self.assertIn("historical_operational_authority_without_classification", result["contradiction_ids"])

    def test_27_stop_or_next_action_projection_disagreement_fails(self):
        drift = self.lib._replace_section_field(
            self.cps,
            "### Registry Metadata And Truth Lifecycle",
            "### Active Protected Work In Progress",
            "CURRENT_STOP_CONDITION",
            "`STOP_SAFE`",
        )
        result = self.delegated_validate(drift)
        self.assertEqual(result["cps_stop_consistency"], "FAIL")
        self.assertIn("delegated_policy_cps_stop_divergence", result["contradiction_ids"])

    def test_28_reconciled_delegated_policy_live_state_is_machine_readable(self):
        result = self.delegated_validate(self.cps)
        self.assertEqual(result["delegated_policy_live_state_consistency"], "PASS")
        self.assertEqual(result["stale_operational_authority_projection_count"], 0)
        self.assertEqual(result["stale_packet_approval_projection_count"], 0)
        self.assertEqual(result["stale_candidate_approval_projection_count"], 0)
        self.assertEqual(result["contradiction_count"], 0)


if __name__ == "__main__":
    unittest.main()
