import unittest

from admin_core import intelligence_workers as workers


def channel_scores(*rows):
    return {"items": list(rows), "confidence": 1.0}


def suitability(*rows):
    return {"items": [{"user": "10.0.0.2", "candidates": list(rows)}], "confidence": 1.0}


class ChannelTrustRecoveryTest(unittest.TestCase):
    def test_successful_feedback_increases_trust_to_trusted_lifecycle(self):
        model = workers.build_channel_trust_recovery_model(
            channel_service_scores_snapshot=channel_scores({
                "channel": "vless",
                "aggregate_score": 92,
                "confidence": 0.92,
                "verdict": "OK",
                "required_low": [],
                "required_missing": [],
            }),
            candidate_suitability_snapshot=suitability({"channel": "vless", "suitability_score": 90, "confidence": 0.9}),
            best_available_pool_snapshot={"items": [{"best_channel": "vless"}]},
            decision_records=[{"result": "success", "selected_moves": [{"user": "10.0.0.2", "target": "vless"}]}],
        )
        row = model["channels"][0]
        self.assertEqual(row["lifecycle"], "TRUSTED")
        self.assertGreaterEqual(row["trust_score"], 80)
        self.assertEqual(row["routing_impact"]["mode"], "advisory_only_no_runtime_weight_applied")
        self.assertFalse(row["routing_impact"]["planner_behavior_changed"])

    def test_failure_feedback_decreases_trust_and_quarantines_channel(self):
        model = workers.build_channel_trust_recovery_model(
            channel_service_scores_snapshot=channel_scores({
                "channel": "awg3",
                "aggregate_score": 88,
                "confidence": 0.9,
                "verdict": "OK",
                "required_low": [],
                "required_missing": [],
            }),
            candidate_suitability_snapshot=suitability({"channel": "awg3", "suitability_score": 85, "confidence": 0.85}),
            best_available_pool_snapshot={"items": []},
            decision_records=[
                {"result": "failed", "selected_moves": [{"user": "10.0.0.2", "target": "awg3"}]},
                {"result": "failed", "selected_moves": [{"user": "10.0.0.3", "target": "awg3"}]},
            ],
        )
        row = model["channels"][0]
        self.assertEqual(row["lifecycle"], "QUARANTINED")
        self.assertTrue(row["recovery"]["operator_review_required"])
        self.assertEqual(row["routing_impact"]["recommended_bias"], "block_until_operator_review")

    def test_recovery_state_uses_success_after_negative_history(self):
        model = workers.build_channel_trust_recovery_model(
            channel_service_scores_snapshot=channel_scores({
                "channel": "awg0",
                "aggregate_score": 78,
                "confidence": 0.82,
                "verdict": "OK",
                "required_low": [],
                "required_missing": [],
            }),
            candidate_suitability_snapshot=suitability({"channel": "awg0", "suitability_score": 80, "confidence": 0.8}),
            best_available_pool_snapshot={"items": []},
            decision_records=[
                {"result": "failed", "selected_moves": [{"user": "10.0.0.2", "target": "awg0"}]},
                {"result": "success", "selected_moves": [{"user": "10.0.0.2", "target": "awg0"}]},
            ],
        )
        row = model["channels"][0]
        self.assertEqual(row["lifecycle"], "RECOVERING")
        self.assertEqual(row["recovery"]["state"], "IN_PROGRESS")
        self.assertEqual(row["routing_impact"]["recommended_bias"], "allow_only_with_operator_attention")

    def test_successful_rollback_does_not_quarantine_healthy_channel(self):
        model = workers.build_channel_trust_recovery_model(
            channel_service_scores_snapshot=channel_scores({
                "channel": "awg0",
                "aggregate_score": 90,
                "confidence": 0.82,
                "verdict": "OK",
                "required_low": [],
                "required_missing": [],
            }),
            candidate_suitability_snapshot=suitability({"channel": "awg0", "suitability_score": 88, "confidence": 0.8}),
            best_available_pool_snapshot={"items": []},
            decision_records=[
                {"result": "rollback_success", "rollback_completed": True, "selected_moves": [{"user": "10.0.0.2", "target": "awg0"}]},
            ],
        )
        row = model["channels"][0]
        self.assertNotEqual(row["lifecycle"], "QUARANTINED")
        self.assertEqual(row["feedback"]["rollback_successes"], 1)
        self.assertEqual(row["feedback"]["rollback_failures"], 0)
        self.assertFalse(row["recovery"]["operator_review_required"])

    def test_no_recent_live_success_applies_advisory_decay_only(self):
        model = workers.build_channel_trust_recovery_model(
            channel_service_scores_snapshot=channel_scores({
                "channel": "reserved",
                "aggregate_score": 72,
                "confidence": 0.6,
                "verdict": "OK",
                "required_low": [],
                "required_missing": [],
            }),
            candidate_suitability_snapshot=suitability({"channel": "reserved", "suitability_score": 70, "confidence": 0.6}),
            best_available_pool_snapshot={"items": []},
            decision_records=[],
        )
        row = model["channels"][0]
        self.assertEqual(row["decay"]["reason"], "no_recent_live_success")
        self.assertLess(row["decay"]["applied_delta"], 0)
        self.assertFalse(row["decay"]["runtime_behavior_changed"])

    def test_healthy_channel_without_success_history_is_watch_not_new(self):
        model = workers.build_channel_trust_recovery_model(
            channel_service_scores_snapshot=channel_scores({
                "channel": "awg3",
                "aggregate_score": 88,
                "confidence": 0.42,
                "verdict": "OK",
                "required_low": [],
                "required_missing": [],
            }),
            candidate_suitability_snapshot=suitability({"channel": "awg3", "suitability_score": 84, "confidence": 0.42}),
            best_available_pool_snapshot={"items": [{"best_channel": "awg3"}]},
            decision_records=[],
        )
        row = model["channels"][0]
        self.assertEqual(row["lifecycle"], "WATCH")
        self.assertEqual(row["lifecycle_reason"], "current_services_look_healthy_but_success_history_is_thin")
        self.assertEqual(model["time_windows"]["maximum_practical_trust_window_days"], 7)

    def test_switch_history_arrival_counts_as_channel_success_feedback(self):
        model = workers.build_channel_trust_recovery_model(
            channel_service_scores_snapshot=channel_scores({
                "channel": "awg3",
                "aggregate_score": 94,
                "confidence": 0.46,
                "verdict": "OK",
                "required_low": [],
                "required_missing": [],
            }),
            candidate_suitability_snapshot=suitability({"channel": "awg3", "suitability_score": 83, "confidence": 0.46}),
            best_available_pool_snapshot={"items": [{"best_channel": "awg3"}]},
            decision_records=[
                {"from": "vless", "to": "awg3", "reason": "autoswitch_rebalance", "user_ip": "10.7.0.2"},
            ],
        )
        row = model["channels"][0]
        self.assertEqual(row["feedback"]["successes"], 1)
        self.assertEqual(row["lifecycle"], "TRUSTED")
        self.assertEqual(row["lifecycle_reason"], "high_score_with_successful_channel_feedback")

    def test_rollback_switch_history_does_not_count_as_success_feedback(self):
        model = workers.build_channel_trust_recovery_model(
            channel_service_scores_snapshot=channel_scores({
                "channel": "awg3",
                "aggregate_score": 94,
                "confidence": 0.46,
                "verdict": "OK",
                "required_low": [],
                "required_missing": [],
            }),
            candidate_suitability_snapshot=suitability({"channel": "awg3", "suitability_score": 83, "confidence": 0.46}),
            best_available_pool_snapshot={"items": [{"best_channel": "awg3"}]},
            decision_records=[
                {"from": "vless", "to": "awg3", "reason": "autoswitch_rollback", "user_ip": "10.7.0.2"},
            ],
        )
        row = model["channels"][0]
        self.assertEqual(row["feedback"]["successes"], 0)
        self.assertEqual(row["feedback"]["rollback_successes"], 1)
        self.assertEqual(row["lifecycle"], "WATCH")

    def test_explainability_and_policy_are_defined_for_channel_lifecycle(self):
        model = workers.build_channel_trust_recovery_model(
            channel_service_scores_snapshot=channel_scores({
                "channel": "degraded",
                "aggregate_score": 55,
                "confidence": 0.7,
                "verdict": "WARN",
                "required_low": ["telegram"],
                "required_missing": [],
            }),
            candidate_suitability_snapshot=suitability({"channel": "degraded", "suitability_score": 58, "confidence": 0.7}),
            best_available_pool_snapshot={"items": []},
            decision_records=[],
        )
        row = model["channels"][0]
        self.assertEqual(row["lifecycle"], "DEGRADED")
        self.assertIn("time_windows", model)
        self.assertIn("decay_policy", model)
        self.assertTrue(any(item.startswith("current_service_score=") for item in row["explainability"]))
        self.assertEqual(model["runtime_decision_authority"], "none_evidence_only")


if __name__ == "__main__":
    unittest.main()
