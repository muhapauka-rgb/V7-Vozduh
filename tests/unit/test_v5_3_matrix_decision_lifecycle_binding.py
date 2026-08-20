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
        cls.phase_g_cps = CPS.read_text(encoding="utf-8")
        for key, value in (
            ("CURRENT_STATE_GENERATION", "cpsgen_SFA_V53_SYSTEM_DECISION_AB9E7C037471"),
            ("CURRENT_TRANSITION_ID", "V5_3_SYSTEM_LEVEL_WEIGHTED_DECISION_CONSUMED_V1"),
            ("CURRENT_ACTIVE_SCOPE", "V5_3_PHASE_G_BOUNDED_EGRESS_PARALLELISM_VALIDATION"),
            ("CURRENT_SAFE_NEXT_ACTION", "EXECUTE V5.3 Phase G controlled Polygon caps 1, 2 and 4; retain full Matrix fallback and automatic FAST HOLD"),
            ("CURRENT_NEXT_ACTION_ID", cls.lib.V5_3_PHASE_G_ACTION),
            ("CURRENT_PROGRAM_EXECUTION_FRONTIER", cls.lib.V5_3_PHASE_G_ACTION),
            ("CURRENT_EXECUTION_FRONTIER", cls.lib.V5_3_PHASE_G_ACTION),
            ("CURRENT_EXECUTION_MISSION_ID", cls.lib.V5_3_SYSTEM_REVALIDATION_MISSION_ID),
            ("CURRENT_EXECUTION_MISSION_STATE", "MISSION_CONSUMED"),
            ("CURRENT_MISSION_ID", cls.lib.V5_3_SYSTEM_REVALIDATION_MISSION_ID),
            ("CURRENT_MISSION_STATE", "MISSION_CONSUMED"),
            ("CURRENT_MISSION_ROLE", "ACTIVE_MISSION"),
            ("CURRENT_COMPLETION_CONTRACT", "ANALYSIS_COMPLETION"),
            ("CURRENT_COMPLETION_VERDICT", "MISSION_CONSUMED"),
            ("PROGRAM_TERMINAL_STATE", "NONE_V5_3_SYSTEM_LEVEL_WEIGHTED_DECISION_CONSUMED_PHASE_G_REQUIRED"),
            ("TRANSACTION_TERMINAL_CLASS", "V5_3_SYSTEM_LEVEL_WEIGHTED_DECISION_CONSUMED"),
            ("NEXT_MISSION_FORMED", "TRUE"),
            ("NEXT_MISSION_ID", cls.lib.V5_3_SYSTEM_REVALIDATION_MISSION_ID),
            ("V5_3_SYSTEM_LEVEL_REVALIDATION_GATE", "CONSUMED"),
            ("V5_3_AUTOMATIC_FAST_CONSUMER_STATUS", "HOLD_PENDING_PHASE_F_G_CONSTRAINTS_AND_EXPLICIT_PHASE_H_ADMISSION"),
        ):
            cls.phase_g_cps = cls.lib._replace_section_field(
                cls.phase_g_cps,
                "## 0. Authoritative Live Current State",
                "## Authoritative Unfinished Capability Closure Registry",
                key,
                f"`{value}`",
            )
        cls.cps = cls.phase_g_cps
        for key, value in (
            ("CURRENT_STATE_GENERATION", "cpsgen_SFA_V53_DECISION_TEST"),
            ("CURRENT_PROGRAM_STAGE", "V5_3_MATRIX_HEALTH_OPTIMIZATION"),
            ("CURRENT_PROGRAM_EXECUTION_FRONTIER", "ADMITTED_READY_READ_ONLY:V7_COMPLETE_HEALTH_TEST_STABILITY_SYSTEM_ATLAS_V1"),
            ("CURRENT_EXECUTION_FRONTIER", "ADMITTED_READY_READ_ONLY:V7_COMPLETE_HEALTH_TEST_STABILITY_SYSTEM_ATLAS_V1"),
            ("CURRENT_EXECUTION_MISSION_ID", "V7_COMPLETE_HEALTH_TEST_STABILITY_SYSTEM_ATLAS_V1"),
            ("CURRENT_EXECUTION_MISSION_STATE", "MISSION_ADMITTED"),
            ("CURRENT_MISSION_ID", "V7_COMPLETE_HEALTH_TEST_STABILITY_SYSTEM_ATLAS_V1"),
            ("CURRENT_MISSION_STATE", "MISSION_ADMITTED"),
            ("CURRENT_NEXT_ACTION_ID", "EXECUTE_V7_COMPLETE_HEALTH_TEST_STABILITY_SYSTEM_ATLAS"),
            ("V5_3_AUTOMATIC_FAST_CONSUMER_STATUS", "HOLD_PENDING_SYSTEM_LEVEL_REVALIDATION"),
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
        cls.decision_cps = cls.cps
        # Restore the present Atlas admission for its own tests.
        for key, value in (
            ("CURRENT_PROGRAM_EXECUTION_FRONTIER", "ADMITTED_READY_READ_ONLY:V7_COMPLETE_HEALTH_TEST_STABILITY_SYSTEM_ATLAS_V1"),
            ("CURRENT_EXECUTION_FRONTIER", "ADMITTED_READY_READ_ONLY:V7_COMPLETE_HEALTH_TEST_STABILITY_SYSTEM_ATLAS_V1"),
            ("CURRENT_EXECUTION_MISSION_ID", "V7_COMPLETE_HEALTH_TEST_STABILITY_SYSTEM_ATLAS_V1"),
            ("CURRENT_EXECUTION_MISSION_STATE", "MISSION_ADMITTED"),
            ("CURRENT_MISSION_ID", "V7_COMPLETE_HEALTH_TEST_STABILITY_SYSTEM_ATLAS_V1"),
            ("CURRENT_MISSION_STATE", "MISSION_ADMITTED"),
            ("CURRENT_NEXT_ACTION_ID", "EXECUTE_V7_COMPLETE_HEALTH_TEST_STABILITY_SYSTEM_ATLAS"),
            ("V5_3_AUTOMATIC_FAST_CONSUMER_STATUS", "HOLD_PENDING_SYSTEM_LEVEL_REVALIDATION"),
        ):
            cls.cps = cls.lib._replace_section_field(
                cls.cps,
                "## 0. Authoritative Live Current State",
                "## Authoritative Unfinished Capability Closure Registry",
                key,
                f"`{value}`",
            )

    def admitted_state(self):
        state = self.lib._normalized_state_from_live_cps(self.decision_cps)
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
        result = self.lib.v5_3_matrix_decision_mission_lifecycle_binding(self.decision_cps)
        self.assertEqual(result["final_verdict"], "PASS")
        self.assertEqual(result["execution_authorization"], "PENDING_CPS_ADMISSION")

    def test_prepared_state_cannot_issue_execution_authorization(self):
        result = self.lib.v5_3_matrix_decision_mission_lifecycle_binding(
            self.decision_cps, requested_state="MISSION_EXECUTION_ALLOWED",
        )
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertIn("v5_3_cps_admission_state_missing", result["errors"])

    def test_atomic_admission_allows_read_only_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "V7_CURRENT_PROGRAM_STATE.md"
            path.write_text(self.decision_cps, encoding="utf-8")
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
        result = self.lib.v5_3_system_revalidation_mission_lifecycle_binding(
            self.cps, requested_state="MISSION_EXECUTION_ALLOWED", root=ROOT,
        )
        self.assertEqual(result["final_verdict"], "PASS", result)
        self.assertEqual(result["execution_authorization"], "MISSION_EXECUTION_ALLOWED")
        self.assertFalse(result["mutation_performed"])

    def test_system_level_decision_is_atomically_consumed_and_keeps_fast_held(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs/programs").mkdir(parents=True)
            (root / "docs/reports/engineering").mkdir(parents=True)
            (root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").write_text(
                self.cps, encoding="utf-8",
            )
            (root / "docs/programs/V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM.md").write_text(
                (ROOT / "docs/programs/V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM.md").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            (root / self.lib.V5_3_SYSTEM_REVALIDATION_DECISION_REPORT).write_text(
                (ROOT / self.lib.V5_3_SYSTEM_REVALIDATION_DECISION_REPORT).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            result = self.lib.reconcile_v5_3_system_revalidation_decision_to_cps(root=root)
            self.assertEqual(result["final_verdict"], "PASS", result)
            self.assertEqual(
                result["program_terminal"],
                "V7_HEALTH_TEST_STABILITY_TARGET_ARCHITECTURE_EVIDENCE_WEIGHTED_DECISION_CONSUMED",
            )
            self.assertFalse(result["forbidden_effects"]["automatic_fast_enablement"])
            updated = (root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text(encoding="utf-8")
            self.assertIn("V5_3_SYSTEM_LEVEL_REVALIDATION_GATE` | `CONSUMED`", updated)
            self.assertIn("HOLD_PENDING_PHASE_F_G_CONSTRAINTS", updated)
            self.assertIn(self.lib.V5_3_PHASE_G_ACTION, updated)
            continuation = self.lib.continue_omp_engineering_control_loop(root=root)
            self.assertEqual(continuation["final_verdict"], "PASS", continuation)
            self.assertEqual(
                continuation["priority_decision"],
                "V5_3_PHASE_G_PREEMPTS_GENERIC_OMP",
            )
            self.assertFalse(continuation["forbidden_effects"]["automatic_fast_enablement"])

    def test_phase_g_no_parallelism_is_consumed_into_existing_t0_t11_track(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs/programs").mkdir(parents=True)
            (root / "docs/reports/engineering").mkdir(parents=True)
            for relative in (
                "docs/programs/V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM.md",
                "docs/programs/OPERATIONAL_MATURITY_PROGRAM.md",
                self.lib.V5_3_PHASE_G_REPORT,
                self.lib.V5_3_T0_T11_LATENCY_TRACK_REPORT,
            ):
                source = ROOT / relative
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
            (root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").write_text(
                self.phase_g_cps, encoding="utf-8",
            )
            result = self.lib.reconcile_v5_3_phase_g_to_t0_t11_latency_track(root=root)
            self.assertEqual(result["final_verdict"], "PASS", result)
            self.assertEqual(
                result["phase_g_decision"],
                "NO_CROSS_EGRESS_PARALLELISM_ADMITTED",
            )
            self.assertEqual(
                result["next_output"],
                self.lib.V5_3_T0_T11_LATENCY_TRACK_ACTION,
            )
            self.assertFalse(result["forbidden_effects"]["runtime_mutation"])
            self.assertFalse(result["forbidden_effects"]["automatic_fast_enablement"])
            updated = (root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text(encoding="utf-8")
            self.assertIn("NO_CROSS_EGRESS_PARALLELISM_ADMITTED", updated)
            self.assertIn(self.lib.V5_3_T0_T11_LATENCY_TRACK_ACTION, updated)
            self.assertIn("HOLD_PENDING_EXPLICIT_PHASE_H_ADMISSION", updated)
            continuation = self.lib.continue_omp_engineering_control_loop(root=root)
            self.assertEqual(continuation["final_verdict"], "PASS", continuation)
            self.assertEqual(
                continuation["priority_decision"],
                "V5_3_T0_T11_LATENCY_TRACK_PREEMPTS_GENERIC_OMP",
            )
            self.assertEqual(
                continuation["real_consumer"],
                "EXISTING_V5_3_HEALTH_TEST_STABILITY_OWNERS",
            )
            self.assertFalse(continuation["forbidden_effects"]["runtime_mutation"])

    def test_continue_omp_keeps_active_system_revalidation_ahead_of_generic_work(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs/programs").mkdir(parents=True)
            (root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").write_text(
                self.cps, encoding="utf-8",
            )
            result = self.lib.continue_omp_engineering_control_loop(root=root)
        self.assertEqual(result["final_verdict"], "PASS", result)
        self.assertEqual(
            result["priority_decision"],
            "ACTIVE_V5_3_SYSTEM_REVALIDATION_PREEMPTS_GENERIC_OMP",
        )
        self.assertEqual(
            result["real_consumer"],
            "EXISTING_V5_3_SYSTEM_REVALIDATION_OWNER",
        )
        self.assertFalse(result["forbidden_effects"]["runtime_mutation"])
        self.assertFalse(result["forbidden_effects"]["routing_mutation"])


if __name__ == "__main__":
    unittest.main()
