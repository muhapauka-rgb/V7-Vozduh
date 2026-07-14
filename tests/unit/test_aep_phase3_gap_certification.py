from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
PHASE2 = ROOT / "docs/reports/research/V7_CURRENT_AUTONOMOUS_BEHAVIOUR_REALITY.md"
LOCK = "128691e74c0b2087e1ffb0fc26c64d6425ef68ec46af79a747f60bae28a73951"


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_aep_phase3", ROOT / "tools/v7_sync_lib.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class AepPhase3GapCertificationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.phase2 = PHASE2.read_text(encoding="utf-8")

    def gap(self, **overrides):
        gap = {
            "primary_classification": "OMP_CONTINUATION_GAP",
            "secondary_classes": ["CONSUMER_AUTOMATION_GAP", "OWNER_EXTENSION_GAP"],
            "behaviour_definition_id": "BD-016",
            "behaviour_instance_id": "BI-028",
            "engineering_chain_id": "AEP-PHASE3->ACCEPTANCE->PHASE4->OMP",
            "engineering_intent": "Accepted AEP output must reach its named next-stage OMP consumer.",
            "current_reality": "Program reconciliation stops at Phase 3 READY and always blocks Phase 4.",
            "expected_reality": "Accepted locked Phase 3 output deterministically opens Phase 4 consumption.",
            "failed_chain_segment": "PHASE3_ACCEPTED_OUTPUT_TO_PHASE4_CONSUMER",
            "producer": "AEP_PHASE_3_CERTIFICATION_OWNER",
            "consumer": "OMP_PROGRAM_EXECUTION_RECONCILIATION",
            "evidence": "tools/v7_sync_lib.py:program_execution_reconciliation and current tests",
            "truth_level": "T4",
            "freshness": "CURRENT_COMMIT",
            "owner": "OMP+AEP+CPS_EXISTING_OWNERS",
            "verification": "Focused tests plus CPS/OMP consumer confirmation.",
            "rollback": "Revert the existing-owner extension and retain Phase 3 acceptance STOP_SAFE.",
            "terminal_path": "PHASE4_OMP_ADMISSION_OR_LEGAL_HOLD",
            "implementation_scope": "Extend existing program reconciliation consumer only.",
            "runtime_impact": "NONE",
            "production_impact": "NONE",
            "authority_context": "Independent Phase Acceptance remains mandatory; no authority expansion.",
            "real_world_context": "No real-world evidence is required for this engineering-plane consumer.",
            "root_cause": "Existing deterministic consumer models only Phase 2 acceptance.",
            "smallest_existing_next_action": "Extend program_execution_reconciliation for accepted Phase 3 input.",
            "dependencies": "EXISTING_CONTRACTS_READY",
            "new_owner_required": False,
            "new_architecture_required": False,
        }
        gap.update(overrides)
        return gap

    def certify(self, gaps=None, **overrides):
        values = {
            "expected_phase2_lock_fingerprint": LOCK,
            "executor": "CODEX_PHASE_EXECUTION_OWNER",
            "acceptance_owner": "",
            "operator_authority": False,
        }
        values.update(overrides)
        return self.lib.aep_phase3_gap_certification(
            self.phase2,
            [self.gap()] if gaps is None else gaps,
            **values,
        )

    def test_01_locked_phase2_input_passes(self):
        self.assertEqual(self.certify()["phase3_input_readiness"], "PASS")

    def test_02_lock_fingerprint_mismatch_fails(self):
        result = self.certify(expected_phase2_lock_fingerprint="0" * 64)
        self.assertIn("phase2_locked_input_mismatch", result["errors"])

    def test_03_all_16_behaviour_definitions_are_reviewed(self):
        self.assertEqual(self.certify()["behaviour_definitions_reviewed"], 16)

    def test_04_all_28_behaviour_instances_are_reviewed(self):
        self.assertEqual(self.certify()["behaviour_instances_reviewed"], 28)

    def test_05_current_chain_break_is_certified(self):
        self.assertEqual(self.certify()["certified_gaps"], 1)

    def test_06_architecture_only_difference_is_rejected(self):
        result = self.certify([self.gap(truth_level="T9")])
        self.assertEqual(result["dispositions"][0]["certification_verdict"], "GAP_REJECTED_NO_CURRENT_REALITY")

    def test_07_ideal_model_only_difference_is_rejected(self):
        result = self.certify([self.gap(evidence_source_class="IDEAL_MODEL_ONLY")])
        self.assertEqual(result["certified_gaps"], 0)

    def test_08_missing_production_outcome_alone_is_real_world_boundary(self):
        result = self.certify([self.gap(primary_classification="REAL_WORLD_BOUNDARY_NOT_A_GAP")])
        self.assertEqual(result["real_world_boundaries_not_gaps"], 1)

    def test_09_authority_boundary_is_not_a_gap(self):
        result = self.certify([self.gap(primary_classification="AUTHORITY_BOUNDARY_NOT_A_GAP")])
        self.assertEqual(result["authority_boundaries_not_gaps"], 1)

    def test_10_dependency_wait_is_not_a_gap(self):
        result = self.certify([self.gap(primary_classification="DEPENDENCY_WAIT_NOT_A_GAP")])
        self.assertEqual(result["dependency_waits_not_gaps"], 1)

    def test_11_unknown_responsibility_holds(self):
        result = self.certify([self.gap(primary_classification="UNKNOWN_WITH_REASON", owner="UNRESOLVED")])
        self.assertEqual(result["held_gaps"], 1)

    def test_12_duplicate_gap_is_suppressed(self):
        result = self.certify([self.gap(), copy.deepcopy(self.gap())])
        self.assertEqual(result["duplicate_gaps"], 1)

    def test_13_existing_gap_identity_is_suppressed(self):
        first = self.certify()
        gap_id = first["dispositions"][0]["gap_id"]
        second = self.certify(existing_gap_ids=[gap_id])
        self.assertEqual(second["duplicate_gaps"], 1)

    def test_14_unknown_behaviour_instance_is_rejected(self):
        result = self.certify([self.gap(behaviour_instance_id="BI-999")])
        self.assertEqual(result["dispositions"][0]["certification_verdict"], "GAP_REJECTED_NO_CURRENT_REALITY")

    def test_15_gap_class_cannot_enter_omp_without_candidate_instance(self):
        result = self.certify([self.gap(verification="")])
        self.assertEqual(result["candidate_instances_created"], 0)

    def test_16_certified_gap_creates_exactly_one_candidate(self):
        self.assertEqual(self.certify()["candidate_instances_created"], 1)

    def test_17_candidate_identity_is_deterministic(self):
        first = self.certify()["candidate_instances"][0]["candidate_instance_id"]
        second = self.certify()["candidate_instances"][0]["candidate_instance_id"]
        self.assertEqual(first, second)

    def test_18_candidate_reality_gate_contract_is_complete(self):
        candidate = self.certify()["candidate_instances"][0]
        self.assertEqual(self.lib.omp_candidate_admission_decision(candidate)["final_verdict"], "PASS")

    def test_19_existing_candidate_identity_is_suppressed(self):
        candidate = self.certify()["candidate_instances"][0]
        result = self.certify(existing_candidates=[candidate])
        self.assertEqual(result["duplicate_gaps"], 1)

    def test_20_omp_admission_is_not_bypassed_before_acceptance(self):
        self.assertEqual(self.certify()["omp_candidates_consumed"], 0)

    def test_21_executor_cannot_accept_own_register(self):
        result = self.certify(acceptance_owner="CODEX_PHASE_EXECUTION_OWNER", operator_authority=True)
        self.assertEqual(result["phase3_acceptance_status"], "AEP_PHASE_3_READY_FOR_ACCEPTANCE")

    def test_22_independent_owner_can_accept(self):
        result = self.certify(acceptance_owner="OPERATOR_ENGINEERING_AUTHORITY", operator_authority=True)
        self.assertEqual(result["phase3_acceptance_status"], "AEP_PHASE_3_GAP_REGISTER_ACCEPTED")

    def test_23_acceptance_creates_deterministic_lock(self):
        result = self.certify(acceptance_owner="OPERATOR_ENGINEERING_AUTHORITY", operator_authority=True)
        self.assertTrue(result["phase3_lock_id"].startswith("aep3lock_"))

    def test_24_phase4_stays_locked_without_independent_acceptance(self):
        self.assertEqual(self.certify()["phase4_status"], "LOCKED_PENDING_PHASE_3_ACCEPTANCE")

    def test_25_phase4_ready_only_after_acceptance(self):
        result = self.certify(acceptance_owner="OPERATOR_ENGINEERING_AUTHORITY", operator_authority=True)
        self.assertEqual(result["phase4_status"], "READY")

    def test_26_zero_gap_register_has_legal_acceptance_boundary(self):
        result = self.certify([])
        self.assertEqual(result["final_verdict"], "AEP_PHASE_3_READY_FOR_INDEPENDENT_ACCEPTANCE")

    def test_27_discovery_has_no_runtime_or_production_impact(self):
        result = self.certify()
        self.assertEqual((result["runtime_impact"], result["production_impact"]), ("NONE", "NONE"))

    def test_28_discovery_has_no_authority_expansion_or_user_movement(self):
        result = self.certify()
        self.assertEqual((result["authority_impact"], result["user_movement"]), ("NONE", "NO"))

    def test_29_register_fingerprint_is_deterministic(self):
        self.assertEqual(self.certify()["register_fingerprint"], self.certify()["register_fingerprint"])

    def test_30_replay_reproduces_dispositions_and_candidate_sequence(self):
        first = self.certify()
        second = self.certify()
        self.assertEqual(first["dispositions"], second["dispositions"])
        self.assertEqual(first["candidate_instances"], second["candidate_instances"])


if __name__ == "__main__":
    unittest.main()
