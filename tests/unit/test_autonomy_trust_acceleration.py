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
                "confidence_score": 45.0,
                "trust_score": 55.0,
                "prediction_confidence": 40.0,
            }
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

        self.assertEqual(batches["reviewable_decisions"], 2)
        self.assertTrue(batches["requires_real_operator_judgement"])
        self.assertFalse(batches["synthetic_agreement_allowed"])
        self.assertEqual(batches["batches"][0]["items"][0]["recommendation"], "MOVE_USER")
        self.assertFalse(batches["batches"][1]["apply_executed"])
        self.assertEqual(batches["batches"][1]["users_moved"], 0)

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
        self.assertEqual(first["prediction_evidence"]["matched_rows"], second["prediction_evidence"]["matched_rows"])
        self.assertFalse(second["runtime_mutation_performed"])
        self.assertFalse(second["apply_executed"])
        self.assertEqual(second["users_moved"], 0)


if __name__ == "__main__":
    unittest.main()
