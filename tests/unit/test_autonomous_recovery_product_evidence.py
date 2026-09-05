from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import unittest

from admin_core import operator_execution


ROOT = Path(__file__).resolve().parents[2]


def load_lib():
    spec = importlib.util.spec_from_file_location(
        "v7_sync_lib_autonomous_recovery_evidence", ROOT / "tools/v7_sync_lib.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class AutonomousRecoveryProductEvidenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = load_lib()
        cls.campaign = cls.lib.autonomous_recovery_product_evidence_campaign(root=ROOT)

    def test_campaign_runs_real_owner_paths_at_1k_then_10k(self):
        result = self.campaign
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertEqual(result["evidence_class"], "DETERMINISTIC_L2_READINESS_NOT_RECOVERY_ACCEPTANCE")
        self.assertIn("L3_OWNER_EMITTED_FAULT_ONSET_AND_S11_REQUIRED", result["errors"])
        self.assertEqual(result["scale_order"], [1000, 10000])
        self.assertEqual(
            [row["affected_scope_count"] for row in result["staged_scale_receipts"]],
            [1000, 10000],
        )
        self.assertEqual(
            {row["scenario_id"] for row in result["multi_channel_fault_receipts"]},
            {"AR-ROUTE-LOSS", "AR-REQUIRED-SERVICE", "AR-PARTIAL-DEGRADATION"},
        )
        self.assertGreaterEqual(result["coverage"]["simultaneous_multi_channel_cases"], 1)
        self.assertEqual(
            set(result["coverage"]["executed_fault_classes"]),
            set(self.lib.AUTONOMOUS_RECOVERY_FAULT_CLASSES),
        )
        for receipt in result["receipts"]:
            self.assertEqual(receipt["validation"]["final_verdict"], "PASS")
            self.assertTrue(receipt["within_7_seconds"])
            self.assertEqual(len(receipt["member_receipts"]), receipt["affected_scope_count"])
            self.assertEqual(receipt["owner_path_evidence"]["planner_selected_count"], 1)
            self.assertEqual(
                receipt["owner_path_evidence"]["adaptive_cohort_count"],
                receipt["affected_scope_count"],
            )
            self.assertEqual(receipt["owner_path_evidence"]["isolated_apply_terminal"], "SUCCESS")
            self.assertFalse(receipt["capacity_resource_envelope"]["hardware_equivalent_claim"])
        self.assertTrue(all(
            row["final_verdict"] == "STOP_SAFE"
            for row in result["negative_gate_receipts"]
        ))

    def test_missing_last_member_and_forged_fast_verdict_fail_closed(self):
        receipt = copy.deepcopy(self.campaign["receipts"][0])
        receipt["member_receipts"].pop()
        receipt["within_7_seconds"] = False
        checked = self.lib.validate_autonomous_recovery_controlled_receipt(receipt)
        self.assertEqual(checked["final_verdict"], "STOP_SAFE")
        self.assertIn("controlled_receipt_complete_scope_missing", checked["errors"])
        self.assertIn("controlled_receipt_slo_verdict_mismatch", checked["errors"])

    def test_stale_generation_and_wrong_scenario_fail_closed(self):
        receipt = copy.deepcopy(self.campaign["receipts"][0])
        receipt["member_receipts"][0]["generation"] = "stale-generation"
        receipt["member_receipts"][1]["scenario_id"] = "wrong-scenario"
        checked = self.lib.validate_autonomous_recovery_controlled_receipt(receipt)
        self.assertEqual(checked["final_verdict"], "STOP_SAFE")
        self.assertIn("controlled_receipt_member_identity_drift", checked["errors"])

    def test_seeded_defect_is_repaired_replayed_and_removed(self):
        proof = self.campaign["seeded_defect_proof"]
        self.assertEqual(proof["final_verdict"], "PASS")
        self.assertEqual(proof["evidence_class"], "HARNESS_SELF_TEST_NOT_PRODUCT_DEFECT_EVIDENCE")
        self.assertEqual(
            proof["causal_record"]["class"],
            "DETERMINISTIC_CAUSAL_RECORD_NOT_NATIVE_ANALYST",
        )
        self.assertTrue(proof["checks"]["origin_experiment_replay_passed"])
        self.assertTrue(proof["seed_cleanup_verified"])
        self.assertFalse(proof["causal_record"]["native_context_claim"])
        self.assertFalse(proof["independent_review_evidence"]["native_reviewer_claim"])

    def test_staged_generic_movement_candidate_never_self_certifies_l3(self):
        rows = [
            operator_execution.build_isolated_generic_movement_equivalence_candidate(scale)
            for scale in (1_000, 10_000)
        ]
        self.assertEqual([row["scale"] for row in rows], [1_000, 10_000])
        for row in rows:
            self.assertEqual(row["final_verdict"], "READY_FOR_L3_REPRESENTATIVE_BINDING")
            self.assertFalse(row["representative_obligation"]["satisfied"])
            self.assertTrue(all(row["checks"].values()))
            self.assertEqual(len(row["assignments"]), row["scale"])
            self.assertEqual(
                len(set(row["per_member_assignment_receipt_fingerprints"])),
                row["scale"],
            )
            self.assertEqual(sum(row["target_counts"].values()), row["scale"])
            self.assertEqual(row["authority_impact"], "NONE")

    def test_generic_movement_candidate_rejects_unstaged_scale(self):
        result = operator_execution.build_isolated_generic_movement_equivalence_candidate(999)
        self.assertEqual(result["final_verdict"], "STOP_SAFE")
        self.assertIn("unsupported_engineering_scale", result["errors"])


if __name__ == "__main__":
    unittest.main()
