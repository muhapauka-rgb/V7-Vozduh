from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "tools/v7_sync_lib.py"
CPS = ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md"


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_completion_gate", LIB)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class OmpMissionCompletionEvidenceGateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.cps = CPS.read_text(encoding="utf-8")

    def gate(self, completion_contract, **evidence):
        return self.lib.mission_completion_evidence_gate({
            "MISSION_TYPE": completion_contract.removesuffix("_COMPLETION"),
            "COMPLETION_CONTRACT": completion_contract,
            **evidence,
        })

    def test_01_report_only_analysis_is_not_complete(self):
        self.assertEqual(self.gate("ANALYSIS_COMPLETION")["completion_verdict"], "PREPARED_NOT_CONSUMED")

    def test_02_tests_only_implementation_is_not_consumed(self):
        result = self.gate("IMPLEMENTATION_COMPLETION", FOCUSED_TESTS_PROVEN=True)
        self.assertEqual(result["completion_verdict"], "IMPLEMENTED_NOT_CONSUMED")

    def test_03_deployed_unused_implementation_stays_not_consumed(self):
        result = self.gate("IMPLEMENTATION_COMPLETION", SOURCE_CHANGE_PROVEN=True, FOCUSED_TESTS_PROVEN=True, DEPLOY_REQUIRED=True, DEPLOY_PROVEN=True)
        self.assertEqual(result["completion_verdict"], "IMPLEMENTED_NOT_CONSUMED")

    def test_04_integration_without_real_caller_fails(self):
        self.assertEqual(self.gate("INTEGRATION_COMPLETION")["completion_verdict"], "INTEGRATION_INCOMPLETE")

    def test_05_real_caller_without_consumer_fails(self):
        result = self.gate("INTEGRATION_COMPLETION", REAL_CALLER_PROVEN=True)
        self.assertIn("CONSUMER_PROVEN", result["missing_evidence"])

    def test_06_consumer_without_behavior_change_fails(self):
        result = self.gate("INTEGRATION_COMPLETION", REAL_CALLER_PROVEN=True, CONSUMER_PROVEN=True)
        self.assertIn("BEHAVIOR_CHANGE_PROVEN", result["missing_evidence"])

    def test_07_behavior_change_without_next_output_fails(self):
        result = self.gate("INTEGRATION_COMPLETION", REAL_CALLER_PROVEN=True, CONSUMER_PROVEN=True, BEHAVIOR_CHANGE_PROVEN=True)
        self.assertIn("NEXT_OUTPUT_PROVEN", result["missing_evidence"])

    def test_08_complete_integration_reaches_consumed(self):
        result = self.gate("INTEGRATION_COMPLETION", REAL_CALLER_PROVEN=True, CONSUMER_PROVEN=True, BEHAVIOR_CHANGE_PROVEN=True, NEXT_OUTPUT_PROVEN=True)
        self.assertEqual(result["completion_verdict"], "COMPLETE_CONSUMED")

    def test_09_acceptance_does_not_require_runtime_effect(self):
        result = self.gate("ACCEPTANCE_COMPLETION", INDEPENDENT_ACCEPTANCE_PROVEN=True, NEXT_OUTPUT_PROVEN=True)
        self.assertEqual(result["completion_verdict"], "COMPLETE_WITH_LEGAL_TERMINAL")

    def test_10_acceptance_requires_next_output(self):
        result = self.gate("ACCEPTANCE_COMPLETION", INDEPENDENT_ACCEPTANCE_PROVEN=True)
        self.assertEqual(result["completion_verdict"], "PREPARED_NOT_CONSUMED")

    def test_11_documentation_can_complete_without_code(self):
        result = self.gate("DOCUMENTATION_COMPLETION", DOCUMENT_OWNER_ACCEPTED=True, EVIDENCE_TRACEABILITY_PROVEN=True)
        self.assertEqual(result["completion_verdict"], "COMPLETE_WITH_LEGAL_TERMINAL")

    def test_12_documentation_requires_owner_acceptance(self):
        result = self.gate("DOCUMENTATION_COMPLETION", EVIDENCE_TRACEABILITY_PROVEN=True)
        self.assertIn("DOCUMENT_OWNER_ACCEPTED", result["missing_evidence"])

    def test_13_automation_requires_independent_trigger(self):
        result = self.gate("AUTOMATION_COMPLETION", ENTRYPOINT_ACTIVE=True, REAL_CALLER_PROVEN=True, CONSUMER_PROVEN=True, BEHAVIOR_CHANGE_PROVEN=True, NEXT_OUTPUT_PROVEN=True, IDEMPOTENCY_PROVEN=True, DUPLICATE_SUPPRESSION_PROVEN=True)
        self.assertEqual(result["completion_verdict"], "AUTOMATION_INCOMPLETE")

    def test_14_complete_automation_reaches_consumed(self):
        result = self.gate("AUTOMATION_COMPLETION", INDEPENDENT_TRIGGER_PROVEN=True, ENTRYPOINT_ACTIVE=True, REAL_CALLER_PROVEN=True, CONSUMER_PROVEN=True, BEHAVIOR_CHANGE_PROVEN=True, NEXT_OUTPUT_PROVEN=True, IDEMPOTENCY_PROVEN=True, DUPLICATE_SUPPRESSION_PROVEN=True)
        self.assertEqual(result["completion_verdict"], "COMPLETE_CONSUMED")

    def test_15_runtime_requires_active_path(self):
        result = self.gate("RUNTIME_COMPLETION", RUNTIME_EFFECT_PROVEN=True, VERIFICATION_PROVEN=True, ROLLBACK_OR_STOP_SAFE_PROVEN=True)
        self.assertEqual(result["completion_verdict"], "RUNTIME_INCOMPLETE")

    def test_16_complete_runtime_reaches_consumed(self):
        result = self.gate("RUNTIME_COMPLETION", RUNTIME_PATH_ACTIVE=True, RUNTIME_EFFECT_PROVEN=True, VERIFICATION_PROVEN=True, ROLLBACK_OR_STOP_SAFE_PROVEN=True)
        self.assertEqual(result["completion_verdict"], "COMPLETE_CONSUMED")

    def test_17_production_requires_real_effect(self):
        result = self.gate("PRODUCTION_COMPLETION", VERIFICATION_PROVEN=True, CONSUMER_PROVEN=True, LEARNING_PROPAGATION_PROVEN=True, NEXT_OUTPUT_PROVEN=True)
        self.assertEqual(result["completion_verdict"], "PRODUCTION_INCOMPLETE")

    def test_18_complete_production_reaches_consumed(self):
        result = self.gate("PRODUCTION_COMPLETION", PRODUCTION_EFFECT_PROVEN=True, VERIFICATION_PROVEN=True, CONSUMER_PROVEN=True, LEARNING_PROPAGATION_PROVEN=True, NEXT_OUTPUT_PROVEN=True)
        self.assertEqual(result["completion_verdict"], "COMPLETE_CONSUMED")

    def test_19_unknown_contract_fails_closed(self):
        self.assertEqual(self.gate("UNKNOWN_COMPLETION")["completion_verdict"], "COMPLETION_TRUTH_UNRESOLVED")

    def test_20_required_lock_is_machine_checked(self):
        result = self.gate("ACCEPTANCE_COMPLETION", INDEPENDENT_ACCEPTANCE_PROVEN=True, NEXT_OUTPUT_PROVEN=True, LOCK_REQUIRED=True)
        self.assertIn("LOCK_PROVEN", result["missing_evidence"])

    def test_21_required_deploy_is_machine_checked(self):
        result = self.gate("IMPLEMENTATION_COMPLETION", SOURCE_CHANGE_PROVEN=True, FOCUSED_TESTS_PROVEN=True, DEPLOY_REQUIRED=True)
        self.assertIn("DEPLOY_PROVEN", result["missing_evidence"])

    def test_22_owner_backed_legal_terminal_can_close(self):
        result = self.gate("AUTOMATION_COMPLETION", LEGAL_TERMINAL=True, EVIDENCE_TRACEABILITY_PROVEN=True, TERMINAL_OWNER_PROVEN=True)
        self.assertEqual(result["completion_verdict"], "COMPLETE_WITH_LEGAL_TERMINAL")

    def test_23_unowned_legal_terminal_cannot_close(self):
        result = self.gate("AUTOMATION_COMPLETION", LEGAL_TERMINAL=True, EVIDENCE_TRACEABILITY_PROVEN=True)
        self.assertEqual(result["completion_verdict"], "AUTOMATION_INCOMPLETE")

    def test_24_tests_pass_cannot_promote_integration(self):
        result = self.gate("INTEGRATION_COMPLETION", FOCUSED_TESTS_PROVEN=True)
        self.assertEqual(result["completion_verdict"], "INTEGRATION_INCOMPLETE")

    def test_25_report_created_cannot_prove_consumer(self):
        result = self.gate("INTEGRATION_COMPLETION", REPORT_CREATED=True, REAL_CALLER_PROVEN=True)
        self.assertFalse(result["consumer_proven"])

    def test_26_manual_codex_run_cannot_prove_automation(self):
        result = self.gate("AUTOMATION_COMPLETION", MANUAL_CODEX_RUN=True)
        self.assertFalse(result["evidence_present"]["INDEPENDENT_TRIGGER_PROVEN"])

    def test_27_replay_is_deterministic(self):
        contract = {"MISSION_TYPE": "INTEGRATION", "COMPLETION_CONTRACT": "INTEGRATION_COMPLETION", "REAL_CALLER_PROVEN": True}
        self.assertEqual(self.lib.mission_completion_evidence_gate(contract), self.lib.mission_completion_evidence_gate(contract))

    def test_28_gate_has_real_truth_consumer_call_site(self):
        result = self.lib.python_function_call_sites(ROOT, "mission_completion_evidence_gate")
        self.assertGreaterEqual(result["real_caller_count"], 1)

    def test_29_current_cps_records_active_gate(self):
        self.assertIn("| `MISSION_COMPLETION_EVIDENCE_GATE` | `ACTIVE_V1` |", self.cps)
        self.assertIn("| `CURRENT_COMPLETION_VERDICT` | `ACTIVE_NOT_CONSUMED` |", self.cps)

    def test_30_active_product_frontier_requires_current_gate_consumer_proof(self):
        result = self.lib.omp_functional_footprint_consistency(self.cps, root=ROOT)
        self.assertEqual(
            result["mission_completion_evidence_gate_status"],
            "RECOVERY_LATENCY_SLO_RUNTIME_EVIDENCE_REQUIRED",
        )
        self.assertEqual(result["current_completion_verdict"], "ACTIVE_NOT_CONSUMED")

    def test_31_program_completion_requires_exact_consumed_boundary(self):
        result = self.gate(
            "PROGRAM_COMPLETION",
            PROGRAM_FRONTIER_RECONCILED=True,
            SCENARIO_OBLIGATIONS_CONSUMED=True,
            CONTROLLED_PREPARATION_PROVEN=True,
            CAPABILITY_CRITERIA_RECONCILED=True,
            EXACT_BOUNDARY_PROVEN=True,
            NEXT_OUTPUT_PROVEN=True,
        )
        self.assertEqual(result["completion_verdict"], "COMPLETE_CONSUMED")

    def test_32_material_change_without_simplification_evidence_is_not_consumed(self):
        result = self.gate(
            "INTEGRATION_COMPLETION",
            MATERIAL_IMPLEMENTATION_CHANGE=True,
            REAL_CALLER_PROVEN=True,
            CONSUMER_PROVEN=True,
            BEHAVIOR_CHANGE_PROVEN=True,
            NEXT_OUTPUT_PROVEN=True,
        )
        self.assertEqual(result["completion_verdict"], "INTEGRATION_INCOMPLETE")
        self.assertTrue(result["simplification_first_required"])
        self.assertIn("DELETE_REUSE_SIMPLIFY_TEST_CONSUMED", result["missing_evidence"])
        self.assertIn("STRUCTURAL_COMPLEXITY_DELTA_ACCEPTED", result["missing_evidence"])

    def test_33_material_change_with_complete_simplification_evidence_is_consumed(self):
        result = self.gate(
            "INTEGRATION_COMPLETION",
            MATERIAL_IMPLEMENTATION_CHANGE=True,
            REAL_CALLER_PROVEN=True,
            CONSUMER_PROVEN=True,
            BEHAVIOR_CHANGE_PROVEN=True,
            NEXT_OUTPUT_PROVEN=True,
            DELETE_REUSE_SIMPLIFY_TEST_CONSUMED=True,
            STRUCTURAL_COMPLEXITY_BEFORE_RECORDED=True,
            STRUCTURAL_COMPLEXITY_AFTER_RECORDED=True,
            STRUCTURAL_COMPLEXITY_DELTA_RECORDED=True,
            STRUCTURAL_COMPLEXITY_DELTA_ACCEPTED=True,
            STRUCTURAL_COMPLEXITY_DELTA_VERDICT="COMPLEXITY_NEUTRAL",
            AFFECTED_REGRESSION_PROOF_PASS=True,
            CURRENT_CONSUMER_PROOF_PASS=True,
            RESIDUE_DISPOSITION_COMPLETE=True,
        )
        self.assertEqual(result["completion_verdict"], "COMPLETE_CONSUMED")
        self.assertTrue(result["simplification_first_change_consumed"])

    def test_34_documentation_change_does_not_invent_complexity_metrics(self):
        result = self.gate(
            "DOCUMENTATION_COMPLETION",
            DOCUMENT_ONLY_CHANGE=True,
            DOCUMENT_OWNER_ACCEPTED=True,
            EVIDENCE_TRACEABILITY_PROVEN=True,
        )
        self.assertEqual(result["completion_verdict"], "COMPLETE_WITH_LEGAL_TERMINAL")
        self.assertFalse(result["simplification_first_required"])
        self.assertEqual(result["structural_complexity_delta_verdict"], "NOT_APPLICABLE")

    def test_35_unjustified_complexity_growth_cannot_close_via_legal_terminal(self):
        result = self.gate(
            "INTEGRATION_COMPLETION",
            MATERIAL_IMPLEMENTATION_CHANGE=True,
            STRUCTURAL_COMPLEXITY_DELTA_VERDICT="COMPLEXITY_INCREASE_JUSTIFIED",
            LEGAL_TERMINAL=True,
            EVIDENCE_TRACEABILITY_PROVEN=True,
            TERMINAL_OWNER_PROVEN=True,
        )
        self.assertEqual(result["completion_verdict"], "INTEGRATION_INCOMPLETE")
        self.assertEqual(
            result["structural_complexity_failure"],
            "UNJUSTIFIED_STRUCTURAL_COMPLEXITY_GROWTH",
        )
        self.assertIn(
            "NEW_CURRENT_PRODUCT_OR_SAFETY_RESPONSIBILITY_PROVEN",
            result["missing_evidence"],
        )

    def test_36_justified_complexity_increase_requires_every_exception_proof(self):
        evidence = {
            "MATERIAL_IMPLEMENTATION_CHANGE": True,
            "REAL_CALLER_PROVEN": True,
            "CONSUMER_PROVEN": True,
            "BEHAVIOR_CHANGE_PROVEN": True,
            "NEXT_OUTPUT_PROVEN": True,
            "DELETE_REUSE_SIMPLIFY_TEST_CONSUMED": True,
            "STRUCTURAL_COMPLEXITY_BEFORE_RECORDED": True,
            "STRUCTURAL_COMPLEXITY_AFTER_RECORDED": True,
            "STRUCTURAL_COMPLEXITY_DELTA_RECORDED": True,
            "STRUCTURAL_COMPLEXITY_DELTA_ACCEPTED": True,
            "STRUCTURAL_COMPLEXITY_DELTA_VERDICT": "COMPLEXITY_INCREASE_JUSTIFIED",
            "AFFECTED_REGRESSION_PROOF_PASS": True,
            "CURRENT_CONSUMER_PROOF_PASS": True,
            "RESIDUE_DISPOSITION_COMPLETE": True,
        }
        evidence.update({field: True for field in self.lib.COMPLEXITY_INCREASE_JUSTIFICATION_EVIDENCE})
        result = self.gate("INTEGRATION_COMPLETION", **evidence)
        self.assertEqual(result["completion_verdict"], "COMPLETE_CONSUMED")
        self.assertEqual(result["structural_complexity_failure"], "NONE")


if __name__ == "__main__":
    unittest.main()
