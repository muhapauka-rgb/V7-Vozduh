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
        drift = self.cps.replace("`NO_CURRENT_PACKET;", "`READ_ONLY_BINDING_DIAGNOSIS_ONLY;", 1)
        self.assertNotEqual(self.validate(drift)["final_verdict"], "PASS")

    def test_02_engineering_authority_with_stop_safe_projection_fails(self):
        drift = self.cps.replace("| `current_primary_stop` | `REAL_WORLD_LIMIT_CAPABILITY_LOCAL; global Continue OMP frontier is bounded at BOUNDED_INVOCATION_BUDGET_REACHED` |", "| `current_primary_stop` | `STOP_SAFE` |", 1)
        self.assertIn("cps_wip_global_context_divergence", self.validate(drift)["errors"])

    def test_03_operational_authority_with_authority_required_no_fails(self):
        drift = self.cps.replace("| `AUTHORITY_REQUIRED_NOW` | `NO_INSIDE_EXISTING_ENGINEERING_PROGRAM_SCOPE` |", "| `AUTHORITY_REQUIRED_NOW` | `YES_OUTSIDE_ACTIVE_POLICY` |", 1)
        self.assertIn("delegated_policy_live_operational_authority_required", self.delegated_validate(drift)["contradiction_ids"])

    def test_04_binding_certified_with_unresolved_cap_u01_drift_fails(self):
        drift = self.cps.replace("PARTIAL_REAL_OUTCOME_CONSUMED; exact U01 SUCCESS", "bundle drifted twice", 1)
        result = self.validate(drift)
        self.assertIn("cps_active_capability_unresolved_binding_drift", result["errors"])

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
        drift = self.lib._replace_section_field(
            self.cps,
            "### Registry Metadata And Truth Lifecycle",
            "### Active Protected Work In Progress",
            "CURRENT_STOP_CONDITION",
            "`STOP_SAFE`",
        )
        self.assertIn("cps_current_stop_divergence", self.validate(drift)["errors"])

    def test_08_active_wip_next_action_context_drift_fails(self):
        drift = self.cps.replace(
            "| `smallest_existing_next_action` | preserve CAP-U07 evidence while the standard Continue OMP trigger recalculates the global frontier |",
            "| `smallest_existing_next_action` | diagnose binding owner |",
            1,
        )
        self.assertIn("cps_wip_next_action_context_divergence", self.validate(drift)["errors"])

    def test_09_sequence_position_one_stop_differs_fails(self):
        row = next(line for line in self.cps.splitlines() if line.startswith("| `1` | `FSSE_04_COMPLETE_BOUNDED_CONTINUE_OMP_READY` program frontier"))
        drift = self.cps.replace(row, row.replace("| `BOUNDED_INVOCATION_BUDGET_REACHED` |", "| `STOP_SAFE` |", 1), 1)
        self.assertIn("cps_sequence_position_1_divergence", self.validate(drift)["errors"])

    def test_10_explicit_historical_stale_values_pass(self):
        drift = self.cps + "\n## Historical Test Snapshot\nREAD_ONLY_BINDING_DIAGNOSIS_ONLY\n"
        self.assertEqual(self.validate(drift)["final_verdict"], "PASS")

    def test_11_historical_binding_drift_does_not_affect_live_scheduling(self):
        self.assertIn("SUPERSEDED/HISTORICAL: SOURCE_SNAPSHOT_BUNDLE_DRIFT", self.cps)
        self.assertEqual(self.validate(self.cps)["current_stop"], "BOUNDED_INVOCATION_BUDGET_REACHED")

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
                written.write_text(text.replace("| `current_primary_stop` | `REAL_WORLD_LIMIT_CAPABILITY_LOCAL; global Continue OMP frontier is bounded at BOUNDED_INVOCATION_BUDGET_REACHED` |", "| `current_primary_stop` | `STOP_SAFE` |", 1), encoding="utf-8")
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
        self.assertTrue(live["CONTROLLED_RUN_EXECUTION_AUTHORIZED"].strip("`").startswith("NO_CURRENT_PACKET"))
        self.assertTrue(live["PRODUCTION_RUNTIME_IMPACT"].strip("`").startswith("NONE"))
        self.assertTrue(live["USER_MOVEMENT"].strip("`").startswith("NO"))
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
            "CURRENT_STOP_CONDITION",
            "`OPERATIONAL_AUTHORITY`",
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
        drift = self.cps.replace("satisfied prerequisite; terminal evidence retained by existing owners", "only after explicit approval", 1)
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

    def test_29_closed_u01_is_counted_once_and_not_open(self):
        registry = self.lib._markdown_field_table(self.lib._markdown_section(
            self.cps, "### Registry Metadata And Truth Lifecycle", "### Active Protected Work In Progress"
        ))
        open_intents = self.lib._markdown_section(
            self.cps,
            "### Open Engineering Intents And Last Responsible Links",
            "### Deterministic Execution Sequence",
        )
        self.assertEqual(registry["COMPLETE_OR_LOCKED_CAPABILITIES"].strip("`"), "13")
        self.assertEqual(registry["UNFINISHED_CAPABILITIES"].strip("`"), "21")
        self.assertEqual(registry["OPEN_ENGINEERING_INTENTS"].strip("`"), "21")
        self.assertNotIn("| `U01` |", open_intents)

    def test_30_real_world_limit_is_local_while_fsse_program_continues(self):
        stops = self.lib._markdown_section(
            self.cps,
            "### Authority, Reality And Safety Stops",
            "### Owner Revalidation Requirements And Contradictions",
        )
        self.assertIn("Capability-local WAITING boundary for CAP-U02/U05/U06", stops)
        self.assertNotIn("Current U01 program terminal", stops)
        self.assertIn("`SUPERSEDED/HISTORICAL`; U01 boundary", stops)
        live = self.lib._markdown_field_table(self.lib._markdown_section(
            self.cps, "## 0. Authoritative Live Current State", "## Authoritative Unfinished Capability Closure Registry"
        ))
        self.assertEqual(live["PROGRAM_TERMINAL_CLASS"].strip("`"), "BOUNDED_INVOCATION_BUDGET_REACHED")
        self.assertEqual(live["NEXT_EXECUTABLE_CAPABILITY"].strip("`"), "NONE")

    def test_31_cap_con_06_matches_current_program_terminal(self):
        row = next(line for line in self.cps.splitlines() if line.startswith("| `CAP-CON-06` |"))
        self.assertIn("current program terminal is `BOUNDED_INVOCATION_BUDGET_REACHED`", row)
        self.assertIn("`SUPERSEDED/HISTORICAL`", row)
        self.assertEqual(self.delegated_validate(self.cps)["contradiction_count"], 0)

    def test_32_cap_con_06_terminal_drift_fails_closed(self):
        row = next(line for line in self.cps.splitlines() if line.startswith("| `CAP-CON-06` |"))
        drifted_row = row.replace(
            "current program terminal is `BOUNDED_INVOCATION_BUDGET_REACHED`",
            "current program terminal is `OPERATIONAL_AUTHORITY`",
            1,
        ).replace("`SUPERSEDED/HISTORICAL`", "historical", 1)
        result = self.delegated_validate(self.cps.replace(row, drifted_row, 1))
        self.assertIn("delegated_policy_cap_con_06_current_terminal_divergence", result["contradiction_ids"])
        self.assertIn("delegated_policy_cap_con_06_stale_operational_authority", result["contradiction_ids"])

    def test_33_normalized_builder_repairs_cap_con_06_terminal_drift(self):
        row = next(line for line in self.cps.splitlines() if line.startswith("| `CAP-CON-06` |"))
        drift = self.cps.replace(
            row,
            "| `CAP-CON-06` | Controlled Run responsibility | stale | CPS/OMP current state | current program terminal is `OPERATIONAL_AUTHORITY` |",
            1,
        )
        rendered = self.lib.build_normalized_cps_document(drift)
        rendered_row = next(line for line in rendered.splitlines() if line.startswith("| `CAP-CON-06` |"))
        self.assertIn("current program terminal is `BOUNDED_INVOCATION_BUDGET_REACHED`", rendered_row)
        self.assertIn("`SUPERSEDED/HISTORICAL`", rendered_row)
        self.assertEqual(self.delegated_validate(rendered)["contradiction_count"], 0)

    def test_34_registry_smallest_action_is_fsse_04(self):
        registry = self.lib._markdown_field_table(self.lib._markdown_section(
            self.cps, "### Registry Metadata And Truth Lifecycle", "### Active Protected Work In Progress"
        ))
        self.assertEqual(registry["EXACT_CURRENT_SMALLEST_NEXT_ACTION_ID"].strip("`"), "CONTINUE_OMP")
        self.assertIn("Continue OMP", registry["EXACT_CURRENT_SMALLEST_NEXT_ACTION"])

    def test_35_registry_continuation_pointer_preempts_capability_wait(self):
        registry = self.lib._markdown_field_table(self.lib._markdown_section(
            self.cps, "### Registry Metadata And Truth Lifecycle", "### Active Protected Work In Progress"
        ))
        self.assertIn("run Continue OMP", registry["OMP_CONTINUATION_POINTER"])
        self.assertIn("preserve CAP-U07 WAITING WIP", registry["OMP_CONTINUATION_POINTER"])

    def test_36_wip_local_wait_does_not_become_global_terminal(self):
        wip = self.lib._markdown_field_table(self.lib._markdown_section(
            self.cps, "### Active Protected Work In Progress", "### Complete Or Locked Capability Records"
        ))
        self.assertIn("REAL_WORLD_LIMIT_CAPABILITY_LOCAL", wip["current_primary_stop"])
        self.assertIn("Continue OMP", wip["current_primary_stop"])
        self.assertIn("BOUNDED_INVOCATION_BUDGET_REACHED", wip["current_primary_stop"])

    def test_37_program_stage_mismatch_fails_derived_projection_gate(self):
        drift = self.lib._replace_section_field(self.cps, "## 0. Authoritative Live Current State", "## Authoritative Unfinished Capability Closure Registry", "CURRENT_PROGRAM_STAGE", "`STALE`")
        result = self.validate(drift)
        self.assertEqual(result["current_state_derived_projection_consistency"], "FAIL")

    def test_38_program_frontier_mismatch_fails_derived_projection_gate(self):
        drift = self.lib._replace_section_field(self.cps, "## 0. Authoritative Live Current State", "## Authoritative Unfinished Capability Closure Registry", "CURRENT_PROGRAM_EXECUTION_FRONTIER", "`HEARTBEAT_DEPLOY`")
        self.assertEqual(self.validate(drift)["current_state_derived_projection_consistency"], "FAIL")

    def test_39_fsse_status_mismatch_fails_derived_projection_gate(self):
        drift = self.lib._replace_section_field(self.cps, "## 0. Authoritative Live Current State", "## Authoritative Unfinished Capability Closure Registry", "FSSE_STATUS", "`FSSE_01_NOT_ADMITTED`")
        self.assertEqual(self.validate(drift)["current_state_derived_projection_consistency"], "FAIL")

    def test_40_next_scenario_mismatch_fails_derived_projection_gate(self):
        drift = self.lib._replace_section_field(self.cps, "## 0. Authoritative Live Current State", "## Authoritative Unfinished Capability Closure Registry", "NEXT_SCENARIO_ID", "`HEALTHY_BASELINE_SMALL`")
        self.assertEqual(self.validate(drift)["current_state_derived_projection_consistency"], "FAIL")

    def test_41_sequence_head_binds_scenario_and_execution_class(self):
        row = next(line for line in self.cps.splitlines() if line.startswith("| `1` |"))
        self.assertIn("next scenario NONE", row)
        self.assertIn("EXISTING_OMP_SELF_CONTINUATION_CONSUMER", row)
        self.assertIn("NEXT_BOUNDED_OMP_ACTION_OR_LEGAL_TERMINAL", row)

    def test_42_current_derived_projection_gate_passes(self):
        result = self.validate(self.cps)
        self.assertEqual(result["current_state_derived_projection_consistency"], "PASS")
        self.assertEqual(result["derived_projection_contradiction_count"], 0)


if __name__ == "__main__":
    unittest.main()
