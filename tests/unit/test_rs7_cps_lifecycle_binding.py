import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "tools" / "v7_sync_lib.py"
CPS = ROOT / "docs" / "programs" / "V7_CURRENT_PROGRAM_STATE.md"


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_rs7_binding_test", LIB)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class Rs7CpsLifecycleBindingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.cps = CPS.read_text(encoding="utf-8")

    @staticmethod
    def packet(**overrides):
        value = {
            "mission_id": "ADMIN_OPERATOR_READ_MODEL_WRAPPER_COLLAPSE_V1",
            "candidate_instance_id": "BDP-ICI-F5B31A66F63355878E9DCA24",
            "candidate_identity": "f5b31a66f63355878e9dca247301ef849fbafff5735f2ddb1dc25e967bb7510f",
            "omp_admission_decision": "MISSION_ACCEPTED",
            "omp_mission_state": "PREPARED_NOT_ACTIVE",
            "scope_classification": "MANAGEMENT_PLANE",
            "existing_owner": "admin_core.operator_views existing owner",
            "runtime_impact": "NONE",
            "production_impact": "NONE",
            "authority_impact": "NONE",
            "product_contract_preserved": True,
            "validation_contract_exists": True,
            "rollback_contract_exists": True,
            "no_new_owner": True,
            "no_new_truth_source": True,
            "no_new_runtime": True,
        }
        value.update(overrides)
        return value

    def projected_admission_cps(self):
        mission_id = self.packet()["mission_id"]
        text = self.cps
        for key, value in (
            ("CURRENT_PROGRAM_STAGE", "RS7_PHYSICAL_SIMPLIFICATION_EXECUTION"),
            ("CURRENT_PROGRAM_EXECUTION_FRONTIER", f"ADMITTED_READY_FOR_IMPLEMENTATION:{mission_id}"),
            ("CURRENT_EXECUTION_MISSION_ID", mission_id),
            ("CURRENT_EXECUTION_MISSION_STATE", "MISSION_ADMITTED"),
        ):
            text = self.lib._replace_section_field(
                text,
                "## 0. Authoritative Live Current State",
                "## Authoritative Unfinished Capability Closure Registry",
                key,
                f"`{value}`",
            )
        return text

    def rs6_pre_admission_cps(self):
        text = self.cps
        for key, value in (
            ("CURRENT_STATE_GENERATION", "cpsgen_RS6_ADMITTED_65CB2232971"),
            ("CURRENT_PROGRAM_STAGE", "RS6_RUNTIME_PACKAGE_MINIMIZATION"),
            ("CURRENT_PROGRAM_EXECUTION_FRONTIER", "ADMITTED_READY_READ_ONLY:V7_OMP_BDP_65CB2232971BC224D937140C_V1"),
            ("CURRENT_EXECUTION_MISSION_ID", "V7_OMP_BDP_65CB2232971BC224D937140C_V1"),
            ("CURRENT_EXECUTION_MISSION_STATE", "PREPARED_NOT_ACTIVE"),
        ):
            text = self.lib._replace_section_field(
                text, "## 0. Authoritative Live Current State",
                "## Authoritative Unfinished Capability Closure Registry", key, f"`{value}`",
            )
        return text

    def rs7_admission_state(self, cps_text=None):
        mission_id = self.packet()["mission_id"]
        state = self.lib._normalized_state_from_live_cps(cps_text or self.rs6_pre_admission_cps())
        state.update({
            "state_captured": "2026-08-14T07:08:37+00:00",
            "current_active_scope": "RS7_PHYSICAL_SIMPLIFICATION_EXECUTION",
            "current_safe_next_action": "EXECUTE_ADMIN_OPERATOR_READ_MODEL_WRAPPER_COLLAPSE_V1",
            "current_scope_class": "BOUNDED_MANAGEMENT_PLANE_SIMPLIFICATION",
            "current_state_generation": "cpsgen_RS7_ADMIN_ADMITTED_F5B31A66F633",
            "current_transition_id": "V7_RS6_SCOPED_TO_RS7_ADMIN_OPERATOR_READ_MODEL_ADMISSION_V1",
            "current_next_action_id": "EXECUTE_ADMIN_OPERATOR_READ_MODEL_WRAPPER_COLLAPSE_V1",
            "current_program_stage": "RS7_PHYSICAL_SIMPLIFICATION_EXECUTION",
            "current_program_execution_frontier": f"ADMITTED_READY_FOR_IMPLEMENTATION:{mission_id}",
            "current_execution_frontier": f"ADMITTED_READY_FOR_IMPLEMENTATION:{mission_id}",
            "program_frontier_input": "RS6 scoped residual isolation PASS for one bounded Management Plane Mission",
            "program_frontier_owner": "EXISTING_OMP_CPS_ATOMIC_RECONCILIATION_OWNER",
            "program_frontier_expected_output": "MISSION_EXECUTION_ALLOWED -> bounded implementation -> validation -> residue closure",
            "program_terminal_state": "NONE_RS7_BOUNDED_MISSION_ADMITTED",
            "current_execution_mission_id": mission_id,
            "current_execution_mission_state": "MISSION_ADMITTED",
            "current_mission_role": "ACTIVE_MISSION",
            "current_mission_id": mission_id,
            "current_run_nonce": "rs7_admin_wrapper_f5b31a66f633",
            "current_mission_state": "MISSION_ADMITTED",
            "current_mission_report": "docs/reports/engineering/2026-08-14_160000_admin_operator_read_model_cps_admission_report.md",
            "current_completion_contract": "IMPLEMENTATION_COMPLETION",
            "current_completion_verdict": "MISSION_ADMITTED",
            "transaction_terminal_class": "RS7_BOUNDED_MISSION_ADMITTED",
            "next_mission_id": mission_id,
            "continuation_stop_reason": "RS6_SCOPED_CONSUMPTION_ELIGIBLE; RS7_ADMIN_MISSION_ADMITTED",
            "no_progress_fingerprint": self.packet()["candidate_identity"],
            "smallest_existing_next_action": "EXECUTE_ADMIN_OPERATOR_READ_MODEL_WRAPPER_COLLAPSE_V1",
            "wip_smallest_existing_next_action_id": "EXECUTE_ADMIN_OPERATOR_READ_MODEL_WRAPPER_COLLAPSE_V1",
            "wip_smallest_existing_next_action": "EXECUTE_ADMIN_OPERATOR_READ_MODEL_WRAPPER_COLLAPSE_V1; preserve CAP-U07 natural-evidence WIP",
            "omp_continuation_pointer": "execute only ADMIN_OPERATOR_READ_MODEL_WRAPPER_COLLAPSE_V1 through existing RS7 lifecycle; preserve RS6 physical-minimization residuals",
            "source_summary": "RS6 scoped residual isolation admits one existing-owner Management Plane Mission; no Runtime, Production or Authority effect.",
        })
        return state

    def test_prepared_packet_is_bound_but_not_authorized_to_execute(self):
        result = self.lib.rs7_physical_mission_lifecycle_binding(self.cps, self.packet())
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertEqual(result["binding_status"], "RS7_LIFECYCLE_BINDING_READY")
        self.assertEqual(result["execution_authorization"], "PENDING_CPS_ADMISSION")
        self.assertFalse(result["mutation_performed"])

    def test_current_rs6_frontier_cannot_issue_execution_authorization(self):
        result = self.lib.rs7_physical_mission_lifecycle_binding(
            self.rs6_pre_admission_cps(), self.packet(), requested_state="MISSION_EXECUTION_ALLOWED",
        )
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertIn("rs7_predecessor_not_consumed", result["errors"])
        self.assertEqual(result["execution_authorization"], "NONE")

    def test_atomic_rs7_admission_projection_can_be_authorized_without_execution(self):
        admitted = self.lib.rs7_physical_mission_lifecycle_binding(
            self.projected_admission_cps(), self.packet(), requested_state="MISSION_ADMITTED",
        )
        self.assertEqual(admitted["final_verdict"], "PASS")
        self.assertEqual(admitted["execution_authorization"], "PENDING_EXECUTION_AUTHORIZATION")
        result = self.lib.rs7_physical_mission_lifecycle_binding(
            self.projected_admission_cps(), self.packet(), requested_state="MISSION_EXECUTION_ALLOWED",
        )
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertEqual(result["execution_authorization"], "MISSION_EXECUTION_ALLOWED")
        self.assertFalse(result["mutation_performed"])

    def test_missing_rollback_contract_stops_safe(self):
        result = self.lib.rs7_physical_mission_lifecycle_binding(
            self.cps, self.packet(rollback_contract_exists=False),
        )
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertIn("rs7_packet_rollback_contract_exists_not_proven", result["errors"])

    def test_engineering_plane_packet_can_be_prepared_without_runtime_authority(self):
        result = self.lib.rs7_physical_mission_lifecycle_binding(
            self.cps, self.packet(scope_classification="ENGINEERING_PLANE"),
        )
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertEqual(result["execution_authorization"], "PENDING_CPS_ADMISSION")

    def test_control_plane_packet_remains_outside_generic_rs7_binding(self):
        result = self.lib.rs7_physical_mission_lifecycle_binding(
            self.cps, self.packet(scope_classification="CONTROL_PLANE"),
        )
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertIn("rs7_packet_scope_classification_invalid", result["errors"])

    def test_atomic_owner_can_admit_one_rs7_mission_without_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "V7_CURRENT_PROGRAM_STATE.md"
            before = self.rs6_pre_admission_cps()
            path.write_text(before, encoding="utf-8")
            result = self.lib.atomic_reconcile_cps(
                path, state=self.rs7_admission_state(before),
                expected_generation="cpsgen_RS6_ADMITTED_65CB2232971", request_external_wake=False,
            )
            self.assertTrue(result["ok"])
            admitted = self.lib.rs7_physical_mission_lifecycle_binding(
                path.read_text(encoding="utf-8"), self.packet(), requested_state="MISSION_EXECUTION_ALLOWED",
            )
            self.assertEqual(admitted["execution_authorization"], "MISSION_EXECUTION_ALLOWED")


if __name__ == "__main__":
    unittest.main()
