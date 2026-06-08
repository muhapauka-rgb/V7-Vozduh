import inspect
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from admin_core import intelligence_snapshots as snapshots
from admin_core import operator_decision_surface as surface


class OperatorDecisionSurfaceTest(unittest.TestCase):
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

    def test_user_recommendation_surface_is_snapshot_derived_and_preview_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_snapshot(root, "candidate-suitability-summary", [
                {
                    "user": "10.7.0.2",
                    "candidates": [
                        {"channel": "slow", "suitability_score": 40, "reason_breakdown": {"trust": 70, "risk": 5}},
                        {"channel": "fast", "suitability_score": 86, "reason_breakdown": {"trust": 82, "risk_penalty": 3}, "reasons": ["service fit"]},
                    ],
                }
            ])
            self.write_snapshot(root, "best-available-pool", [
                {
                    "user": "10.7.0.2",
                    "pool": [
                        {"channel": "fast", "suitability_score": 86, "reason_breakdown": {"trust": 82, "risk_penalty": 3}, "reasons": ["service fit"]},
                        {"channel": "slow", "suitability_score": 40, "reason_breakdown": {"trust": 70, "risk": 5}},
                    ],
                }
            ])
            self.write_snapshot(root, "prediction-summaries", [{"channel_forecasts": [{"channel": "fast", "confidence": 0.88, "summary": "stable"}]}])

            model = surface.build_operator_decision_surface(
                snapshot_root=root,
                users=[{"ip": "10.7.0.2", "current": "slow", "enabled": "1"}],
                egress=[{"id": "slow", "enabled": "1"}, {"id": "fast", "enabled": "1"}],
                runtime_state={"egress": {"fast": {"code": "200"}}},
            )

        row = model["users_by_ip"]["10.7.0.2"]
        self.assertEqual(row["recommended_channel"], "fast")
        self.assertEqual(row["recommendation"], "move_recommended")
        self.assertTrue(row["highlight"])
        self.assertFalse(model["execution_allowed_now"])
        self.assertFalse(model["authority"]["execution_path_changed"])
        self.assertIn("approval_packet", row["action_chain"])
        self.assertEqual(model["batch_preview"]["users_to_move"][0]["to"], "fast")

    def test_recommendation_fingerprint_changes_when_advice_changes(self):
        first = surface.recommendation_fingerprint("10.7.0.2", "slow", "fast", "aaa")
        second = surface.recommendation_fingerprint("10.7.0.2", "slow", "faster", "aaa")
        self.assertNotEqual(first, second)

    def test_missing_snapshots_are_conservative_but_non_mutating(self):
        with tempfile.TemporaryDirectory() as tmp:
            model = surface.build_operator_decision_surface(
                snapshot_root=Path(tmp),
                users=[{"ip": "10.7.0.2", "current": "slow", "enabled": "1"}],
                egress=[{"id": "slow", "enabled": "1"}],
                runtime_state={},
            )

        row = model["users_by_ip"]["10.7.0.2"]
        self.assertEqual(row["recommendation"], "keep")
        self.assertIn("best_candidate_missing", row["blockers"])
        self.assertFalse(row["runtime_mutation_performed"])
        self.assertFalse(model["authority"]["new_truth_sources_created"])

    def test_channel_state_api_uses_trust_recovery_snapshot_with_human_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_snapshot(root, "trust-evolution-summaries", [{
                "channel_trust_recovery": {
                    "channels": [{
                        "channel": "awg3",
                        "lifecycle": "WATCH",
                        "lifecycle_reason": "current_services_look_healthy_but_success_history_is_thin",
                        "trust_score": 74,
                        "current_service_score": 88,
                        "feedback": {
                            "successes": 0,
                            "failures": 0,
                            "rollback_successes": 0,
                            "rollback_failures": 0,
                        },
                        "recovery": {"state": "NOT_NEEDED"},
                    }]
                }
            }])

            model = surface.build_operator_decision_surface(
                snapshot_root=root,
                users=[],
                egress=[{"id": "awg3", "enabled": "1"}],
                runtime_state={"egress": {"awg3": {"code": "200"}}},
            )

        row = model["channels_by_id"]["awg3"]
        self.assertEqual(row["channel_state"], "WATCH")
        self.assertEqual(row["channel_state_label"], "WATCH")
        self.assertIn("works now", row["channel_state_explanation"])
        self.assertIn("24-72 hours", row["channel_state_next_step"])
        self.assertEqual(row["channel_state_policy"]["maximum_practical_trust_window_days"], 7)
        self.assertEqual(row["channel_state_source"], "trust-evolution-summaries.channel_trust_recovery")
        self.assertEqual(row["state"], "WATCH")

    def test_admin_channel_state_surface_is_existing_column_and_click_drawer(self):
        source = Path(__file__).resolve().parents[2] / "admin" / "v7-admin-api"
        text = source.read_text(encoding="utf-8")
        self.assertIn("{id:'channel_state', label:'Состояние доверия'", text)
        self.assertIn("function channelStateCell", text)
        self.assertIn("openChannelStateDrawer", text)
        self.assertIn("channel_state_explanation", text)
        self.assertIn("channel_state_next_step", text)

    def test_module_exposes_no_execution_or_write_api(self):
        source = inspect.getsource(surface)
        forbidden = ("subprocess", "run_action", "write_json_atomic", "write_text_atomic", "append_jsonl", "audit_admin")
        for name in forbidden:
            self.assertNotIn(name, source)


if __name__ == "__main__":
    unittest.main()
