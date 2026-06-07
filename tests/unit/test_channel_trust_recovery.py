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
