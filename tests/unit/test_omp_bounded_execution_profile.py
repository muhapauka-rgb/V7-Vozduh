from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "tools/v7_sync_lib.py"
CPS = ROOT / "docs/programs/V7_CURRENT_PROGRAM_STATE.md"


def load_lib():
    spec = importlib.util.spec_from_file_location("v7_sync_lib_profile_test", LIB)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class OmpBoundedExecutionProfileTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()

    def profile(self, **overrides):
        value = self.lib.gpt_decision_review_profile_contract(
            mission_id="V7_PROFILE_TEST_MISSION_V1",
            run_nonce="profile-test-run-v1",
            input_fingerprint="1" * 64,
            repo_fingerprint="2" * 64,
        )
        value.update(overrides)
        return value

    def admitted(self):
        result = self.lib.admit_execution_profile_contract(
            self.profile(), mission_id="V7_PROFILE_TEST_MISSION_V1",
        )
        self.assertEqual(result["final_verdict"], "PASS")
        return result

    def output(self, admitted):
        return {
            "mission_reference": admitted["mission_id"],
            "profile_reference": admitted["profile_fingerprint"],
            "input_fingerprint": admitted["input_fingerprint"],
            "current_facts": ["bounded fact"],
            "as_is": "current evidence",
            "to_be": "accepted contract",
            "exact_residual": "identity binding",
            "options": ["reuse"],
            "recommended_option": "reuse",
            "owner_impact": "NONE",
            "state_impact": "NONE",
            "safety_impact": "READ_ONLY",
            "latency_impact": "NONE",
            "structural_impact": "BOUNDED",
            "owner_decision_required": False,
            "owner_decision_reason": "NONE",
            "unproven_claims": [],
            "terminal_verdict": "PASS_DECISION_READY",
        }

    def contracts(self):
        admitted = self.admitted()
        result = self.lib.gpt_decision_review_result_contract(
            admitted, self.output(admitted), executor_context_id="executor-context",
        )
        review = self.lib.execution_profile_review_record(
            admitted, result, review_type="ARCHITECTURE_REVIEW",
            review_verdict="PASS", review_context_id="review-context",
        )
        contract = {
            "MISSION_TYPE": "ACCEPTANCE",
            "COMPLETION_CONTRACT": "ACCEPTANCE_COMPLETION",
            "INDEPENDENT_ACCEPTANCE_PROVEN": True,
            "NEXT_OUTPUT_PROVEN": True,
            "EXECUTION_PROFILE_CONTRACT": admitted,
            "EXECUTION_PROFILE_RESULT": result,
            "EXECUTION_PROFILE_REVIEWS": [review],
            "CURRENT_MISSION_ID": admitted["mission_id"],
            "CURRENT_RUN_NONCE": admitted["run_nonce"],
            "CURRENT_INPUT_FINGERPRINT": admitted["input_fingerprint"],
            "CURRENT_REPO_FINGERPRINT": admitted["repo_fingerprint"],
            "MISSION_CURRENT": True,
            "MISSION_SUPERSEDED": False,
            "EXPECTED_RESULT_FINGERPRINT": result["result_fingerprint"],
            "EXISTING_RESULT_FINGERPRINTS": [],
        }
        return admitted, result, review, contract

    def test_01_valid_read_only_profile_is_admitted(self):
        admitted = self.admitted()
        self.assertEqual(admitted["mutation_class"], "READ_ONLY")
        self.assertEqual(admitted["tool_class_allowlist"], ["READ_ONLY_ENGINEERING_EVIDENCE"])
        self.assertFalse(admitted["dispatch_performed"])

    def test_02_missing_field_is_rejected(self):
        profile = self.profile()
        del profile["input_fingerprint"]
        result = self.lib.admit_execution_profile_contract(
            profile, mission_id="V7_PROFILE_TEST_MISSION_V1",
        )
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertIn("execution_profile_field_missing:input_fingerprint", result["errors"])

    def test_03_unknown_profile_is_rejected(self):
        result = self.lib.admit_execution_profile_contract(
            self.profile(profile_type="CODEX_IMPLEMENTATION"),
            mission_id="V7_PROFILE_TEST_MISSION_V1",
        )
        self.assertIn("execution_profile_type_unauthorized", result["errors"])

    def test_04_mutation_or_authority_expansion_is_rejected(self):
        for field, value in (("mutation_class", "SOURCE_WRITE"), ("authority_class", "RUNTIME")):
            with self.subTest(field=field):
                result = self.lib.admit_execution_profile_contract(
                    self.profile(**{field: value}), mission_id="V7_PROFILE_TEST_MISSION_V1",
                )
                self.assertEqual(result["final_verdict"], "STOP_SAFE")

    def test_05_valid_result_and_review_reach_existing_completion_consumer(self):
        _, _, _, contract = self.contracts()
        result = self.lib.mission_completion_evidence_gate(contract)
        self.assertEqual(result["completion_verdict"], "COMPLETE_WITH_LEGAL_TERMINAL")
        self.assertTrue(result["execution_profile_binding_consumed"])

    def test_06_wrong_current_identity_fails_closed(self):
        for field in ("CURRENT_MISSION_ID", "CURRENT_RUN_NONCE", "CURRENT_INPUT_FINGERPRINT", "CURRENT_REPO_FINGERPRINT"):
            with self.subTest(field=field):
                _, _, _, contract = self.contracts()
                contract[field] = "wrong"
                result = self.lib.mission_completion_evidence_gate(contract)
                self.assertFalse(result["execution_profile_binding_consumed"])

    def test_07_stale_or_superseded_mission_is_rejected(self):
        _, _, _, contract = self.contracts()
        contract["MISSION_SUPERSEDED"] = True
        result = self.lib.mission_completion_evidence_gate(contract)
        self.assertIn(
            "execution_profile_mission_stale_or_superseded",
            result["execution_profile_binding"]["errors"],
        )

    def test_08_wrong_output_fingerprint_is_rejected(self):
        _, _, _, contract = self.contracts()
        contract["EXECUTION_PROFILE_RESULT"]["output_fingerprint"] = "3" * 64
        result = self.lib.mission_completion_evidence_gate(contract)
        self.assertFalse(result["execution_profile_binding_consumed"])

    def test_09_result_for_another_profile_is_rejected(self):
        _, _, _, contract = self.contracts()
        contract["EXECUTION_PROFILE_RESULT"]["profile_version"] = "v2"
        result = self.lib.mission_completion_evidence_gate(contract)
        self.assertIn(
            "execution_profile_result_profile_version_mismatch",
            result["execution_profile_binding"]["errors"],
        )

    def test_10_required_review_missing_or_wrong_output_is_rejected(self):
        _, _, _, missing = self.contracts()
        missing["EXECUTION_PROFILE_REVIEWS"] = []
        self.assertFalse(
            self.lib.mission_completion_evidence_gate(missing)["execution_profile_binding_consumed"]
        )
        _, _, _, wrong = self.contracts()
        wrong["EXECUTION_PROFILE_REVIEWS"][0]["submitted_output_fingerprint"] = "4" * 64
        self.assertFalse(
            self.lib.mission_completion_evidence_gate(wrong)["execution_profile_binding_consumed"]
        )

    def test_11_insufficient_review_does_not_consume_completion(self):
        admitted, result, _, contract = self.contracts()
        contract["EXECUTION_PROFILE_REVIEWS"] = [self.lib.execution_profile_review_record(
            admitted, result, review_type="ARCHITECTURE_REVIEW",
            review_verdict="INSUFFICIENT_EVIDENCE", review_context_id="review-context",
        )]
        outcome = self.lib.mission_completion_evidence_gate(contract)
        self.assertFalse(outcome["execution_profile_binding_consumed"])

    def test_12_review_cannot_modify_submission_or_share_executor_context(self):
        _, _, _, contract = self.contracts()
        review = contract["EXECUTION_PROFILE_REVIEWS"][0]
        review["submitted_output_modified"] = True
        review["review_context_id"] = "executor-context"
        outcome = self.lib.mission_completion_evidence_gate(contract)
        self.assertFalse(outcome["execution_profile_binding_consumed"])

    def test_13_exact_duplicate_is_idempotent_and_conflict_rejected(self):
        _, result, _, duplicate = self.contracts()
        duplicate["EXISTING_RESULT_FINGERPRINTS"] = [result["result_fingerprint"]]
        bound = self.lib.mission_completion_evidence_gate(duplicate)["execution_profile_binding"]
        self.assertEqual(bound["duplicate_disposition"], "IDEMPOTENT_EXACT_DUPLICATE")
        _, _, _, conflict = self.contracts()
        conflict["EXISTING_RESULT_FINGERPRINTS"] = ["5" * 64]
        outcome = self.lib.mission_completion_evidence_gate(conflict)
        self.assertFalse(outcome["execution_profile_binding_consumed"])

    def test_14_historical_completion_contract_remains_backward_compatible(self):
        result = self.lib.mission_completion_evidence_gate({
            "MISSION_TYPE": "ACCEPTANCE",
            "COMPLETION_CONTRACT": "ACCEPTANCE_COMPLETION",
            "INDEPENDENT_ACCEPTANCE_PROVEN": True,
            "NEXT_OUTPUT_PROVEN": True,
        })
        self.assertEqual(result["completion_verdict"], "COMPLETE_WITH_LEGAL_TERMINAL")
        self.assertEqual(result["execution_profile_binding_consumed"], "NOT_APPLICABLE")

    def test_15_read_only_end_to_end_proof_does_not_change_cps(self):
        before = CPS.read_bytes()
        first = self.lib.bounded_execution_profile_contract_proof(root=ROOT)
        second = self.lib.bounded_execution_profile_contract_proof(root=ROOT)
        self.assertEqual(first["final_verdict"], "PASS")
        self.assertEqual(first["result"]["result_fingerprint"], second["result"]["result_fingerprint"])
        self.assertTrue(first["no_cps_effect"])
        self.assertEqual(before, CPS.read_bytes())

    def test_16_profile_binding_does_not_change_candidate_semantic_identity(self):
        proof = self.lib.bounded_execution_profile_contract_proof(root=ROOT)
        candidate = proof["handoff"]["candidate"]
        without_profile = self.lib.omp_candidate_admission_decision(
            candidate, mission_id="V7_OMP_BOUNDED_EXECUTION_PROFILE_READ_ONLY_PROOF_V1",
        )
        with_profile = proof["handoff"]["admission"]
        self.assertEqual(
            candidate["candidate_instance_id"],
            f"BDP-ICI-{candidate['identity_sha256'][:24].upper()}",
        )
        self.assertEqual(without_profile["mission_id"], with_profile["mission_id"])
        self.assertFalse(without_profile["execution_profile_governed"])
        self.assertTrue(with_profile["execution_profile_governed"])


if __name__ == "__main__":
    unittest.main()
