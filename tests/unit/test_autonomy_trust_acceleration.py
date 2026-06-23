import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from admin_core import autonomy_trust_acceleration as accel
from admin_core import intelligence_snapshots as snapshots
from admin_core import shadow_autonomy


class AutonomyTrustAccelerationTest(unittest.TestCase):
    def write_snapshot(self, root: Path, family: str, content, confidence=0.9):
        payload = snapshots.build_snapshot_envelope(
            family,
            generated_at=datetime.now(timezone.utc).isoformat(),
            source_hashes={"unit": family},
            generator="unit-test",
            item_count=len(content) if isinstance(content, list) else 1,
            content=content,
            confidence=confidence,
        )
        path = snapshots.snapshot_path(root, family)
        path.write_text(json.dumps(payload), encoding="utf-8")

    def populate_snapshots(self, root: Path):
        self.write_snapshot(root, "prediction-summaries", [{
            "channel_forecasts": [
                {"channel": "awg0", "forecast_quality": 80, "confidence": 0.9},
                {"channel": "vless", "forecast_quality": 75, "confidence": 0.8},
            ],
            "service_forecasts": [],
        }])
        self.write_snapshot(root, "service-scores", [
            {"channel": "awg0", "score": 82, "confidence": 0.9},
        ])
        self.write_snapshot(root, "channel-service-scores", [])
        self.write_snapshot(root, "trust-evolution-summaries", [{
            "confidence_summary": {
                "decision_confidence": 50.0,
                "service_confidence": 40.0,
                "suitability_confidence": 30.0,
                "blast_radius_confidence": 100.0,
                "rollback_confidence": 100.0,
                "prediction_confidence": 40.0,
            },
            "prediction_accuracy": {
                "forecasts_seen": 2,
                "actuals_seen": 1,
                "matched_count": 1,
                "forecast_accuracy": 100.0,
                "prediction_confidence": 40.0,
                "rows": [
                    {"id": "awg0", "status": "MATCHED", "accuracy": 100.0, "confidence": 0.4},
                ],
            },
            "service_intelligence_trust": {
                "rows_seen": 1,
                "service_confidence": 40.0,
                "rows": [
                    {"id": "awg0", "correctness": 100.0, "confidence": 0.4},
                ],
            },
            "suitability_trust": {
                "candidates_seen": 2,
                "outcomes_seen": 1,
                "suitability_confidence": 30.0,
                "rows": [
                    {"key": "10.7.0.2:awg0", "outcome_seen": True, "correctness": 60.0, "confidence": 0.5},
                    {"key": "10.7.0.3:vless", "outcome_seen": False, "correctness": 40.0, "confidence": 0.25},
                ],
            },
            "rollback_intelligence": {"records_seen": 3},
            "blast_radius_confidence_model": {"records_seen": 2},
            "outcome_mapper_counts": {
                "service_actuals_count": 1,
                "candidate_outcomes_count": 1,
            },
        }])

    def decision_surface(self):
        return {
            "users": [
                {
                    "user": "10.7.0.2",
                    "current_channel": "vless",
                    "recommended_channel": "awg0",
                    "recommendation": "move_recommended",
                    "confidence": 0.46,
                    "trust": 3.15,
                    "risk": 0.1,
                    "prediction": {"confidence": 0.4},
                    "reasons": ["best available channel has higher advisory suitability"],
                },
                {
                    "user": "10.7.0.3",
                    "current_channel": "awg3",
                    "recommended_channel": "awg3",
                    "recommendation": "keep_current",
                    "confidence": 0.46,
                    "trust": 3.15,
                    "risk": 0.1,
                    "prediction": {"confidence": 0.4},
                    "reasons": ["current route remains stable"],
                },
            ]
        }

    def test_prediction_collection_plan_uses_existing_forecast_actual_model(self):
        plan = accel.build_prediction_collection_plan(
            prediction_snapshot={"items": [{
                "channel_forecasts": [
                    {"channel": "awg0", "forecast_quality": 80, "confidence": 0.9},
                    {"channel": "vless", "forecast_quality": 75, "confidence": 0.8},
                ]
            }]},
            service_scores_snapshot={"items": [{"channel": "awg0", "score": 82, "confidence": 0.9}]},
            channel_service_scores_snapshot={"items": []},
            decision_records=[],
        )

        self.assertEqual(plan["forecasts_seen"], 2)
        self.assertEqual(plan["forecast_actuals_seen"], 1)
        self.assertEqual(plan["matched_rows"], 1)
        self.assertEqual(plan["pending_rows"], 1)
        self.assertFalse(plan["synthetic_actuals_created"])
        self.assertFalse(plan["runtime_mutation_performed"])
        self.assertGreater(plan["best_possible_gain_if_all_pending_match"], 0)

    def test_operator_review_batches_are_real_review_only(self):
        model = shadow_autonomy.build_shadow_autonomy_model(self.decision_surface(), now="2026-06-23T00:00:00+00:00")
        batches = accel.build_operator_review_batches(model["operator_review_packet"], batch_sizes=[1, 2])

        self.assertEqual(batches["evidence_role"], "secondary_supervised_confirmation")
        self.assertEqual(batches["reviewable_decisions"], 2)
        self.assertTrue(batches["requires_real_operator_judgement"])
        self.assertTrue(batches["requires_operator_context"])
        self.assertFalse(batches["blind_review_required"])
        self.assertFalse(batches["bulk_training_data"])
        self.assertFalse(batches["synthetic_agreement_allowed"])
        self.assertEqual(batches["batches"][0]["items"][0]["recommendation"], "MOVE_USER")
        self.assertFalse(batches["batches"][1]["apply_executed"])
        self.assertEqual(batches["batches"][1]["users_moved"], 0)

    def test_trust_source_classification_marks_observed_outcomes_primary(self):
        classification = accel.build_trust_source_classification()

        primary = {row["source"]: row for row in classification["primary"]}
        secondary = {row["source"]: row for row in classification["secondary"]}
        diagnostic = {row["source"]: row for row in classification["diagnostic"]}

        self.assertEqual(primary["observed_service_outcome"]["autonomy_trust_use"], "primary")
        self.assertEqual(primary["observed_channel_quality"]["autonomy_trust_use"], "primary")
        self.assertEqual(primary["forecast_to_actual_accuracy"]["autonomy_trust_use"], "primary")
        self.assertEqual(secondary["operator_comparison"]["autonomy_trust_use"], "secondary_supervised_confirmation")
        self.assertFalse(secondary["operator_comparison"]["blind_review_required"])
        self.assertEqual(diagnostic["raw_technical_health"]["autonomy_trust_use"], "diagnostic_only")

    def test_operator_authority_is_not_fake_agreement(self):
        model = accel.build_operator_authority_model()

        self.assertTrue(model["manual_action_authoritative"])
        self.assertFalse(model["manual_action_is_fake_agreement"])
        self.assertTrue(model["outcome_observation_after_manual_action"])
        self.assertFalse(model["blind_bulk_review_required"])
        self.assertEqual(
            model["operator_comparison_role"],
            "secondary_supervised_confirmation_only_when_context_is_sufficient",
        )

    def test_acceleration_inventory_survives_reread_and_refresh_style_rebuild(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            base_model = shadow_autonomy.build_shadow_autonomy_model(self.decision_surface(), now="2026-06-23T00:00:00+00:00")
            comparison = shadow_autonomy.operator_comparison_record(
                base_model["current_decisions"][0],
                operator_decision="agree",
                category="trust",
                reason="real operator reviewed",
                now="2026-06-23T00:01:00+00:00",
            )
            raw = json.dumps(comparison, sort_keys=True)
            reread_history = [json.loads(raw)]
            first = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=reread_history,
                decision_records=[],
                generated_at="2026-06-23T00:02:00+00:00",
            )
            second = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[json.loads(json.dumps(comparison, sort_keys=True))],
                decision_records=[],
                generated_at="2026-06-23T00:03:00+00:00",
            )

        self.assertEqual(first["operator_comparisons"]["current"]["comparison_count"], 1)
        self.assertEqual(second["operator_comparisons"]["current"]["comparison_count"], 1)
        self.assertEqual(second["operator_comparisons"]["evidence_role"], "secondary_supervised_confirmation")
        self.assertFalse(second["operator_comparisons"]["blind_review_required"])
        self.assertEqual(
            second["canary_proximity"]["readiness_model"],
            "observed_outcome_primary_operator_comparison_secondary",
        )
        self.assertIn("trust", second["canary_proximity"]["missing"])
        self.assertNotIn("operator_earned_confidence", second["canary_proximity"]["missing"])
        self.assertIn("operator_earned_confidence", second["canary_proximity"]["secondary_missing"])
        self.assertFalse(second["collection_plan"]["blind_operator_training_required"])
        self.assertIn("primary_real_evidence_path", second["collection_plan"])
        self.assertIn("secondary_supervised_confirmation_path", second["collection_plan"])
        self.assertEqual(first["prediction_evidence"]["matched_rows"], second["prediction_evidence"]["matched_rows"])
        self.assertEqual(second["canary_proximity"]["floors"]["confidence"]["current"], 40.0)
        self.assertEqual(second["canary_proximity"]["floors"]["trust"]["current"], 55.0)
        self.assertEqual(second["floor_forensics"]["component_values"]["service_confidence"], 40.0)
        self.assertEqual(second["floor_forensics"]["prediction_root_cause"]["root_cause"], "low_forecast_source_confidence")
        self.assertEqual(second["floor_forensics"]["suitability_root_cause"]["rows_without_outcome"], 1)
        self.assertTrue(second["materialization_audit"]["prediction_actuals"]["materialized"])
        self.assertFalse(second["materialization_audit"]["prediction_actuals"]["safe_fix_available_now"])
        self.assertFalse(second["runtime_mutation_performed"])
        self.assertFalse(second["apply_executed"])
        self.assertEqual(second["users_moved"], 0)


if __name__ == "__main__":
    unittest.main()
