import importlib.util
from importlib.machinery import SourceFileLoader
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from admin_core import intelligence_workers as workers
from admin_core.intelligence_snapshots import read_snapshot_family, validate_snapshot


GENERATED = "2026-06-03T10:00:00+00:00"


def service_matrix():
    return {
        "updated": GENERATED,
        "items": {
            "awg0": {
                "services": {
                    "telegram": {"ok": True, "status": "OK", "first_byte_sec": 0.2, "confidence": 0.9, "score": 90, "sample_count": 4},
                    "chatgpt": {"ok": True, "status": "OK", "first_byte_sec": 0.4, "confidence": 0.8, "score": 80, "sample_count": 4},
                }
            },
            "vless": {
                "services": {
                    "telegram": {"ok": False, "status": "FAIL", "first_byte_sec": 3.0, "confidence": 0.4, "score": 20, "sample_count": 4},
                    "chatgpt": {"ok": True, "status": "OK", "first_byte_sec": 0.5, "confidence": 0.8, "score": 82, "sample_count": 4},
                }
            },
        },
    }


def quality_summary():
    return {
        "updated": GENERATED,
        "items": {
            "awg0": {"windows": {"1h": {"avg_mbps": 100, "fail_rate": 0.01, "stability": 0.95, "samples": 20}}},
            "vless": {"windows": {"1h": {"avg_mbps": 50, "fail_rate": 0.2, "stability": 0.65, "samples": 20}}},
        },
    }


class IntelligenceWorkersTest(unittest.TestCase):
    def test_service_score_worker_outputs_valid_service_and_channel_snapshots(self):
        result = workers.build_service_score_snapshots(
            service_matrix=service_matrix(),
            quality_summary=quality_summary(),
            service_preferences={"required_services": ["telegram", "chatgpt"]},
            generated_at=GENERATED,
        )
        self.assertIn("service-scores", result)
        self.assertIn("channel-service-scores", result)
        for name, payload in result.items():
            validation = validate_snapshot(payload, name)
            self.assertTrue(validation.ok, validation.errors)
            self.assertEqual(payload["generator"], workers.GENERATOR)
            self.assertGreater(payload["item_count"], 0)
        channel_items = result["channel-service-scores"]["items"]
        awg0 = next(row for row in channel_items if row["channel"] == "awg0")
        vless = next(row for row in channel_items if row["channel"] == "vless")
        self.assertGreater(awg0["aggregate_score"], vless["aggregate_score"])

    def test_ri4_cd_service_scores_include_framework_and_calibration(self):
        result = workers.build_service_score_snapshots(
            service_matrix=service_matrix(),
            quality_summary=quality_summary(),
            service_preferences={"required_services": ["telegram", "chatgpt"]},
            generated_at=GENERATED,
        )
        metadata = result["service-scores"]["metadata"]
        self.assertEqual(metadata["framework"]["schema_version"], "ri4cd.service-quality-framework.v1")
        calibration = metadata["calibration"]
        self.assertEqual(calibration["schema"], "ri4cd.service-calibration.v1")
        self.assertEqual(metadata["model_governance"]["model_version"], "v7.intelligence-platform.model.v1")
        self.assertEqual(metadata["explainability"]["schema_version"], "v7.intelligence.explainability-framework.v1")
        self.assertIn(calibration["channel_distribution"]["calibration_state"], {"OK", "LOW_SPREAD", "HIGH_SCORE_COMPRESSION", "LOW_SCORE_COMPRESSION"})
        telegram = next(row for row in result["service-scores"]["items"] if row["service"] == "telegram")
        self.assertIn("score_distribution", telegram)
        self.assertIn("trend_summary", telegram)

    def test_trust_worker_is_bounded_and_valid(self):
        records = [{"result": "success", "blast_radius": 1} for _ in range(workers.MAX_HISTORY_RECORDS + 20)]
        records.append({"result": "failed", "rollback_failed": True})
        payload = workers.build_trust_snapshot(audit_records=records, generated_at=GENERATED)
        validation = validate_snapshot(payload, "trust-summaries")
        self.assertTrue(validation.ok, validation.errors)
        item = payload["items"][0]
        self.assertTrue(item["bounded"])
        self.assertEqual(item["records_seen"], workers.MAX_HISTORY_RECORDS)
        self.assertIn("history_records_truncated_to_bound", payload["warnings"])

    def test_risk_worker_uses_service_snapshots(self):
        service = workers.build_service_score_snapshots(
            service_matrix=service_matrix(),
            quality_summary=quality_summary(),
            service_preferences={"required_services": ["telegram", "chatgpt"]},
            generated_at=GENERATED,
        )
        risk = workers.build_risk_snapshot(
            service_scores_snapshot=service["service-scores"],
            channel_service_scores_snapshot=service["channel-service-scores"],
            quality_summary=quality_summary(),
            generated_at=GENERATED,
        )
        self.assertTrue(validate_snapshot(risk, "risk-summaries").ok)
        summary = risk["items"][0]
        self.assertGreater(summary["service_risk"], 0)
        self.assertIn("vless", summary["high_risk_channels"])

    def test_blast_radius_worker_reuses_trust_and_risk_models(self):
        trust = workers.build_trust_snapshot(audit_records=[{"result": "success"}] * 20, generated_at=GENERATED)
        risk = workers.build_risk_snapshot(
            service_scores_snapshot={"items": [{"average_score": 90}], "confidence": 1.0},
            channel_service_scores_snapshot={"items": [{"channel": "awg0", "aggregate_score": 90, "verdict": "OK"}], "confidence": 1.0},
            quality_summary=quality_summary(),
            generated_at=GENERATED,
        )
        blast = workers.build_blast_radius_snapshot(
            trust_summary_snapshot=trust,
            risk_summary_snapshot=risk,
            total_users=2000,
            affected_candidates=50,
            generated_at=GENERATED,
        )
        self.assertTrue(validate_snapshot(blast, "blast-radius-summaries").ok)
        rec = blast["items"][0]["recommendation"]
        self.assertLessEqual(rec["recommended_budget"], 25)
        self.assertEqual(rec["runtime_decision_authority"], "none_shadow_only")

    def test_overview_worker_outputs_admin_only_summary(self):
        overview = workers.build_overview_snapshot(
            runtime_state={"egress": {"awg0": {"code": "200"}}},
            users_registry=[{"ip": "10.7.0.2", "enabled": "1"}, {"ip": "10.7.0.3", "enabled": "0"}],
            egress_registry=[{"id": "awg0"}],
            snapshot_statuses={"service-scores": {"freshness_state": "FRESH", "runtime_behavior": "ALLOW"}},
            generated_at=GENERATED,
        )
        self.assertTrue(validate_snapshot(overview, "overview-summary").ok)
        self.assertEqual(overview["summary"]["users_total"], 2)
        self.assertEqual(overview["summary"]["users_active"], 1)
        self.assertEqual(overview["summary"]["snapshot_families_fresh"], 1)

    def test_user_service_scores_are_user_specific_snapshot(self):
        payload = workers.build_user_service_scores_snapshot(
            service_matrix=service_matrix(),
            quality_summary=quality_summary(),
            service_preferences={
                "required_services": ["telegram", "chatgpt"],
                "users": {"10.7.0.2": {"weights": {"telegram": 90, "chatgpt": 10}}},
            },
            users_registry=[{"ip": "10.7.0.2", "enabled": "1"}],
            generated_at=GENERATED,
        )
        self.assertTrue(validate_snapshot(payload, "user-service-scores").ok)
        row = payload["items"][0]
        self.assertEqual(row["user"], "10.7.0.2")
        services = {item["service"]: item for item in row["services"]}
        self.assertGreater(services["telegram"]["weight"], services["chatgpt"]["weight"])
        self.assertEqual(row["runtime_decision_authority"], "none_snapshot_only")

    def test_ri4_cd_user_service_scores_include_history_risk_trust_influence(self):
        trust = workers.build_trust_snapshot(audit_records=[{"result": "success"}] * 20, generated_at=GENERATED)
        service = workers.build_service_score_snapshots(
            service_matrix=service_matrix(),
            quality_summary=quality_summary(),
            service_preferences={"required_services": ["telegram", "chatgpt"]},
            generated_at=GENERATED,
        )
        risk = workers.build_risk_snapshot(
            service_scores_snapshot=service["service-scores"],
            channel_service_scores_snapshot=service["channel-service-scores"],
            quality_summary=quality_summary(),
            generated_at=GENERATED,
        )
        payload = workers.build_user_service_scores_snapshot(
            service_matrix=service_matrix(),
            quality_summary=quality_summary(),
            service_preferences={
                "required_services": ["telegram", "chatgpt"],
                "users": {"10.7.0.2": {"weights": {"telegram": 90, "chatgpt": 10}}},
            },
            users_registry=[{"ip": "10.7.0.2", "enabled": "1"}],
            trust_summary_snapshot=trust,
            risk_summary_snapshot=risk,
            generated_at=GENERATED,
        )
        row = payload["items"][0]
        telegram = next(item for item in row["services"] if item["service"] == "telegram")
        for key in (
            "importance_influence",
            "required_service_influence",
            "history_influence",
            "risk_influence",
            "trust_influence",
            "service_suitability_influence",
        ):
            self.assertIn(key, telegram)
        self.assertEqual(telegram["runtime_decision_authority"], "none_snapshot_only")

    def test_candidate_suitability_and_best_pool_snapshots_are_advisory_only(self):
        trust = workers.build_trust_snapshot(audit_records=[{"result": "success", "blast_radius": 1}] * 20, generated_at=GENERATED)
        service = workers.build_service_score_snapshots(
            service_matrix=service_matrix(),
            quality_summary=quality_summary(),
            service_preferences={"required_services": ["telegram", "chatgpt"]},
            generated_at=GENERATED,
        )
        risk = workers.build_risk_snapshot(
            service_scores_snapshot=service["service-scores"],
            channel_service_scores_snapshot=service["channel-service-scores"],
            quality_summary=quality_summary(),
            generated_at=GENERATED,
        )
        blast = workers.build_blast_radius_snapshot(
            trust_summary_snapshot=trust,
            risk_summary_snapshot=risk,
            total_users=1,
            affected_candidates=2,
            generated_at=GENERATED,
        )
        suitability = workers.build_candidate_suitability_snapshot(
            service_matrix=service_matrix(),
            quality_summary=quality_summary(),
            service_preferences={
                "required_services": ["telegram", "chatgpt"],
                "users": {"10.7.0.2": {"weights": {"telegram": 90, "chatgpt": 10}}},
            },
            users_registry=[{"ip": "10.7.0.2", "enabled": "1"}],
            egress_registry=[{"id": "awg0", "enabled": "1"}, {"id": "vless", "enabled": "1"}],
            trust_summary_snapshot=trust,
            risk_summary_snapshot=risk,
            blast_radius_snapshot=blast,
            generated_at=GENERATED,
        )
        self.assertTrue(validate_snapshot(suitability, "candidate-suitability-summary").ok)
        user_row = suitability["items"][0]
        candidates = {item["channel"]: item for item in user_row["candidates"]}
        self.assertGreater(candidates["awg0"]["suitability_score"], candidates["vless"]["suitability_score"])
        self.assertIn("reason_breakdown", candidates["awg0"])
        self.assertEqual(candidates["awg0"]["authority"]["runtime_execution_authority"], "none")

        pool = workers.build_best_available_pool_snapshot(
            candidate_suitability_snapshot=suitability,
            runtime_state={"egress": {"awg0": {"users": 1}, "vless": {"users": 1}}},
            egress_registry=[{"id": "awg0", "enabled": "1"}, {"id": "vless", "enabled": "1"}],
            generated_at=GENERATED,
        )
        self.assertTrue(validate_snapshot(pool, "best-available-pool").ok)
        self.assertEqual(pool["items"][0]["single_best_channel_authority"], "none")
        self.assertGreaterEqual(pool["items"][0]["pool_size"], 1)

    def test_ri5_prediction_snapshot_forecasts_are_advisory_only(self):
        trust = workers.build_trust_snapshot(audit_records=[{"result": "success", "blast_radius": 1}] * 20, generated_at=GENERATED)
        service = workers.build_service_score_snapshots(
            service_matrix=service_matrix(),
            quality_summary=quality_summary(),
            service_preferences={"required_services": ["telegram", "chatgpt"]},
            generated_at=GENERATED,
        )
        risk = workers.build_risk_snapshot(
            service_scores_snapshot=service["service-scores"],
            channel_service_scores_snapshot=service["channel-service-scores"],
            quality_summary=quality_summary(),
            generated_at=GENERATED,
        )
        blast = workers.build_blast_radius_snapshot(
            trust_summary_snapshot=trust,
            risk_summary_snapshot=risk,
            total_users=1,
            affected_candidates=2,
            generated_at=GENERATED,
        )
        payload = workers.build_prediction_snapshot(
            service_matrix=service_matrix(),
            quality_summary=quality_summary(),
            risk_summary_snapshot=risk,
            trust_summary_snapshot=trust,
            blast_radius_snapshot=blast,
            generated_at=GENERATED,
        )
        self.assertTrue(validate_snapshot(payload, "prediction-summaries").ok)
        summary = payload["items"][0]
        self.assertTrue(summary["prediction_enabled"])
        self.assertGreater(len(summary["channel_forecasts"]), 0)
        self.assertGreater(len(summary["service_forecasts"]), 0)
        self.assertEqual(summary["execution_authority"], "none")
        self.assertEqual(payload["metadata"]["model_governance"]["weights_version"], "v7.intelligence-platform.weights.v1")
        self.assertEqual(payload["metadata"]["observability"]["schema_version"], "v7.intelligence.observability-model.v1")
        self.assertFalse(payload["metadata"]["runtime_forecasting_performed"])

    def test_ri6_trust_evolution_snapshot_is_advisory_only(self):
        trust = workers.build_trust_snapshot(
            audit_records=[{"result": "success", "service_delta": 10, "prediction_delta": 5, "blast_radius": 1}] * 20,
            rollback_records=[{"result": "rollback_success", "rollback_completed": True}],
            generated_at=GENERATED,
        )
        service = workers.build_service_score_snapshots(
            service_matrix=service_matrix(),
            quality_summary=quality_summary(),
            service_preferences={"required_services": ["telegram", "chatgpt"]},
            generated_at=GENERATED,
        )
        risk = workers.build_risk_snapshot(
            service_scores_snapshot=service["service-scores"],
            channel_service_scores_snapshot=service["channel-service-scores"],
            quality_summary=quality_summary(),
            generated_at=GENERATED,
        )
        blast = workers.build_blast_radius_snapshot(
            trust_summary_snapshot=trust,
            risk_summary_snapshot=risk,
            total_users=1,
            affected_candidates=1,
            generated_at=GENERATED,
        )
        suitability = workers.build_candidate_suitability_snapshot(
            service_matrix=service_matrix(),
            quality_summary=quality_summary(),
            service_preferences={"required_services": ["telegram", "chatgpt"]},
            users_registry=[{"ip": "10.7.0.2", "enabled": "1"}],
            egress_registry=[{"id": "awg0", "enabled": "1"}, {"id": "vless", "enabled": "1"}],
            trust_summary_snapshot=trust,
            risk_summary_snapshot=risk,
            blast_radius_snapshot=blast,
            generated_at=GENERATED,
        )
        pool = workers.build_best_available_pool_snapshot(
            candidate_suitability_snapshot=suitability,
            runtime_state={"egress": {"awg0": {"users": 1}, "vless": {"users": 1}}},
            egress_registry=[{"id": "awg0", "enabled": "1"}, {"id": "vless", "enabled": "1"}],
            generated_at=GENERATED,
        )
        prediction = workers.build_prediction_snapshot(
            service_matrix=service_matrix(),
            quality_summary=quality_summary(),
            risk_summary_snapshot=risk,
            trust_summary_snapshot=trust,
            blast_radius_snapshot=blast,
            generated_at=GENERATED,
        )
        payload = workers.build_trust_evolution_snapshot(
            audit_records=[{"result": "success", "service_delta": 10, "prediction_delta": 5, "blast_radius": 1}],
            rollback_records=[{"result": "rollback_success", "rollback_completed": True}],
            service_scores_snapshot=service["service-scores"],
            channel_service_scores_snapshot=service["channel-service-scores"],
            trust_summary_snapshot=trust,
            prediction_summary_snapshot=prediction,
            candidate_suitability_snapshot=suitability,
            best_available_pool_snapshot=pool,
            blast_radius_snapshot=blast,
            generated_at=GENERATED,
        )
        self.assertTrue(validate_snapshot(payload, "trust-evolution-summaries").ok)
        summary = payload["items"][0]
        self.assertEqual(summary["execution_authority"], "none")
        self.assertEqual(summary["runtime_decision_authority"], "none_evidence_only")
        self.assertNotIn("prediction_actual_outcomes_missing", payload["warnings"])
        self.assertEqual(summary["prediction_accuracy"]["validation_status"], "VALIDATED")
        self.assertGreater(summary["outcome_mapper_counts"]["prediction_actuals_count"], 0)
        self.assertGreater(summary["outcome_mapper_counts"]["service_actuals_count"], 0)
        self.assertIn("decision_outcome_learning", summary)
        self.assertGreaterEqual(summary["outcome_mapper_counts"]["learning_records_count"], 1)
        self.assertEqual(summary["decision_outcome_learning"]["schema_version"], "v7.decision-outcome-learning.model.v1")
        self.assertGreater(summary["decision_outcome_learning"]["effectiveness"]["recommendation_correct_rate"], 0)
        self.assertFalse(summary["autonomy_readiness"]["autonomy_enabled"])

    def test_candidate_outcomes_from_selected_move_audit(self):
        candidates = [{
            "user": "10.7.0.2",
            "candidates": [{"channel": "awg0", "suitability_score": 90, "confidence": 0.9}],
        }]
        outcomes = workers.build_candidate_outcome_rows(candidates, [{
            "result": "OK",
            "terminal_state": "APPLIED",
            "selected_moves": [{"user": "10.7.0.2", "target": "awg0"}],
            "timestamp": GENERATED,
        }])
        self.assertEqual(len(outcomes), 1)
        self.assertEqual(outcomes[0]["user"], "10.7.0.2")
        self.assertEqual(outcomes[0]["channel"], "awg0")
        self.assertTrue(outcomes[0]["success"])
        self.assertEqual(outcomes[0]["outcome_status"], "success")

    def test_trust_evolution_candidate_outcomes_survive_bounded_decision_window(self):
        service = workers.build_service_score_snapshots(
            service_matrix=service_matrix(),
            quality_summary=quality_summary(),
            service_preferences={"required_services": ["telegram", "chatgpt"]},
            generated_at=GENERATED,
        )
        candidate_snapshot = {
            "items": [{
                "user": "10.7.0.2",
                "candidates": [{"channel": "awg0", "suitability_score": 90, "confidence": 0.9}],
            }],
            "confidence": 0.9,
        }
        old_real_outcome = {
            "result": "success",
            "terminal_state": "APPLIED",
            "selected_moves": [{"user": "10.7.0.2", "target": "awg0"}],
            "timestamp": GENERATED,
        }
        noise = [{"message": f"bounded noise {index}", "timestamp": GENERATED} for index in range(workers.MAX_HISTORY_RECORDS + 5)]

        payload = workers.build_trust_evolution_snapshot(
            audit_records=[old_real_outcome] + noise,
            switch_records=[],
            rollback_records=[],
            service_scores_snapshot=service["service-scores"],
            channel_service_scores_snapshot=service["channel-service-scores"],
            trust_summary_snapshot={"items": [], "confidence": 0.9},
            prediction_summary_snapshot={"items": [{"channel_forecasts": [], "service_forecasts": []}], "confidence": 0.9},
            candidate_suitability_snapshot=candidate_snapshot,
            best_available_pool_snapshot={"items": [], "confidence": 0.9},
            blast_radius_snapshot={"items": [], "confidence": 0.9},
            generated_at=GENERATED,
        )

        self.assertTrue(validate_snapshot(payload, "trust-evolution-summaries").ok)
        summary = payload["items"][0]
        self.assertEqual(summary["outcome_mapper_counts"]["bounded_decision_count"], workers.MAX_HISTORY_RECORDS)
        self.assertEqual(summary["outcome_mapper_counts"]["candidate_outcomes_count"], 1)
        self.assertEqual(summary["suitability_trust"]["outcomes_seen"], 1)
        self.assertTrue(summary["suitability_trust"]["rows"][0]["outcome_seen"])

    def test_candidate_outcomes_from_switch_history_to_field(self):
        candidates = [{
            "user": "10.7.0.2",
            "candidates": [{"channel": "awg0", "suitability_score": 90, "confidence": 0.9}],
        }]
        outcomes = workers.build_candidate_outcome_rows(candidates, [{
            "user_ip": "10.7.0.2",
            "from": "vless",
            "to": "awg0",
            "reason": "switch completed",
            "ts": GENERATED,
        }])
        self.assertEqual(len(outcomes), 1)
        self.assertEqual(outcomes[0]["user"], "10.7.0.2")
        self.assertEqual(outcomes[0]["channel"], "awg0")
        self.assertEqual(outcomes[0]["outcome_status"], "success")
        self.assertEqual(outcomes[0]["evidence_source"], "switch_history_channel_arrival")
        self.assertEqual(outcomes[0]["event_time"], GENERATED)

    def test_candidate_outcomes_from_execution_feedback(self):
        candidates = [{
            "user": "10.0.0.3",
            "candidates": [{"channel": "vless", "suitability_score": 80, "confidence": 0.8}],
        }]
        outcomes = workers.build_candidate_outcome_rows(candidates, [{
            "schema_version": "v7.execution-outcome-record.v1",
            "user": "10.0.0.3",
            "source_channel": "awg3",
            "target_channel": "vless",
            "outcome_status": "success",
            "execution_outcome": {"success": True, "result": "applied", "selected_move_count": 2},
            "verification_result": {"verification_passed": True},
            "rollback_result": {"rollback_required": False},
            "created_at": GENERATED,
        }])

        self.assertEqual(len(outcomes), 1)
        self.assertEqual(outcomes[0]["channel"], "vless")
        self.assertTrue(outcomes[0]["success"])
        self.assertEqual(outcomes[0]["outcome_status"], "success")

    def test_blast_radius_evidence_groups_execution_feedback_by_operation(self):
        records = [
            {
                "schema_version": "v7.execution-outcome-record.v1",
                "audit_reference": "runtime_autoswitch_small",
                "user": "10.0.0.3",
                "target_channel": "vless",
                "outcome_status": "success",
                "execution_outcome": {"success": True, "result": "applied"},
                "verification_result": {"verification_passed": True},
                "rollback_result": {"rollback_required": False},
            },
            {
                "schema_version": "v7.execution-outcome-record.v1",
                "audit_reference": "runtime_autoswitch_small",
                "user": "10.0.0.6",
                "target_channel": "vless",
                "outcome_status": "success",
                "execution_outcome": {"success": True, "result": "applied"},
                "verification_result": {"verification_passed": True},
                "rollback_result": {"rollback_required": False},
            },
        ]
        blast_rows = workers.build_blast_radius_evidence_rows(records)

        self.assertEqual(len(blast_rows), 1)
        self.assertEqual(blast_rows[0]["blast_radius"], 2)
        self.assertTrue(blast_rows[0]["success"])

    def test_candidate_outcomes_ignore_unknown_selected_move_audit(self):
        candidates = [{
            "user": "10.7.0.2",
            "candidates": [{"channel": "awg0", "suitability_score": 90, "confidence": 0.9}],
        }]
        outcomes = workers.build_candidate_outcome_rows(candidates, [{
            "selected_moves": [{"user": "10.7.0.2", "target": "awg0"}],
            "timestamp": GENERATED,
        }])
        self.assertEqual(outcomes, [])

    def test_candidate_outcomes_ignore_rollback_only_switch_history(self):
        candidates = [{
            "user": "10.7.0.2",
            "candidates": [{"channel": "awg3", "suitability_score": 90, "confidence": 0.9}],
        }]
        outcomes = workers.build_candidate_outcome_rows(candidates, [{
            "user_ip": "10.7.0.2",
            "from": "vless",
            "to": "awg3",
            "reason": "autoswitch_rollback",
            "ts": GENERATED,
        }])
        rollback_rows = workers.build_rollback_evidence_rows([], [{
            "user_ip": "10.7.0.2",
            "from": "vless",
            "to": "awg3",
            "reason": "autoswitch_rollback",
            "ts": GENERATED,
        }])

        self.assertEqual(outcomes, [])
        self.assertEqual(len(rollback_rows), 1)

    def test_candidate_outcomes_empty_when_no_match(self):
        candidates = [{
            "user": "10.7.0.2",
            "candidates": [{"channel": "awg0", "suitability_score": 90, "confidence": 0.9}],
        }]
        outcomes = workers.build_candidate_outcome_rows(candidates, [{
            "result": "OK",
            "terminal_state": "APPLIED",
            "selected_moves": [{"user": "10.7.0.9", "target": "vless"}],
        }])
        self.assertEqual(outcomes, [])

    def test_prediction_actuals_from_service_channel_evidence(self):
        forecasts = [{"channel": "awg0", "forecast_quality": 90}, {"service": "telegram", "future_quality": 88}]
        actuals = workers.build_prediction_actual_rows(
            forecasts,
            [{"channel": "awg0", "aggregate_score": 86, "confidence": 0.9}, {"service": "telegram", "average_score": 84, "confidence": 0.8}],
            [{"result": "success"}],
        )
        keys = {row["id"] for row in actuals}
        self.assertEqual(keys, {"awg0", "telegram"})
        self.assertTrue(all(row["evidence_source"] == "prediction_actual_from_existing_service_channel_evidence" for row in actuals))

    def test_prediction_actuals_from_existing_execution_feedback(self):
        forecasts = [{"channel": "awg0", "forecast_quality": 80, "confidence": 0.9}]
        actuals = workers.build_prediction_actual_rows(
            forecasts,
            [],
            [{
                "schema_version": "v7.execution-prediction-feedback.v1",
                "user": "10.0.0.3",
                "target_channel": "awg0",
                "outcome_status": "success",
                "prediction_expected": 0.8,
                "prediction_actual": 0.82,
                "created_at": GENERATED,
            }],
        )
        self.assertEqual(len(actuals), 1)
        self.assertEqual(actuals[0]["id"], "awg0")
        self.assertEqual(actuals[0]["quality"], 82.0)
        self.assertEqual(actuals[0]["prediction_expected"], 80.0)
        self.assertEqual(actuals[0]["evidence_source"], "prediction_actual_from_existing_execution_feedback")

    def test_service_actuals_from_service_rows(self):
        actuals = workers.build_service_actual_rows(
            [{"channel": "awg0", "aggregate_score": 86, "confidence": 0.9}, {"service": "telegram", "average_score": 84, "confidence": 0.8}],
            [{"result": "success"}],
        )
        self.assertEqual(len(actuals), 2)
        self.assertEqual({row.get("channel") or row.get("service") for row in actuals}, {"awg0", "telegram"})
        self.assertTrue(all("score" in row and "evidence_confidence" in row for row in actuals))

    def test_trust_evolution_no_longer_forces_empty_actuals(self):
        result = workers.build_all_snapshots(
            service_matrix=service_matrix(),
            quality_summary=quality_summary(),
            service_preferences={"required_services": ["telegram", "chatgpt"]},
            audit_records=[{
                "result": "OK",
                "terminal_state": "APPLIED",
                "selected_moves": [{"user": "10.7.0.2", "target": "awg0"}],
                "blast_radius": 1,
            }],
            switch_records=[{"result": "OK", "blast_radius": 1}],
            rollback_records=[],
            runtime_state={"egress": {"awg0": {}}},
            users_registry=[{"ip": "10.7.0.2", "enabled": "1"}],
            egress_registry=[{"id": "awg0"}, {"id": "vless"}],
            total_users=1,
            affected_candidates=1,
            generated_at=GENERATED,
        )
        trust = result.snapshots["trust-evolution-summaries"]["items"][0]
        counts = trust["outcome_mapper_counts"]
        self.assertGreater(counts["prediction_actuals_count"], 0)
        self.assertGreater(counts["service_actuals_count"], 0)
        self.assertGreater(counts["candidate_outcomes_count"], 0)
        self.assertTrue(trust["confidence_summary"]["live_calibrated"])

    def test_prediction_feedback_actual_survives_snapshot_write_and_reread(self):
        old_feedback = {
            "schema_version": "v7.execution-prediction-feedback.v1",
            "user": "10.0.0.3",
            "target_channel": "awg0",
            "outcome_status": "success",
            "prediction_expected": 0.8,
            "prediction_actual": 0.82,
            "created_at": GENERATED,
        }
        noisy_recent_records = [
            {"schema_version": "v7.switch-history.v1", "result": "noop", "operation_id": f"recent_{index}"}
            for index in range(workers.MAX_HISTORY_RECORDS + 25)
        ]
        prediction = {
            "items": [{
                "channel_forecasts": [{"channel": "awg0", "forecast_quality": 80, "confidence": 0.9}],
                "service_forecasts": [],
            }],
            "confidence": 0.9,
        }
        payload = workers.build_trust_evolution_snapshot(
            audit_records=[old_feedback] + noisy_recent_records,
            rollback_records=[],
            service_scores_snapshot={"items": [], "confidence": 1.0},
            channel_service_scores_snapshot={"items": [], "confidence": 1.0},
            trust_summary_snapshot={"items": [{"trust": {"score": 90}}], "confidence": 1.0},
            prediction_summary_snapshot=prediction,
            candidate_suitability_snapshot={"items": [], "confidence": 1.0},
            best_available_pool_snapshot={"items": [], "confidence": 1.0},
            blast_radius_snapshot={"items": [], "confidence": 1.0},
            generated_at=GENERATED,
        )
        trust = payload["items"][0]
        self.assertEqual(trust["outcome_mapper_counts"]["bounded_decision_count"], workers.MAX_HISTORY_RECORDS)
        self.assertEqual(trust["outcome_mapper_counts"]["prediction_actuals_count"], 1)
        self.assertEqual(trust["prediction_accuracy"]["matched_count"], 1)
        self.assertEqual(trust["prediction_accuracy"]["prediction_confidence"], 88.2)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            written = workers.write_snapshots(out, {"trust-evolution-summaries": payload})
            reread = read_snapshot_family(out, "trust-evolution-summaries")
        self.assertIn("trust-evolution-summaries", written)
        self.assertTrue(reread.validation.ok, reread.validation.errors)
        reread_trust = reread.payload["items"][0]
        self.assertEqual(reread_trust["outcome_mapper_counts"]["prediction_actuals_count"], 1)
        self.assertEqual(reread_trust["prediction_accuracy"]["matched_count"], 1)
        self.assertEqual(reread_trust["prediction_accuracy"]["prediction_confidence"], 88.2)
        self.assertIn("decision_outcome_learning", reread_trust)
        self.assertEqual(reread_trust["decision_outcome_learning"]["schema_version"], "v7.decision-outcome-learning.model.v1")
        self.assertFalse(reread_trust["decision_outcome_learning"]["runtime_mutation_performed"])

    def test_trust_evolution_uses_execution_feedback_for_suitability_and_blast_radius(self):
        result = workers.build_all_snapshots(
            service_matrix=service_matrix(),
            quality_summary=quality_summary(),
            service_preferences={"required_services": ["telegram", "chatgpt"]},
            audit_records=[{
                "schema_version": "v7.execution-outcome-record.v1",
                "audit_reference": "runtime_autoswitch_small",
                "user": "10.0.0.3",
                "source_channel": "awg3",
                "target_channel": "awg0",
                "outcome_status": "success",
                "execution_outcome": {"success": True, "result": "applied"},
                "verification_result": {"verification_passed": True},
                "rollback_result": {"rollback_required": False},
            }],
            switch_records=[],
            rollback_records=[],
            runtime_state={"egress": {"awg0": {}}},
            users_registry=[{"ip": "10.0.0.3", "enabled": "1"}],
            egress_registry=[{"id": "awg0"}, {"id": "vless"}],
            total_users=1,
            affected_candidates=1,
            generated_at=GENERATED,
        )
        trust = result.snapshots["trust-evolution-summaries"]["items"][0]

        self.assertGreater(trust["outcome_mapper_counts"]["candidate_outcomes_count"], 0)
        self.assertGreater(trust["outcome_mapper_counts"]["blast_radius_evidence_count"], 0)
        self.assertGreater(trust["suitability_trust"]["suitability_confidence"], 20)
        self.assertEqual(trust["blast_radius_confidence_model"]["successful_small_operations"], 1)
        self.assertEqual(trust["blast_radius_confidence_model"]["blast_radius_confidence"], 100)

    def test_trust_evolution_blast_radius_survives_bounded_decision_tail(self):
        old_feedback = [{
            "schema_version": "v7.execution-outcome-record.v1",
            "audit_reference": "runtime_autoswitch_old",
            "user": "10.0.0.3",
            "source_channel": "awg3",
            "target_channel": "awg0",
            "outcome_status": "success",
            "execution_outcome": {"success": True, "result": "applied"},
            "verification_result": {"verification_passed": True},
            "rollback_result": {"rollback_required": False},
            "blast_radius": 5,
        }]
        switch_tail = [
            {"schema_version": "v7.switch-history.v1", "result": "noop", "operation_id": f"switch_{i}"}
            for i in range(workers.MAX_HISTORY_RECORDS + 25)
        ]

        result = workers.build_all_snapshots(
            service_matrix=service_matrix(),
            quality_summary=quality_summary(),
            service_preferences={"required_services": ["telegram", "chatgpt"]},
            audit_records=old_feedback,
            switch_records=switch_tail,
            rollback_records=[],
            runtime_state={"egress": {"awg0": {}}},
            users_registry=[{"ip": "10.0.0.3", "enabled": "1"}],
            egress_registry=[{"id": "awg0"}, {"id": "vless"}],
            total_users=1,
            affected_candidates=1,
            generated_at=GENERATED,
        )
        trust = result.snapshots["trust-evolution-summaries"]["items"][0]
        counts = trust["outcome_mapper_counts"]

        self.assertEqual(counts["bounded_decision_count"], workers.MAX_HISTORY_RECORDS)
        self.assertGreater(counts["blast_radius_source_record_count"], workers.MAX_HISTORY_RECORDS)
        self.assertEqual(counts["blast_radius_evidence_count"], 1)
        self.assertEqual(trust["blast_radius_confidence_model"]["blast_radius_confidence"], 100)

    def test_trust_evolution_includes_channel_recovery_and_explainability(self):
        result = workers.build_all_snapshots(
            service_matrix=service_matrix(),
            quality_summary=quality_summary(),
            service_preferences={"required_services": ["telegram", "chatgpt"]},
            audit_records=[{
                "result": "success",
                "terminal_state": "APPLIED",
                "selected_moves": [{"user": "10.7.0.2", "target": "awg0"}],
                "blast_radius": 1,
            }],
            switch_records=[{"result": "OK", "blast_radius": 1}],
            rollback_records=[],
            runtime_state={"egress": {"awg0": {}}},
            users_registry=[{"ip": "10.7.0.2", "enabled": "1"}],
            egress_registry=[{"id": "awg0"}, {"id": "vless"}],
            total_users=1,
            affected_candidates=1,
            generated_at=GENERATED,
        )
        summary = result.snapshots["trust-evolution-summaries"]["items"][0]
        channel_model = summary["channel_trust_recovery"]
        self.assertEqual(channel_model["owner"], "admin_core.intelligence_workers.trust-evolution-summaries")
        self.assertFalse(channel_model["routing_behavior_changed"])
        self.assertIn("time_windows", channel_model)
        self.assertIn("decay_policy", channel_model)
        awg0 = next(row for row in channel_model["channels"] if row["channel"] == "awg0")
        self.assertIn("explainability", awg0)
        self.assertEqual(awg0["runtime_decision_authority"], "none_evidence_only")
        self.assertEqual(summary["explainability_foundation"]["scope"], "channel_trust_recovery_advisory_only")

    def test_malformed_records_do_not_crash(self):
        self.assertEqual(workers.build_candidate_outcome_rows([{"bad": object()}], [{"selected_moves": ["bad"], "result": object()}]), [])
        actuals = workers.build_prediction_actual_rows([{"channel": "awg0"}], [{"channel": "awg0", "aggregate_score": "bad"}])
        self.assertEqual(actuals[0]["quality"], 0.0)

    def test_terminal_state_rollback_and_confidence_mapping(self):
        applied = workers.normalize_outcome_evidence({"terminal_state": "APPLIED"})
        rollback = workers.normalize_outcome_evidence({"result": "rollback_failed", "rollback_failed": True})
        partial = workers.normalize_outcome_evidence({"apply": True})
        self.assertEqual(applied["outcome_status"], "success")
        self.assertEqual(rollback["outcome_status"], "rollback_failure")
        self.assertEqual(partial["evidence_status"], "partial")
        self.assertGreater(applied["evidence_confidence"], partial["evidence_confidence"])

    def test_rollback_evidence_rows_reuse_existing_audit_records(self):
        rows = workers.build_rollback_evidence_rows(
            [
                {"result": "success", "rollback_required": False, "rollback_manifest_id": "rb-1"},
                {"result": "success"},
            ],
            [{"result": "rollback_success", "rollback_completed": True}],
        )

        self.assertEqual(len(rows), 2)
        self.assertTrue(any(row.get("rollback_manifest_id") == "rb-1" for row in rows))
        self.assertTrue(any(row.get("rollback_completed") for row in rows))

    def test_no_runtime_authority_imports(self):
        source = Path(workers.__file__).read_text(encoding="utf-8")
        self.assertNotIn("subprocess", source)
        self.assertNotIn("autoswitch apply", source.lower())
        self.assertNotIn("operator_execution", source)

    def test_snapshot_build_outputs_11_families(self):
        result = workers.build_all_snapshots(
            service_matrix=service_matrix(),
            quality_summary=quality_summary(),
            service_preferences={"required_services": ["telegram", "chatgpt"]},
            audit_records=[{"result": "success"}],
            runtime_state={"egress": {"awg0": {}}},
            users_registry=[{"ip": "10.7.0.2", "enabled": "1"}],
            egress_registry=[{"id": "awg0"}],
            total_users=1,
            affected_candidates=1,
            generated_at=GENERATED,
        )
        self.assertEqual(len(result.snapshots), 11)

    def test_snapshot_refresh_defaults_consume_existing_audit_logs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "egress" / "state"
            events = root / "events"
            audit = root / "audit"
            state.mkdir(parents=True)
            events.mkdir()
            audit.mkdir()
            (state / "service-matrix.json").write_text(json.dumps(service_matrix()), encoding="utf-8")
            (state / "egress-quality-summary.json").write_text(json.dumps(quality_summary()), encoding="utf-8")
            (state / "service-preferences.json").write_text(json.dumps({"required_services": ["telegram", "chatgpt"]}), encoding="utf-8")
            (state / "users.registry").write_text("ip=10.7.0.2 enabled=1\n", encoding="utf-8")
            (state / "egress.registry").write_text("id=awg0 enabled=1\n", encoding="utf-8")
            (state / "v7-state.json").write_text(json.dumps({"egress": {"awg0": {}}}), encoding="utf-8")
            (events / "switch-history.jsonl").write_text(json.dumps({"result": "OK", "blast_radius": 1}) + "\n", encoding="utf-8")
            (audit / "audit.jsonl").write_text(json.dumps({"result": "OK", "selected_moves": [{"user": "10.7.0.2", "target": "awg0"}]}) + "\n", encoding="utf-8")
            (audit / "operator-execution-audit.jsonl").write_text(json.dumps({"terminal_state": "APPLIED"}) + "\n", encoding="utf-8")
            (audit / "operator-runtime-governance-actions.jsonl").write_text(json.dumps({"result": "OK"}) + "\n", encoding="utf-8")
            completed = subprocess.run(
                [
                    sys.executable,
                    str(Path(__file__).resolve().parents[2] / "tools" / "v7-intelligence-snapshot-refresh"),
                    "--state-dir",
                    str(state),
                    "--event-dir",
                    str(events),
                    "--dry-run",
                ],
                check=True,
                text=True,
                capture_output=True,
            )
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["snapshot_count"], 11)
        self.assertEqual(payload["written"], {})
        self.assertTrue(any(path.endswith("/audit/audit.jsonl") for path in payload["audit_inputs"]))
        self.assertTrue(any(path.endswith("/audit/operator-execution-audit.jsonl") for path in payload["audit_inputs"]))

    def test_snapshot_refresh_jsonl_family_reads_rotated_stores_oldest_first(self):
        tool_path = Path(__file__).resolve().parents[2] / "tools" / "v7-intelligence-snapshot-refresh"
        spec = importlib.util.spec_from_loader(
            "v7_intelligence_snapshot_refresh",
            SourceFileLoader("v7_intelligence_snapshot_refresh", str(tool_path)),
        )
        self.assertIsNotNone(spec)
        refresh = importlib.util.module_from_spec(spec)
        self.assertIsNotNone(spec.loader)
        spec.loader.exec_module(refresh)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            log = root / "execution-events.jsonl"
            (root / "execution-events.jsonl.2").write_text(json.dumps({"order": "oldest"}) + "\n", encoding="utf-8")
            (root / "execution-events.jsonl.1").write_text(json.dumps({"order": "newer"}) + "\n", encoding="utf-8")
            log.write_text(json.dumps({"order": "active"}) + "\n", encoding="utf-8")

            self.assertEqual(
                [path.name for path in refresh.jsonl_family_paths(log)],
                ["execution-events.jsonl.2", "execution-events.jsonl.1", "execution-events.jsonl"],
            )
            self.assertEqual(
                [row["order"] for row in refresh.read_jsonl_family(log)],
                ["oldest", "newer", "active"],
            )

    def test_snapshot_refresh_jsonl_family_keeps_extended_evidence_window(self):
        tool_path = Path(__file__).resolve().parents[2] / "tools" / "v7-intelligence-snapshot-refresh"
        spec = importlib.util.spec_from_loader(
            "v7_intelligence_snapshot_refresh",
            SourceFileLoader("v7_intelligence_snapshot_refresh", str(tool_path)),
        )
        self.assertIsNotNone(spec)
        refresh = importlib.util.module_from_spec(spec)
        self.assertIsNotNone(spec.loader)
        spec.loader.exec_module(refresh)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            log = root / "execution-events.jsonl"
            log.write_text(
                "".join(json.dumps({"order": index}) + "\n" for index in range(workers.MAX_HISTORY_RECORDS + 25)),
                encoding="utf-8",
            )

            rows = refresh.read_jsonl_family(log)

        self.assertEqual(len(rows), workers.MAX_HISTORY_RECORDS + 25)
        self.assertEqual(rows[0]["order"], 0)
        self.assertEqual(rows[-1]["order"], workers.MAX_HISTORY_RECORDS + 24)

    def test_snapshot_refresh_current_state_window_bounds_history_without_deleting_evidence(self):
        tool_path = Path(__file__).resolve().parents[2] / "tools" / "v7-intelligence-snapshot-refresh"
        spec = importlib.util.spec_from_loader(
            "v7_intelligence_snapshot_refresh",
            SourceFileLoader("v7_intelligence_snapshot_refresh", str(tool_path)),
        )
        self.assertIsNotNone(spec)
        refresh = importlib.util.module_from_spec(spec)
        self.assertIsNotNone(spec.loader)
        spec.loader.exec_module(refresh)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            log = root / "execution-events.jsonl"
            log.write_text(
                "".join(json.dumps({"order": index}) + "\n" for index in range(400)),
                encoding="utf-8",
            )

            rows = refresh.read_jsonl_family(log, limit=16, max_bytes=4096)

        self.assertEqual(len(rows), 16)
        self.assertEqual(rows[0]["order"], 384)
        self.assertEqual(rows[-1]["order"], 399)

    def test_snapshot_refresh_current_state_window_builds_required_projections_only(self):
        tool_path = Path(__file__).resolve().parents[2] / "tools" / "v7-intelligence-snapshot-refresh"
        spec = importlib.util.spec_from_loader(
            "v7_intelligence_snapshot_refresh",
            SourceFileLoader("v7_intelligence_snapshot_refresh", str(tool_path)),
        )
        self.assertIsNotNone(spec)
        refresh = importlib.util.module_from_spec(spec)
        self.assertIsNotNone(spec.loader)
        spec.loader.exec_module(refresh)

        result = refresh.build_current_state_snapshots(inputs={
            "service_matrix": service_matrix(),
            "quality_summary": quality_summary(),
            "service_preferences": {"required_services": ["telegram"]},
            "audit_records": [{"result": "OK"}],
            "switch_records": [],
            "rollback_records": [],
            "runtime_state": {"egress": {"awg0": {}}},
            "users_registry": [{"ip": "10.7.0.2", "enabled": "1"}],
            "egress_registry": [{"id": "awg0", "enabled": "1"}],
        })

        self.assertEqual(
            set(result.snapshots),
            {
                "service-scores",
                "channel-service-scores",
                "trust-summaries",
                "risk-summaries",
                "blast-radius-summaries",
                "candidate-suitability-summary",
                "best-available-pool",
                "overview-summary",
            },
        )
        self.assertEqual(result.metrics["snapshot_count"], 8)

    def test_snapshot_refresh_current_state_window_can_bound_candidate_projection_to_exact_user(self):
        tool_path = Path(__file__).resolve().parents[2] / "tools" / "v7-intelligence-snapshot-refresh"
        spec = importlib.util.spec_from_loader(
            "v7_intelligence_snapshot_refresh_exact_user",
            SourceFileLoader("v7_intelligence_snapshot_refresh_exact_user", str(tool_path)),
        )
        self.assertIsNotNone(spec)
        refresh = importlib.util.module_from_spec(spec)
        self.assertIsNotNone(spec.loader)
        spec.loader.exec_module(refresh)

        result = refresh.build_current_state_snapshots(inputs={
            "service_matrix": service_matrix(),
            "quality_summary": quality_summary(),
            "service_preferences": {"required_services": ["telegram"]},
            "audit_records": [{"result": "OK"}],
            "switch_records": [],
            "rollback_records": [],
            "runtime_state": {"egress": {"awg0": {}}},
            "users_registry": [
                {"ip": "10.7.0.2", "enabled": "1"},
                {"ip": "10.7.0.3", "enabled": "1"},
            ],
            "egress_registry": [{"id": "awg0", "enabled": "1"}],
        }, current_state_user="10.7.0.3")

        self.assertEqual(result.metrics["candidate_scope"]["mode"], "EXACT_USER")
        self.assertEqual(result.metrics["candidate_scope"]["candidate_user_count"], 1)
        self.assertEqual(
            result.snapshots["candidate-suitability-summary"]["items"][0]["user"],
            "10.7.0.3",
        )

    def test_snapshot_refresh_preserves_rotated_blast_evidence_through_regeneration(self):
        tool_path = Path(__file__).resolve().parents[2] / "tools" / "v7-intelligence-snapshot-refresh"
        spec = importlib.util.spec_from_loader(
            "v7_intelligence_snapshot_refresh",
            SourceFileLoader("v7_intelligence_snapshot_refresh", str(tool_path)),
        )
        self.assertIsNotNone(spec)
        refresh = importlib.util.module_from_spec(spec)
        self.assertIsNotNone(spec.loader)
        spec.loader.exec_module(refresh)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "egress" / "state"
            events = root / "events"
            out = root / "intelligence"
            state.mkdir(parents=True)
            events.mkdir()
            out.mkdir()
            (state / "service-matrix.json").write_text(json.dumps(service_matrix()), encoding="utf-8")
            (state / "egress-quality-summary.json").write_text(json.dumps(quality_summary()), encoding="utf-8")
            (state / "service-preferences.json").write_text(json.dumps({"required_services": ["telegram", "chatgpt"]}), encoding="utf-8")
            (state / "users.registry").write_text("ip=10.0.0.3 enabled=1\n", encoding="utf-8")
            (state / "egress.registry").write_text("id=awg0 enabled=1\nid=vless enabled=1\n", encoding="utf-8")
            (state / "v7-state.json").write_text(json.dumps({"egress": {"awg0": {}, "vless": {}}}), encoding="utf-8")
            (state / "execution-events.jsonl").write_text("", encoding="utf-8")
            (state / "execution-events.jsonl.1").write_text(json.dumps({
                "schema_version": "v7.execution-outcome-record.v1",
                "audit_reference": "runtime_autoswitch_rotated",
                "user": "10.0.0.3",
                "source_channel": "awg3",
                "target_channel": "awg0",
                "outcome_status": "success",
                "execution_outcome": {"success": True, "result": "applied"},
                "verification_result": {"verification_passed": True},
                "rollback_result": {"rollback_required": False},
                "blast_radius": 5,
            }) + "\n", encoding="utf-8")
            (events / "switch-history.jsonl").write_text(
                "".join(
                    json.dumps({
                        "schema_version": "v7.switch-history.v1",
                        "result": "noop",
                        "operation_id": f"switch_{i}",
                    }) + "\n"
                    for i in range(workers.MAX_HISTORY_RECORDS + 25)
                ),
                encoding="utf-8",
            )
            (events / "rollback-history.jsonl").write_text("", encoding="utf-8")

            first_result, first_status = refresh.build_stable_snapshot_run(
                state_dir=state,
                service_matrix_file=state / "service-matrix.json",
                quality_summary_file=state / "egress-quality-summary.json",
                service_preferences_file=state / "service-preferences.json",
                audit_paths=[],
                feedback_paths=[state / "execution-events.jsonl"],
                switch_history_file=events / "switch-history.jsonl",
                rollback_history_file=events / "rollback-history.jsonl",
                total_users=1,
                affected_candidates=1,
                max_source_retries=2,
                source_retry_sleep_sec=0,
            )
            second_result, second_status = refresh.build_stable_snapshot_run(
                state_dir=state,
                service_matrix_file=state / "service-matrix.json",
                quality_summary_file=state / "egress-quality-summary.json",
                service_preferences_file=state / "service-preferences.json",
                audit_paths=[],
                feedback_paths=[state / "execution-events.jsonl"],
                switch_history_file=events / "switch-history.jsonl",
                rollback_history_file=events / "rollback-history.jsonl",
                total_users=1,
                affected_candidates=1,
                max_source_retries=2,
                source_retry_sleep_sec=0,
            )
            written = workers.write_snapshots(out, second_result.snapshots)
            reread = read_snapshot_family(out, "trust-evolution-summaries")

        self.assertTrue(first_status["source_stable"])
        self.assertTrue(second_status["source_stable"])
        for result in (first_result, second_result):
            trust = result.snapshots["trust-evolution-summaries"]["items"][0]
            counts = trust["outcome_mapper_counts"]
            self.assertEqual(counts["bounded_decision_count"], workers.MAX_HISTORY_RECORDS)
            self.assertGreater(counts["blast_radius_source_record_count"], workers.MAX_HISTORY_RECORDS)
            self.assertEqual(counts["blast_radius_evidence_count"], 1)
            self.assertEqual(trust["blast_radius_confidence_model"]["blast_radius_confidence"], 100)
        self.assertIn("trust-evolution-summaries", written)
        self.assertTrue(reread.validation.ok, reread.validation.errors)
        reread_trust = reread.payload["items"][0]
        self.assertEqual(reread_trust["outcome_mapper_counts"]["blast_radius_evidence_count"], 1)
        self.assertEqual(reread_trust["blast_radius_confidence_model"]["blast_radius_confidence"], 100)

    def test_snapshot_refresh_retries_when_source_changes_during_build(self):
        tool_path = Path(__file__).resolve().parents[2] / "tools" / "v7-intelligence-snapshot-refresh"
        spec = importlib.util.spec_from_loader(
            "v7_intelligence_snapshot_refresh",
            SourceFileLoader("v7_intelligence_snapshot_refresh", str(tool_path)),
        )
        self.assertIsNotNone(spec)
        refresh = importlib.util.module_from_spec(spec)
        self.assertIsNotNone(spec.loader)
        spec.loader.exec_module(refresh)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "egress" / "state"
            events = root / "events"
            audit = root / "audit"
            state.mkdir(parents=True)
            events.mkdir()
            audit.mkdir()
            matrix = service_matrix()
            changed_matrix = service_matrix()
            changed_matrix["items"]["awg0"]["services"]["telegram"]["score"] = 77
            (state / "service-matrix.json").write_text(json.dumps(matrix), encoding="utf-8")
            (state / "egress-quality-summary.json").write_text(json.dumps(quality_summary()), encoding="utf-8")
            (state / "service-preferences.json").write_text(json.dumps({"required_services": ["telegram", "chatgpt"]}), encoding="utf-8")
            (state / "users.registry").write_text("ip=10.7.0.2 enabled=1\n", encoding="utf-8")
            (state / "egress.registry").write_text("id=awg0 enabled=1\n", encoding="utf-8")
            (state / "v7-state.json").write_text(json.dumps({"egress": {"awg0": {}}}), encoding="utf-8")
            (events / "switch-history.jsonl").write_text("", encoding="utf-8")
            (events / "rollback-history.jsonl").write_text("", encoding="utf-8")
            calls = {"count": 0}
            original_build = refresh.build_all_snapshots

            def build_and_change_once(**kwargs):
                result = original_build(**kwargs)
                calls["count"] += 1
                if calls["count"] == 1:
                    (state / "service-matrix.json").write_text(json.dumps(changed_matrix), encoding="utf-8")
                return result

            refresh.build_all_snapshots = build_and_change_once
            try:
                result, source_status = refresh.build_stable_snapshot_run(
                    state_dir=state,
                    service_matrix_file=state / "service-matrix.json",
                    quality_summary_file=state / "egress-quality-summary.json",
                    service_preferences_file=state / "service-preferences.json",
                    audit_paths=[audit / "audit.jsonl"],
                    switch_history_file=events / "switch-history.jsonl",
                    rollback_history_file=events / "rollback-history.jsonl",
                    total_users=0,
                    affected_candidates=0,
                    max_source_retries=2,
                    source_retry_sleep_sec=0,
                )
            finally:
                refresh.build_all_snapshots = original_build
        self.assertTrue(source_status["source_stable"])
        self.assertEqual(source_status["source_consistency_attempts"], 2)
        self.assertEqual(
            result.snapshots["service-scores"]["source_hashes"]["service_matrix"],
            refresh.sha256_json(changed_matrix),
        )

    def test_stable_matrix_generation_handoff_consumes_captured_generation_while_writer_advances(self):
        tool_path = Path(__file__).resolve().parents[2] / "tools" / "v7-intelligence-snapshot-refresh"
        loader = SourceFileLoader("v7_intelligence_snapshot_refresh_handoff", str(tool_path))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        refresh = importlib.util.module_from_spec(spec)
        self.assertIsNotNone(spec.loader)
        spec.loader.exec_module(refresh)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "egress" / "state"
            events = root / "events"
            audit = root / "audit"
            state.mkdir(parents=True)
            events.mkdir()
            audit.mkdir()
            matrix = service_matrix()
            matrix["updated"] = datetime.now(timezone.utc).isoformat()
            advanced = service_matrix()
            advanced["updated"] = matrix["updated"]
            advanced["items"]["awg0"]["path_evidence"] = {
                "path_fingerprint": "advanced-path-generation",
                "component_status": {"interface": "PASS"},
            }
            matrix_file = state / "service-matrix.json"
            matrix_file.write_text(json.dumps(matrix), encoding="utf-8")
            (state / "egress-quality-summary.json").write_text(json.dumps(quality_summary()), encoding="utf-8")
            (state / "service-preferences.json").write_text(
                json.dumps({"required_services": ["telegram", "chatgpt"]}), encoding="utf-8"
            )
            (state / "users.registry").write_text("ip=10.7.0.2 enabled=1\n", encoding="utf-8")
            (state / "egress.registry").write_text("id=awg0 enabled=1\n", encoding="utf-8")
            (state / "v7-state.json").write_text(json.dumps({"egress": {"awg0": {}}}), encoding="utf-8")
            (events / "switch-history.jsonl").write_text("", encoding="utf-8")
            (events / "rollback-history.jsonl").write_text("", encoding="utf-8")
            original_build = refresh.build_all_snapshots

            def build_and_advance_once(**kwargs):
                result = original_build(**kwargs)
                matrix_file.write_text(json.dumps(advanced), encoding="utf-8")
                return result

            refresh.build_all_snapshots = build_and_advance_once
            try:
                result, source_status = refresh.build_stable_snapshot_run(
                    state_dir=state,
                    service_matrix_file=matrix_file,
                    quality_summary_file=state / "egress-quality-summary.json",
                    service_preferences_file=state / "service-preferences.json",
                    audit_paths=[audit / "audit.jsonl"],
                    switch_history_file=events / "switch-history.jsonl",
                    rollback_history_file=events / "rollback-history.jsonl",
                    total_users=0,
                    affected_candidates=0,
                    max_source_retries=2,
                    source_retry_sleep_sec=0,
                    stable_matrix_generation_handoff=True,
                )
            finally:
                refresh.build_all_snapshots = original_build
        self.assertIsNotNone(result)
        self.assertTrue(source_status["source_stable"])
        self.assertEqual(source_status["source_consistency_attempts"], 1)
        handoff = source_status["stable_matrix_generation_handoff"]
        self.assertEqual(handoff["status"], "PASS")
        self.assertTrue(handoff["generation"]["writer_advanced_during_build"])
        self.assertTrue(handoff["consumer_reads_one_completed_generation"])
        self.assertFalse(handoff["mixed_matrix_generation_read"])
        self.assertEqual(
            result.snapshots["service-scores"]["source_hashes"]["service_matrix"],
            refresh.sha256_json(matrix),
        )
        self.assertEqual(
            result.snapshots["service-scores"]["matrix_generation"]["generation_id"],
            handoff["generation"]["generation_id"],
        )

    def test_stable_matrix_generation_handoff_stops_on_required_service_state_change(self):
        tool_path = Path(__file__).resolve().parents[2] / "tools" / "v7-intelligence-snapshot-refresh"
        loader = SourceFileLoader("v7_intelligence_snapshot_refresh_service_drift", str(tool_path))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        refresh = importlib.util.module_from_spec(spec)
        self.assertIsNotNone(spec.loader)
        spec.loader.exec_module(refresh)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "egress" / "state"
            events = root / "events"
            audit = root / "audit"
            state.mkdir(parents=True)
            events.mkdir()
            audit.mkdir()
            matrix = service_matrix()
            matrix["updated"] = datetime.now(timezone.utc).isoformat()
            changed = service_matrix()
            changed["updated"] = matrix["updated"]
            changed["items"]["awg0"]["services"]["telegram"]["score"] = 1
            matrix_file = state / "service-matrix.json"
            matrix_file.write_text(json.dumps(matrix), encoding="utf-8")
            (state / "egress-quality-summary.json").write_text(json.dumps(quality_summary()), encoding="utf-8")
            (state / "service-preferences.json").write_text(
                json.dumps({"required_services": ["telegram", "chatgpt"]}), encoding="utf-8"
            )
            (state / "users.registry").write_text("ip=10.7.0.2 enabled=1\n", encoding="utf-8")
            (state / "egress.registry").write_text("id=awg0 enabled=1\n", encoding="utf-8")
            (state / "v7-state.json").write_text("{}", encoding="utf-8")
            (events / "switch-history.jsonl").write_text("", encoding="utf-8")
            (events / "rollback-history.jsonl").write_text("", encoding="utf-8")
            original_build = refresh.build_all_snapshots

            def build_and_change_service(**kwargs):
                result = original_build(**kwargs)
                matrix_file.write_text(json.dumps(changed), encoding="utf-8")
                return result

            refresh.build_all_snapshots = build_and_change_service
            try:
                result, source_status = refresh.build_stable_snapshot_run(
                    state_dir=state,
                    service_matrix_file=matrix_file,
                    quality_summary_file=state / "egress-quality-summary.json",
                    service_preferences_file=state / "service-preferences.json",
                    audit_paths=[audit / "audit.jsonl"],
                    switch_history_file=events / "switch-history.jsonl",
                    rollback_history_file=events / "rollback-history.jsonl",
                    total_users=0,
                    affected_candidates=0,
                    max_source_retries=2,
                    source_retry_sleep_sec=0,
                    stable_matrix_generation_handoff=True,
                )
            finally:
                refresh.build_all_snapshots = original_build
        self.assertIsNotNone(result)
        self.assertFalse(source_status["source_stable"])
        self.assertEqual(
            source_status["source_consistency_errors"],
            ["required_service_state_changed_after_matrix_generation"],
        )
        self.assertEqual(source_status["stable_matrix_generation_handoff"]["status"], "STOP_SAFE")

    def test_all_worker_generates_and_writes_readable_snapshots(self):
        result = workers.build_all_snapshots(
            service_matrix=service_matrix(),
            quality_summary=quality_summary(),
            service_preferences={"required_services": ["telegram", "chatgpt"]},
            audit_records=[{"result": "success"}],
            runtime_state={"egress": {"awg0": {}}},
            users_registry=[{"ip": "10.7.0.2", "enabled": "1"}],
            egress_registry=[{"id": "awg0"}],
            total_users=1,
            affected_candidates=1,
            generated_at=GENERATED,
        )
        self.assertIn("service-scores", result.snapshots)
        self.assertIn("user-service-scores", result.snapshots)
        self.assertIn("candidate-suitability-summary", result.snapshots)
        self.assertIn("best-available-pool", result.snapshots)
        self.assertIn("prediction-summaries", result.snapshots)
        self.assertIn("trust-evolution-summaries", result.snapshots)
        self.assertIn("overview-summary", result.snapshots)
        self.assertGreater(result.metrics["snapshot_count"], 0)
        with tempfile.TemporaryDirectory() as tmp:
            written = workers.write_snapshots(Path(tmp), result.snapshots)
            self.assertIn("service-scores", written)
            read = read_snapshot_family(Path(tmp), "service-scores")
        self.assertTrue(read.validation.ok)

    def test_missing_inputs_fail_safely_with_warnings(self):
        result = workers.build_all_snapshots(
            service_matrix={"items": {}},
            quality_summary={"items": {}},
            service_preferences={},
            audit_records=[],
            runtime_state={},
            users_registry=[],
            egress_registry=[],
            generated_at=GENERATED,
        )
        self.assertIn("service_matrix_missing_or_empty", result.snapshots["service-scores"]["warnings"])
        self.assertIn("history_missing", result.snapshots["trust-summaries"]["warnings"])
        self.assertIn("runtime_state_missing", result.snapshots["overview-summary"]["warnings"])
        for name, payload in result.snapshots.items():
            self.assertTrue(validate_snapshot(payload, name).ok)

    def test_jsonl_tail_reader_bounds_history_and_skips_corruption(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "history.jsonl"
            path.write_text(
                "\n".join([json.dumps({"idx": i}) for i in range(20)] + ["broken"]),
                encoding="utf-8",
            )
            rows = workers.read_jsonl_tail(path, limit=5)
        self.assertEqual([row["idx"] for row in rows], [15, 16, 17, 18, 19])

    def test_jsonl_tail_matching_prefilters_but_preserves_chronology(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "history.jsonl"
            path.write_text(
                "\n".join([
                    json.dumps({"idx": 1, "incident": "other"}),
                    json.dumps({"idx": 2, "incident": "wanted"}),
                    "broken wanted",
                    json.dumps({"idx": 3, "incident": "other"}),
                    json.dumps({"idx": 4, "incident": "wanted"}),
                ]),
                encoding="utf-8",
            )
            rows = workers.read_jsonl_tail_matching(
                path, markers=["wanted"], limit=2,
            )
        self.assertEqual([row["idx"] for row in rows], [2, 4])

    def test_jsonl_tail_matching_requires_all_markers_and_skips_partial_window_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "history.jsonl"
            rows = [
                {"idx": 1, "incident": "wanted", "source": "other"},
                {"idx": 2, "incident": "wanted", "source": "exact"},
                {"idx": 3, "incident": "wanted", "source": "exact"},
            ]
            payload = "\n".join(json.dumps(row) for row in rows)
            path.write_text(payload, encoding="utf-8")
            # Begin inside row 1.  Only complete rows inside the bounded tail
            # may be considered canonical evidence.
            max_bytes = len(payload.encode("utf-8")) - 5
            matched = workers.read_jsonl_tail_matching(
                path,
                markers=["wanted", "exact"],
                limit=2,
                max_bytes=max_bytes,
                require_all=True,
            )
        self.assertEqual([row["idx"] for row in matched], [2, 3])

    def test_worker_architecture_forbids_runtime_authority(self):
        architecture = workers.worker_architecture()
        forbidden = set(architecture["forbidden"])
        self.assertIn("user movement", forbidden)
        self.assertIn("runtime actions", forbidden)
        self.assertEqual(architecture["runtime_integration"], "none_in_PERF3")


if __name__ == "__main__":
    unittest.main()
