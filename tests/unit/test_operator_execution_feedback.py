import unittest
from pathlib import Path

from admin_core import operator_execution_feedback as feedback


ROOT = Path(__file__).resolve().parents[2]
ADMIN_API = ROOT / "admin" / "v7-admin-api"


class OperatorExecutionFeedbackTest(unittest.TestCase):
    def test_execution_feedback_contract_materializes_all_feedback_links(self):
        contract = feedback.execution_feedback_contract(
            user="10.7.0.3",
            source_channel="awg0",
            target_channel="awg3",
            execution_result={"success": True, "result": "applied"},
            verification_result={"success": True, "result": "verified"},
            recommendation_hash="rec-1",
            prediction_expected=0.8,
            prediction_actual=0.75,
            audit_reference="audit-1",
            closure_reference="closure-1",
        )
        records = feedback.materialized_feedback_records(contract)

        self.assertEqual(contract["outcome_status"], "success")
        self.assertGreater(contract["trust_delta"], 0)
        self.assertGreater(contract["prediction_delta"], 0)
        self.assertGreater(contract["recommendation_delta"], 0)
        self.assertEqual(set(records), {"outcome", "trust", "prediction", "recommendation", "closure"})
        self.assertEqual(records["closure"]["closure_state"], "CLOSED")

    def test_feedback_materializes_stability_window_for_authority_promotion(self):
        contract = feedback.execution_feedback_contract(
            user="10.7.0.3",
            source_channel="vless",
            target_channel="awg3",
            execution_result={"success": True, "result": "applied"},
            verification_result={"success": True, "result": "verified"},
            recommendation_hash="rec-stability",
            stability_window_seconds=900,
        )
        records = feedback.materialized_feedback_records(contract)

        self.assertEqual(contract["stability_window_seconds"], 900)
        for row in records.values():
            self.assertEqual(row["stability_window_seconds"], 900)

    def test_failure_and_rollback_reduce_feedback(self):
        failure = feedback.execution_feedback_contract(
            user="10.7.0.3",
            source_channel="awg0",
            target_channel="awg3",
            execution_result={"success": False, "result": "failed"},
            verification_result={"success": False},
            recommendation_hash="rec-2",
        )
        rollback = feedback.execution_feedback_contract(
            user="10.7.0.3",
            source_channel="awg0",
            target_channel="awg3",
            execution_result={"rollback_required": True},
            verification_result={"rollback_required": True},
            recommendation_hash="rec-3",
        )

        self.assertEqual(failure["outcome_status"], "failure")
        self.assertLess(failure["trust_delta"], 0)
        self.assertEqual(rollback["outcome_status"], "rollback_required")
        self.assertLess(rollback["recommendation_delta"], 0)

    def test_recommendation_approval_intent_is_not_execution(self):
        packet = feedback.recommendation_approval_packet(
            {
                "user": "10.7.0.3",
                "current_channel": "awg0",
                "recommended_channel": "awg3",
                "recommendation_hash": "rec-4",
                "confidence": 0.9,
                "trust": 88,
                "risk": 2,
                "prediction": {"available": True},
                "ctr_governance_evidence": {
                    "state": "DEGRADED",
                    "review_required": True,
                    "review_reason": "Есть просадка качества или сервисов.",
                    "review_category": "degraded_channel_review",
                    "review_severity": "high",
                    "packet_preview": {
                        "ctr_state": "DEGRADED",
                        "ctr_review_status": "REVIEW_REQUIRED",
                        "ctr_review_reason": "Есть просадка качества или сервисов.",
                    },
                },
                "review_required": True,
                "review_required_reasons": ["ctr_state_requires_operator_review"],
                "review_category": "degraded_channel_review",
                "review_severity": "high",
                "review_recommendation": "Не использовать как обычную цель без review.",
                "review_warning": "Сначала проверить причину деградации.",
                "review_next_action": "Обновить проверки.",
                "emergency_only": False,
            },
            actor="operator-a",
        )

        self.assertEqual(packet["schema_version"], "v7.operator-recommendation-approval-intent.v1")
        self.assertTrue(packet["approval_packet_required"])
        self.assertFalse(packet["execution_allowed_now"])
        self.assertEqual(packet["next_state"], "EXECUTION_RECHECK_REQUIRED")
        self.assertIn("direct_user_switch", packet["blocked_actions"])
        self.assertTrue(packet["ctr_review"]["review_required"])
        self.assertEqual(packet["ctr_review"]["review_category"], "degraded_channel_review")
        self.assertEqual(packet["ctr_review"]["review_severity"], "high")
        self.assertEqual(packet["ctr_review"]["approval_authority"], "none")
        self.assertEqual(packet["ctr_review"]["denial_authority"], "none")
        self.assertFalse(packet["ctr_review"]["packet_authority_changed"])
        self.assertFalse(packet["ctr_review"]["execution_authority_changed"])
        self.assertEqual(packet["ctr_packet_evidence_preview"]["ctr_state"], "DEGRADED")

    def test_module_is_pure_no_runtime_invocation(self):
        source = Path(feedback.__file__).read_text(encoding="utf-8")

        self.assertNotIn("subprocess", source)
        self.assertNotIn("run_action", source)
        self.assertNotIn("os.system", source)

    def test_admin_exposes_recommendation_approve_action(self):
        source = ADMIN_API.read_text(encoding="utf-8")

        self.assertIn('elif path == "/api/actions/recommendation-approve":', source)
        self.assertIn('elif path == "/api/actions/execution-feedback-materialize":', source)
        self.assertIn("operator_recommendation_approve_response", source)
        self.assertIn("execution_feedback_materialize_response", source)
        self.assertIn("approveUserRecommendation", source)
        self.assertNotIn("stability_window_seconds=to_int", source)
        self.assertIn("stability_window_seconds=bounded_int_value", source)


if __name__ == "__main__":
    unittest.main()
