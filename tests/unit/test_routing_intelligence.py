import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from admin_core.routing_intelligence import (
    DynamicBlastRadiusModel,
    ExecutionTrustModel,
    PredictiveFoundation,
    RoutingIntelligenceShadow,
    ServiceHistoryStore,
    ServiceIntelligenceEngine,
    UserServiceWeights,
    service_quality_contract,
    service_quality_framework,
)


ROOT = Path(__file__).resolve().parents[2]


def service_matrix():
    return {
        "updated": "2026-06-03T07:00:00+00:00",
        "items": {
            "awg0": {
                "services": {
                    "telegram": {"ok": True, "status": "OK", "score": 95, "first_byte_sec": 0.2, "confidence": 0.9},
                    "youtube": {"ok": True, "status": "OK", "score": 90, "first_byte_sec": 0.6, "confidence": 0.8},
                    "instagram": {"ok": True, "status": "OK", "score": 88, "first_byte_sec": 0.8, "confidence": 0.8},
                    "chatgpt": {"ok": True, "status": "OK", "score": 84, "first_byte_sec": 0.9, "confidence": 0.7},
                    "google": {"ok": True, "status": "OK", "score": 90, "first_byte_sec": 0.4, "confidence": 0.8},
                    "google_auth": {"ok": True, "status": "OK", "score": 90, "first_byte_sec": 0.5, "confidence": 0.8},
                }
            },
            "bad": {
                "services": {
                    "telegram": {"ok": False, "status": "DOWN", "score": 0, "first_byte_sec": 0.0, "confidence": 0.2},
                    "youtube": {"ok": False, "status": "FAIL", "score": 0, "confidence": 0.2},
                    "instagram": {"ok": False, "status": "FAIL", "score": 0, "confidence": 0.2},
                    "chatgpt": {"ok": False, "status": "FAIL", "score": 0, "confidence": 0.2},
                }
            },
        },
    }


def quality_summary():
    return {
        "updated": "2026-06-03T07:00:00+00:00",
        "items": {
            "awg0": {
                "windows": {
                    "1h": {"avg_mbps": 40, "stability": 0.9, "fail_rate": 0.01, "samples": 12},
                    "24h": {"avg_mbps": 38, "stability": 0.86, "fail_rate": 0.03, "samples": 100},
                    "7d": {"avg_mbps": 36, "stability": 0.82, "fail_rate": 0.05, "samples": 700},
                }
            },
            "bad": {
                "windows": {
                    "1h": {"avg_mbps": 1, "stability": 0.1, "fail_rate": 0.9, "samples": 12},
                    "24h": {"avg_mbps": 20, "stability": 0.6, "fail_rate": 0.2, "samples": 100},
                    "7d": {"avg_mbps": 25, "stability": 0.7, "fail_rate": 0.1, "samples": 700},
                }
            },
        },
    }


class RoutingIntelligenceTest(unittest.TestCase):
    def test_service_history_model_contains_required_services_and_windows(self):
        store = ServiceHistoryStore.from_runtime_inputs(service_matrix(), quality_summary())
        data = store.to_dict()
        self.assertEqual(data["schema_version"], "ri1.service-history.v1")
        for service in ("telegram", "youtube", "instagram", "chatgpt", "google", "google_auth"):
            self.assertIn(service, data["services"])
            self.assertIn("awg0", data["services"][service]["targets"])
            self.assertEqual(set(data["services"][service]["targets"]["awg0"]["windows"]), {"1h", "24h", "7d", "30d"})
        telegram = store.metric("telegram", "awg0")
        self.assertTrue(telegram["availability"])
        self.assertGreater(telegram["latency_ms"], 0)
        self.assertGreater(telegram["throughput_mbps"], 0)

    def test_service_intelligence_scores_good_target_above_failed_target(self):
        store = ServiceHistoryStore.from_runtime_inputs(service_matrix(), quality_summary())
        engine = ServiceIntelligenceEngine(store)
        good = engine.score_target("awg0", ["telegram", "youtube", "instagram", "chatgpt"])
        bad = engine.score_target("bad", ["telegram", "youtube", "instagram", "chatgpt"])
        self.assertGreater(good["aggregate_score"], bad["aggregate_score"])
        self.assertEqual(good["verdict"], "OK")
        self.assertTrue(any(item.startswith("latency_ms=") for item in good["per_service"][0]["explainability"]))
        self.assertEqual(bad["verdict"], "REVIEW_REQUIRED_LOW_SERVICE_SCORE")

    def test_ri4_cd_service_quality_contracts_cover_primary_services(self):
        framework = service_quality_framework()
        self.assertEqual(framework["schema_version"], "ri4cd.service-quality-framework.v1")
        for service in ("telegram", "youtube", "instagram", "chatgpt"):
            contract = service_quality_contract(service)
            self.assertIn(service, framework["supported_services"])
            self.assertIn("availability", contract["criteria"])
            self.assertEqual(contract["runtime_decision_authority"], "none_shadow_only")

    def test_ri4_cd_service_specific_components_are_scored_and_trended(self):
        matrix = service_matrix()
        matrix["items"]["awg0"]["services"]["telegram"].update({
            "message_latency_ms": 120,
            "media_latency_ms": 900,
            "media_success_rate": 0.98,
            "connection_success": 1.0,
        })
        matrix["items"]["awg0"]["services"]["youtube"].update({
            "startup_delay_ms": 700,
            "buffer_probability": 0.01,
        })
        matrix["items"]["awg0"]["services"]["instagram"].update({
            "feed_load_ms": 500,
            "story_load_ms": 600,
            "video_load_ms": 900,
            "reliability": 0.95,
        })
        matrix["items"]["awg0"]["services"]["chatgpt"].update({
            "response_latency_ms": 900,
            "stream_start_latency_ms": 500,
            "stream_continuity": 0.98,
        })
        store = ServiceHistoryStore.from_runtime_inputs(matrix, quality_summary())
        engine = ServiceIntelligenceEngine(store)
        for service in ("telegram", "youtube", "instagram", "chatgpt"):
            row = engine.score_service(service, "awg0", "1h")
            self.assertEqual(row["schema_version"], "ri4cd.service-quality-score.v1")
            self.assertGreater(row["score"], 70)
            self.assertTrue(row["quality_components"])
            self.assertIn("quality_trend", row)

    def test_user_service_weights_normalize_per_user_priorities(self):
        prefs = {
            "required_services": ["telegram", "chatgpt"],
            "users": {
                "10.7.0.10": {"weights": {"telegram": 70, "chatgpt": 30}},
                "10.7.0.11": {"priority_services": ["youtube", "instagram"]},
            },
        }
        weights = UserServiceWeights.from_service_preferences(prefs)
        self.assertEqual(weights.for_user("10.7.0.10"), {"chatgpt": 30.0, "telegram": 70.0})
        self.assertEqual(sum(weights.for_user("10.7.0.11").values()), 100.0)

    def test_execution_trust_model_rewards_success_and_penalizes_violations(self):
        good = ExecutionTrustModel.from_records(
            [
                {"result": "OK", "blast_radius": 1},
                {"result": "success", "rollback_executed": "rollback_success"},
            ]
        )
        bad = ExecutionTrustModel.from_records(
            [
                {"result": "failed", "blast_radius_violation": True},
                {"result": "error", "governance_violation": True},
                {"result": "rollback_failed"},
            ]
        )
        self.assertGreater(good["score"], bad["score"])
        self.assertGreaterEqual(good["counters"]["successful_executions"], 1)
        self.assertGreater(bad["counters"]["governance_violations"], 0)

    def test_dynamic_blast_radius_is_conservative_and_bounded(self):
        low = DynamicBlastRadiusModel.recommend(
            total_users=100,
            affected_users=50,
            execution_trust=40,
            service_risk=20,
            platform_health=90,
        )
        high = DynamicBlastRadiusModel.recommend(
            total_users=100,
            affected_users=8,
            execution_trust=90,
            service_risk=10,
            platform_health=90,
        )
        self.assertEqual(low["recommended_budget"], 1)
        self.assertLessEqual(high["recommended_budget"], 8)
        self.assertEqual(high["runtime_decision_authority"], "none_shadow_only")

    def test_predictive_foundation_is_disabled_and_detects_degradation(self):
        store = ServiceHistoryStore.from_runtime_inputs(service_matrix(), quality_summary())
        prediction = PredictiveFoundation.analyze_service_trends(store)
        self.assertFalse(prediction["prediction_enabled"])
        degraded = [row for row in prediction["examples"] if row["target"] == "bad" and row["service"] == "telegram"]
        self.assertEqual(degraded[0]["trend"], "degrading")

    def test_ri5_prediction_summary_forecasts_without_authority(self):
        store = ServiceHistoryStore.from_runtime_inputs(service_matrix(), quality_summary())
        summary = PredictiveFoundation.prediction_summary(
            store,
            risk_summary={"service_risk": 30},
            trust_summary={"trust": {"score": 80, "counters": {"successful_executions": 10}}},
        )
        self.assertTrue(summary["prediction_enabled"])
        self.assertEqual(summary["schema_version"], "ri5.prediction-summary.v1")
        self.assertGreater(len(summary["channel_forecasts"]), 0)
        self.assertGreater(len(summary["service_forecasts"]), 0)
        self.assertIn("risk_forecast", summary)
        self.assertIn("trust_forecast", summary)
        self.assertEqual(summary["execution_authority"], "none")
        self.assertEqual(summary["selected_moves_write_authority"], "none")
        bad = next(row for row in summary["channel_forecasts"] if row["channel"] == "bad")
        self.assertGreater(bad["degradation_probability"], 0)

    def test_shadow_replay_outputs_intelligence_without_runtime_action_fields(self):
        result = RoutingIntelligenceShadow.replay(
            service_matrix=service_matrix(),
            quality_summary=quality_summary(),
            service_preferences={"required_services": ["telegram", "youtube", "instagram", "chatgpt"]},
            audit_records=[{"result": "OK", "blast_radius": 1}],
            total_users=20,
            affected_users=5,
        )
        encoded = json.dumps(result, sort_keys=True)
        self.assertEqual(result["mode"], "shadow_read_only")
        self.assertIn("service_intelligence_scores", result)
        self.assertIn("execution_trust", result)
        self.assertNotIn("selected_moves", encoded)
        self.assertNotIn("apply_requested", encoded)
        self.assertNotIn("runtime_action_record", encoded)

    def test_shadow_cli_reads_files_and_writes_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            state.mkdir()
            (state / "service-matrix.json").write_text(json.dumps(service_matrix()), encoding="utf-8")
            (state / "egress-quality-summary.json").write_text(json.dumps(quality_summary()), encoding="utf-8")
            (state / "service-preferences.json").write_text(
                json.dumps({"required_services": ["telegram", "youtube", "instagram", "chatgpt"]}),
                encoding="utf-8",
            )
            audit = root / "audit.jsonl"
            audit.write_text(json.dumps({"result": "OK", "blast_radius": 1}) + "\n", encoding="utf-8")
            output = root / "shadow.json"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "tools" / "v7-routing-intelligence-shadow"),
                    "--state-dir",
                    str(state),
                    "--audit-log",
                    str(audit),
                    "--total-users",
                    "20",
                    "--affected-users",
                    "5",
                    "--output",
                    str(output),
                    "--pretty",
                ],
                check=False,
                text=True,
                capture_output=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            data = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(data["schema_version"], "ri1.shadow-replay.v1")
            self.assertTrue(data["non_authority_guards"]["no_user_movement"])


if __name__ == "__main__":
    unittest.main()
