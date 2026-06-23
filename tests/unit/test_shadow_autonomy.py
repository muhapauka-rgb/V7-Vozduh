import unittest
import json
import tempfile
from pathlib import Path

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

    def test_repeated_operator_agreement_can_certify_earned_confidence(self):
        decisions = [
            {
                "decision_id": f"shadow-{i}",
                "confidence": 86.0,
                "prediction": {"confidence": 0.86},
                "trust": 88.0,
                "risk": 4.0,
            }
            for i in range(5)
        ]
        comparisons = [{
            "record_type": shadow_autonomy.COMPARISON_RECORD_TYPE,
            "decision_id": decision["decision_id"],
            "operator_agreed": True,
            "override": False,
        } for decision in decisions]

        early_quality = shadow_autonomy.decision_quality_summary(decisions[:1], history=comparisons[:1])
        early_confidence = shadow_autonomy.confidence_model(decisions[:1], early_quality)
        mature_quality = shadow_autonomy.decision_quality_summary(decisions, history=comparisons)
        mature_confidence = shadow_autonomy.confidence_model(decisions, mature_quality)

        self.assertIn("shadow_comparison_history_below_minimum", early_confidence["blockers"])
        self.assertGreater(mature_confidence["comparison_history_count"], early_confidence["comparison_history_count"])
        self.assertGreaterEqual(mature_confidence["earned_confidence"], shadow_autonomy.OBSERVATION_TARGETS["minimum_earned_confidence"])
        self.assertTrue(mature_confidence["certified"])

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

    def test_observation_window_and_readiness_require_real_comparisons(self):
        base = shadow_autonomy.build_shadow_autonomy_model(self.decision_surface(), now="2026-06-08T10:00:00+00:00")
        comparisons = [
            shadow_autonomy.operator_comparison_record(
                base["current_decisions"][0],
                operator_decision="agree",
                category="trust",
                reason="ok",
                now=f"2026-06-08T1{i}:00:00+00:00",
            )
            for i in range(5)
        ]
        history = list(base["current_decisions"]) + comparisons
        model = shadow_autonomy.build_shadow_autonomy_model(self.decision_surface(), history=history, now="2026-06-09T12:00:00+00:00")

        self.assertTrue(model["observation_window"]["enough_comparisons"])
        self.assertFalse(model["observation_window"]["enough_decisions"])
        self.assertEqual(model["operator_behavior"]["behavior_pattern"], "MOSTLY_AGREEING")
        self.assertFalse(model["autonomy_evidence"]["evidence_targets_met"])
        self.assertEqual(model["autonomy_readiness"]["closest_stage"], "SHADOW_ONLY")
        self.assertIn("minimum_decisions", model["autonomy_evidence"]["missing_targets"])
        self.assertFalse(model["safety"]["execution_allowed_now"])

    def test_disagreement_and_confidence_evolution_are_classified(self):
        base = shadow_autonomy.build_shadow_autonomy_model(self.decision_surface(), now="2026-06-08T10:00:00+00:00")
        comparison = shadow_autonomy.operator_comparison_record(
            base["current_decisions"][0],
            operator_decision="disagree",
            category="capacity",
            reason="capacity concern",
            now="2026-06-08T11:00:00+00:00",
        )
        model = shadow_autonomy.build_shadow_autonomy_model(
            self.decision_surface(),
            history=[base["current_decisions"][0], comparison],
            now="2026-06-08T12:00:00+00:00",
        )

        self.assertEqual(model["disagreement_analysis"]["by_category"]["capacity"], 1)
        self.assertEqual(model["disagreement_analysis"]["primary_disagreement_reason"], "capacity")
        self.assertIn(model["confidence_evolution"]["trend"], {"STABLE", "GROWING", "DECLINING"})
        self.assertIn("rollback", model["gap_analysis"]["gap_classes"])

    def test_operator_review_packet_marks_real_review_eligibility(self):
        model = shadow_autonomy.build_shadow_autonomy_model(self.decision_surface(), now="2026-06-08T10:00:00+00:00")
        packet = model["operator_review_packet"]

        self.assertEqual(packet["reviewable_decisions"], 2)
        self.assertFalse(packet["synthetic_agreement_allowed"])
        self.assertTrue(packet["requires_real_operator_judgement"])
        self.assertFalse(packet["runtime_mutation_performed"])
        self.assertFalse(packet["apply_executed"])
        self.assertEqual(packet["items"][0]["source_channel"], "awg0")
        self.assertEqual(packet["items"][0]["target_channel"], "vless")
        self.assertTrue(packet["items"][0]["comparison_eligibility"]["eligible"])

    def test_review_packet_and_comparison_survive_rebuild_and_reread(self):
        base = shadow_autonomy.build_shadow_autonomy_model(self.decision_surface(), now="2026-06-08T10:00:00+00:00")
        decision = base["current_decisions"][0]
        comparison = shadow_autonomy.operator_comparison_record(
            decision,
            operator_decision="agree",
            category="trust",
            reason="real operator reviewed",
            now="2026-06-08T10:01:00+00:00",
        )
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "shadow-autonomy-decisions.jsonl"
            log.write_text(
                "\n".join(json.dumps(row, sort_keys=True) for row in [decision, comparison]) + "\n",
                encoding="utf-8",
            )
            reread = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines() if line.strip()]

        rebuilt = shadow_autonomy.build_shadow_autonomy_model(
            self.decision_surface(),
            history=reread,
            now="2026-06-08T10:02:00+00:00",
        )

        self.assertEqual(rebuilt["quality"]["comparisons_total"], 1)
        self.assertEqual(rebuilt["quality"]["agreement_rate"], 1.0)
        self.assertGreater(rebuilt["confidence"]["earned_confidence"], 0)
        self.assertEqual(rebuilt["operator_review_packet"]["reviewed_decisions"], 1)
        self.assertEqual(rebuilt["operator_review_packet"]["reviewable_decisions"], 1)
        self.assertFalse(rebuilt["operator_review_packet"]["synthetic_agreement_allowed"])

    def test_growth_projection_uses_existing_confidence_formula(self):
        projection = shadow_autonomy.comparison_growth_projection(45.828)
        by_key = {
            (row["comparisons"], row["agreement_rate"]): row["earned_confidence"]
            for row in projection["rows"]
        }

        self.assertFalse(projection["synthetic_agreement_created"])
        self.assertEqual(by_key[(5, 1.0)], 59.371)
        self.assertEqual(by_key[(10, 0.9)], 67.914)
        self.assertEqual(by_key[(15, 0.8)], 71.457)
        self.assertEqual(by_key[(20, 0.75)], 75.0)


if __name__ == "__main__":
    unittest.main()
