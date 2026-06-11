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
            self.write_snapshot(root, "trust-evolution-summaries", [{
                "channel_trust_recovery": {
                    "channels": [{
                        "channel": "fast",
                        "lifecycle": "NEW",
                        "lifecycle_reason": "insufficient_live_feedback",
                        "trust_score": 62,
                        "current_service_score": 86,
                        "feedback": {
                            "successes": 0,
                            "failures": 0,
                            "rollback_successes": 0,
                            "rollback_failures": 0,
                        },
                        "recovery": {"state": "NOT_NEEDED", "operator_review_required": False},
                    }]
                }
            }])

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
        ctr = row["ctr_governance_evidence"]
        self.assertEqual(ctr["state"], "NEW")
        self.assertTrue(ctr["review_required"])
        self.assertEqual(ctr["review_category"], "new_channel_review")
        self.assertEqual(ctr["review_severity"], "medium")
        self.assertFalse(ctr["emergency_only"])
        self.assertEqual(ctr["approval_authority"], "none")
        self.assertEqual(ctr["denial_authority"], "none")
        self.assertIn("ctr_state_requires_operator_review", row["review_required_reasons"])
        self.assertEqual(model["batch_preview"]["users_to_move"][0]["ctr_governance_evidence"]["state"], "NEW")
        self.assertEqual(model["batch_preview"]["ctr_review_summary"]["review_required_count"], 1)

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

    def test_snapshot_status_contract_includes_autonomy_gate_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_snapshot(root, "service-scores", [{"service": "telegram", "confidence": 0.9}])

            model = surface.build_operator_decision_surface(
                snapshot_root=root,
                users=[],
                egress=[],
                runtime_state={},
            )

        status = model["snapshot_statuses"]["service-scores"]
        self.assertEqual(status["status"], "OK")
        self.assertTrue(status["validation_ok"])
        self.assertEqual(status["freshness_state"], "FRESH")
        self.assertEqual(status["runtime_behavior"], "ALLOW")
        self.assertFalse(status["stop_required"])
        self.assertEqual(status["errors"], [])
        self.assertEqual(status["validation_errors"], [])
        self.assertIn("source_hashes", status)

    def test_trust_evolution_advice_exposes_outcome_evidence_without_authority(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_snapshot(root, "trust-evolution-summaries", [{
                "overall_confidence": 84,
                "confidence_summary": {
                    "decision_confidence": 88,
                    "prediction_confidence": 86,
                    "service_confidence": 82,
                    "suitability_confidence": 79,
                    "rollback_confidence": 91,
                    "blast_radius_confidence": 85,
                    "live_calibrated": True,
                },
                "outcome_mapper_counts": {
                    "candidate_outcomes_count": 8,
                    "prediction_actuals_count": 8,
                    "service_actuals_count": 8,
                },
                "autonomy_readiness": {"current_level": "OPERATOR_APPROVAL_READY"},
                "governed_to_autonomy_trust_bridge": {
                    "governed_execution_evidence_score": 100,
                    "inherited_execution_trust": 82,
                    "autonomy_specific_gap_score": 45,
                    "autonomy_boundary_cap": "OPERATOR_APPROVAL_READY",
                    "approval_autonomy_review_ready": True,
                    "bounded_autonomy_blockers": ["autonomous_trigger_not_certified"],
                    "operator_summary_ru": "Governed-история учитывается, автономия отдельно заблокирована.",
                    "execution_authority": "none",
                    "autonomy_enabled": False,
                },
                "rollback_intelligence": {"validation_status": "VALIDATED"},
            }])

            model = surface.build_operator_decision_surface(
                snapshot_root=root,
                users=[],
                egress=[],
                runtime_state={},
            )

        advice = model["trust_evolution_advice"]
        self.assertTrue(advice["available"])
        self.assertTrue(advice["live_calibrated"])
        self.assertEqual(advice["decision_confidence"], 88)
        self.assertEqual(advice["candidate_outcomes_count"], 8)
        self.assertEqual(advice["governed_evidence_score"], 100)
        self.assertEqual(advice["inherited_execution_trust"], 82)
        self.assertEqual(advice["autonomy_specific_gap_score"], 45)
        self.assertTrue(advice["approval_autonomy_review_ready"])
        self.assertIn("autonomous_trigger_not_certified", advice["bounded_autonomy_blockers"])
        self.assertEqual(advice["execution_authority"], "none")
        self.assertFalse(advice["autonomy_enabled"])
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
        self.assertIn("рабочим", row["channel_state_explanation"])
        self.assertIn("24-72 часа", row["channel_state_next_step"])
        self.assertIn("TRUSTED", row["channel_state_recovery_path"])
        self.assertIn("review", row["channel_state_blocked_action_summary"])
        self.assertEqual(row["channel_state_policy"]["maximum_practical_trust_window_days"], 7)
        self.assertEqual(row["channel_state_source"], "trust-evolution-summaries.channel_trust_recovery")
        self.assertEqual(row["state"], "WATCH")

    def test_ctr_visibility_copy_is_short_russian_and_complete_for_all_states(self):
        required = {
            "reason",
            "explanation",
            "next_step",
            "safe_now",
            "recovery_path",
            "blocked_action_summary",
        }
        for state, copy in surface.CHANNEL_STATE_COPY.items():
            with self.subTest(state=state):
                self.assertEqual(set(copy), required)
                for value in copy.values():
                    self.assertIsInstance(value, str)
                    self.assertLessEqual(len(value), 180)
                self.assertRegex(copy["reason"], r"[А-Яа-яЁё]")
                self.assertRegex(copy["next_step"], r"[А-Яа-яЁё]")
                self.assertRegex(copy["recovery_path"], r"[А-Яа-яЁё]")
                self.assertRegex(copy["blocked_action_summary"], r"[А-Яа-яЁё]")

    def test_ctr_review_matrix_matches_governance_contract(self):
        expected = {
            "TRUSTED": (False, "normal", "info", False),
            "WATCH": (True, "expansion_review", "low", False),
            "NEW": (True, "new_channel_review", "medium", False),
            "RECOVERING": (True, "recovery_review", "medium", False),
            "DEGRADED": (True, "degraded_channel_review", "high", False),
            "QUARANTINED": (True, "emergency_only_review", "critical", True),
        }
        for state, (required, category, severity, emergency_only) in expected.items():
            with self.subTest(state=state):
                row = surface.ctr_review_semantics(state)
                self.assertEqual(row["review_required"], required)
                self.assertEqual(row["review_category"], category)
                self.assertEqual(row["review_severity"], severity)
                self.assertEqual(row["emergency_only"], emergency_only)
                self.assertRegex(row["review_reason"], r"[А-Яа-яЁё]")
                self.assertRegex(row["review_recommendation"], r"[А-Яа-яЁё]")
                self.assertRegex(row["review_warning"], r"[А-Яа-яЁё]")

    def test_admin_channel_state_surface_is_existing_column_and_click_drawer(self):
        source = Path(__file__).resolve().parents[2] / "admin" / "v7-admin-api"
        text = source.read_text(encoding="utf-8")
        self.assertIn("{id:'channel_state', label:'Состояние доверия'", text)
        self.assertIn("function channelStateCell", text)
        self.assertIn("openChannelStateDrawer", text)
        self.assertIn("channel_state_explanation", text)
        self.assertIn("channel_state_next_step", text)
        self.assertIn("channel_state_recovery_path", text)
        self.assertIn("channel_state_blocked_action_summary", text)
        self.assertIn("'Путь восстановления'", text)
        self.assertIn("'Заблокировано'", text)
        self.assertIn("'CTR review'", text)
        self.assertIn("'Причина review'", text)
        self.assertIn("'Emergency only'", text)
        self.assertIn("review_required_reasons", text)

    def test_module_exposes_no_execution_or_write_api(self):
        source = inspect.getsource(surface)
        forbidden = ("subprocess", "run_action", "write_json_atomic", "write_text_atomic", "append_jsonl", "audit_admin")
        for name in forbidden:
            self.assertNotIn(name, source)

    def test_ctr_surface_cannot_bypass_runtime_governance_or_ownership(self):
        source = inspect.getsource(surface)
        forbidden = (
            "approve_packet",
            "write_restore_barrier",
            "restore_barrier_written_now",
            "selected_moves.append",
            "selected_moves =",
            "--apply",
            "autoswitch_apply_run",
            "promote_authority",
            "capacity_decision",
            "batch_owner",
        )
        for name in forbidden:
            self.assertNotIn(name, source)

        model = surface.build_operator_decision_surface(
            snapshot_root=Path("/tmp/does-not-exist"),
            users=[],
            egress=[],
            runtime_state={},
        )

        self.assertFalse(model["execution_allowed_now"])
        self.assertFalse(model["authority"]["planner_authority_changed"])
        self.assertFalse(model["authority"]["governance_changed"])
        self.assertFalse(model["authority"]["execution_path_changed"])
        self.assertFalse(model["authority"]["rollback_path_changed"])
        self.assertFalse(model["authority"]["new_truth_sources_created"])
        self.assertFalse(model["authority"]["duplicate_systems_created"])


if __name__ == "__main__":
    unittest.main()
