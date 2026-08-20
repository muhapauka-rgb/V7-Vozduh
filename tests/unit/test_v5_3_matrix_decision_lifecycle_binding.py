import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "tools" / "v7_sync_lib.py"
CPS = ROOT / "docs" / "programs" / "V7_CURRENT_PROGRAM_STATE.md"


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_v53_binding_test", LIB)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class V53MatrixDecisionLifecycleBindingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.cps = CPS.read_text(encoding="utf-8")
        for key, value in (
            ("CURRENT_STATE_GENERATION", "cpsgen_SFA_V53_DECISION_TEST"),
            ("CURRENT_PROGRAM_STAGE", "V5_3_MATRIX_HEALTH_OPTIMIZATION"),
            ("CURRENT_PROGRAM_EXECUTION_FRONTIER", "ADMITTED_READY_READ_ONLY:V7_MATRIX_HEALTH_PHASE_C_D_E_DECISION_V1"),
            ("CURRENT_EXECUTION_FRONTIER", "ADMITTED_READY_READ_ONLY:V7_MATRIX_HEALTH_PHASE_C_D_E_DECISION_V1"),
            ("CURRENT_EXECUTION_MISSION_ID", "V7_MATRIX_HEALTH_PHASE_C_D_E_DECISION_V1"),
            ("CURRENT_EXECUTION_MISSION_STATE", "PREPARED_NOT_ACTIVE"),
            ("CURRENT_MISSION_ROLE", "ACTIVE_MISSION"),
            ("CURRENT_MISSION_ID", "V7_MATRIX_HEALTH_PHASE_C_D_E_DECISION_V1"),
            ("CURRENT_MISSION_STATE", "PREPARED_NOT_ACTIVE"),
        ):
            cls.cps = cls.lib._replace_section_field(
                cls.cps,
                "## 0. Authoritative Live Current State",
                "## Authoritative Unfinished Capability Closure Registry",
                key,
                f"`{value}`",
            )

    def admitted_state(self):
        state = self.lib._normalized_state_from_live_cps(self.cps)
        state.update({
            "state_captured": "2026-08-20T08:00:00+00:00",
            "current_state_generation": "cpsgen_SFA_V53_ADMITTED_TEST",
            "current_transition_id": "V5_3_MATRIX_DECISION_MISSION_ADMITTED_V1",
            "current_execution_mission_state": "MISSION_ADMITTED",
            "current_mission_state": "MISSION_ADMITTED",
            "current_completion_contract": "ANALYSIS_COMPLETION",
            "current_completion_verdict": "MISSION_ADMITTED",
            "transaction_terminal_class": "V5_3_READ_ONLY_MISSION_ADMITTED",
        })
        return state

    def test_prepared_mission_requires_atomic_cps_admission(self):
        result = self.lib.v5_3_matrix_decision_mission_lifecycle_binding(self.cps)
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertEqual(result["execution_authorization"], "PENDING_CPS_ADMISSION")

    def test_prepared_state_cannot_issue_execution_authorization(self):
        result = self.lib.v5_3_matrix_decision_mission_lifecycle_binding(
            self.cps, requested_state="MISSION_EXECUTION_ALLOWED",
        )
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertIn("v5_3_cps_admission_state_missing", result["errors"])

    def test_atomic_admission_allows_read_only_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "V7_CURRENT_PROGRAM_STATE.md"
            path.write_text(self.cps, encoding="utf-8")
            result = self.lib.atomic_reconcile_cps(
                path,
                state=self.admitted_state(),
                expected_generation="cpsgen_SFA_V53_DECISION_TEST",
                request_external_wake=False,
            )
            self.assertTrue(result["ok"], result)
            binding = self.lib.v5_3_matrix_decision_mission_lifecycle_binding(
                path.read_text(encoding="utf-8"),
                requested_state="MISSION_EXECUTION_ALLOWED",
                root=ROOT,
            )
            self.assertEqual(binding["execution_authorization"], "MISSION_EXECUTION_ALLOWED")
            self.assertFalse(binding["mutation_performed"])

    def test_superseded_implementation_mission_cannot_bypass_system_gate(self):
        current = CPS.read_text(encoding="utf-8")
        result = self.lib.v5_3_matrix_implementation_mission_lifecycle_binding(
            current, requested_state="MISSION_EXECUTION_ALLOWED", root=ROOT,
        )
        self.assertEqual(result["final_verdict"], "STOP_SAFE", result)
        self.assertEqual(result["execution_authorization"], "NONE")
        self.assertFalse(result["mutation_performed"])

    def test_current_system_revalidation_mission_is_execution_allowed(self):
        current = CPS.read_text(encoding="utf-8")
        result = self.lib.v5_3_system_revalidation_mission_lifecycle_binding(
            current, requested_state="MISSION_EXECUTION_ALLOWED", root=ROOT,
        )
        self.assertEqual(result["final_verdict"], "PASS", result)
        self.assertEqual(result["execution_authorization"], "MISSION_EXECUTION_ALLOWED")
        self.assertFalse(result["mutation_performed"])


if __name__ == "__main__":
    unittest.main()
