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
        self.assertIn("trust_evolution", certification)

    def test_ri6_trust_evolution_models_preserve_authority(self):
        summary = platform.trust_evolution_summary(
            decision_records=[
                {"result": "success", "service_delta": 12, "prediction_delta": 5, "blast_radius": 1},
                {"result": "rollback_success", "rollback_required": True, "rollback_completed": True, "blast_radius": 1},
            ],
            prediction_forecasts=[{"channel": "awg0", "forecast_quality": 90, "confidence": 0.9}],
            prediction_actuals=[{"channel": "awg0", "quality": 85}],
            service_rows=[{"channel": "awg0", "aggregate_score": 88, "confidence": 0.9}],
            service_actuals=[{"channel": "awg0", "score": 86}],
            candidate_rows=[{"user": "10.7.0.2", "candidates": [{"channel": "awg0", "suitability_score": 90, "confidence": 0.9}]}],
            candidate_outcomes=[{"user": "10.7.0.2", "channel": "awg0", "result": "success"}],
            rollback_records=[{"result": "rollback_success", "rollback_completed": True}],
            blast_radius_records=[{"result": "success", "blast_radius": 1}],
            blast_radius_metrics={"recommendation": {"recommended_budget": 1}},
        )
        self.assertEqual(summary["schema_version"], "v7.ri6.trust-evolution.v1")
        self.assertGreater(summary["confidence_summary"]["decision_confidence"], 0)
        self.assertGreater(summary["prediction_accuracy"]["prediction_confidence"], 70)
        self.assertGreater(summary["service_intelligence_trust"]["service_confidence"], 70)
        self.assertGreater(summary["suitability_trust"]["suitability_confidence"], 70)
        self.assertEqual(summary["autonomy_readiness"]["autonomy_enabled"], False)
        self.assertEqual(summary["execution_authority"], "none")
        self.assertEqual(summary["selected_moves_write_authority"], "none")
        self.assertIn("governed_to_autonomy_trust_bridge", summary)
        bridge = summary["governed_to_autonomy_trust_bridge"]
        self.assertEqual(bridge["model"], "PARTIALLY_INHERITED_GOVERNED_TRUST_WITH_AUTONOMY_CAPS")
        self.assertFalse(bridge["bounded_autonomy_ready"])
        self.assertFalse(bridge["production_autonomy_ready"])
        self.assertFalse(bridge["autonomy_enabled"])
        self.assertEqual(bridge["execution_authority"], "none")

    def test_governed_to_autonomy_trust_bridge_inherits_but_caps_authority(self):
        bridge = platform.governed_to_autonomy_trust_bridge(
            confidence_summary={
                "decision_confidence": 50,
                "prediction_confidence": 37,
                "service_confidence": 39,
                "suitability_confidence": 28,
                "rollback_confidence": 100,
                "live_calibrated": True,
            },
            evidence_counts={
                "candidate_outcomes_count": 22,
                "prediction_actuals_count": 22,
                "service_actuals_count": 22,
            },
            rollback_model={"rollback_confidence": 100},
        )

        self.assertGreaterEqual(bridge["inherited_execution_trust"], 70)
        self.assertTrue(bridge["approval_autonomy_review_ready"])
        self.assertEqual(bridge["autonomy_boundary_cap"], "OPERATOR_APPROVAL_READY")
        self.assertIn("autonomous_trigger_not_certified", bridge["bounded_autonomy_blockers"])
        self.assertIn("operator_free_apply_not_certified", bridge["bounded_autonomy_blockers"])
        self.assertFalse(bridge["bounded_autonomy_ready"])
        self.assertFalse(bridge["authority_changed"])
        self.assertFalse(bridge["runtime_mutation_performed"])
        self.assertFalse(bridge["autonomy_enabled"])

    def test_governed_bridge_does_not_approve_without_live_calibration(self):
        bridge = platform.governed_to_autonomy_trust_bridge(
            confidence_summary={"rollback_confidence": 100, "live_calibrated": False},
            evidence_counts={
                "candidate_outcomes_count": 22,
                "prediction_actuals_count": 22,
                "service_actuals_count": 22,
            },
        )

        self.assertEqual(bridge["autonomy_boundary_cap"], "OPERATOR_VISIBLE_READY")
        self.assertFalse(bridge["approval_autonomy_review_ready"])
        self.assertFalse(bridge["bounded_autonomy_ready"])

    def test_ri6_pending_outcomes_are_not_treated_as_validated_accuracy(self):
        prediction = platform.prediction_accuracy_model(
            forecasts=[{"channel": "awg0", "forecast_quality": 90, "confidence": 0.8}],
            actuals=[],
        )
        self.assertEqual(prediction["validation_status"], "LIVE_OUTCOME_REQUIRED")
        self.assertEqual(prediction["matched_count"], 0)
        self.assertLess(prediction["prediction_confidence"], 60)
        readiness = platform.autonomy_readiness_model({
            "decision_confidence": 80,
            "prediction_confidence": 55,
            "service_confidence": 85,
            "suitability_confidence": 80,
            "rollback_confidence": 80,
            "blast_radius_confidence": 80,
            "live_calibrated": False,
        })
        self.assertEqual(readiness["current_level"], "OPERATOR_VISIBLE_READY")
        self.assertFalse(readiness["governance_changed"])

    def test_rollback_readiness_validation_is_counted_without_executed_rollback(self):
        rollback = platform.rollback_intelligence_model([
            {
                "result": "success",
                "verification_passed": True,
                "rollback_required": False,
                "rollback_manifest": {"items": [{"user_ip": "10.0.0.3", "rollback_target": "awg0"}]},
            }
        ])

        self.assertEqual(rollback["rollback_required"], 0)
        self.assertEqual(rollback["rollback_readiness_validations"], 1)
        self.assertEqual(rollback["rollback_confidence"], 70.0)
        self.assertEqual(rollback["validation_status"], "VALIDATED_READINESS_ONLY")

    def test_autoswitch_rollback_switch_rows_count_as_completed_rollback(self):
        rollback = platform.rollback_intelligence_model([
            {"reason": "autoswitch_rollback", "from": "vless", "to": "awg3", "user_ip": "10.0.0.3"},
        ])

        self.assertEqual(rollback["rollback_required"], 1)
        self.assertEqual(rollback["rollback_completed"], 1)
        self.assertEqual(rollback["rollback_success_rate"], 100.0)
        self.assertEqual(rollback["rollback_confidence"], 100.0)
        self.assertEqual(rollback["validation_status"], "VALIDATED")

    def test_prediction_confidence_requires_accuracy_and_forecast_confidence(self):
        low_confidence = platform.prediction_accuracy_model(
            forecasts=[{"channel": "awg0", "forecast_quality": 90, "confidence": 0.35}],
            actuals=[{"channel": "awg0", "quality": 90}],
        )
        high_confidence = platform.prediction_accuracy_model(
            forecasts=[{"channel": "awg0", "forecast_quality": 90, "confidence": 0.9}],
            actuals=[{"channel": "awg0", "quality": 90}],
        )

        self.assertEqual(low_confidence["forecast_accuracy"], 100.0)
        self.assertLess(low_confidence["prediction_confidence"], 70.0)
        self.assertGreaterEqual(high_confidence["prediction_confidence"], 70.0)
        self.assertEqual(high_confidence["validation_status"], "VALIDATED")

    def test_governed_staging_shadow_lifecycle_is_virtual_only(self):
        lifecycle = platform.shadow_execution_lifecycle(
            selected_move_count=1,
            requested_blast_radius=1,
            confidence_summary={
                "decision_confidence": 80,
                "prediction_confidence": 75,
                "service_confidence": 85,
                "suitability_confidence": 80,
                "rollback_confidence": 90,
                "blast_radius_confidence": 88,
                "live_calibrated": True,
            },
            production_converged=True,
            operator_approval_present=True,
        )
        self.assertTrue(lifecycle["shadow_execution_complete"])
        self.assertFalse(lifecycle["runtime_mutation_performed"])
        self.assertFalse(lifecycle["users_moved"])
        self.assertFalse(lifecycle["autonomy_enabled"])
        self.assertEqual(lifecycle["authority"]["execution_authority"], "none")

    def test_governed_staging_certification_blocks_without_live_truth(self):
        trust = platform.trust_evolution_summary(
            decision_records=[{"result": "success", "service_delta": 10, "prediction_delta": 2, "blast_radius": 1}],
            prediction_forecasts=[{"channel": "awg0", "forecast_quality": 90, "confidence": 0.9}],
            prediction_actuals=[{"channel": "awg0", "quality": 88}],
            service_rows=[{"channel": "awg0", "aggregate_score": 90, "confidence": 0.9}],
            service_actuals=[],
            candidate_rows=[{"user": "10.7.0.2", "candidates": [{"channel": "awg0", "suitability_score": 90, "confidence": 0.9}]}],
            candidate_outcomes=[{"user": "10.7.0.2", "channel": "awg0", "result": "success"}],
            rollback_records=[{"result": "rollback_success", "rollback_completed": True}],
            blast_radius_records=[{"result": "success", "blast_radius": 1}],
            blast_radius_metrics={"recommendation": {"recommended_budget": 1}},
        )
        cert = platform.governed_staging_certification(
            trust_summary=trust,
            production_converged=False,
            current_runtime_truth_known=False,
            prior_runtime_certification={
                "blast_radius_1_pass": True,
                "blast_radius_2_pass": False,
                "blast_radius_5_pass": True,
                "blast_radius_10_pass": True,
            },
        )
        self.assertTrue(cert["SHADOW_READY"])
        self.assertFalse(cert["OPERATOR_APPROVAL_READY"])
        self.assertFalse(cert["BOUNDED_AUTONOMY_READY"])
        self.assertFalse(cert["PRODUCTION_AUTONOMY_READY"])
        self.assertFalse(cert["AUTONOMY_CERTIFIED"])
        self.assertIn("current_runtime_truth_unknown", cert["BLOCKERS"])
        self.assertIn("ri6_not_production_converged", cert["BLOCKERS"])
        self.assertFalse(cert["runtime_mutation_performed"])

    def test_blast_radius_ladder_requires_prior_certification_and_live_calibration(self):
        ladder = platform.blast_radius_certification_ladder(
            confidence_summary={
                "decision_confidence": 95,
                "rollback_confidence": 95,
                "blast_radius_confidence": 95,
                "live_calibrated": True,
            },
            prior_runtime_certification={
                "blast_radius_1_pass": True,
                "blast_radius_2_pass": False,
                "blast_radius_5_pass": True,
                "blast_radius_10_pass": True,
            },
        )
        self.assertEqual(ladder["max_ready_blast_radius"], 10)
        two = next(row for row in ladder["tiers"] if row["blast_radius"] == 2)
        self.assertFalse(two["ready"])
        self.assertIn("blast_radius_2_pass_not_currently_certified", two["blockers"])
        safety = platform.autonomy_safety_model()
        self.assertFalse(safety["autonomy_enabled"])
        self.assertFalse(safety["runtime_authority_created"])

    def test_production_reality_and_convergence_block_when_commits_diverge(self):
        cert = platform.production_convergence_live_calibration_certification(
            local_commit="d5bf93244502f7a851a21186cfa6ee077773d246",
            github_commit="67ee9965f4d759f9a9d0bb90b893a9c024701307",
            production_commit="67ee9965f4d759f9a9d0bb90b893a9c024701307",
            runtime_truth_status="PARTIAL",
            state_truth_status="KNOWN",
            runtime_access_status="CONFIGURED_WITH_BLOCKERS",
            components={
                "RI4.B": True,
                "RI4.CD": True,
                "RI5": True,
                "INTELLIGENCE_PLATFORM": True,
                "RI6": True,
                "GOVERNED_STAGING": True,
            },
            production_snapshots_loaded=False,
            live_outcomes=[],
        )
        self.assertFalse(cert["production_truth_known"])
        self.assertFalse(cert["ri6_production_converged"])
        self.assertFalse(cert["governed_staging_production_converged"])
        self.assertFalse(cert["shadow_runtime_certified"])
        self.assertTrue(cert["live_outcome_collection_ready"])
        self.assertTrue(cert["live_calibration_ready"])
        self.assertTrue(cert["shadow_accuracy_framework_ready"])
        self.assertFalse(cert["operator_visible_ready"])
        self.assertFalse(cert["operator_approval_ready"])
        self.assertFalse(cert["bounded_autonomy_ready"])
        self.assertFalse(cert["production_autonomy_ready"])
        self.assertFalse(cert["runtime_mutation_performed"])
        self.assertFalse(cert["users_moved"])
        self.assertFalse(cert["autoswitch_apply_performed"])
        self.assertFalse(cert["deploy_performed"])
        self.assertIn("local_github_production_commit_mismatch", cert["BLOCKERS"])
        self.assertIn("production_runtime_truth_not_known", cert["BLOCKERS"])

    def test_live_outcome_and_calibration_reuse_existing_truth_sources(self):
        outcome = platform.live_outcome_collection_model()
        self.assertTrue(outcome["ready"])
        self.assertFalse(outcome["new_truth_source_created"])
        self.assertFalse(outcome["new_snapshot_root_created"])
        self.assertIn("runtime audit logs", outcome["reused_sources"])

        calibration = platform.live_calibration_model()
        self.assertTrue(calibration["ready"])
        self.assertFalse(calibration["calibrated"])
        self.assertEqual(calibration["outcomes_seen"], 0)
        self.assertFalse(calibration["runtime_mutation_performed"])

        strategy = platform.outcome_snapshot_strategy()
        self.assertFalse(strategy["new_snapshot_root_created"])
        self.assertFalse(strategy["new_snapshot_family_required_now"])

    def test_shadow_runtime_and_accuracy_are_framework_ready_but_not_certified_without_live_evidence(self):
        shadow = platform.production_shadow_runtime_certification(
            production_truth_known=False,
            production_snapshots_loaded=False,
        )
        self.assertFalse(shadow["shadow_runtime_certified"])
        self.assertFalse(shadow["runtime_mutation_performed"])
        self.assertFalse(shadow["users_moved"])
        self.assertIn("production_truth_not_known", shadow["blockers"])
        self.assertIn("production_snapshots_not_loaded", shadow["blockers"])

        accuracy = platform.shadow_accuracy_certification(evidence_count=0)
        self.assertTrue(accuracy["framework_ready"])
        self.assertFalse(accuracy["shadow_accuracy_certified"])
        self.assertIn("live_shadow_outcome_evidence_missing", accuracy["blockers"])

    def test_production_duplication_performance_and_failure_models_remain_read_only(self):
        duplication = platform.production_duplication_audit()
        self.assertFalse(duplication["duplicate_planner"])
        self.assertFalse(duplication["duplicate_shadow_runtime"])
        self.assertFalse(duplication["new_runtime_authority_created"])
        self.assertTrue(duplication["outcome_collection_reuses_existing_audit"])

        failure = platform.production_failure_certification()
        self.assertTrue(failure["fail_closed_certified"])
        self.assertFalse(failure["runtime_mutation_performed"])

        performance = platform.production_performance_certification()
        self.assertTrue(performance["performance_ready"])
        self.assertTrue(performance["live_calibration_off_runtime"])
        self.assertFalse(performance["runtime_mutation_performed"])

    def test_shadow_recommendation_model_is_operator_visible_and_non_executing(self):
        user = {
            "user": "10.7.0.11",
            "current_channel": "awg1",
            "candidates": [
                {
                    "egress": "awg1",
                    "eligible": True,
                    "service_suitability": {"aggregate_score": 72.0, "confidence": 0.7},
                    "quality_decision": {"hist_1h_avg_mbps": 12.0, "hist_1h_min_mbps": 8.0, "hist_1h_stability": 0.55},
                    "routing_intelligence": {"advisory_score": 60.0},
                },
                {
                    "egress": "awg3",
                    "eligible": True,
                    "service_suitability": {"aggregate_score": 96.0, "confidence": 0.9},
                    "quality_decision": {"hist_1h_avg_mbps": 35.0, "hist_1h_min_mbps": 25.0, "hist_1h_stability": 0.9},
                    "routing_intelligence": {"advisory_score": 85.0},
                    "trust": {"score": 80.0},
                    "prediction": {"score": 78.0},
                },
            ],
        }
        recommendation = platform.shadow_recommendation_for_user(
            user,
            production_truth_known=True,
            snapshot_gate={
                "stop_required": False,
                "results": {"service-scores": {"confidence": 0.9}, "trust-summaries": {"confidence": 1.0}},
            },
        )
        self.assertEqual(recommendation["recommended_channel"], "awg3")
        self.assertEqual(recommendation["recommendation"], "move_recommended_shadow_only")
        self.assertTrue(recommendation["operator_visible"])
        self.assertFalse(recommendation["approval_ready"])
        self.assertFalse(recommendation["hypothetical_execution"]["would_execute"])
        self.assertFalse(recommendation["runtime_mutation_performed"])
        self.assertFalse(recommendation["users_moved"])
        self.assertFalse(recommendation["autoswitch_apply_performed"])
        self.assertEqual(recommendation["authority"]["execution_authority"], "none")
        for key in ("why", "why_now", "why_this_channel", "why_not_current", "why_confidence", "why_risk"):
            self.assertTrue(recommendation[key])

    def test_production_shadow_pipeline_reuses_planner_cycle_and_blocks_approval_on_snapshot_stop(self):
        planner_cycle = {
            "operation": {"operation_id": "runtime_autoswitch_test", "selected_move_count": 0},
            "routing_brain": {
                "snapshot_gate": {
                    "stop_required": True,
                    "results": {"service-scores": {"confidence": 0.9}},
                }
            },
            "users": [
                {
                    "user": "10.7.0.11",
                    "current_channel": "awg1",
                    "candidates": [
                        {
                            "egress": "awg3",
                            "eligible": True,
                            "service_suitability": {"aggregate_score": 95.0, "confidence": 0.9},
                            "quality_decision": {"hist_1h_avg_mbps": 40.0, "hist_1h_min_mbps": 30.0, "hist_1h_stability": 0.95},
                            "routing_intelligence": {"advisory_score": 85.0},
                        }
                    ],
                }
            ],
        }
        pipeline = platform.production_shadow_execution_pipeline(planner_cycle, production_truth_known=True)
        self.assertEqual(pipeline["recommendation_count"], 1)
        self.assertIn("snapshot_gate_stop_required", pipeline["blockers"])
        self.assertFalse(pipeline["runtime_mutation_performed"])
        self.assertFalse(pipeline["users_moved"])

        operator_model = platform.operator_visible_recommendation_model(pipeline)
        self.assertEqual(operator_model["operator_visible_count"], 1)
        self.assertFalse(operator_model["approval_buttons_enabled"])
        self.assertFalse(operator_model["execution_buttons_enabled"])

        approval = platform.approval_workflow_readiness_model(pipeline)
        self.assertFalse(approval["operator_approval_ready"])
        self.assertIn("snapshot_gate_stop_required", approval["blockers"])

    def test_production_shadow_recommendation_certification_never_grants_autonomy(self):
        planner_cycle = {
            "operation": {"operation_id": "runtime_autoswitch_test", "selected_move_count": 0},
            "routing_brain": {"snapshot_gate": {"stop_required": False}},
            "users": [
                {
                    "user": "10.7.0.11",
                    "current_channel": "awg1",
                    "candidates": [
                        {
                            "egress": "awg3",
                            "eligible": True,
                            "service_suitability": {"aggregate_score": 95.0, "confidence": 0.9},
                            "quality_decision": {"hist_1h_avg_mbps": 40.0, "hist_1h_min_mbps": 30.0, "hist_1h_stability": 0.95},
                            "routing_intelligence": {"advisory_score": 85.0},
                            "trust": {"score": 80.0},
                            "prediction": {"score": 78.0},
                        }
                    ],
                }
            ],
        }
        cert = platform.production_shadow_recommendation_certification(
            planner_cycle,
            production_truth_known=True,
            production_truth_aligned=True,
            live_outcomes=[],
        )
        self.assertTrue(cert["recommendation_engine_implemented"])
        self.assertTrue(cert["operator_visible_model_ready"])
        self.assertTrue(cert["operator_visible_ready"])
        self.assertFalse(cert["operator_approval_ready"])
        self.assertFalse(cert["bounded_autonomy_ready"])
        self.assertFalse(cert["production_autonomy_ready"])
        self.assertFalse(cert["runtime_mutation_performed"])
        self.assertFalse(cert["users_moved"])
        self.assertFalse(cert["autoswitch_apply_performed"])
        self.assertIn("live_outcome_baseline_missing", cert["BLOCKERS"])


if __name__ == "__main__":
    unittest.main()
