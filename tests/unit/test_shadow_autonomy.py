import unittest

from admin_core import shadow_autonomy


class ShadowAutonomyTest(unittest.TestCase):
    def decision_surface(self):
        return {
            "users": [
                {
                    "user": "10.0.0.3",
                    "current_channel": "awg0",
                    "recommended_channel": "vless",
                    "recommendation": "move_recommended",
                    "confidence": 91,
                    "trust": 88,
                    "risk": 4,
                    "prediction": {"available": True, "confidence": 0.86},
                    "reasons": ["service fit"],
                    "recommendation_hash": "rec-1",
                    "source_hash": "src-1",
                },
                {
                    "user": "10.0.0.6",
                    "current_channel": "vless",
                    "recommended_channel": "vless",
                    "recommendation": "keep",
                    "confidence": 80,
                    "trust": 82,
                    "risk": 5,
                    "prediction": {"available": True, "confidence": 0.8},
                    "recommendation_hash": "rec-2",
                    "source_hash": "src-1",
                },
            ],
        }

    def test_shadow_decisions_are_advisory_and_non_mutating(self):
        model = shadow_autonomy.build_shadow_autonomy_model(self.decision_surface(), now="2026-06-08T10:00:00+00:00")
        decisions = model["current_decisions"]

        self.assertEqual(len(decisions), 2)
        self.assertEqual(decisions[0]["recommended_action"], "MOVE_USER")
        self.assertEqual(decisions[0]["recommended_target"], "vless")
        self.assertFalse(decisions[0]["execution_allowed_now"])
        self.assertFalse(decisions[0]["runtime_mutation_performed"])
        self.assertEqual(decisions[0]["users_moved"], 0)
        self.assertFalse(decisions[0]["apply_executed"])
        self.assertFalse(decisions[0]["autonomy_enabled"])
        self.assertTrue(model["certification"]["shadow_decision_model_defined"])
        self.assertTrue(model["certification"]["decision_log_certified"])

    def test_operator_comparison_updates_quality_and_confidence(self):
        base = shadow_autonomy.build_shadow_autonomy_model(self.decision_surface(), now="2026-06-08T10:00:00+00:00")
        first = base["current_decisions"][0]
        comparison = shadow_autonomy.operator_comparison_record(
            first,
            operator_decision="agree",
            category="trust",
            reason="operator agrees with trust signal",
            actor="admin",
            now="2026-06-08T10:01:00+00:00",
        )
        model = shadow_autonomy.build_shadow_autonomy_model(
            self.decision_surface(),
            history=[first, comparison],
            now="2026-06-08T10:02:00+00:00",
        )

        self.assertEqual(model["quality"]["comparisons_total"], 1)
        self.assertEqual(model["quality"]["agreement_rate"], 1.0)
        self.assertEqual(model["quality"]["override_rate"], 0.0)
        self.assertGreater(model["confidence"]["earned_confidence"], 0)
        self.assertFalse(comparison["runtime_mutation_performed"])
        self.assertFalse(comparison["apply_executed"])
        self.assertFalse(comparison["autonomy_enabled"])

    def test_override_is_counted_without_execution(self):
        base = shadow_autonomy.build_shadow_autonomy_model(self.decision_surface(), now="2026-06-08T10:00:00+00:00")
        comparison = shadow_autonomy.operator_comparison_record(
            base["current_decisions"][0],
            operator_decision="override",
            category="manual_preference",
            reason="manual review",
        )
        model = shadow_autonomy.build_shadow_autonomy_model(self.decision_surface(), history=[comparison])

        self.assertEqual(model["quality"]["override_rate"], 1.0)
        self.assertEqual(model["quality"]["agreement_rate"], 0.0)
        self.assertEqual(model["safety"]["users_moved"], 0)


if __name__ == "__main__":
    unittest.main()

