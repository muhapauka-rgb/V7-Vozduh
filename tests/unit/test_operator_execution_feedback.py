import unittest
from pathlib import Path

from admin_core import operator_execution_feedback as feedback


ROOT = Path(__file__).resolve().parents[2]
ADMIN_API = ROOT / "admin" / "v7-admin-api"


class OperatorExecutionFeedbackTest(unittest.TestCase):
    def test_terminal_aliases_normalize_to_existing_outcome_taxonomy(self):
        expected = {
            "applied": "SUCCESS",
            "stay": "CORRECT_STAY",
            "stop_safe_no_action": "STOP_SAFE",
            "no_legal_candidate": "NO_CANDIDATE",
            "opportunity_missed": "MISSED",
            "rollback_success": "ROLLBACK_SUCCESS",
        }
        for alias, canonical in expected.items():
            with self.subTest(alias=alias):
                self.assertEqual(
                    feedback.normalize_terminal_outcome_classification(alias),
                    canonical,
                )

    def test_feedback_preserves_durable_replay_and_evidence_identity(self):
        contract = feedback.execution_feedback_contract(
            user="10.7.0.16",
            source_channel="controlled-source",
            target_channel="vless",
            execution_result={"success": True},
            verification_result={"verification_passed": True},
            rollback_result={"rollback_required": False},
            packet_id="pkt-replay",
            evidence_class="CONTROLLED_PRODUCTION",
            decision_trace_id="decision-replay",
            input_snapshot_identity="snapshot-replay",
            expected_terminal="SUCCESS",
        )

        outcome = feedback.materialized_feedback_records(contract)["outcome"]

        self.assertEqual(outcome["evidence_class"], "CONTROLLED_PRODUCTION")
        self.assertEqual(outcome["decision_trace_id"], "decision-replay")
        self.assertEqual(outcome["input_snapshot_identity"], "snapshot-replay")
        self.assertEqual(outcome["expected_terminal"], "SUCCESS")

    def test_execution_feedback_contract_materializes_all_feedback_links(self):
        contract = feedback.execution_feedback_contract(
            user="10.7.0.3",
            source_channel="awg0",
            target_channel="awg3",
            execution_result={"success": True, "result": "applied"},
            verification_result={
                "success": True,
                "result": "verified",
                "service_outcome": {"telegram": "ok"},
                "user_outcome": {"connected": True},
            },
            recommendation_hash="rec-1",
            packet_id="packet-1",
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
        self.assertEqual(contract["outcome_quality"]["outcome_quality"], "SUCCESS")
        self.assertEqual(contract["outcome_quality"]["learning_value"], "HIGH")
        self.assertIn("Decision Outcome", contract["knowledge_growth"]["knowledge_improved"])
        self.assertEqual(contract["learning_record"]["schema_version"], "v7.decision-outcome-learning-record.v1")
        self.assertEqual(set(records), {"outcome", "trust", "prediction", "recommendation", "closure"})
        self.assertEqual(records["closure"]["closure_state"], "CLOSED")
        self.assertEqual(records["outcome"]["packet_id"], "packet-1")
        self.assertEqual(records["outcome"]["selected_moves"][0]["user"], "10.7.0.3")
        self.assertEqual(records["outcome"]["selected_moves"][0]["target"], "awg3")
        self.assertEqual(records["outcome"]["learning_record"]["learning_record_id"], contract["learning_record"]["learning_record_id"])

    def test_decision_outcome_learning_model_uses_existing_records_only(self):
        good = feedback.execution_feedback_contract(
            user="10.7.0.3",
            source_channel="awg0",
            target_channel="awg3",
            execution_result={"success": True, "result": "applied"},
            verification_result={"success": True, "result": "verified"},
            recommendation_hash="rec-good",
            packet_id="packet-good",
            prediction_expected=0.9,
            prediction_actual=0.88,
        )
        bad = feedback.execution_feedback_contract(
            user="10.7.0.4",
            source_channel="awg0",
            target_channel="vless",
            execution_result={"success": False, "result": "failed"},
            verification_result={"success": False},
            recommendation_hash="rec-bad",
            packet_id="packet-bad",
        )
        model = feedback.decision_outcome_learning_model([good, bad], generated_at="2026-06-24T00:00:00+00:00")

        self.assertEqual(model["outcome_quality_counts"]["SUCCESS"], 1)
        self.assertEqual(model["outcome_quality_counts"]["FAILED"], 1)
        self.assertGreater(model["effectiveness"]["recommendation_correct_rate"], 0)
        self.assertIn("Suitability", model["knowledge_growth"]["knowledge_degraded"])
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertEqual(model["users_moved"], 0)

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
            execution_result={"applied": True, "result": "applied"},
            verification_result={"success": False, "result": "failed"},
            rollback_result={"rollback_required": True, "rollback_verdict": "ROLLBACK_COMPLETED"},
            recommendation_hash="rec-3",
        )

        self.assertEqual(failure["outcome_status"], "failure")
        self.assertLess(failure["trust_delta"], 0)
        self.assertEqual(rollback["outcome_status"], "rollback_success")
        self.assertLess(rollback["recommendation_delta"], 0)

    def test_terminal_outcome_classification_matrix(self):
        success = feedback.execution_feedback_contract(
            user="10.7.0.3",
            source_channel="vless",
            target_channel="awg3",
            execution_result={"applied": True, "result": "applied"},
            verification_result={"success": True, "result": "verified"},
            rollback_result={"rollback_required": False, "rollback_verdict": "NOT_REQUIRED"},
            recommendation_hash="rec-success",
            prediction_expected=1.0,
            prediction_actual=1.0,
        )
        rollback_success = feedback.execution_feedback_contract(
            user="10.7.0.4",
            source_channel="vless",
            target_channel="awg3",
            execution_result={"applied": True, "result": "applied"},
            verification_result={"success": False, "result": "failed"},
            rollback_result={"rollback_required": True, "rollback_verdict": "ROLLBACK_COMPLETED"},
            recommendation_hash="rec-rollback-success",
            prediction_expected=1.0,
            prediction_actual=0.0,
        )
        rollback_failure = feedback.execution_feedback_contract(
            user="10.7.0.5",
            source_channel="vless",
            target_channel="awg3",
            execution_result={"applied": True, "result": "applied"},
            verification_result={"success": False, "result": "failed"},
            rollback_result={"rollback_required": True, "rollback_verdict": "ROLLBACK_FAILED"},
            recommendation_hash="rec-rollback-failure",
            prediction_expected=1.0,
            prediction_actual=0.0,
        )
        no_execution = feedback.execution_feedback_contract(
            user="10.7.0.6",
            source_channel="vless",
            target_channel="awg3",
            execution_result={"apply_attempted": False, "result": "stop_safe"},
            verification_result={},
            rollback_result={},
            recommendation_hash="rec-no-execution",
        )
        model = feedback.decision_outcome_learning_model(
            [success, rollback_success, rollback_failure, no_execution],
            generated_at="2026-06-27T00:00:00+00:00",
        )

        self.assertEqual(success["terminal_outcome_classification"], "SUCCESS")
        self.assertEqual(success["outcome_quality"]["outcome_quality"], "SUCCESS")
        self.assertGreater(success["trust_delta"], 0)

        self.assertEqual(rollback_success["terminal_outcome_classification"], "ROLLBACK_SUCCESS")
        self.assertEqual(rollback_success["outcome_quality"]["outcome_quality"], "ROLLBACK_SUCCESS")
        self.assertEqual(rollback_success["trust_delta"], 0.0)
        self.assertLess(rollback_success["recommendation_delta"], 0)
        self.assertIn("Recovery", rollback_success["knowledge_growth"]["knowledge_improved"])

        self.assertEqual(rollback_failure["terminal_outcome_classification"], "ROLLBACK_FAILURE")
        self.assertEqual(rollback_failure["outcome_quality"]["outcome_quality"], "ROLLBACK_FAILURE")
        self.assertLess(rollback_failure["recommendation_delta"], 0)
        self.assertIn("Recovery", rollback_failure["knowledge_growth"]["knowledge_degraded"])

        self.assertEqual(no_execution["terminal_outcome_classification"], "NO_EXECUTION")
        self.assertEqual(no_execution["outcome_quality"]["outcome_quality"], "NO_EXECUTION")
        self.assertFalse(no_execution["knowledge_growth"]["knowledge_gained"])

        self.assertEqual(model["outcome_quality_counts"]["SUCCESS"], 1)
        self.assertEqual(model["outcome_quality_counts"]["ROLLBACK_SUCCESS"], 1)
        self.assertEqual(model["outcome_quality_counts"]["ROLLBACK_FAILURE"], 1)
        self.assertEqual(model["outcome_quality_counts"]["NO_EXECUTION"], 1)
        self.assertLess(model["effectiveness"]["recommendation_correct_rate"], 1.0)

    def test_nonempty_not_required_rollback_is_not_reported_as_used(self):
        contract = feedback.execution_feedback_contract(
            user="10.7.0.100",
            source_channel="1",
            target_channel="vless",
            execution_result={"applied": True, "result": "applied"},
            verification_result={"success": True, "result": "verified"},
            rollback_result={
                "rollback_required": False,
                "rollback_verdict": "NOT_REQUIRED",
            },
            recommendation_hash="rec-no-rollback",
        )

        self.assertEqual(contract["outcome_status"], "success")
        self.assertFalse(contract["outcome_quality"]["rollback_used"])

    def test_actual_rollback_is_reported_as_used(self):
        contract = feedback.execution_feedback_contract(
            user="10.7.0.101",
            source_channel="1",
            target_channel="vless",
            execution_result={"applied": True, "result": "applied"},
            verification_result={"success": False, "result": "failed"},
            rollback_result={
                "rollback_required": True,
                "rollback_attempted": True,
                "rollback_verdict": "ROLLBACK_COMPLETED",
            },
            recommendation_hash="rec-rollback-used",
        )

        self.assertEqual(contract["outcome_status"], "rollback_success")
        self.assertTrue(contract["outcome_quality"]["rollback_used"])

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
