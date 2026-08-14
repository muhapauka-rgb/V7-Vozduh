import importlib.util
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

    def test_prepared_packet_is_bound_but_not_authorized_to_execute(self):
        result = self.lib.rs7_physical_mission_lifecycle_binding(self.cps, self.packet())
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertEqual(result["binding_status"], "RS7_LIFECYCLE_BINDING_READY")
        self.assertEqual(result["execution_authorization"], "PENDING_CPS_ADMISSION")
        self.assertFalse(result["mutation_performed"])

    def test_current_rs6_frontier_cannot_issue_execution_authorization(self):
        result = self.lib.rs7_physical_mission_lifecycle_binding(
            self.cps, self.packet(), requested_state="MISSION_EXECUTION_ALLOWED",
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


if __name__ == "__main__":
    unittest.main()
