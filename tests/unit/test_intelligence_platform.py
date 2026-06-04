import unittest

from admin_core import intelligence_platform as platform


class IntelligencePlatformHardeningTest(unittest.TestCase):
    def test_reality_gap_truth_and_duplication_maps_preserve_authority(self):
        reality = platform.intelligence_reality_map()
        gaps = platform.intelligence_gap_map()
        truth = platform.intelligence_truth_source_map()
        duplication = platform.duplication_audit()
        self.assertIn("RI.5", reality["chain"])
        self.assertTrue(gaps["problem_closure_required"])
        self.assertTrue(truth["one_truth_rule"])
        self.assertFalse(duplication["duplicate_planner"])
        self.assertFalse(duplication["duplicate_snapshot_roots"])

    def test_slo_sla_model_covers_supported_services(self):
        model = platform.service_slo_sla_model()
        for service in ("telegram", "youtube", "instagram", "chatgpt", "google", "google_auth"):
            self.assertIn(service, model["services"])
            self.assertIn("GOOD", model["services"][service]["thresholds"])
        self.assertEqual(model["runtime_decision_authority"], "none_contract_only")

    def test_model_governance_versions_and_migration_rules_exist(self):
        governance = platform.model_governance_framework()
        self.assertEqual(governance["model_version"], platform.MODEL_VERSION)
        self.assertEqual(governance["weights_version"], platform.WEIGHTS_VERSION)
        self.assertEqual(governance["calibration_version"], platform.CALIBRATION_VERSION)
        self.assertIn("schema_change", governance["migration_rules"])
        self.assertEqual(governance["authority"]["planner_authority"], "tools/v7-users-autoswitch")

    def test_replay_forecast_validation_and_drift_metrics(self):
        replay = platform.replay_framework(
            predicted=[{"id": "a", "degradation_probability": 90}, {"id": "b", "degradation_probability": 10}],
            actual=[{"id": "a", "failed": True}, {"id": "b", "score": 90}],
        )
        self.assertEqual(replay["agreement_rate"], 1.0)
        self.assertEqual(replay["false_positives"], 0)
        validation = platform.forecast_validation_framework(
            forecasts=[{"id": "a", "forecast_quality": 80, "confidence": 0.8}],
            actuals=[{"id": "a", "quality": 75}],
        )
        self.assertGreater(validation["forecast_accuracy"], 90)
        drift = platform.drift_detection_framework(
            baseline=[{"score": 90}, {"score": 80}],
            current=[{"score": 40}, {"score": 30}],
        )
        self.assertEqual(drift["service_scoring_drift"], "HIGH")

    def test_explainability_rollout_trust_probe_observability_and_certification(self):
        explanation = platform.explain_score(
            "telegram",
            82,
            {"latency": 15, "risk": -5, "prediction": 8},
            confidence=0.8,
            source="service-scores",
        )
        self.assertIn("latency", explanation["positive_components"])
        self.assertIn("risk", explanation["negative_components"])
        rollout = platform.rollout_governance_model()
        self.assertEqual(rollout["default_level"], "shadow_only")
        self.assertIn("bounded_influence", rollout["levels"])
        trust = platform.trust_evolution_foundation()
        self.assertIn("successful_execution", trust["increase_trust"])
        probes = platform.service_probe_audit()
        self.assertEqual(probes["services"]["telegram"]["classification"], "EXISTS")
        observability = platform.observability_model()
        self.assertIn("snapshot_integrity", observability["alerts"])
        certification = platform.platform_certification()
        self.assertEqual(certification["operational_readiness"], "READY_FOR_GOVERNED_STAGING")
        self.assertEqual(certification["authority"]["execution_authority"], "none")


if __name__ == "__main__":
    unittest.main()

