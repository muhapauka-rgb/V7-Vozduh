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
        self.write_snapshot(root, "candidate-suitability-summary", [
            {
                "user": "10.7.0.2",
                "candidates": [
                    {"channel": "awg0", "suitability_score": 80, "confidence": 0.6},
                ],
            },
            {
                "user": "10.7.0.3",
                "candidates": [
                    {"channel": "vless", "suitability_score": 70, "confidence": 0.4},
                ],
            },
        ])
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
                "learning_records_count": 1,
            },
            "decision_outcome_learning": {
                "schema_version": "v7.decision-outcome-learning.model.v1",
                "outcome_quality_counts": {"SUCCESS": 1, "PARTIAL_SUCCESS": 0, "FAILED": 0, "UNKNOWN": 0},
                "effectiveness": {
                    "recommendation_correct_rate": 1.0,
                    "service_improved_rate": 1.0,
                    "rollback_rate": 0.0,
                    "fit_prediction_correct_rate": 1.0,
                    "recovery_prediction_correct_rate": 0.0,
                    "prediction_correct_rate": 1.0,
                },
                "knowledge_growth": {
                    "knowledge_gained": 1,
                    "knowledge_improved": ["Decision Outcome", "Suitability", "Prediction"],
                    "knowledge_degraded": [],
                    "knowledge_unchanged_count": 1,
                },
                "rows": [],
                "runtime_mutation_performed": False,
                "users_moved": 0,
                "apply_executed": False,
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
        self.assertEqual(
            second["canary_proximity"]["risk_tier_review"]["nearest_reachable_status"],
            "MARGINAL_OPERATOR_REVIEW",
        )
        self.assertEqual(
            second["canary_proximity"]["risk_tier_review"]["autonomous_one_user_status"],
            "NO_GO",
        )
        self.assertFalse(second["canary_proximity"]["risk_tier_review"]["apply_executed"])
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
        self.assertEqual(second["evidence_sufficiency"]["verdict"], "MIXED")
        self.assertIn("prediction_matches", second["evidence_sufficiency"]["low_attribution_sources"])
        self.assertIn("candidate_outcomes", second["evidence_sufficiency"]["insufficient_sources"])
        self.assertIn("service_outcomes", second["evidence_sufficiency"]["insufficient_sources"])
        self.assertEqual(
            second["source_confidence_collection_plan"]["fastest_real_growth_path"][0]["source"],
            "service_outcomes",
        )
        self.assertFalse(second["source_confidence_collection_plan"]["fastest_real_growth_path"][0]["runtime_apply_allowed"])
        reality = second["confidence_reality_audit"]
        self.assertEqual(reality["final_classification"], "CONFIDENCE_MIXED")
        self.assertIn("Prediction", reality["undervalued_sources"])
        self.assertIn("Service", reality["fair_sources"])
        self.assertEqual(reality["required_real_evidence"]["prediction"]["current_matched"], 1)
        self.assertGreaterEqual(
            reality["required_real_evidence"]["suitability"]["missing_outcomes_to_full_coverage"],
            1,
        )
        self.assertTrue(reality["new_real_world_outcomes_required"])
        self.assertFalse(reality["can_confidence_grow_materially_without_new_runtime_actions"])
        outcome_inventory = second["real_outcome_source_inventory"]
        self.assertIn("service_outcomes", outcome_inventory["acceleration_summary"]["acceleratable"])
        self.assertIn("feedback_outcomes", outcome_inventory["acceleration_summary"]["acceleratable"])
        self.assertIn("candidate_outcomes", outcome_inventory["acceleration_summary"]["wait_for_reality"])
        self.assertIn("governed_outcomes", outcome_inventory["acceleration_summary"]["blocked"])
        projection = second["real_outcome_growth_projection"]
        self.assertTrue(projection["projection_only"])
        self.assertTrue(projection["uses_current_formulas_only"])
        self.assertFalse(projection["synthetic_evidence_created"])
        self.assertEqual([row["additional_real_outcome_cycles"] for row in projection["projections"]], [10, 25, 50])
        first_projection = projection["projections"][0]
        self.assertGreater(first_projection["projected_service_confidence"], projection["current"]["service_confidence"])
        self.assertGreater(first_projection["projected_prediction_confidence"], projection["current"]["prediction_confidence"])
        self.assertGreaterEqual(first_projection["converted_missing_candidate_outcomes"], 1)
        self.assertEqual(first_projection["projected_suitability_scope"], "visible_rows_with_full_coverage_counter")
        self.assertEqual(first_projection["known_candidate_count"], 2)
        self.assertEqual(first_projection["known_candidate_outcomes"], 1)
        self.assertEqual(first_projection["known_missing_candidate_outcomes"], 1)
        self.assertEqual(first_projection["visible_suitability_rows"], 2)
        self.assertFalse(projection["canary_can_start_now"])
        leverage = second["outcome_leverage_model"]
        self.assertEqual(leverage["schema_version"], "v7.autonomy-trust.outcome-leverage-model.v1")
        self.assertEqual(leverage["final_verdict"], "MIXED_PATH")
        self.assertNotEqual(leverage["highest_leverage"]["activity"], "governed_one_user_canary")
        self.assertFalse(leverage["governed_canary_analysis"]["is_automatically_best_next_action"])
        self.assertTrue(leverage["safe_existing_owner_improvement_implemented"])
        self.assertFalse(leverage["synthetic_evidence_created"])
        self.assertFalse(leverage["runtime_mutation_performed"])
        self.assertFalse(leverage["apply_executed"])
        self.assertEqual(leverage["users_moved"], 0)
        self.assertFalse(second["runtime_mutation_performed"])
        self.assertFalse(second["apply_executed"])
        self.assertEqual(second["users_moved"], 0)
        candidate_reality = second["candidate_outcome_reality_collection"]
        self.assertEqual(candidate_reality["coverage"]["candidate_count"], 2)
        self.assertEqual(candidate_reality["coverage"]["candidate_outcomes_consumed"], 0)
        self.assertEqual(candidate_reality["coverage"]["missing_candidate_outcomes"], 2)
        self.assertEqual(candidate_reality["missing_outcome_analysis"]["never_happened"], 2)
        self.assertFalse(candidate_reality["acceleration"]["synthetic_outcomes_allowed"])
        self.assertFalse(candidate_reality["acceleration"]["runtime_apply_allowed_in_this_phase"])
        self.assertEqual(candidate_reality["users_moved"], 0)

    def test_candidate_outcome_reality_classifies_missing_candidate_coverage(self):
        candidate_snapshot = {
            "items": [
                {
                    "user": "10.7.0.2",
                    "candidates": [
                        {"channel": "awg0", "suitability_score": 80, "confidence": 0.6},
                    ],
                },
                {
                    "user": "10.7.0.3",
                    "candidates": [
                        {"channel": "vless", "suitability_score": 70, "confidence": 0.4},
                    ],
                },
                {
                    "user": "10.7.0.4",
                    "candidates": [
                        {"channel": "wireguard", "suitability_score": 90, "confidence": 0.7},
                    ],
                },
            ]
        }
        decision_records = [
            {
                "selected_moves": [{"user": "10.7.0.2", "target": "awg0"}],
                "result": "success",
                "status": "applied",
            },
            {
                "selected_moves": [{"user": "10.7.0.3", "target": "vless"}],
                "status": "preview_only",
            },
        ]

        collection = accel.build_candidate_outcome_reality_collection(
            candidate_suitability_snapshot=candidate_snapshot,
            decision_records=decision_records,
            floor_forensics={
                "component_values": {"suitability_confidence": 27.7, "prediction_confidence": 39.6},
                "floor_values": {"confidence": {"current": 45.8}, "trust": {"current": 54.6}},
            },
            increments=[1, 2],
        )

        self.assertEqual(collection["coverage"]["candidate_count"], 3)
        self.assertEqual(collection["coverage"]["candidate_outcomes_consumed"], 1)
        self.assertEqual(collection["coverage"]["missing_candidate_outcomes"], 2)
        self.assertEqual(collection["missing_outcome_analysis"]["happened_but_not_captured"], 1)
        self.assertEqual(collection["missing_outcome_analysis"]["never_happened"], 1)
        self.assertEqual(collection["missing_outcome_analysis"]["captured_but_not_consumed"], 0)
        self.assertEqual(collection["readiness_impact"]["exact_outcome_deficit_blocks_canary"], 0)
        self.assertEqual(collection["readiness_impact"]["inventory_deficit_supporting_signal"], 2)
        self.assertFalse(collection["readiness_impact"]["inventory_deficit_is_mandatory_certification_requirement"])
        self.assertEqual(collection["readiness_impact"]["signal_category"], "INVENTORY_SIGNAL")
        self.assertEqual(collection["diversity"]["all_candidates"]["unique_channels"], 3)
        self.assertEqual(collection["growth_model"]["projections"][0]["converted_missing_candidate_outcomes"], 1)
        self.assertFalse(collection["runtime_mutation_performed"])
        self.assertFalse(collection["apply_executed"])
        self.assertEqual(collection["users_moved"], 0)

    def test_growth_projection_keeps_full_missing_candidate_counter_when_rows_are_truncated(self):
        floor_forensics = {
            "component_values": {
                "decision_confidence": 50,
                "service_confidence": 40,
                "suitability_confidence": 28,
                "prediction_confidence": 35,
                "blast_radius_confidence": 100,
            },
            "floor_values": {
                "confidence": {"current": 39},
                "trust": {"current": 54},
            },
            "prediction_root_cause": {
                "forecasts_seen": 21,
                "matched_rows": 21,
                "forecast_accuracy": 93,
                "mean_forecast_confidence": 0.38,
            },
            "service_root_cause": {"rows_seen": 21},
            "suitability_root_cause": {
                "candidates_seen": 156,
                "outcomes_seen": 83,
            },
            "raw_rows": {
                "suitability": [
                    {"key": "10.7.0.2:awg0", "outcome_seen": False, "correctness": 40, "confidence": 0.25},
                ],
            },
        }
        projection = accel.build_real_outcome_growth_projection(
            floor_forensics=floor_forensics,
            confidence_reality_audit={
                "required_real_evidence": {
                    "suitability": {
                        "current_candidates": 156,
                        "current_outcomes": 83,
                        "missing_outcomes_to_full_coverage": 73,
                    }
                }
            },
            operator_comparisons={"current": {"earned_confidence": 45}, "growth_projection": {"rows": []}},
            increments=[10],
        )

        row = projection["projections"][0]
        self.assertEqual(row["visible_suitability_rows"], 1)
        self.assertEqual(row["visible_converted_missing_candidate_outcomes"], 1)
        self.assertEqual(row["visible_missing_candidate_outcomes_remaining"], 0)
        self.assertEqual(row["known_candidate_count"], 156)
        self.assertEqual(row["known_candidate_outcomes"], 83)
        self.assertEqual(row["known_missing_candidate_outcomes"], 73)
        self.assertEqual(row["converted_missing_candidate_outcomes"], 10)
        self.assertEqual(row["missing_candidate_outcomes_remaining"], 63)

    def test_outcome_leverage_model_ranks_real_outcome_paths_without_authority(self):
        floor_forensics = {
            "component_values": {
                "decision_confidence": 50,
                "service_confidence": 40,
                "suitability_confidence": 28,
                "prediction_confidence": 35,
                "blast_radius_confidence": 100,
            },
            "floor_values": {
                "confidence": {"current": 39},
                "trust": {"current": 54},
            },
            "prediction_root_cause": {
                "forecasts_seen": 21,
                "matched_rows": 21,
                "forecast_accuracy": 94,
                "mean_forecast_confidence": 0.38,
            },
            "service_root_cause": {"rows_seen": 21},
            "suitability_root_cause": {
                "candidates_seen": 156,
                "outcomes_seen": 84,
            },
        }
        confidence_reality = {
            "required_real_evidence": {
                "prediction": {
                    "additional_matched_rows_needed_if_future_confidence_1_0": 31,
                },
                "service": {
                    "additional_comparable_rows_needed_if_future_confidence_1_0": 22,
                },
                "suitability": {
                    "missing_outcomes_to_full_coverage": 72,
                    "target_correctness_if_mean_confidence_0_85": 82.353,
                },
                "operator": {
                    "first_projection_to_floor": {"earned_confidence": 72.0},
                },
            }
        }
        candidate_reality = {
            "coverage": {"missing_candidate_outcomes": 72},
            "growth_model": {
                "projections": [{
                    "additional_real_candidate_outcomes": 1,
                    "projected_suitability": 28.35,
                    "projected_confidence": 39.18,
                    "projected_trust": 54.12,
                }]
            },
        }
        projection = {
            "current": {
                "confidence": 39,
                "trust": 54,
                "prediction_confidence": 35,
                "suitability_confidence": 28,
            }
        }
        model = accel.build_outcome_leverage_model(
            floor_forensics=floor_forensics,
            confidence_reality_audit=confidence_reality,
            real_outcome_source_inventory={},
            candidate_outcome_reality_collection=candidate_reality,
            real_outcome_growth_projection=projection,
            operator_comparisons={
                "current": {"earned_confidence": 45},
                "growth_projection": {"rows": []},
            },
        )

        self.assertEqual(model["final_verdict"], "MIXED_PATH")
        self.assertEqual(model["highest_leverage"]["activity"], "prediction_outcome_cycle")
        self.assertFalse(model["governed_canary_analysis"]["is_automatically_best_next_action"])
        self.assertGreater(model["governed_canary_analysis"]["expected_suitability_gain"], 0)
        self.assertEqual(model["roadmap_to_tier_2"][0]["status"], "TIER_2_NO_GO")
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["new_truth_source_created"])

    def test_knowledge_quality_read_model_is_deterministic_and_read_only(self):
        first = accel.build_knowledge_quality_read_model(generated_at="2026-06-24T00:00:00+00:00")
        second = accel.build_knowledge_quality_read_model(generated_at="2026-06-24T00:00:00+00:00")

        self.assertEqual(first, second)
        self.assertEqual(first["schema_version"], "v7.knowledge-quality.read-model.v1")
        self.assertTrue(first["read_only"])
        self.assertFalse(first["runtime_mutation_performed"])
        self.assertFalse(first["apply_executed"])
        self.assertEqual(first["users_moved"], 0)
        self.assertFalse(first["synthetic_evidence_created"])
        self.assertFalse(first["new_truth_source_created"])
        self.assertFalse(first["planner_redesigned"])
        self.assertFalse(first["governance_redesigned"])
        self.assertFalse(first["execution_redesigned"])

        expected = {
            "Channel",
            "Service",
            "User Assignment",
            "Route",
            "Capacity",
            "Quality",
            "Failure",
            "Recovery",
            "Decision Outcome",
            "Prediction",
            "Suitability",
            "Trust",
            "Policy",
            "Freshness",
            "Safety",
            "Event",
            "Operator Context",
        }
        observed = {row["object"] for row in first["knowledge_objects"]}
        self.assertEqual(observed, expected)
        valid = set(accel.VALID_KNOWLEDGE_MATURITY_STAGES)
        for row in first["knowledge_objects"]:
            self.assertIn(row["maturity_stage"], valid)
            self.assertEqual(set(row["quality_dimensions"]), set(accel.KNOWLEDGE_QUALITY_DIMENSIONS))
            self.assertEqual(row["score_source"], "docs/reference/V7_KNOWLEDGE_QUALITY_MODEL.md")
            self.assertFalse(row["heuristic_fallback"])
        self.assertEqual(
            sum(item["count"] for item in first["maturity_distribution"].values()),
            len(expected),
        )
        self.assertIn("tier_readiness_knowledge", first)
        self.assertIn("10k_readiness", first)
        self.assertIn("p0_gaps", first)

    def test_fit_model_respects_required_services_and_blocks_bad_service(self):
        freshness = accel.build_freshness_actionability({
            "service-scores": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            "channel-service-scores": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            "user-service-scores": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
        })
        model = accel.build_service_user_sla_fit(
            {
                "users": [
                    {
                        "user": "10.7.0.2",
                        "current_channel": "awg3",
                        "required_services": ["telegram", "youtube"],
                        "candidates": [
                            {"channel": "wireguard", "suitability_score": 91, "required_low": ["youtube"]},
                            {"channel": "vless", "suitability_score": 82},
                        ],
                    }
                ]
            },
            freshness_actionability=freshness,
        )

        row = model["rows"][0]
        self.assertEqual(row["best_channel"], "vless")
        self.assertEqual(row["fit_verdict"], "FIT")
        blocked = {item["channel"]: item for item in row["candidates"]}
        self.assertEqual(blocked["wireguard"]["fit_verdict"], "BLOCKED")
        self.assertIn("youtube", blocked["wireguard"]["missing_requirements"])
        self.assertFalse(model["runtime_mutation_performed"])

    def test_fit_model_respects_policy_capacity_and_stale_service(self):
        stale = accel.build_freshness_actionability({
            "service-scores": {"exists": True, "freshness_state": "STALE", "runtime_behavior": "WARN", "stop_required": False},
        })
        model = accel.build_service_user_sla_fit(
            {
                "users": [
                    {
                        "user": "10.7.0.3",
                        "current_channel": "awg3",
                        "required_services": ["telegram"],
                        "candidates": [
                            {"channel": "awg0", "suitability_score": 95, "capacity_decision": "over_limit"},
                            {"channel": "vless", "suitability_score": 94, "policy_eligible": False},
                        ],
                    }
                ]
            },
            freshness_actionability=stale,
        )

        candidates = {item["channel"]: item for item in model["rows"][0]["candidates"]}
        self.assertEqual(candidates["awg0"]["fit_verdict"], "BLOCKED")
        self.assertIn("capacity_or_load_blocks_fit", candidates["awg0"]["reason"])
        self.assertEqual(candidates["vless"]["fit_verdict"], "BLOCKED")
        self.assertEqual(stale["domains"]["service"]["classification"], "STALE_RECHECK_REQUIRED")

    def test_recovery_requires_staged_admission_not_single_pass(self):
        fresh = accel.build_freshness_actionability({
            "trust-evolution-summaries": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
        })
        model = accel.build_recovery_admission(
            {},
            freshness_actionability=fresh,
            channel_recovery_inputs=[{"channel": "awg0", "lifecycle": "RECOVERING", "successful_checks": 1}],
        )

        row = model["rows"][0]
        self.assertNotEqual(row["admission_state"], "ELIGIBLE")
        self.assertIn("insufficient_successful_checks", row["blockers"])
        self.assertFalse(model["runtime_mutation_performed"])

    def test_anti_flap_blocks_rapid_oscillation(self):
        model = accel.build_anti_flapping([
            {"user": "10.7.0.2", "from": "awg3", "to": "wireguard"},
            {"user": "10.7.0.2", "from": "wireguard", "to": "awg3"},
        ])

        row = model["rows"][0]
        self.assertTrue(row["blocked"])
        self.assertEqual(row["decision_stability"], "BLOCKED_BY_ANTI_FLAP")
        self.assertIn("rapid_reverse_move_detected", row["reasons"])
        self.assertFalse(model["apply_executed"])

    def test_closure_requires_real_outcome_fields(self):
        incomplete = accel.build_decision_outcome_closure([
            {"feedback_id": "f1", "recommendation_id": "r1", "outcome_status": "pending"}
        ])
        complete = accel.build_decision_outcome_closure([
            {
                "recommendation_id": "r1",
                "decision_id": "d1",
                "packet_id": "p1",
                "apply_result": "success",
                "post_action_verification": {"status": "passed"},
                "service_outcome": {"telegram": "ok"},
                "user_outcome": {"user": "10.7.0.2"},
                "learning_record": {"stored": True},
                "outcome_observed_at": "2026-06-24T00:00:00+00:00",
            }
        ])

        self.assertEqual(incomplete["closure_state"], "PARTIAL")
        self.assertGreater(incomplete["summary"]["missing_closure_records"], 0)
        self.assertEqual(complete["closure_state"], "COMPLETE")
        self.assertEqual(complete["summary"]["valid_closures"], 1)
        self.assertFalse(complete["synthetic_outcomes_created"])

    def test_closure_ignores_non_outcome_audit_history(self):
        complete = accel.build_decision_outcome_closure([
            {"user": "10.0.0.2", "channel": "vless", "event_time": "2026-06-24T00:00:00+00:00"},
            {"user": "10.0.0.3", "channel": "awg2", "status": "preview_only"},
            {
                "recommendation_id": "r1",
                "decision_id": "d1",
                "packet_id": "p1",
                "apply_result": "success",
                "post_action_verification": {"status": "passed"},
                "service_outcome": {"telegram": "ok"},
                "user_outcome": {"user": "10.7.0.2"},
                "learning_record": {"stored": True},
                "outcome_observed_at": "2026-06-24T00:01:00+00:00",
            },
        ])

        self.assertEqual(complete["closure_state"], "COMPLETE")
        self.assertEqual(complete["summary"]["source_records_seen"], 3)
        self.assertEqual(complete["summary"]["records_seen"], 1)
        self.assertEqual(complete["summary"]["non_closure_records_ignored"], 2)
        self.assertEqual(complete["summary"]["valid_closures"], 1)

    def test_closure_ignores_explicit_non_executed_dry_run_records(self):
        model = accel.build_decision_outcome_closure([
            {
                "recommendation_id": "r-preview",
                "decision_id": "d-preview",
                "outcome_status": "NO_EXECUTION",
                "execution_mode": "DRY_RUN",
                "runtime_mutation_performed": False,
                "apply_executed": False,
                "users_moved": 0,
            }
        ])

        self.assertEqual(model["closure_state"], "ABSENT")
        self.assertEqual(model["summary"]["records_seen"], 0)
        self.assertEqual(model["summary"]["non_executed_outcome_records_ignored"], 1)

    def test_inventory_exposes_routing_foundation_top_level_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-24T00:00:00+00:00",
            )

        for key in (
            "service_user_sla_fit",
            "decision_outcome_closure",
            "recovery_admission",
            "anti_flapping",
            "freshness_actionability",
            "action_class_freshness_windows",
            "routing_recommendation_readiness",
            "decision_outcome_learning",
            "hard_failure_classification",
            "liveness_evidence_aggregation",
            "hard_failure_policy_windows",
            "soft_degradation_threshold_vocabulary",
            "degradation_signal_policy_mapping",
            "observed_degradation_attribution",
            "v7_native_degradation_response_mapping",
            "service_objective_policy_threshold_binding",
            "recovery_admission_certification",
            "post_admission_observation_windows",
            "recovery_slow_start_progression",
            "org_cohort_identity_policy_integration",
            "next_action_class_stage_certification",
            "service_pool_cohort_blast_radius_scope",
            "all_at_once_promotion_unavailable_verification",
            "stale_read_mutation_blocking",
            "owner_issued_version_lease_pattern",
            "hysteresis_state_change_cost_mapping",
            "hard_failure_override_anti_flap_arbitration",
            "per_user_routing_control_mode",
            "fail_open_fail_closed_action_class_behavior",
        ):
            self.assertIn(key, inventory)
            self.assertFalse(inventory[key]["runtime_mutation_performed"])
            self.assertFalse(inventory[key]["apply_executed"])
            self.assertEqual(inventory[key]["users_moved"], 0)
        self.assertIn("decision_effectiveness", inventory)
        self.assertEqual(inventory["decision_effectiveness"]["recommendation_correct_rate"], 1.0)
        self.assertEqual(inventory["knowledge_growth"]["knowledge_gained"], 1)

    def test_hard_failure_classification_requires_liveness_evidence(self):
        model = accel.build_hard_failure_classification(
            event_rows=[
                {
                    "source": "service_matrix",
                    "channel": "awg0",
                    "status": "DOWN",
                    "message": "all probes failed",
                    "updated_at": "2026-06-25T00:00:00Z",
                    "confidence": 0.9,
                },
                {
                    "source": "telegram_sentinel",
                    "channel": "awg0",
                    "status": "DOWN",
                    "message": "telegram no response",
                    "updated_at": "2026-06-25T00:00:10Z",
                    "confidence": 0.86,
                },
            ],
            freshness_actionability={"domains": {}},
            generated_at="2026-06-25T00:01:00+00:00",
        )

        self.assertEqual(model["schema_version"], "v7.policy-001.hard-failure-classification.v1")
        self.assertEqual(model["classification"], "HARD_FAILURE_CONFIRMED")
        self.assertEqual(model["summary"]["confirmed"], 1)
        row = model["rows"][0]
        self.assertEqual(row["object"], "awg0")
        self.assertEqual(row["classification"], "HARD_FAILURE_CONFIRMED")
        self.assertEqual(row["explicit_liveness_evidence_count"], 2)
        self.assertIn("service_matrix", row["independent_sources"])
        self.assertIn("telegram_sentinel", row["independent_sources"])
        self.assertFalse(row["runtime_apply_allowed"])
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["synthetic_evidence_created"])
        self.assertFalse(model["new_truth_source_created"])

    def test_hard_failure_single_noisy_observation_is_only_suspected(self):
        model = accel.build_hard_failure_classification(
            event_rows=[
                {
                    "source": "service_matrix",
                    "channel": "awg3",
                    "message": "youtube timeout",
                    "updated_at": "2026-06-25T00:00:00Z",
                },
            ],
            freshness_actionability={"domains": {}},
            generated_at="2026-06-25T00:01:00+00:00",
        )

        self.assertEqual(model["classification"], "HARD_FAILURE_SUSPECTED")
        self.assertEqual(model["summary"]["suspected"], 1)
        self.assertTrue(model["rows"][0]["requires_confirmation"])
        self.assertFalse(model["rows"][0]["reaction_allowed_without_policy"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)

    def test_b1_liveness_evidence_aggregation_groups_source_family_and_confidence(self):
        hard_failure = accel.build_hard_failure_classification(
            event_rows=[
                {
                    "source": "service_matrix",
                    "channel": "awg0",
                    "status": "DOWN",
                    "message": "all probes failed",
                    "confidence": 0.9,
                },
                {
                    "source": "telegram_sentinel",
                    "channel": "awg0",
                    "status": "DOWN",
                    "message": "telegram no response",
                    "confidence": 0.86,
                },
                {
                    "source": "quality_compact",
                    "channel": "awg0",
                    "status": "DEGRADED",
                    "message": "quality cannot carry service",
                    "confidence": 0.62,
                },
            ],
            freshness_actionability={"domains": {}},
            generated_at="2026-06-29T00:20:00+00:00",
        )
        aggregation = accel.build_liveness_evidence_aggregation(
            hard_failure_classification=hard_failure,
            snapshot_statuses={
                "service-scores": {
                    "exists": True,
                    "freshness_state": "FRESH",
                    "runtime_behavior": "ALLOW",
                    "stop_required": False,
                    "confidence": 0.9,
                },
                "channel-service-scores": {
                    "exists": True,
                    "freshness_state": "FRESH",
                    "runtime_behavior": "ALLOW",
                    "stop_required": False,
                    "confidence": 0.8,
                },
                "risk-summaries": {
                    "exists": True,
                    "freshness_state": "FRESH",
                    "runtime_behavior": "ALLOW",
                    "stop_required": False,
                    "confidence": 0.7,
                },
            },
            generated_at="2026-06-29T00:21:00+00:00",
        )

        self.assertEqual(aggregation["schema_version"], "v7.b1.liveness-evidence-aggregation.v1")
        self.assertEqual(aggregation["backlog_item"], "B1")
        self.assertEqual(aggregation["summary"]["confirmed_objects"], 1)
        self.assertEqual(aggregation["summary"]["evidence_count"], 3)
        by_family = {row["source_family"]: row for row in aggregation["source_family_rows"]}
        self.assertEqual(by_family["service_matrix"]["owner"], "tools/v7-service-matrix-refresh-all")
        self.assertEqual(by_family["telegram_sentinel"]["owner"], "tools/v7-telegram-sentinel")
        self.assertEqual(by_family["quality_compact"]["owner"], "tools/v7-egress-quality-compact")
        self.assertEqual(by_family["service_matrix"]["average_confidence"], 90.0)
        self.assertEqual(by_family["telegram_sentinel"]["confidence_band"], "HIGH")
        self.assertEqual(by_family["quality_compact"]["policy_relevance"], "quality_degradation_liveness")
        self.assertEqual(aggregation["object_rows"][0]["object"], "awg0")
        self.assertIn("service_matrix", aggregation["object_rows"][0]["source_families"])
        self.assertFalse(aggregation["runtime_mutation_performed"])
        self.assertFalse(aggregation["apply_executed"])
        self.assertEqual(aggregation["users_moved"], 0)
        self.assertFalse(aggregation["authority_expanded"])
        self.assertFalse(aggregation["synthetic_evidence_created"])
        self.assertFalse(aggregation["new_truth_source_created"])

    def test_inventory_exposes_b1_liveness_evidence_aggregation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                event_rows=[
                    {
                        "source": "service_matrix",
                        "channel": "awg0",
                        "status": "DOWN",
                        "message": "all probes failed",
                        "confidence": 0.9,
                    },
                    {
                        "source": "telegram_sentinel",
                        "channel": "awg0",
                        "status": "DOWN",
                        "message": "telegram no response",
                        "confidence": 0.86,
                    },
                ],
                generated_at="2026-06-29T00:22:00+00:00",
            )

        aggregation = inventory["liveness_evidence_aggregation"]
        self.assertEqual(aggregation["backlog_item"], "B1")
        self.assertEqual(aggregation["summary"]["confirmed_object_names"], ["awg0"])
        self.assertGreaterEqual(aggregation["summary"]["source_families"], 2)
        self.assertFalse(aggregation["runtime_mutation_performed"])
        self.assertFalse(aggregation["apply_executed"])
        self.assertEqual(aggregation["users_moved"], 0)

    def test_b2_hard_failure_policy_windows_maps_risk_class_without_timer_change(self):
        freshness = accel.build_freshness_actionability({
            "service-scores": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            "channel-service-scores": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            "user-service-scores": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            "risk-summaries": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            "overview-summary": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            "capacity-forecast-summaries": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            "blast-radius-summaries": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            "prediction-summaries": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            "candidate-suitability-summary": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            "best-available-pool": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            "trust-evolution-summaries": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
        })
        windows = accel.build_action_class_freshness_windows(freshness)
        confirmed = accel.build_hard_failure_classification(
            event_rows=[
                {"source": "service_matrix", "channel": "awg0", "status": "DOWN", "message": "all probes failed", "confidence": 0.9},
                {"source": "telegram_sentinel", "channel": "awg0", "status": "DOWN", "message": "telegram no response", "confidence": 0.86},
            ],
            freshness_actionability=freshness,
        )
        aggregation = accel.build_liveness_evidence_aggregation(
            hard_failure_classification=confirmed,
            snapshot_statuses={
                "service-scores": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
                "channel-service-scores": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            },
        )
        model = accel.build_hard_failure_policy_windows(
            hard_failure_classification=confirmed,
            liveness_evidence_aggregation=aggregation,
            action_class_freshness_windows=windows,
            anti_flapping={"policy": accel.ANTI_FLAP_POLICY, "summary": {"blocked_users": 0}},
        )

        self.assertEqual(model["schema_version"], "v7.b2.hard-failure-policy-windows.v1")
        self.assertEqual(model["backlog_item"], "B2")
        row = model["rows"][0]
        self.assertEqual(row["object"], "awg0")
        self.assertEqual(row["risk_class"], "CRITICAL_CONFIRMED_HARD_FAILURE")
        self.assertEqual(row["selected_action_class"], "channel hard-fail failover")
        self.assertEqual(row["reaction_window_seconds"], 300)
        self.assertTrue(row["policy_window_ready"])
        self.assertFalse(row["timer_changed"])
        self.assertFalse(row["runtime_apply_allowed"])
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])
        self.assertFalse(model["new_truth_source_created"])

    def test_b2_suspected_hard_failure_uses_confirmation_window_and_blocks_fast_path(self):
        suspected = accel.build_hard_failure_classification(
            event_rows=[
                {"source": "service_matrix", "channel": "awg3", "message": "youtube timeout"},
            ],
            freshness_actionability={"domains": {}},
        )
        aggregation = accel.build_liveness_evidence_aggregation(hard_failure_classification=suspected)
        model = accel.build_hard_failure_policy_windows(
            hard_failure_classification=suspected,
            liveness_evidence_aggregation=aggregation,
            anti_flapping={"policy": accel.ANTI_FLAP_POLICY, "summary": {"blocked_users": 1}},
        )

        row = model["rows"][0]
        self.assertEqual(row["risk_class"], "SUSPECTED_HARD_FAILURE")
        self.assertEqual(row["selected_action_class"], "single-user governed candidate failover")
        self.assertIn("anti_flap_blocks_recent_oscillation", row["blockers"])
        self.assertFalse(row["policy_window_ready"])
        self.assertFalse(row["risk_class_changes_runtime"])

    def test_b3_soft_degradation_threshold_vocabulary_aligns_existing_signals(self):
        freshness = accel.build_freshness_actionability({
            "service-scores": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            "channel-service-scores": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            "user-service-scores": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            "prediction-summaries": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
        })
        model = accel.build_soft_degradation_threshold_vocabulary_alignment(
            decision_surface={
                "users": [{
                    "user": "10.7.0.2",
                    "current_channel": "awg0",
                    "recommended_channel": "awg1",
                    "candidates": [
                        {
                            "channel": "awg1",
                            "score": 77,
                            "ctr_state": "DEGRADED",
                            "reasons": ["service_signal_DEGRADED_SERVICE"],
                        }
                    ],
                }]
            },
            service_scores_snapshot={"items": [{"channel": "awg1", "status": "DEGRADED", "score": 77}]},
            channel_service_scores_snapshot={"items": [{"channel": "awg1", "score": {"current": 77, "trend": "degrading"}}]},
            freshness_actionability=freshness,
            anti_flapping={"policy": accel.ANTI_FLAP_POLICY, "summary": {"blocked_users": 0}},
            generated_at="2026-06-29T01:20:00+00:00",
        )

        self.assertEqual(model["schema_version"], "v7.b3.soft-degradation-threshold-vocabulary.v1")
        self.assertEqual(model["backlog_item"], "B3")
        row = {item["object"]: item for item in model["rows"]}["awg1"]
        self.assertEqual(row["canonical_policy"], "POLICY_002_SOFT_DEGRADATION")
        self.assertEqual(row["canonical_policy_result"], "SOFT_DEGRADATION")
        self.assertEqual(row["canonical_decision_action"], "ASK_OPERATOR")
        self.assertIn("tools/v7-users-autoswitch", row["owner_sources"])
        self.assertIn("tools/v7-egress-quality-compact", row["owner_sources"])
        self.assertFalse(row["threshold_values_changed"])
        self.assertFalse(row["formula_changed"])
        self.assertFalse(row["runtime_apply_allowed"])
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])
        self.assertFalse(model["synthetic_evidence_created"])
        self.assertFalse(model["new_truth_source_created"])

    def test_inventory_exposes_b3_soft_degradation_threshold_vocabulary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-29T01:21:00+00:00",
            )

        model = inventory["soft_degradation_threshold_vocabulary"]
        self.assertEqual(model["backlog_item"], "B3")
        self.assertTrue(model["read_only"])
        self.assertEqual(model["summary"]["threshold_changes"], 0)
        self.assertEqual(model["summary"]["formula_changes"], 0)
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)

    def test_b4_degradation_signal_policy_mapping_normalizes_existing_signal_families(self):
        freshness = accel.build_freshness_actionability({
            "service-scores": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            "channel-service-scores": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            "user-service-scores": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            "prediction-summaries": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
        })
        b3 = accel.build_soft_degradation_threshold_vocabulary_alignment(
            decision_surface={
                "users": [{
                    "user": "10.7.0.2",
                    "current_channel": "awg0",
                    "recommended_channel": "awg1",
                    "candidates": [{
                        "channel": "awg1",
                        "score": 77,
                        "ctr_state": "DEGRADED",
                        "reasons": ["service_signal_DEGRADED_SERVICE"],
                    }],
                }]
            },
            service_scores_snapshot={"items": [{"channel": "awg1", "status": "DEGRADED", "score": 77}]},
            channel_service_scores_snapshot={"items": [{"channel": "awg1", "score": {"current": 77, "trend": "degrading"}}]},
            freshness_actionability=freshness,
        )
        model = accel.build_degradation_signal_policy_mapping(
            decision_surface={
                "users": [{
                    "user": "10.7.0.2",
                    "current_channel": "awg0",
                    "recommended_channel": "awg1",
                    "candidates": [{
                        "channel": "awg1",
                        "score": 77,
                        "reasons": ["service_signal_DEGRADED_SERVICE", "latency p95 high"],
                    }],
                }]
            },
            service_scores_snapshot={"items": [{"channel": "awg1", "services": {"instagram": {"ok": False, "status": "DEGRADED", "score": 40}}}]},
            channel_service_scores_snapshot={"items": [{"channel": "awg1", "p95_latency_ms": 1800, "score": {"current": 77, "trend": "degrading"}}]},
            risk_summaries_snapshot={"items": [{"channel": "awg1", "route_safe": False, "reason": "route_class_VIDEO_OPTIMIZED_failed"}]},
            soft_degradation_threshold_vocabulary=b3,
            freshness_actionability=freshness,
            generated_at="2026-06-29T01:45:00+00:00",
        )

        self.assertEqual(model["schema_version"], "v7.b4.degradation-signal-policy-mapping.v1")
        self.assertEqual(model["backlog_item"], "B4")
        families = {row["signal_family"]: row for row in model["signal_family_rows"]}
        self.assertIn("latency", families)
        self.assertIn("service_response", families)
        self.assertIn("route_readiness", families)
        self.assertEqual(families["latency"]["canonical_signal"], "LATENCY_DEGRADATION")
        self.assertEqual(families["service_response"]["canonical_policy_result"], "SOFT_DEGRADATION")
        self.assertEqual(families["route_readiness"]["canonical_decision_action"], "PROBE_ONLY")
        self.assertEqual(model["summary"]["threshold_changes"], 0)
        self.assertEqual(model["summary"]["formula_changes"], 0)
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])
        self.assertFalse(model["synthetic_evidence_created"])
        self.assertFalse(model["new_truth_source_created"])

    def test_inventory_exposes_b4_degradation_signal_policy_mapping(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-29T01:46:00+00:00",
            )

        model = inventory["degradation_signal_policy_mapping"]
        self.assertEqual(model["backlog_item"], "B4")
        self.assertTrue(model["read_only"])
        self.assertEqual(model["summary"]["threshold_changes"], 0)
        self.assertEqual(model["summary"]["formula_changes"], 0)
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)

    def test_b5_observed_degradation_attribution_joins_active_and_passive_evidence(self):
        b4 = accel.build_degradation_signal_policy_mapping(
            service_scores_snapshot={
                "items": [{
                    "channel": "awg1",
                    "services": {"instagram": {"ok": False, "status": "DEGRADED", "score": 40}},
                }]
            },
            channel_service_scores_snapshot={
                "items": [{"channel": "awg1", "p95_latency_ms": 1800, "score": {"current": 51, "trend": "degrading"}}]
            },
            generated_at="2026-06-29T02:05:00+00:00",
        )
        model = accel.build_observed_degradation_attribution(
            service_scores_snapshot={
                "items": [{
                    "channel": "awg1",
                    "services": {"instagram": {"ok": False, "status": "DEGRADED", "score": 40}},
                }]
            },
            channel_service_scores_snapshot={
                "items": [{"channel": "awg1", "p95_latency_ms": 1800, "score": {"current": 51, "trend": "degrading"}}]
            },
            degradation_signal_policy_mapping=b4,
            decision_outcome_learning={
                "knowledge_growth": {"knowledge_degraded": ["service_signal"]},
                "outcome_quality_counts": {"FAILED": 1},
            },
            decision_records=[{
                "decision_id": "d-b5",
                "channel": "awg1",
                "outcome_quality": {"service_impact": "DEGRADED"},
                "service_delta": {"instagram": "failed after degraded route"},
            }],
            generated_at="2026-06-29T02:06:00+00:00",
        )

        self.assertEqual(model["schema_version"], "v7.b5.observed-degradation-attribution.v1")
        self.assertEqual(model["backlog_item"], "B5")
        rows = {row["object"]: row for row in model["rows"]}
        self.assertIn("awg1", rows)
        self.assertEqual(rows["awg1"]["attribution_state"], "ACTIVE_AND_PASSIVE_OBSERVED")
        self.assertGreater(rows["awg1"]["active_evidence_count"], 0)
        self.assertGreater(rows["awg1"]["passive_evidence_count"], 0)
        self.assertFalse(rows["awg1"]["root_cause_claimed"])
        self.assertEqual(model["summary"]["root_cause_claims"], 0)
        self.assertEqual(model["summary"]["threshold_changes"], 0)
        self.assertEqual(model["summary"]["formula_changes"], 0)
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])
        self.assertFalse(model["synthetic_evidence_created"])
        self.assertFalse(model["new_truth_source_created"])

    def diagnosis_record(self, **overrides):
        payload = {
            "subject": {"type": "execution_block", "id": "domain_11_gap"},
            "source_object": "docs/reports/research/V7_STAGE1_DIAGNOSIS_RECOVERY_DISCOVERY.md#root-cause",
            "evidence_refs": [{
                "type": "report",
                "path": "docs/reports/research/V7_STAGE1_DIAGNOSIS_RECOVERY_DISCOVERY.md",
                "section": "Root Cause of NOT CERTIFIED",
            }],
            "diagnosis_status": "PROVEN",
            "symptom": {
                "type": "certification_gap",
                "value": "Domain 11 missing executable diagnosis projection",
                "producer": "V7_PHASE1_DOMAIN_CERTIFICATION.md",
            },
            "root_cause": "diagnosis_owner_resolution_record_missing",
            "root_cause_proven": True,
            "unknown_state": "NONE",
            "blocking_owner": "admin_core.autonomy_trust_acceleration",
            "owner_resolution_state": "RESOLVED",
            "terminal_classification": "IMPLEMENTATION_MISSING",
            "required_resolution": "implement_v7_diagnosis_owner_resolution_record",
            "confidence": "HIGH",
            "evidence_quality": "HIGH",
            "generated_at": "2026-07-07T00:00:00+00:00",
        }
        payload.update(overrides)
        return accel.build_diagnosis_owner_resolution_record(**payload)

    def test_diagnosis_owner_resolution_record_is_valid_read_only_contract(self):
        record = self.diagnosis_record()
        validation = accel.validate_diagnosis_owner_resolution_record(record)

        self.assertEqual(record["schema_version"], "v7.diagnosis-owner-resolution.v1")
        self.assertTrue(record["read_only"])
        self.assertEqual(record["producer"], "admin_core.autonomy_trust_acceleration.build_diagnosis_owner_resolution_record")
        self.assertTrue(validation["valid"])
        self.assertEqual(validation["errors"], [])
        self.assertFalse(record["mutation_boundary"]["runtime_apply_allowed"])
        self.assertFalse(record["mutation_boundary"]["authority_expanded"])
        self.assertFalse(record["mutation_boundary"]["restore_barrier_written"])
        self.assertEqual(record["mutation_boundary"]["users_moved"], 0)
        self.assertFalse(record["mutation_boundary"]["synthetic_evidence_created"])
        self.assertFalse(record["mutation_boundary"]["new_owner_created"])
        self.assertFalse(record["mutation_boundary"]["new_runtime_created"])
        self.assertFalse(record["mutation_boundary"]["new_planner_created"])

    def test_diagnosis_owner_resolution_record_preserves_unknown_without_fake_root_cause(self):
        record = accel.build_diagnosis_owner_resolution_record(
            subject={"type": "execution_block", "id": "unknown_gap"},
            source_object="engineering_report:unknown",
            evidence_refs=[],
            diagnosis_status="NO_EVIDENCE",
            symptom={
                "type": "blocking_owner",
                "value": "owner not proven",
                "producer": "unit-test",
            },
            root_cause="tempting_but_unproven_guess",
            root_cause_proven=False,
            blocking_owner="UNKNOWN",
            terminal_classification="UNKNOWN",
            required_resolution="collect_missing_evidence",
            generated_at="2026-07-07T00:00:00+00:00",
        )
        validation = accel.validate_diagnosis_owner_resolution_record(record)

        self.assertEqual(record["root_cause"], "UNKNOWN")
        self.assertFalse(record["root_cause_proven"])
        self.assertEqual(record["unknown_state"], "MISSING_EVIDENCE")
        self.assertTrue(validation["valid"])

    def test_diagnosis_owner_resolution_terminal_classifications_are_canonical(self):
        for terminal in [
            "POLICY_PROHIBITION",
            "IMPLEMENTATION_MISSING",
            "OWNER_INVOCATION_MISSING",
            "IMPLEMENTATION_DEFECT",
            "CANONICAL_IMPOSSIBILITY",
        ]:
            with self.subTest(terminal=terminal):
                record = self.diagnosis_record(terminal_classification=terminal)
                validation = accel.validate_diagnosis_owner_resolution_record(record)
                self.assertTrue(validation["valid"], validation["errors"])
                self.assertEqual(record["terminal_classification"], terminal)
                self.assertEqual(record["owner_resolution_state"], "RESOLVED")

    def test_diagnosis_owner_resolution_first_divergence_requires_evidence_fields(self):
        record = self.diagnosis_record(
            first_divergence={
                "producer": "Planner",
                "consumer": "Runtime",
                "field": "selected_moves_after_gate",
                "before": 1,
                "after": 0,
                "evidence_ref": "docs/reports/research/domain11.md#first-divergence",
            }
        )
        self.assertTrue(accel.validate_diagnosis_owner_resolution_record(record)["valid"])

        invalid = json.loads(json.dumps(record))
        invalid["first_divergence"] = {"producer": "Planner"}
        validation = accel.validate_diagnosis_owner_resolution_record(invalid)
        self.assertFalse(validation["valid"])
        self.assertIn("first_divergence_missing:evidence_ref", validation["errors"])

    def test_diagnosis_owner_resolution_validator_rejects_unsafe_or_unproven_records(self):
        record = self.diagnosis_record()

        wrong_schema = json.loads(json.dumps(record))
        wrong_schema["schema_version"] = "wrong"
        self.assertIn(
            "invalid_schema_version",
            accel.validate_diagnosis_owner_resolution_record(wrong_schema)["errors"],
        )

        no_evidence = json.loads(json.dumps(record))
        no_evidence["evidence_refs"] = []
        self.assertIn(
            "proven_root_cause_requires_evidence_refs",
            accel.validate_diagnosis_owner_resolution_record(no_evidence)["errors"],
        )

        bad_terminal = json.loads(json.dumps(record))
        bad_terminal["terminal_classification"] = "BLOCKED_BY_SAFETY_OWNER"
        self.assertIn(
            "invalid_terminal_classification",
            accel.validate_diagnosis_owner_resolution_record(bad_terminal)["errors"],
        )

        mutation = json.loads(json.dumps(record))
        mutation["mutation_boundary"]["runtime_apply_allowed"] = True
        self.assertIn(
            "mutation_boundary_violation:runtime_apply_allowed",
            accel.validate_diagnosis_owner_resolution_record(mutation)["errors"],
        )

        new_owner = json.loads(json.dumps(record))
        new_owner["blocking_owner"] = "NEW_OWNER"
        self.assertIn(
            "blocking_owner_must_reuse_existing_owner",
            accel.validate_diagnosis_owner_resolution_record(new_owner)["errors"],
        )

    def test_diagnosis_owner_resolution_consumer_projection_uses_same_record(self):
        record = self.diagnosis_record()
        projection = accel.build_diagnosis_owner_resolution_consumer_projection(record)

        self.assertEqual(projection["schema_version"], "v7.diagnosis-owner-resolution.consumer-projection.v1")
        self.assertTrue(projection["validation"]["valid"])
        self.assertEqual(projection["projections"]["omp"]["source_record_id"], record["record_id"])
        self.assertEqual(
            projection["projections"]["current_program_state"]["blocking_owner"],
            record["blocking_owner"],
        )
        self.assertEqual(
            projection["projections"]["current_program_state"]["terminal_root_cause"],
            record["root_cause"],
        )
        self.assertFalse(projection["projections"]["production_maturity"]["authority_granted"])
        self.assertFalse(projection["projections"]["governance_check"]["recompute_diagnosis_truth"])
        self.assertTrue(projection["projections"]["engineering_reports"]["embeddable_record"])
        self.assertTrue(projection["projections"]["future_certification"]["recovery_gap_closed"])

    def test_diagnosis_owner_resolution_validator_accepts_compatible_extensions(self):
        record = self.diagnosis_record()
        record["future_optional_field"] = {"ignored_by_v1": True}
        validation = accel.validate_diagnosis_owner_resolution_record(record)

        self.assertTrue(validation["valid"])
        self.assertEqual(validation["errors"], [])

    def test_inventory_exposes_b5_observed_degradation_attribution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[{
                    "decision_id": "d-b5",
                    "channel": "awg1",
                    "outcome_quality": {"service_impact": "DEGRADED"},
                }],
                generated_at="2026-06-29T02:07:00+00:00",
            )

        model = inventory["observed_degradation_attribution"]
        self.assertEqual(model["backlog_item"], "B5")
        self.assertTrue(model["read_only"])
        self.assertEqual(model["summary"]["root_cause_claims"], 0)
        self.assertEqual(model["summary"]["threshold_changes"], 0)
        self.assertEqual(model["summary"]["formula_changes"], 0)
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)

    def test_b6_maps_circuit_breaker_and_outlier_ejection_to_v7_actions(self):
        observed = {
            "rows": [{
                "object": "awg1",
                "attribution_state": "ACTIVE_AND_PASSIVE_OBSERVED",
                "signal_families": ["latency", "service_response"],
                "owners": ["tools/v7-service-matrix-refresh-all"],
                "sources": ["service_scores"],
            }],
        }
        model = accel.build_v7_native_degradation_response_mapping(
            decision_surface={
                "users": [{
                    "user": "10.7.0.2",
                    "current_channel": "awg0",
                    "recommended_channel": "awg1",
                    "candidates": [
                        {"channel": "awg1", "ctr_state": "DEGRADED"},
                        {"channel": "awg2", "ctr_state": "QUARANTINED"},
                    ],
                }]
            },
            observed_degradation_attribution=observed,
            degradation_signal_policy_mapping={
                "evidence_rows": [{
                    "object": "awg1",
                    "signal_family": "latency",
                    "source": "operator_decision_surface",
                    "owner": "admin_core.operator_decision_surface",
                }]
            },
            anti_flapping={"summary": {"blocked_users": 0}},
            recovery_admission={"summary": {"blocked_or_quarantined": 1}},
            generated_at="2026-06-29T02:30:00+00:00",
        )

        self.assertEqual(model["schema_version"], "v7.b6.v7-native-degradation-response-mapping.v1")
        self.assertEqual(model["backlog_item"], "B6")
        rows = {row["object"]: row for row in model["rows"]}
        self.assertEqual(rows["awg1"]["external_practice"], "CIRCUIT_BREAKER_OPEN_AND_OUTLIER_REVIEW")
        self.assertIn("ASK_OPERATOR", rows["awg1"]["v7_native_actions"])
        self.assertIn("PROBE_ONLY", rows["awg1"]["v7_native_actions"])
        self.assertEqual(rows["awg2"]["external_practice"], "OUTLIER_EJECTION")
        self.assertIn("QUARANTINE_FOR_NORMAL_TARGET_USE", rows["awg2"]["v7_native_actions"])
        self.assertEqual(model["summary"]["runtime_actions_created"], 0)
        self.assertEqual(model["summary"]["threshold_changes"], 0)
        self.assertEqual(model["summary"]["formula_changes"], 0)
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])
        self.assertFalse(model["synthetic_evidence_created"])
        self.assertFalse(model["new_owner_created"])
        self.assertFalse(model["new_planner_created"])

    def test_inventory_exposes_b6_v7_native_degradation_response_mapping(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-29T02:31:00+00:00",
            )

        model = inventory["v7_native_degradation_response_mapping"]
        self.assertEqual(model["backlog_item"], "B6")
        self.assertTrue(model["read_only"])
        self.assertEqual(model["summary"]["runtime_actions_created"], 0)
        self.assertEqual(model["summary"]["threshold_changes"], 0)
        self.assertEqual(model["summary"]["formula_changes"], 0)
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)

    def test_b7_binds_service_objectives_to_existing_policy_threshold_sources(self):
        freshness = accel.build_freshness_actionability({
            "service-scores": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            "channel-service-scores": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            "user-service-scores": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
        })
        fit = accel.build_service_user_sla_fit(
            {
                "users": [{
                    "user": "10.7.0.2",
                    "current_channel": "awg0",
                    "required_services": ["telegram", "youtube"],
                    "candidates": [
                        {"channel": "awg1", "suitability_score": 88},
                        {"channel": "vless", "suitability_score": 60, "required_low": ["youtube"]},
                    ],
                }]
            },
            freshness_actionability=freshness,
            generated_at="2026-06-29T02:50:00+00:00",
        )
        model = accel.build_service_objective_policy_threshold_binding(
            service_user_sla_fit=fit,
            freshness_actionability=freshness,
            soft_degradation_threshold_vocabulary={
                "rows": [{"object": "awg1", "canonical_policy_result": "NO_DEGRADATION"}],
            },
            v7_native_degradation_response_mapping={
                "rows": [{"object": "awg1", "v7_native_actions": ["KEEP"]}],
            },
            generated_at="2026-06-29T02:51:00+00:00",
        )

        self.assertEqual(model["schema_version"], "v7.b7.service-objective-policy-threshold-binding.v1")
        self.assertEqual(model["backlog_item"], "B7")
        rows = {row["candidate_channel"]: row for row in model["rows"]}
        self.assertIn("awg1", rows)
        objectives = {item["objective"]: item for item in rows["awg1"]["objective_bindings"]}
        self.assertIn("required_service_reachability", objectives)
        self.assertIn("service_freshness", objectives)
        self.assertIn("soft_degradation_policy", objectives)
        self.assertIn("degradation_response", objectives)
        for binding in objectives.values():
            self.assertFalse(binding["threshold_values_changed"])
            self.assertFalse(binding["formula_changed"])
        self.assertEqual(model["summary"]["threshold_changes"], 0)
        self.assertEqual(model["summary"]["formula_changes"], 0)
        self.assertEqual(model["summary"]["runtime_actions_created"], 0)
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])
        self.assertFalse(model["synthetic_evidence_created"])
        self.assertFalse(model["new_owner_created"])

    def test_inventory_exposes_b7_service_objective_policy_threshold_binding(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-29T02:52:00+00:00",
            )

        model = inventory["service_objective_policy_threshold_binding"]
        self.assertEqual(model["backlog_item"], "B7")
        self.assertTrue(model["read_only"])
        self.assertEqual(model["summary"]["threshold_changes"], 0)
        self.assertEqual(model["summary"]["formula_changes"], 0)
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)

    def test_b8_certifies_recovery_admission_with_repeated_readiness_evidence(self):
        freshness = accel.build_freshness_actionability({
            "trust-evolution-summaries": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            "service-scores": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            "channel-service-scores": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            "user-service-scores": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
        })
        recovery = accel.build_recovery_admission(
            {},
            freshness_actionability=freshness,
            channel_recovery_inputs=[{
                "channel": "awg1",
                "lifecycle": "WATCH",
                "successful_checks": 3,
                "service_specific_recovery_ok": True,
            }],
            generated_at="2026-06-29T03:10:00+00:00",
        )
        model = accel.build_recovery_admission_certification(
            recovery_admission=recovery,
            service_scores_snapshot={
                "items": [{"channel": "awg1", "services": {"telegram": {"ok": True, "status": "OK"}}}]
            },
            channel_service_scores_snapshot={
                "items": [{"channel": "awg1", "score": {"current": 88, "trend": "stable"}}]
            },
            freshness_actionability=freshness,
            service_objective_policy_threshold_binding={
                "rows": [{"candidate_channel": "awg1", "binding_state": "BOUND_TO_EXISTING_POLICY_GATES", "objective_bindings": [{"objective": "service_freshness"}]}]
            },
            generated_at="2026-06-29T03:11:00+00:00",
        )

        self.assertEqual(model["schema_version"], "v7.b8.recovery-admission-certification.v1")
        self.assertEqual(model["backlog_item"], "B8")
        row = model["rows"][0]
        self.assertEqual(row["certification_state"], "CERTIFIED_FOR_RECOVERY_ADMISSION_REVIEW")
        self.assertTrue(row["repeated_success_evidence"])
        self.assertTrue(row["service_readiness_evidence"])
        self.assertTrue(row["quality_readiness_evidence"])
        self.assertTrue(row["objective_binding_evidence"])
        self.assertEqual(row["blockers"], [])
        self.assertEqual(model["summary"]["certified"], 1)
        self.assertEqual(model["summary"]["runtime_actions_created"], 0)
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])
        self.assertFalse(model["synthetic_evidence_created"])

    def test_b8_blocks_single_pass_or_missing_readiness_evidence(self):
        freshness = accel.build_freshness_actionability({
            "trust-evolution-summaries": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            "service-scores": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            "channel-service-scores": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
            "user-service-scores": {"exists": True, "freshness_state": "FRESH", "runtime_behavior": "ALLOW", "stop_required": False},
        })
        recovery = accel.build_recovery_admission(
            {},
            freshness_actionability=freshness,
            channel_recovery_inputs=[{"channel": "awg1", "lifecycle": "RECOVERING", "successful_checks": 1}],
        )
        model = accel.build_recovery_admission_certification(
            recovery_admission=recovery,
            service_scores_snapshot={"items": [{"channel": "awg1", "services": {"telegram": {"ok": True}}}]},
            channel_service_scores_snapshot={"items": []},
            freshness_actionability=freshness,
        )

        row = model["rows"][0]
        self.assertEqual(row["certification_state"], "NOT_CERTIFIED_COLLECT_REAL_EVIDENCE")
        self.assertIn("insufficient_repeated_success_evidence", row["blockers"])
        self.assertIn("quality_readiness_evidence_missing", row["blockers"])
        self.assertEqual(model["summary"]["certified"], 0)
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)

    def test_b9_verifies_post_admission_observation_windows(self):
        model = accel.build_post_admission_observation_windows(
            recovery_admission_certification={
                "rows": [{
                    "channel": "awg1",
                    "certification_state": "CERTIFIED_FOR_RECOVERY_ADMISSION_REVIEW",
                }],
            },
            service_scores_snapshot={
                "items": [{"channel": "awg1", "services": {"telegram": {"ok": True, "status": "OK"}}}]
            },
            channel_service_scores_snapshot={
                "items": [{
                    "channel": "awg1",
                    "windows": {
                        "5m": {"samples": 3, "fail_rate": 0.0, "stability": 1.0},
                        "1h": {"samples": 12, "fail_rate": 0.0, "stability": 1.0},
                    },
                }]
            },
            generated_at="2026-06-29T03:30:00+00:00",
        )

        self.assertEqual(model["schema_version"], "v7.b9.post-admission-observation-windows.v1")
        self.assertEqual(model["backlog_item"], "B9")
        row = model["rows"][0]
        self.assertEqual(row["verification_state"], "POST_ADMISSION_WINDOWS_VERIFIED_READ_ONLY")
        self.assertEqual(row["observed_windows"], ["1h", "5m"])
        self.assertTrue(row["service_observed"])
        self.assertEqual(row["blockers"], [])
        self.assertEqual(model["summary"]["verified"], 1)
        self.assertEqual(model["summary"]["runtime_actions_created"], 0)
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])
        self.assertFalse(model["synthetic_evidence_created"])

    def test_b9_blocks_missing_post_admission_observation_window(self):
        model = accel.build_post_admission_observation_windows(
            recovery_admission_certification={
                "rows": [{
                    "channel": "awg1",
                    "certification_state": "CERTIFIED_FOR_RECOVERY_ADMISSION_REVIEW",
                }],
            },
            service_scores_snapshot={
                "items": [{"channel": "awg1", "services": {"telegram": {"ok": True}}}]
            },
            channel_service_scores_snapshot={
                "items": [{"channel": "awg1", "windows": {"5m": {"samples": 2}}}]
            },
        )

        row = model["rows"][0]
        self.assertEqual(row["verification_state"], "POST_ADMISSION_WINDOWS_NOT_VERIFIED")
        self.assertIn("post_admission_quality_windows_missing:1h", row["blockers"])
        self.assertEqual(model["summary"]["verified"], 0)
        self.assertEqual(model["summary"]["not_verified"], 1)
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)

    def test_b10_defines_recovery_slow_start_progression_without_runtime_apply(self):
        model = accel.build_recovery_slow_start_progression(
            post_admission_observation_windows={
                "rows": [{
                    "channel": "awg1",
                    "verification_state": "POST_ADMISSION_WINDOWS_VERIFIED_READ_ONLY",
                }],
            },
            recovery_admission_certification={
                "rows": [{
                    "channel": "awg1",
                    "certification_state": "CERTIFIED_FOR_RECOVERY_ADMISSION_REVIEW",
                }],
            },
            class_level_blast_radius_certification={
                "certification_state": "BEYOND_ONE_USER_EVIDENCE_CERTIFIED_READ_ONLY",
                "current_one_user_guard_certified": True,
                "beyond_one_user_certified": True,
                "max_historical_certified_blast_radius_users": 2,
            },
            generated_at="2026-06-29T04:00:00+00:00",
        )

        self.assertEqual(model["schema_version"], "v7.b10.recovery-slow-start-progression.v1")
        self.assertEqual(model["backlog_item"], "B10")
        row = model["rows"][0]
        self.assertEqual(row["progression_state"], "SLOW_START_PROGRESSION_READY_READ_ONLY")
        self.assertEqual(row["safe_next_stage"], "ONE_USER_GOVERNED_RECOVERY_REVIEW")
        self.assertEqual(row["blockers"], [])
        self.assertIn("runtime_apply", row["still_blocked_capabilities"])
        self.assertIn("ONE_USER_GOVERNED_RECOVERY_REVIEW", [stage["stage"] for stage in model["stage_catalog"]])
        self.assertEqual(model["summary"]["ready_for_one_user_governed_recovery_review"], 1)
        self.assertEqual(model["summary"]["runtime_actions_created"], 0)
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])
        self.assertFalse(model["synthetic_evidence_created"])

    def test_b10_blocks_slow_start_without_post_admission_windows(self):
        model = accel.build_recovery_slow_start_progression(
            post_admission_observation_windows={
                "rows": [{
                    "channel": "awg1",
                    "verification_state": "POST_ADMISSION_WINDOWS_NOT_VERIFIED",
                }],
            },
            recovery_admission_certification={
                "rows": [{
                    "channel": "awg1",
                    "certification_state": "CERTIFIED_FOR_RECOVERY_ADMISSION_REVIEW",
                }],
            },
            class_level_blast_radius_certification={"current_one_user_guard_certified": True},
        )

        row = model["rows"][0]
        self.assertEqual(row["progression_state"], "SLOW_START_PROGRESSION_BLOCKED")
        self.assertEqual(row["safe_next_stage"], "BLOCKED")
        self.assertIn("post_admission_observation_windows_not_verified", row["blockers"])
        self.assertEqual(model["summary"]["blocked"], 1)
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)

    def test_b11_integrates_org_cohort_identity_policy_gates_read_only(self):
        model = accel.build_org_cohort_identity_policy_integration(
            decision_surface={
                "users": [{"ip": "10.7.0.11", "current": "awg1", "group": "vip", "recommended_channel": "awg2"}],
                "channels": [{"id": "awg1"}, {"id": "awg2", "groups": "vip,staff"}],
            },
            org_policy={
                "default_isolation": "shared",
                "groups": {
                    "vip": {
                        "allowed_egress": ["awg*"],
                        "preferred_egress": ["awg2"],
                        "excluded_egress": [],
                        "isolation": "shared",
                    }
                },
                "egress": {"awg2": {"groups": ["vip", "staff"]}},
            },
            recovery_slow_start_progression={"schema_version": "v7.b10.recovery-slow-start-progression.v1"},
            generated_at="2026-06-29T04:30:00+00:00",
        )

        self.assertEqual(model["schema_version"], "v7.b11.org-cohort-identity-policy-integration.v1")
        self.assertEqual(model["backlog_item"], "B11")
        target = next(row for row in model["rows"] if row["target_channel"] == "awg2")
        self.assertEqual(target["integration_state"], "ORG_COHORT_IDENTITY_POLICY_INTEGRATED_READ_ONLY")
        self.assertEqual(target["blockers"], [])
        self.assertTrue(target["is_preferred_target"])
        self.assertEqual(model["summary"]["integrated_rows"], 2)
        self.assertEqual(model["summary"]["runtime_actions_created"], 0)
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])
        self.assertFalse(model["synthetic_evidence_created"])

    def test_b11_exposes_existing_policy_blocks_without_runtime_apply(self):
        model = accel.build_org_cohort_identity_policy_integration(
            decision_surface={
                "users": [
                    {"ip": "10.7.0.11", "current": "awg1", "group": "vip", "recommended_channel": "awg2"},
                    {"ip": "10.7.0.12", "current": "awg2", "group": "staff", "recommended_channel": "awg2"},
                ],
                "channels": [{"id": "awg1"}, {"id": "awg2", "exclusive_group": "staff"}],
            },
            org_policy={
                "default_isolation": "exclusive",
                "groups": {
                    "vip": {"allowed_egress": ["awg1"], "isolation": "exclusive"},
                    "staff": {"allowed_egress": ["awg2"], "isolation": "exclusive"},
                },
            },
        )

        target = next(row for row in model["rows"] if row["user"] == "10.7.0.11" and row["target_channel"] == "awg2")
        self.assertEqual(target["integration_state"], "ORG_COHORT_IDENTITY_POLICY_BLOCKED_BY_EXISTING_GATES")
        self.assertIn("group_allowed_egress", target["blockers"])
        self.assertIn("egress_exclusive_group", target["blockers"])
        self.assertIn("exclusive_isolation", target["blockers"])
        self.assertGreaterEqual(model["summary"]["blocked_by_existing_policy_gates"], 1)
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)

    def test_action_class_freshness_windows_reuse_owner_issued_fields(self):
        freshness = accel.build_freshness_actionability({
            "service-scores": {
                "exists": True,
                "freshness_state": "FRESH",
                "runtime_behavior": "ALLOW",
                "stop_required": False,
                "confidence": 0.9,
                "source_hashes": {"service-matrix.json": "abc"},
            },
            "channel-service-scores": {
                "exists": True,
                "freshness_state": "FRESH",
                "runtime_behavior": "ALLOW",
                "stop_required": False,
                "confidence": 0.8,
                "source_hashes": {"egress-quality-summary.json": "def"},
            },
            "user-service-scores": {
                "exists": True,
                "freshness_state": "FRESH",
                "runtime_behavior": "ALLOW",
                "stop_required": False,
                "confidence": 0.7,
            },
        })
        model = accel.build_action_class_freshness_windows(
            freshness,
            generated_at="2026-06-25T00:01:00+00:00",
        )

        self.assertEqual(model["schema_version"], "v7.action-class-freshness-windows.v1")
        rows = {row["action_class"]: row for row in model["rows"]}
        canary = rows["single-user governed candidate failover"]
        self.assertEqual(canary["freshness_windows"]["service"], 900)
        service_domain = {row["domain"]: row for row in canary["domains"]}["service"]
        self.assertEqual(service_domain["classification"], "ACTIONABLE_NOW")
        self.assertIn("service-scores", service_domain["owner_issued_fields"])
        self.assertEqual(
            service_domain["owner_issued_fields"]["service-scores"]["source_hashes"]["service-matrix.json"],
            "abc",
        )
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["new_truth_source_created"])

    def test_acceleration_inventory_exposes_knowledge_quality_read_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-24T00:00:00+00:00",
            )

        self.assertIn("knowledge_quality_read_model", inventory)
        self.assertIn("knowledge_objects", inventory)
        self.assertIn("maturity_distribution", inventory)
        self.assertIn("tier_readiness_knowledge", inventory)
        self.assertIn("10k_readiness", inventory)
        self.assertIn("p0_gaps", inventory)
        self.assertEqual(
            inventory["knowledge_objects"],
            inventory["knowledge_quality_read_model"]["knowledge_objects"],
        )
        self.assertEqual(
            inventory["knowledge_quality_read_model"]["owner"],
            "admin_core.autonomy_trust_acceleration",
        )
        self.assertFalse(inventory["knowledge_quality_read_model"]["runtime_mutation_performed"])
        self.assertFalse(inventory["knowledge_quality_read_model"]["apply_executed"])
        self.assertEqual(inventory["knowledge_quality_read_model"]["users_moved"], 0)

    def test_inventory_exposes_autonomy_grade_suitability_program(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-24T00:00:00+00:00",
            )

        quality = inventory["suitability_quality_model"]
        growth = inventory["suitability_knowledge_growth"]
        effectiveness = inventory["suitability_effectiveness_expansion"]
        program = inventory["autonomy_grade_suitability_program"]

        self.assertEqual(quality["schema_version"], "v7.autonomy-trust.suitability-quality-model.v1")
        self.assertEqual(quality["current_stage"], "STABLE_SIGNAL")
        self.assertFalse(quality["autonomy_grade_ready"])
        self.assertIn("candidate_source_confidence_below_confirmed_floor", quality["missing_knowledge"]["primary_blockers"])
        self.assertEqual(growth["schema_version"], "v7.autonomy-trust.suitability-knowledge-growth.v1")
        self.assertEqual(growth["growth_direction"], "INCREASED")
        self.assertGreaterEqual(len(growth["fastest_suitability_growth_activities"]), 1)
        self.assertEqual(effectiveness["schema_version"], "v7.autonomy-trust.suitability-effectiveness-expansion.v1")
        self.assertEqual(effectiveness["decision_correctness"], 1.0)
        self.assertEqual(effectiveness["fit_correctness"], 1.0)
        self.assertEqual(effectiveness["candidate_correctness"], 0.5)
        self.assertEqual(program["schema_version"], "v7.autonomy-trust.autonomy-grade-suitability-program.v1")
        self.assertEqual(program["improvements"]["suitability_quality_model"], "IMPLEMENTED_READ_ONLY")
        self.assertFalse(program["autonomy_grade_ready"])
        for key in (
            "suitability_quality_model",
            "suitability_knowledge_growth",
            "suitability_effectiveness_expansion",
            "autonomy_grade_suitability_program",
        ):
            self.assertFalse(inventory[key]["runtime_mutation_performed"])
            self.assertFalse(inventory[key]["apply_executed"])
            self.assertEqual(inventory[key]["users_moved"], 0)

    def test_suitability_program_survives_refresh_style_rebuild(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            first = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-24T00:00:00+00:00",
            )
            second = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=json.loads(json.dumps(self.decision_surface(), sort_keys=True)),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-24T00:01:00+00:00",
            )

        for key in (
            "current_stage",
            "autonomy_grade_ready",
            "measurements",
            "missing_knowledge",
        ):
            self.assertEqual(first["suitability_quality_model"][key], second["suitability_quality_model"][key])
        self.assertEqual(
            first["suitability_effectiveness_expansion"]["candidate_correctness"],
            second["suitability_effectiveness_expansion"]["candidate_correctness"],
        )
        self.assertEqual(
            first["suitability_knowledge_growth"]["candidate_outcome_gap"],
            second["suitability_knowledge_growth"]["candidate_outcome_gap"],
        )
        self.assertFalse(second["autonomy_grade_suitability_program"]["runtime_mutation_performed"])
        self.assertEqual(second["autonomy_grade_suitability_program"]["users_moved"], 0)

    def test_knowledge_quality_overlay_includes_suitability_autonomy_stage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-24T00:00:00+00:00",
            )

        objects = {row["object"]: row for row in inventory["knowledge_objects"]}
        suitability_overlay = objects["Suitability"]["evidence_overlay"]
        self.assertEqual(suitability_overlay["autonomy_grade_stage"], "STABLE_SIGNAL")
        self.assertFalse(suitability_overlay["autonomy_grade_ready"])
        self.assertIn("candidate_source_confidence_below_confirmed_floor", suitability_overlay["primary_blockers"])

    def test_autonomous_knowledge_growth_program_exposes_cycle_maturity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-25T00:00:00+00:00",
            )

        program = inventory["autonomous_knowledge_growth_program"]
        self.assertEqual(program["schema_version"], "v7.autonomy-trust.autonomous-knowledge-growth-program.v1")
        self.assertEqual(program["cycle_count"], 12)
        self.assertGreater(program["overall_autonomy_maturity_score"], 0)
        self.assertFalse(program["runtime_apply_allowed"])
        self.assertFalse(program["runtime_mutation_performed"])
        self.assertEqual(program["users_moved"], 0)
        self.assertFalse(program["apply_executed"])
        self.assertFalse(program["synthetic_evidence_created"])
        cycles = {row["cycle"]: row for row in program["cycles"]}
        self.assertEqual(cycles["Knowledge-Gated Dry-Run Cycle"]["automation_level"], "AUTONOMOUS_UNTIL_BOUNDARY")
        self.assertEqual(cycles["Knowledge-Gated Dry-Run Cycle"]["authority_boundary"], "AUTHORITY_BOUNDARY")
        self.assertEqual(cycles["Outcome Leverage Cycle"]["automation_level"], "FULLY_AUTONOMOUS")
        self.assertIn("Suitability Growth Cycle", program["cycles_more_autonomous_after_this_phase"])
        self.assertIn("AUTHORITY_BOUNDARY", program["legitimate_boundaries"])
        for row in program["cycles"]:
            self.assertFalse(row["runtime_mutation_performed"])
            self.assertFalse(row["apply_executed"])
            self.assertEqual(row["users_moved"], 0)

    def test_autonomous_knowledge_growth_program_survives_refresh_rebuild(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            first = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-25T00:00:00+00:00",
            )
            second = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=json.loads(json.dumps(self.decision_surface(), sort_keys=True)),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-25T00:01:00+00:00",
            )

        first_program = first["autonomous_knowledge_growth_program"]
        second_program = second["autonomous_knowledge_growth_program"]
        self.assertEqual(first_program["cycle_count"], second_program["cycle_count"])
        self.assertEqual(first_program["automation_counts"], second_program["automation_counts"])
        self.assertEqual(first_program["automation_percentages"], second_program["automation_percentages"])
        self.assertEqual(first_program["overall_autonomy_maturity_score"], second_program["overall_autonomy_maturity_score"])
        self.assertEqual(
            {row["cycle"]: row["automation_level"] for row in first_program["cycles"]},
            {row["cycle"]: row["automation_level"] for row in second_program["cycles"]},
        )
        self.assertFalse(second_program["runtime_mutation_performed"])
        self.assertEqual(second_program["users_moved"], 0)
        self.assertFalse(second_program["apply_executed"])

    def test_autonomous_routing_evolution_program_integrates_existing_cycles(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-25T00:00:00+00:00",
            )

        program = inventory["autonomous_routing_evolution_program"]
        self.assertEqual(
            program["schema_version"],
            "v7.autonomy-trust.autonomous-routing-evolution-program.v1",
        )
        self.assertEqual(program["exact_stop_reason"], "AUTHORITY_BOUNDARY")
        self.assertEqual(
            program["phase_status"]["A_AUTONOMOUS_KNOWLEDGE_GROWTH"],
            "ADVANCED",
        )
        self.assertEqual(
            program["phase_status"]["E_EVENT_TO_DECISION_TO_OUTCOME"],
            "AUTONOMOUS_UNTIL_AUTHORITY_BOUNDARY",
        )
        self.assertEqual(program["tier_2_distance"]["status"], "BLOCKED")
        self.assertIn("confidence", program["tier_2_distance"]["missing_primary_floors"])
        self.assertIn("prediction", program["tier_2_distance"]["missing_primary_floors"])
        self.assertEqual(
            program["current_suitability_maturity"]["stage"],
            "STABLE_SIGNAL",
        )
        self.assertIn("prediction_outcome_cycle", program["highest_leverage_next_activities"])
        self.assertFalse(program["runtime_mutation_performed"])
        self.assertEqual(program["users_moved"], 0)
        self.assertFalse(program["apply_executed"])
        self.assertFalse(program["autonomy_enabled"])

    def test_action_class_runtime_enablement_exposes_approved_bounded_policy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-25T00:00:00+00:00",
            )

        enablement = inventory["action_class_runtime_enablement"]
        self.assertEqual(enablement["schema_version"], "v7.action-class-runtime-enablement.v2")
        self.assertEqual(enablement["path_status"], "PARTIAL")
        self.assertEqual(enablement["semantic_reuse_audit"]["semantic_coverage_percent"], 78)
        self.assertFalse(enablement["semantic_reuse_audit"]["need_new_owner"])
        self.assertEqual(enablement["semantic_reuse_audit"]["duplicate_detector_result"], "NO_DUPLICATE_OWNER_CREATED")
        self.assertEqual(enablement["current_action_class"], "single-user governed candidate failover")
        self.assertEqual(enablement["current_state"], "GOVERNED_ONLY")
        self.assertEqual(enablement["next_promotion_target"], "CERTIFIED_FOR_CLASS_APPROVAL")
        self.assertFalse(enablement["runtime_capability_view"]["runtime_can_execute_automatically"])
        self.assertFalse(enablement["runtime_capability_view"]["runtime_apply_allowed_now"])
        self.assertEqual(enablement["runtime_capability_view"]["current_autonomy_mode"], "DELEGATED_AUTONOMY")
        self.assertEqual(enablement["runtime_capability_view"]["target_autonomy_mode"], "DELEGATED_AUTONOMY")
        self.assertEqual(enablement["enablement_readiness"]["stop_condition_if_promoted"], "AUTHORITY_BOUNDARY")
        self.assertIn("class-level authority_policy_approval", enablement["enablement_readiness"]["missing_evidence"])
        self.assertNotIn("class-level blast_radius_certification", enablement["enablement_readiness"]["missing_evidence"])
        self.assertNotIn("class-level rollback_or_no_rollback_certification", enablement["enablement_readiness"]["missing_evidence"])
        self.assertIn("current-class suitability decision-context real outcome", enablement["enablement_readiness"]["missing_evidence"])
        self.assertEqual(enablement["historical_certification_reuse"]["max_certified_user_count"], 48)
        self.assertEqual(enablement["historical_certification_reuse"]["current_action_class_identity"], "DECISION_CONTEXT_MISMATCH")
        self.assertEqual(enablement["promotion_recommendation"]["promotion_evaluation"], "PROMOTION_BLOCKED_WITH_EXACT_DELTA")
        self.assertNotIn(
            "missing_candidate_outcomes",
            " ".join(enablement["enablement_readiness"]["missing_evidence"]),
        )
        self.assertIn(
            "missing_candidate_outcomes=2",
            enablement["enablement_readiness"]["inventory_signals"],
        )
        self.assertFalse(enablement["enablement_readiness"]["inventory_signals_are_mandatory"])
        self.assertFalse(enablement["downstream_certification_alignment"]["A4"]["inventory_coverage_is_hard_gate"])
        self.assertFalse(enablement["downstream_certification_alignment"]["A6"]["inventory_coverage_is_runtime_blocker"])
        policy = enablement["delegated_autonomy_policy_preview"]
        self.assertEqual(policy["policy_id"], "dap_default_tier1_readonly")
        self.assertEqual(policy["policy_state"], "APPROVED")
        self.assertEqual(policy["max_blast_radius"]["users"], 1)
        self.assertEqual(policy["max_concurrent_transactions"], 1)
        self.assertTrue(policy["runtime_apply_enabled"])
        self.assertFalse(policy["operator_candidate_approval_required"])
        self.assertFalse(policy["operator_packet_approval_required"])
        self.assertFalse(policy["self_expansion_allowed"])
        self.assertEqual(len(policy["policy_scope_hash"]), 64)
        self.assertFalse(policy["authority_expanded"])
        self.assertTrue(policy["autonomy_enabled"])
        eligibility = enablement["delegated_autonomy_runtime_eligibility"]
        self.assertNotIn("POLICY_NOT_APPROVED", eligibility["blockers"])
        self.assertNotIn("ACTION_CLASS_NOT_AUTONOMOUS_RUNTIME", eligibility["blockers"])
        self.assertNotIn("RUNTIME_APPLY_NOT_ENABLED", eligibility["blockers"])
        self.assertTrue(eligibility["governed_learning_policy_consumed"])
        self.assertFalse(eligibility["authority_expansion_allowed_by_runtime"])
        self.assertEqual(
            enablement["packet_to_action_class_mapping"]["action_class"],
            "single-user governed candidate failover",
        )
        self.assertEqual(enablement["packet_to_action_class_mapping"]["subject"], ["10.7.0.2"])
        self.assertEqual(enablement["packet_to_action_class_mapping"]["target"], ["awg0"])
        self.assertFalse(enablement["authority_to_action_class_mapping"]["authority_expansion_performed"])
        self.assertFalse(enablement["runtime_mutation_performed"])
        self.assertFalse(enablement["restore_barrier_written_now"])
        self.assertFalse(enablement["apply_executed"])
        self.assertEqual(enablement["users_moved"], 0)
        self.assertFalse(enablement["authority_expanded"])
        self.assertTrue(enablement["autonomy_enabled"])
        self.assertFalse(enablement["new_planner_created"])
        self.assertFalse(enablement["new_governance_created"])
        self.assertFalse(enablement["new_execution_path_created"])
        self.assertFalse(enablement["new_truth_source_created"])

    def test_delegated_autonomy_policy_eligibility_is_policy_bounded(self):
        packet_mapping = {
            "action_class": "single-user governed candidate failover",
            "selected_move_count": 1,
        }
        policy = accel.build_delegated_autonomy_policy_preview({
            "policy_state": "APPROVED",
            "current_mode": "DELEGATED_AUTONOMY",
            "runtime_apply_enabled": True,
        })
        eligibility = accel.build_delegated_autonomy_runtime_eligibility(
            policy_preview=policy,
            packet_mapping=packet_mapping,
            current_state="AUTONOMOUS_RUNTIME",
            missing_evidence=[],
            freshness_actionability={"domains": {}},
        )

        self.assertTrue(eligibility["runtime_may_self_approve_operational_decision"])
        self.assertFalse(eligibility["runtime_must_stop"])
        self.assertEqual(eligibility["blockers"], [])
        self.assertFalse(eligibility["authority_expansion_allowed_by_runtime"])
        self.assertFalse(eligibility["policy_expansion_allowed_by_runtime"])

        oversized = accel.build_delegated_autonomy_runtime_eligibility(
            policy_preview=policy,
            packet_mapping={
                "action_class": "small-batch movement",
                "selected_move_count": 3,
            },
            current_state="AUTONOMOUS_RUNTIME",
            missing_evidence=[],
            freshness_actionability={"domains": {}},
        )

        self.assertFalse(oversized["runtime_may_self_approve_operational_decision"])
        self.assertIn("ACTION_CLASS_NOT_ALLOWED", oversized["blockers"])
        self.assertIn("BLAST_RADIUS_EXCEEDED", oversized["blockers"])
        self.assertFalse(oversized["apply_executed"])
        self.assertEqual(oversized["users_moved"], 0)

    def test_delegated_policy_allows_governed_only_without_promoting_class(self):
        policy = accel.build_delegated_autonomy_policy_preview()
        eligibility = accel.build_delegated_autonomy_runtime_eligibility(
            policy_preview=policy,
            packet_mapping={
                "action_class": "single-user governed candidate failover",
                "selected_move_count": 1,
            },
            current_state="GOVERNED_ONLY",
            missing_evidence=[],
            freshness_actionability={"domains": {}},
        )

        self.assertTrue(eligibility["runtime_may_self_approve_operational_decision"])
        self.assertTrue(eligibility["governed_learning_policy_consumed"])
        self.assertEqual(eligibility["blockers"], [])
        self.assertEqual(policy["policy_state"], "APPROVED")
        self.assertFalse(policy["self_expansion_allowed"])

    def test_a5_class_level_blast_radius_certification_consumes_historical_proofs_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[{
                    "recommendation_id": "r1",
                    "decision_id": "decision-1",
                    "packet_id": "p1",
                    "apply_result": "success",
                    "post_action_verification": {"status": "passed"},
                    "service_outcome": {"telegram": "ok"},
                    "user_outcome": {"user": "10.7.0.2"},
                    "learning_record": {"stored": True},
                    "outcome_observed_at": "2026-06-24T00:00:00+00:00",
                    "blast_radius": 1,
                    "selected_move_count": 1,
                    "user": "10.7.0.2",
                    "target": "awg0",
                    "service_delta": 5,
                    "prediction_delta": 3,
                }],
                generated_at="2026-06-25T00:00:00+00:00",
            )

        certification = inventory["class_level_blast_radius_certification"]
        self.assertEqual(certification["schema_version"], "v7.a5-class-level-blast-radius-certification.v1")
        self.assertEqual(certification["backlog_item"], "A5")
        self.assertEqual(certification["owner"], "admin_core.autonomy_trust_acceleration")
        self.assertTrue(certification["current_one_user_guard_certified"])
        self.assertTrue(certification["beyond_one_user_certified"])
        self.assertGreaterEqual(certification["max_historical_certified_blast_radius_users"], 2)
        self.assertEqual(certification["certification_state"], "BEYOND_ONE_USER_EVIDENCE_CERTIFIED_READ_ONLY")
        self.assertNotIn("beyond_one_user_real_outcome_evidence_missing", certification["blockers"])
        self.assertIn("class_authority_not_approved", certification["blockers"])
        self.assertEqual(
            certification["omp_output"]["recommendation"],
            "CERTIFY_A5_EVIDENCE_ONLY_DO_NOT_EXPAND_AUTHORITY",
        )
        self.assertEqual(
            certification["omp_output"]["stop_condition_if_scope_expansion_requested"],
            "ENGINEERING_AUTHORITY",
        )
        self.assertFalse(certification["runtime_mutation_performed"])
        self.assertFalse(certification["apply_executed"])
        self.assertEqual(certification["users_moved"], 0)
        self.assertFalse(certification["authority_expanded"])
        self.assertFalse(certification["autonomy_enabled"])
        self.assertFalse(certification["new_owner_created"])
        self.assertFalse(certification["new_runtime_created"])

    def test_historical_movement_certifications_reuse_layers_without_authority(self):
        evidence = accel.build_historical_blast_radius_evidence(
            generated_at="2026-07-11T00:00:00+00:00",
        )

        self.assertEqual(evidence["schema_version"], "v7.historical-blast-radius-evidence.v2")
        self.assertEqual(evidence["historical_certifications_found"], 9)
        self.assertEqual(evidence["real_movement_certifications_found"], 9)
        self.assertEqual(evidence["max_certified_blast_radius_users"], 48)
        self.assertEqual(evidence["current_action_class_identity"], "DECISION_CONTEXT_MISMATCH")
        self.assertEqual(evidence["exact_current_class_real_outcomes"], 0)
        self.assertTrue(evidence["reusable_dimensions"]["execution_path"])
        self.assertTrue(evidence["reusable_dimensions"]["blast_radius"])
        self.assertTrue(evidence["reusable_dimensions"]["rollback_or_no_rollback"])
        self.assertFalse(evidence["reusable_dimensions"]["current_decision_context"])
        self.assertFalse(evidence["authority_granted"])
        self.assertFalse(evidence["runtime_apply_allowed"])

    def test_deployed_owner_consumes_repository_certified_provenance_without_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence = accel.build_historical_blast_radius_evidence(
                evidence_dir=Path(tmp) / "missing-e29",
                report_root=Path(tmp),
                generated_at="2026-07-11T00:00:00+00:00",
            )

        self.assertEqual(evidence["real_movement_certifications_found"], 9)
        self.assertEqual(evidence["max_certified_blast_radius_users"], 48)
        self.assertTrue(all(
            row["validation_basis"] == "DEPLOYED_REPOSITORY_CERTIFIED_PROVENANCE_POINTER"
            for row in evidence["certification_inventory"]
        ))
        self.assertFalse(evidence["authority_granted"])
        self.assertFalse(evidence["runtime_apply_allowed"])

    def test_a5_class_level_blast_radius_certification_blocks_without_historical_proofs(self):
        certification = accel.build_class_level_blast_radius_certification(
            action_class_runtime_enablement={
                "current_action_class": "single-user governed candidate failover",
                "action_classes": [
                    {
                        "action_class": "single-user governed candidate failover",
                        "required_blast_radius": "exactly one user",
                        "runtime_enablement_state": "GOVERNED_ONLY",
                    },
                    {
                        "action_class": "two-user governed candidate failover",
                        "required_blast_radius": "bounded cohort",
                        "runtime_enablement_state": "NOT_CERTIFIED",
                    },
                ],
            },
            floor_forensics={
                "component_values": {"blast_radius_confidence": 100},
                "rollback_and_blast": {"blast_records_seen": 1},
            },
            service_user_sla_fit={"summary": {"users_seen": 1, "verdict_counts": {"PASS": 1}}},
            hard_failure_classification={"classification": "HARD_FAILURE_CONFIRMED"},
            decision_outcome_closure={"closure_state": "COMPLETE", "summary": {"valid_closures": 1}},
            historical_blast_radius_evidence={
                "max_certified_blast_radius_users": 1,
                "required_historical_proofs_present": True,
            },
        )

        self.assertTrue(certification["current_one_user_guard_certified"])
        self.assertFalse(certification["beyond_one_user_certified"])
        self.assertIn("beyond_one_user_real_outcome_evidence_missing", certification["blockers"])
        self.assertFalse(certification["authority_expanded"])
        self.assertFalse(certification["apply_executed"])

    def recovery_runtime_gate_inputs(self):
        return {
            "recovery_admission_certification": {
                "schema_version": "v7.b8.recovery-admission-certification.v1",
                "rows": [{
                    "channel": "awg1",
                    "certification_state": "CERTIFIED_FOR_RECOVERY_ADMISSION_REVIEW",
                    "admission_state": "RECOVERED_WATCH",
                    "blockers": [],
                }],
            },
            "post_admission_observation_windows": {
                "schema_version": "v7.b9.post-admission-observation-windows.v1",
                "rows": [{
                    "channel": "awg1",
                    "verification_state": "POST_ADMISSION_WINDOWS_VERIFIED_READ_ONLY",
                    "blockers": [],
                }],
            },
            "recovery_slow_start_progression": {
                "schema_version": "v7.b10.recovery-slow-start-progression.v1",
                "rows": [{
                    "channel": "awg1",
                    "progression_state": "SLOW_START_PROGRESSION_READY_READ_ONLY",
                    "safe_next_stage": "ONE_USER_GOVERNED_RECOVERY_REVIEW",
                    "blockers": [],
                }],
            },
        }

    def build_a6_with_recovery(self, **overrides):
        recovery = self.recovery_runtime_gate_inputs()
        recovery.update(overrides)
        return accel.build_runtime_eligibility_arbitration(
            action_class_runtime_enablement={
                "delegated_autonomy_runtime_eligibility": {
                    "blockers": ["AUTHORITY_POLICY_NOT_APPROVED"],
                    "runtime_can_execute_automatically": False,
                    "stale_required_domains": [],
                },
                "enablement_readiness": {"missing_evidence": []},
            },
            class_level_blast_radius_certification={
                "beyond_one_user_certified": True,
                "current_one_user_guard_certified": True,
            },
            freshness_actionability={"domains": {}},
            anti_flapping={"summary": {"blocked_users": 0}},
            decision_outcome_closure={"closure_state": "COMPLETE"},
            decision_outcome_learning={"knowledge_growth": {"knowledge_gained": 1}},
            routing_recommendation_readiness={"blockers": []},
            **recovery,
        )

    def test_a6_consumes_valid_b8_b9_b10_as_bounded_read_only_recovery_contract(self):
        arbitration = self.build_a6_with_recovery()

        gates = {row["gate"]: row for row in arbitration["gate_rows"]}
        self.assertEqual(gates["recovery_admission"]["state"], "PASS")
        integration = arbitration["recovery_runtime_integration"]
        self.assertEqual(integration["state"], "READY_FOR_EXISTING_AUTHORITY_REVIEW_READ_ONLY")
        self.assertEqual(integration["execution_owner"], "tools/v7-users-autoswitch")
        self.assertEqual(integration["ready_channels"], ["awg1"])
        self.assertEqual(integration["bounded_recovery_candidates"][0]["max_users"], 1)
        self.assertTrue(integration["bounded_recovery_candidates"][0]["packet_lease_identity_required"])
        self.assertTrue(integration["bounded_recovery_candidates"][0]["rollback_and_verification_required"])
        self.assertTrue(integration["read_only"])
        self.assertFalse(integration["runtime_mutation_performed"])
        self.assertFalse(integration["runtime_apply_allowed"])
        self.assertFalse(integration["direct_execution_allowed"])
        self.assertFalse(integration["authority_created_by_recovery_evidence"])
        self.assertEqual(integration["users_moved"], 0)
        self.assertEqual(arbitration["runtime_execute_decision"], "STOP_SAFE")
        self.assertIn("authority", arbitration["stop_gates"])
        self.assertIn("runtime_apply", arbitration["stop_gates"])
        self.assertFalse(arbitration["apply_executed"])
        self.assertEqual(arbitration["users_moved"], 0)

    def test_a6_recovery_gate_stops_when_b10_contract_is_missing(self):
        arbitration = self.build_a6_with_recovery(recovery_slow_start_progression={})

        self.assertIn("recovery_admission", arbitration["stop_gates"])
        blockers = arbitration["recovery_runtime_integration"]["blockers"]
        self.assertIn("b10_recovery_slow_start_progression_missing_or_unknown", blockers)
        self.assertIn("b10_recovery_slow_start_progression_missing", blockers)
        self.assertEqual(arbitration["runtime_execute_decision"], "STOP_SAFE")

    def test_a6_recovery_gate_stops_on_failed_observation_verification(self):
        recovery = self.recovery_runtime_gate_inputs()
        recovery["post_admission_observation_windows"]["rows"][0].update({
            "verification_state": "POST_ADMISSION_WINDOWS_NOT_VERIFIED",
            "blockers": ["post_admission_quality_windows_missing:1h"],
        })
        arbitration = self.build_a6_with_recovery(**recovery)

        self.assertIn("recovery_admission", arbitration["stop_gates"])
        blockers = arbitration["recovery_runtime_integration"]["blockers"]
        self.assertIn("b9_post_admission_observation_windows_not_verified", blockers)
        self.assertIn("post_admission_quality_windows_missing:1h", blockers)

    def test_a6_recovery_gate_preserves_upstream_stale_cooldown_and_quarantine_blocks(self):
        recovery = self.recovery_runtime_gate_inputs()
        recovery["recovery_admission_certification"]["rows"][0].update({
            "certification_state": "NOT_CERTIFIED_COLLECT_REAL_EVIDENCE",
            "blockers": [
                "recovery_freshness_not_actionable",
                "cooldown_active",
                "quarantine_or_degraded_lifecycle",
            ],
        })
        arbitration = self.build_a6_with_recovery(**recovery)

        self.assertIn("recovery_admission", arbitration["stop_gates"])
        blockers = arbitration["recovery_runtime_integration"]["blockers"]
        self.assertIn("recovery_freshness_not_actionable", blockers)
        self.assertIn("cooldown_active", blockers)
        self.assertIn("quarantine_or_degraded_lifecycle", blockers)

    def test_a6_non_recovery_routing_remains_compatible(self):
        arbitration = self.build_a6_with_recovery(
            recovery_admission_certification={
                "schema_version": "v7.b8.recovery-admission-certification.v1",
                "rows": [{
                    "channel": "awg1",
                    "certification_state": "CERTIFIED_FOR_RECOVERY_ADMISSION_REVIEW",
                    "admission_state": "ELIGIBLE",
                    "blockers": [],
                }],
            },
        )

        gates = {row["gate"]: row for row in arbitration["gate_rows"]}
        self.assertEqual(gates["recovery_admission"]["state"], "NOT_APPLICABLE")
        self.assertNotIn("recovery_admission", arbitration["stop_gates"])
        self.assertEqual(
            arbitration["recovery_runtime_integration"]["state"],
            "NOT_APPLICABLE_NO_RECOVERY_CANDIDATE",
        )

    def test_a6_runtime_eligibility_arbitration_is_read_only_stop_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[{
                    "recommendation_id": "r1",
                    "decision_id": "decision-1",
                    "packet_id": "p1",
                    "apply_result": "success",
                    "post_action_verification": {"status": "passed"},
                    "service_outcome": {"telegram": "ok"},
                    "user_outcome": {"user": "10.7.0.2"},
                    "learning_record": {"stored": True},
                    "outcome_observed_at": "2026-06-24T00:00:00+00:00",
                    "blast_radius": 1,
                    "selected_move_count": 1,
                    "user": "10.7.0.2",
                    "target": "awg0",
                    "service_delta": 5,
                    "prediction_delta": 3,
                }],
                generated_at="2026-06-25T00:00:00+00:00",
            )

        arbitration = inventory["runtime_eligibility_arbitration"]
        self.assertEqual(arbitration["schema_version"], "v7.a6-runtime-eligibility-arbitration.v1")
        self.assertEqual(arbitration["backlog_item"], "A6")
        gates = {row["gate"]: row["state"] for row in arbitration["gate_rows"]}
        self.assertIn("freshness", gates)
        self.assertIn("authority", gates)
        self.assertIn("blast_radius", gates)
        self.assertIn("rollback_or_no_rollback", gates)
        self.assertIn("anti_flap", gates)
        self.assertIn("verification", gates)
        self.assertIn("learning", gates)
        self.assertIn("routing_readiness", gates)
        self.assertIn("recovery_admission", gates)
        self.assertIn("runtime_apply", gates)
        self.assertEqual(gates["blast_radius"], "PASS")
        self.assertEqual(gates["authority"], "PASS")
        self.assertEqual(gates["runtime_apply"], "STOP")
        self.assertEqual(gates["recovery_admission"], "NOT_APPLICABLE")
        self.assertNotIn("recovery_admission", arbitration["stop_gates"])
        self.assertEqual(arbitration["runtime_execute_decision"], "STOP_SAFE")
        self.assertFalse(arbitration["runtime_apply_allowed"])
        self.assertFalse(arbitration["runtime_can_execute_automatically"])
        self.assertFalse(arbitration["authority_expanded"])
        self.assertFalse(arbitration["apply_executed"])
        self.assertEqual(arbitration["users_moved"], 0)
        self.assertFalse(arbitration["new_runtime_created"])

    def test_a6_runtime_eligibility_arbitration_blocks_evidence_gates(self):
        arbitration = accel.build_runtime_eligibility_arbitration(
            action_class_runtime_enablement={
                "delegated_autonomy_runtime_eligibility": {
                    "blockers": [],
                    "runtime_can_execute_automatically": False,
                    "stale_required_domains": [],
                },
                "enablement_readiness": {"missing_evidence": ["class-level rollback_or_no_rollback_certification"]},
            },
            class_level_blast_radius_certification={"beyond_one_user_certified": False},
            freshness_actionability={"domains": {}},
            anti_flapping={"summary": {"blocked_users": 1}},
            decision_outcome_closure={"closure_state": "PARTIAL"},
            decision_outcome_learning={"knowledge_growth": {"knowledge_gained": 0}},
            routing_recommendation_readiness={"blockers": ["service_user_sla_fit_not_clear"]},
        )

        self.assertEqual(arbitration["arbitration_state"], "STOP_AT_AUTHORITY_OR_RUNTIME_APPLY")
        self.assertIn("blast_radius", arbitration["stop_gates"])
        self.assertIn("anti_flap", arbitration["stop_gates"])
        self.assertIn("verification", arbitration["stop_gates"])
        self.assertIn("learning", arbitration["stop_gates"])
        self.assertFalse(arbitration["runtime_mutation_performed"])
        self.assertFalse(arbitration["autonomy_enabled"])

    def test_b13_metric_reliability_certifies_blocking_recommendation_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[{
                    "recommendation_id": "r1",
                    "decision_id": "decision-1",
                    "packet_id": "p1",
                    "apply_result": "success",
                    "post_action_verification": {"status": "passed"},
                    "service_outcome": {"telegram": "ok"},
                    "user_outcome": {"user": "10.7.0.2"},
                    "learning_record": {"stored": True},
                    "outcome_observed_at": "2026-06-24T00:00:00+00:00",
                    "blast_radius": 1,
                    "selected_move_count": 1,
                    "user": "10.7.0.2",
                    "target": "awg0",
                    "service_delta": 5,
                    "prediction_delta": 3,
                }],
                generated_at="2026-06-25T00:00:00+00:00",
            )

        certification = inventory["metric_reliability_certification"]
        self.assertEqual(certification["schema_version"], "v7.b13-metric-reliability-certification.v1")
        self.assertEqual(certification["backlog_item"], "B13")
        self.assertEqual(certification["certification_state"], "CERTIFIED_FOR_BLOCKING_RECOMMENDATIONS_ONLY")
        metrics = {row["metric"]: row["state"] for row in certification["metric_rows"]}
        self.assertIn("confidence", metrics)
        self.assertIn("trust", metrics)
        self.assertIn("prediction_confidence", metrics)
        self.assertIn("prediction_matches", metrics)
        self.assertIn("service_outcomes", metrics)
        self.assertIn("candidate_outcomes", metrics)
        self.assertIn("rollback_evidence", metrics)
        self.assertIn("blast_radius_evidence", metrics)
        self.assertIn("outcome_closure", metrics)
        self.assertIn("learning", metrics)
        self.assertIn("a6_runtime_eligibility", metrics)
        self.assertTrue(certification["blocking_recommendation_certified"])
        self.assertFalse(certification["automated_positive_promotion_recommendation_allowed"])
        self.assertIn("runtime_apply", certification["positive_promotion_blockers"])
        self.assertEqual(
            certification["omp_output"]["next_safe_action"],
            "continue to B16 rollback authority certification",
        )
        self.assertFalse(certification["runtime_mutation_performed"])
        self.assertFalse(certification["apply_executed"])
        self.assertEqual(certification["users_moved"], 0)
        self.assertFalse(certification["authority_expanded"])
        self.assertFalse(certification["new_owner_created"])

    def test_b13_metric_reliability_blocks_mandatory_metric_gate_failures(self):
        certification = accel.build_metric_reliability_certification(
            canary_proximity={"primary_floors": {}},
            floor_forensics={"component_values": {}},
            source_confidence_inventory={"sources": []},
            evidence_sufficiency={"insufficient_sources": ["candidate_outcomes"]},
            decision_outcome_closure={"closure_state": "PARTIAL"},
            decision_outcome_learning={"knowledge_growth": {"knowledge_gained": 0}},
            freshness_actionability={"domains": {"service": {"classification": "UNKNOWN"}}},
            routing_recommendation_readiness={"blockers": ["decision_outcome_closure_incomplete"]},
            action_class_runtime_enablement={"enablement_readiness": {"missing_evidence": ["class-level authority_policy_approval"]}},
            class_level_blast_radius_certification={"beyond_one_user_certified": False},
            runtime_eligibility_arbitration={"schema_version": "missing", "runtime_execute_decision": "UNKNOWN"},
        )

        self.assertEqual(certification["certification_state"], "NOT_CERTIFIED_MANDATORY_METRIC_GATE_FAILED")
        self.assertFalse(certification["blocking_recommendation_certified"])
        self.assertIn("outcome_closure", certification["stop_metrics"])
        self.assertIn("learning", certification["stop_metrics"])
        self.assertIn("freshness", certification["partial_metrics"])
        self.assertIn("a5_blast_radius", certification["stop_metrics"])
        self.assertIn("a6_runtime_eligibility", certification["stop_metrics"])
        self.assertFalse(certification["runtime_mutation_performed"])
        self.assertFalse(certification["autonomy_enabled"])

    def test_b12_next_action_class_stage_certification_is_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[{
                    "recommendation_id": "r1",
                    "decision_id": "decision-1",
                    "packet_id": "p1",
                    "apply_result": "success",
                    "post_action_verification": {"status": "passed"},
                    "service_outcome": {"telegram": "ok"},
                    "user_outcome": {"user": "10.7.0.2"},
                    "learning_record": {"stored": True},
                    "outcome_observed_at": "2026-06-24T00:00:00+00:00",
                    "blast_radius": 1,
                    "selected_move_count": 1,
                    "user": "10.7.0.2",
                    "target": "awg0",
                    "service_delta": 5,
                    "prediction_delta": 3,
                }],
                generated_at="2026-06-25T00:00:00+00:00",
            )

        certification = inventory["next_action_class_stage_certification"]
        self.assertEqual(certification["schema_version"], "v7.b12-next-action-class-stage-certification.v1")
        self.assertEqual(certification["backlog_item"], "B12")
        self.assertEqual(
            certification["next_stage"]["stage_certification_state"],
            "NEXT_ACTION_CLASS_STAGE_CERTIFIED_FOR_AUTHORITY_REVIEW_READ_ONLY",
        )
        self.assertTrue(certification["next_stage"]["stage_certified_for_review"])
        self.assertFalse(certification["next_stage"]["stage_certified_for_runtime"])
        self.assertFalse(certification["next_stage"]["stage_promoted"])
        self.assertFalse(certification["next_stage"]["runtime_apply_allowed"])
        self.assertFalse(certification["next_stage"]["direct_class_promotion_allowed"])
        self.assertIn("authority_boundary", certification["next_stage"]["blockers"])
        self.assertIn("runtime_apply_boundary", certification["next_stage"]["blockers"])
        self.assertEqual(certification["summary"]["hard_blockers"], 0)
        self.assertFalse(certification["runtime_mutation_performed"])
        self.assertFalse(certification["apply_executed"])
        self.assertEqual(certification["users_moved"], 0)
        self.assertFalse(certification["authority_expanded"])
        self.assertFalse(certification["direct_class_promotion_performed"])
        self.assertFalse(certification["new_owner_created"])

    def test_b12_blocks_when_required_certification_evidence_is_missing(self):
        certification = accel.build_next_action_class_stage_certification(
            action_class_runtime_enablement={
                "current_action_class": "single-user governed candidate failover",
                "action_classes": [{
                    "action_class": "single-user governed candidate failover",
                    "current_state": "NOT_CERTIFIED",
                    "next_state": "GOVERNED_ONLY",
                }],
            },
            class_level_blast_radius_certification={
                "schema_version": "v7.a5-class-level-blast-radius-certification.v1",
                "beyond_one_user_certified": False,
            },
            runtime_eligibility_arbitration={"schema_version": "missing"},
            metric_reliability_certification={
                "schema_version": "v7.b13-metric-reliability-certification.v1",
                "blocking_recommendation_certified": False,
            },
            org_cohort_identity_policy_integration={"schema_version": "missing"},
        )

        self.assertEqual(
            certification["next_stage"]["stage_certification_state"],
            "NEXT_ACTION_CLASS_STAGE_BLOCKED_BY_EVIDENCE",
        )
        self.assertFalse(certification["next_stage"]["stage_certified_for_review"])
        self.assertIn("action_class_ladder_current_stage", certification["next_stage"]["blockers"])
        self.assertIn("a5_blast_radius_certification", certification["next_stage"]["blockers"])
        self.assertIn("a6_runtime_eligibility_arbitration", certification["next_stage"]["blockers"])
        self.assertIn("b13_blocking_recommendation_metric_reliability", certification["next_stage"]["blockers"])
        self.assertIn("b11_identity_policy_boundary", certification["next_stage"]["blockers"])
        self.assertFalse(certification["authority_expanded"])
        self.assertFalse(certification["autonomy_enabled"])
        self.assertFalse(certification["direct_class_promotion_performed"])

    def test_b14_service_pool_cohort_blast_radius_scope_is_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[{
                    "recommendation_id": "r1",
                    "decision_id": "decision-1",
                    "packet_id": "p1",
                    "apply_result": "success",
                    "post_action_verification": {"status": "passed"},
                    "service_outcome": {"telegram": "ok"},
                    "user_outcome": {"user": "10.7.0.2"},
                    "learning_record": {"stored": True},
                    "outcome_observed_at": "2026-06-24T00:00:00+00:00",
                    "blast_radius": 1,
                    "selected_move_count": 1,
                    "user": "10.7.0.2",
                    "target": "awg0",
                    "service_delta": 5,
                    "prediction_delta": 3,
                }],
                generated_at="2026-06-25T00:00:00+00:00",
            )

        scope = inventory["service_pool_cohort_blast_radius_scope"]
        self.assertEqual(scope["schema_version"], "v7.b14-service-pool-cohort-blast-radius-scope.v1")
        self.assertEqual(scope["backlog_item"], "B14")
        self.assertEqual(scope["consumed_prior_capabilities"]["B11"], "v7.b11.org-cohort-identity-policy-integration.v1")
        self.assertEqual(scope["consumed_prior_capabilities"]["B12"], "v7.b12-next-action-class-stage-certification.v1")
        self.assertGreaterEqual(scope["summary"]["scope_rows"], 1)
        self.assertIn("service_pool_cohort_scope_is_read_only_visibility_not_runtime_apply", scope["canonical_rules"])
        self.assertFalse(scope["runtime_mutation_performed"])
        self.assertFalse(scope["apply_executed"])
        self.assertEqual(scope["users_moved"], 0)
        self.assertFalse(scope["authority_expanded"])
        self.assertFalse(scope["blast_radius_expanded"])
        self.assertFalse(scope["synthetic_evidence_created"])
        self.assertFalse(scope["new_owner_created"])
        self.assertFalse(scope["threshold_values_changed"])
        self.assertFalse(scope["formula_changed"])
        first = scope["rows"][0]
        self.assertIn("service_scope", first)
        self.assertIn("pool_scope", first)
        self.assertIn("cohort_scope", first)
        self.assertIn("blast_radius_scope", first)
        self.assertFalse(first["runtime_apply_allowed"])
        self.assertFalse(first["authority_expanded"])

    def test_b14_blocks_scope_when_existing_gates_are_missing(self):
        scope = accel.build_service_pool_cohort_blast_radius_scope(
            decision_surface={"users": [{"user": "10.7.0.2", "current_channel": "vless", "recommended_channel": "awg0"}]},
            service_user_sla_fit={
                "schema_version": "v7.routing-foundation.service-user-sla-fit.v1",
                "rows": [{
                    "user": "10.7.0.2",
                    "current_assignment": "vless",
                    "required_services": ["telegram"],
                    "best_channel": "awg0",
                    "fit_verdict": "BLOCKED",
                    "candidates": [{
                        "channel": "awg0",
                        "fit_verdict": "BLOCKED",
                        "missing_requirements": ["telegram"],
                    }],
                }],
            },
            class_level_blast_radius_certification={
                "schema_version": "v7.a5-class-level-blast-radius-certification.v1",
                "beyond_one_user_certified": False,
            },
            next_action_class_stage_certification={
                "schema_version": "v7.b12-next-action-class-stage-certification.v1",
                "next_stage": {"stage_certification_state": "NEXT_ACTION_CLASS_STAGE_BLOCKED_BY_EVIDENCE"},
            },
            org_cohort_identity_policy_integration={"schema_version": "missing", "rows": []},
            generated_at="2026-06-25T00:00:00+00:00",
        )

        self.assertEqual(scope["summary"]["scope_rows"], 1)
        self.assertEqual(scope["summary"]["mapped_rows"], 0)
        self.assertEqual(scope["rows"][0]["scope_state"], "SERVICE_POOL_COHORT_SCOPE_BLOCKED_BY_EXISTING_GATES")
        self.assertIn("cohort_scope_missing", scope["rows"][0]["blockers"])
        self.assertIn("a5_blast_radius_not_certified_beyond_one_user", scope["rows"][0]["blockers"])
        self.assertIn("b12_next_action_class_stage_not_certified_for_review", scope["rows"][0]["blockers"])
        self.assertFalse(scope["runtime_mutation_performed"])
        self.assertFalse(scope["apply_executed"])
        self.assertEqual(scope["users_moved"], 0)
        self.assertFalse(scope["authority_expanded"])
        self.assertFalse(scope["blast_radius_expanded"])

    def test_c4_all_at_once_promotion_unavailable_verification_is_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[{
                    "recommendation_id": "r1",
                    "decision_id": "decision-1",
                    "packet_id": "p1",
                    "apply_result": "success",
                    "post_action_verification": {"status": "passed"},
                    "service_outcome": {"telegram": "ok"},
                    "user_outcome": {"user": "10.7.0.2"},
                    "learning_record": {"stored": True},
                    "outcome_observed_at": "2026-06-24T00:00:00+00:00",
                    "blast_radius": 1,
                    "selected_move_count": 1,
                    "user": "10.7.0.2",
                    "target": "awg0",
                    "service_delta": 5,
                    "prediction_delta": 3,
                }],
                generated_at="2026-06-25T00:00:00+00:00",
            )

        verification = inventory["all_at_once_promotion_unavailable_verification"]
        self.assertEqual(verification["schema_version"], "v7.c4-all-at-once-promotion-unavailable.v1")
        self.assertEqual(verification["backlog_item"], "C4")
        self.assertEqual(
            verification["verification_state"],
            "DONE_READ_ONLY_ALL_AT_ONCE_PROMOTION_UNAVAILABLE",
        )
        self.assertFalse(verification["all_at_once_promotion_allowed"])
        self.assertFalse(verification["direct_class_promotion_allowed"])
        self.assertFalse(verification["runtime_apply_allowed"])
        self.assertFalse(verification["authority_expanded"])
        self.assertFalse(verification["blast_radius_expanded"])
        self.assertFalse(verification["automation_enabled"])
        self.assertEqual(verification["summary"]["all_at_once_promotions_available"], 0)
        self.assertEqual(verification["summary"]["direct_promotions_available"], 0)
        self.assertEqual(verification["summary"]["runtime_apply_paths_available"], 0)
        self.assertIn(
            "c4_keeps_all_at_once_promotion_unavailable_for_current_action_classes",
            verification["canonical_rules"],
        )
        self.assertEqual(
            verification["omp_output"]["unlocked_capability"],
            "C5_ROLLBACK_OPERATIONAL_COMPENSATION_NOT_TRANSACTION_ROLLBACK",
        )
        self.assertIn(
            "all_at_once_action_class_promotion",
            verification["omp_output"]["blocked_later_steps"],
        )
        self.assertFalse(verification["runtime_mutation_performed"])
        self.assertFalse(verification["apply_executed"])
        self.assertEqual(verification["users_moved"], 0)
        self.assertFalse(verification["synthetic_evidence_created"])
        self.assertFalse(verification["new_owner_created"])
        self.assertFalse(verification["new_runtime_created"])

    def test_c4_all_at_once_promotion_verification_stops_on_existing_gate_violation(self):
        verification = accel.build_all_at_once_promotion_unavailable_verification(
            action_class_runtime_enablement={
                "schema_version": "v7.action-class-runtime-enablement.v2",
                "action_classes": [{
                    "action_class": "single-user governed candidate failover",
                    "current_state": "GOVERNED_ONLY",
                    "next_state": "CERTIFIED_FOR_CLASS_APPROVAL",
                }],
            },
            class_level_blast_radius_certification={
                "schema_version": "v7.a5-class-level-blast-radius-certification.v1",
            },
            next_action_class_stage_certification={
                "schema_version": "v7.b12-next-action-class-stage-certification.v1",
                "next_stage": {
                    "authority_review_required": False,
                    "direct_class_promotion_allowed": True,
                    "stage_promoted": True,
                },
            },
            service_pool_cohort_blast_radius_scope={
                "schema_version": "v7.b14-service-pool-cohort-blast-radius-scope.v1",
                "rows": [{"runtime_apply_allowed": True}],
                "blast_radius_expanded": True,
            },
            generated_at="2026-06-25T00:00:00+00:00",
        )

        self.assertEqual(
            verification["verification_state"],
            "STOP_SAFE_PROMOTION_AVAILABILITY_VIOLATION_DETECTED",
        )
        self.assertIn("authority_review_required", verification["violations"])
        self.assertIn("runtime_apply_remains_disabled", verification["violations"])
        self.assertIn("blast_radius_not_expanded_now", verification["violations"])
        self.assertIn("direct_class_promotion_forbidden", verification["violations"])
        self.assertFalse(verification["all_at_once_promotion_allowed"])
        self.assertFalse(verification["direct_class_promotion_allowed"])
        self.assertFalse(verification["runtime_mutation_performed"])
        self.assertFalse(verification["new_owner_created"])

    def test_b17_stale_read_mutation_blocking_is_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-25T00:00:00+00:00",
            )

        model = inventory["stale_read_mutation_blocking"]
        self.assertEqual(model["schema_version"], "v7.b17-stale-read-mutation-blocking.v1")
        self.assertEqual(model["backlog_item"], "B17")
        self.assertIn("stale_reads_are_reportable", model["read_only_contract"])
        self.assertTrue(model["read_only_contract"]["stale_reads_are_reportable"])
        self.assertFalse(model["read_only_contract"]["stale_reads_can_authorize_mutation"])
        self.assertIn("runtime_apply_boundary", model["mutation_blockers"])
        self.assertIn("authority_boundary", model["mutation_blockers"])
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])
        self.assertFalse(model["synthetic_evidence_created"])
        self.assertFalse(model["threshold_values_changed"])
        self.assertFalse(model["formula_changed"])
        self.assertFalse(model["new_owner_created"])

    def test_b17_reports_stale_reads_while_blocking_mutation(self):
        freshness = accel.build_freshness_actionability({
            "service-scores": {"freshness_state": "STALE", "stop_required": True, "runtime_behavior": "STOP"},
            "channel-service-scores": {"freshness_state": "FRESH", "stop_required": False, "runtime_behavior": "READ"},
        })
        runtime = {
            "schema_version": "v7.a6-runtime-eligibility-arbitration.v1",
            "gate_rows": [{"gate": "freshness", "state": "STOP", "owner": "freshness_actionability"}],
        }
        model = accel.build_stale_read_mutation_blocking(
            freshness_actionability=freshness,
            runtime_eligibility_arbitration=runtime,
            routing_recommendation_readiness={
                "schema_version": "v7.routing-foundation.recommendation-readiness.v1",
                "blockers": ["freshness_not_actionable:service"],
            },
            generated_at="2026-06-25T00:00:00+00:00",
        )

        stale_rows = [row for row in model["rows"] if row["read_visibility"] == "REPORT_STALE_READ"]
        self.assertGreaterEqual(len(stale_rows), 1)
        self.assertIn("stale_read:service", model["mutation_blockers"])
        self.assertIn("runtime_eligibility_freshness_gate_stop", model["mutation_blockers"])
        self.assertIn("routing:freshness_not_actionable:service", model["mutation_blockers"])
        self.assertTrue(all(row["runtime_read_allowed"] for row in model["rows"]))
        self.assertTrue(all(row["runtime_mutation_allowed"] is False for row in model["rows"]))
        self.assertEqual(model["summary"]["runtime_actions_created"], 0)
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])

    def test_b18_owner_issued_version_lease_pattern_is_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-25T00:00:00+00:00",
            )

        model = inventory["owner_issued_version_lease_pattern"]
        self.assertEqual(model["schema_version"], "v7.b18-owner-issued-version-lease-pattern.v1")
        self.assertEqual(model["backlog_item"], "B18")
        self.assertEqual(model["existing_execution_lease_contract"]["status"], "REUSED_NO_BEHAVIOR_CHANGE")
        self.assertTrue(model["existing_execution_lease_contract"]["freshness_only_change_preserves_lease"])
        self.assertTrue(model["existing_execution_lease_contract"]["material_state_change_invalidates_lease"])
        self.assertGreaterEqual(model["summary"]["coverage_rows"], 1)
        self.assertEqual(model["summary"]["runtime_actions_created"], 0)
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])
        self.assertFalse(model["synthetic_evidence_created"])
        self.assertFalse(model["threshold_values_changed"])
        self.assertFalse(model["formula_changed"])
        self.assertFalse(model["lease_behavior_changed"])
        self.assertFalse(model["new_owner_created"])

    def test_b18_classifies_owner_issued_pattern_present_and_partial(self):
        freshness = accel.build_freshness_actionability({
            "service-scores": {
                "exists": True,
                "schema": "v7.intelligence.service-scores.v1",
                "generated_at": "2026-06-25T00:00:00+00:00",
                "expires_at": "2026-06-25T00:02:00+00:00",
                "ttl_seconds": 120,
                "freshness_state": "FRESH",
                "runtime_behavior": "ALLOW",
                "source_hashes": {"service-matrix": "hash-service"},
                "generator": "test-owner",
                "path": "/tmp/service-scores.json",
            },
            "channel-service-scores": {
                "exists": True,
                "freshness_state": "FRESH",
                "runtime_behavior": "ALLOW",
            },
        })
        windows = accel.build_action_class_freshness_windows(freshness)
        stale = accel.build_stale_read_mutation_blocking(
            freshness_actionability=freshness,
            runtime_eligibility_arbitration={
                "schema_version": "v7.a6-runtime-eligibility-arbitration.v1",
                "gate_rows": [{"gate": "freshness", "state": "PASS"}],
            },
        )
        model = accel.build_owner_issued_version_lease_pattern(
            freshness_actionability=freshness,
            action_class_freshness_windows=windows,
            stale_read_mutation_blocking=stale,
            generated_at="2026-06-25T00:00:00+00:00",
        )

        service_row = next(row for row in model["rows"] if row["snapshot_family"] == "service-scores")
        channel_row = next(row for row in model["rows"] if row["snapshot_family"] == "channel-service-scores")
        self.assertEqual(service_row["pattern_status"], "OWNER_ISSUED_VERSION_LEASE_PATTERN_PRESENT")
        self.assertEqual(channel_row["pattern_status"], "OWNER_ISSUED_VERSION_LEASE_PATTERN_MISSING")
        self.assertTrue(service_row["owner_issued_identity_present"])
        self.assertTrue(service_row["owner_issued_lifetime_present"])
        self.assertFalse(channel_row["runtime_mutation_allowed"])
        self.assertEqual(model["omp_output"]["b18_status"], "DONE_READ_ONLY_OWNER_ISSUED_VERSION_LEASE_PATTERN")
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])

    def test_b19_hysteresis_state_change_cost_mapping_is_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-25T00:00:00+00:00",
            )

        model = inventory["hysteresis_state_change_cost_mapping"]
        self.assertEqual(model["schema_version"], "v7.b19-hysteresis-state-change-cost-mapping.v1")
        self.assertEqual(model["backlog_item"], "B19")
        controls = {row["control"] for row in model["catalog_rows"]}
        self.assertIn("sticky_current_bias", controls)
        self.assertIn("cooldown_hold_down", controls)
        self.assertIn("user_freeze", controls)
        self.assertIn("pair_reversal_window", controls)
        self.assertIn("recovery_success_threshold", controls)
        self.assertIn("hard_failure_override_is_not_implemented_by_b19_and_remains_b20", model["canonical_rules"])
        self.assertEqual(model["summary"]["threshold_changes"], 0)
        self.assertEqual(model["summary"]["formula_changes"], 0)
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])
        self.assertFalse(model["synthetic_evidence_created"])
        self.assertFalse(model["threshold_values_changed"])
        self.assertFalse(model["formula_changed"])
        self.assertFalse(model["new_owner_created"])

    def test_b19_maps_active_anti_flap_block_without_runtime_apply(self):
        anti = accel.build_anti_flapping([
            {"user": "10.7.0.11", "from": "vless", "to": "awg0"},
            {"user": "10.7.0.11", "from": "awg0", "to": "vless"},
        ])
        recovery = accel.build_recovery_admission(
            {"channels": [{"channel": "awg0", "successful_checks": 3, "lifecycle": "RECOVERING"}]},
            freshness_actionability=accel.build_freshness_actionability({
                "trust-evolution-summaries": {"freshness_state": "FRESH", "runtime_behavior": "ALLOW"}
            }),
        )
        model = accel.build_hysteresis_state_change_cost_mapping(
            anti_flapping=anti,
            recovery_admission=recovery,
            owner_issued_version_lease_pattern={"schema_version": "v7.b18-owner-issued-version-lease-pattern.v1"},
            generated_at="2026-06-25T00:00:00+00:00",
        )

        self.assertEqual(model["summary"]["active_anti_flap_blocked_users"], 1)
        self.assertEqual(model["active_evidence"]["blocked_users"], 1)
        self.assertEqual(model["omp_output"]["b19_status"], "DONE_READ_ONLY_HYSTERESIS_STATE_CHANGE_COST_MAPPING")
        self.assertIn("threshold_formula_mutation", model["omp_output"]["blocked_later_steps"])
        self.assertIn("hard_failure_override", model["omp_output"]["blocked_later_steps"])
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])

    def test_b20_confirmed_hard_failure_marks_anti_flap_override_candidate_read_only(self):
        anti = accel.build_anti_flapping([
            {"user": "10.7.0.11", "from": "vless", "to": "awg0"},
            {"user": "10.7.0.11", "from": "awg0", "to": "vless"},
        ])
        model = accel.build_hard_failure_override_anti_flap_arbitration(
            hard_failure_classification={"schema_version": "v7.policy-001.hard-failure-classification.v1"},
            hard_failure_policy_windows={
                "schema_version": "v7.b2.hard-failure-policy-windows.v1",
                "rows": [{
                    "object": "awg0",
                    "risk_class": "CRITICAL_CONFIRMED_HARD_FAILURE",
                    "hard_failure_classification": "HARD_FAILURE_CONFIRMED",
                    "selected_action_class": "channel hard-fail failover",
                    "blockers": ["anti_flap_blocks_recent_oscillation"],
                }],
            },
            anti_flapping=anti,
            hysteresis_state_change_cost_mapping={"schema_version": "v7.b19-hysteresis-state-change-cost-mapping.v1"},
            generated_at="2026-06-25T00:00:00+00:00",
        )

        self.assertEqual(model["schema_version"], "v7.b20-hard-failure-override-anti-flap-arbitration.v1")
        self.assertEqual(model["backlog_item"], "B20")
        row = model["rows"][0]
        self.assertEqual(row["arbitration_result"], "HARD_FAILURE_OVERRIDE_ELIGIBLE_FOR_AUTHORITY_REVIEW")
        self.assertEqual(row["anti_flap_result"], "OVERRIDE_CANDIDATE_READ_ONLY")
        self.assertTrue(row["anti_flap_conflict"])
        self.assertFalse(row["hard_failure_override_executed"])
        self.assertFalse(row["runtime_apply_allowed"])
        self.assertFalse(row["authority_expansion_allowed"])
        self.assertEqual(model["summary"]["override_candidates"], 1)
        self.assertEqual(model["summary"]["runtime_actions_created"], 0)
        self.assertEqual(model["summary"]["threshold_changes"], 0)
        self.assertIn("confirmed_hard_failure_may_override_anti_flap_only_as_read_only_authority_review_candidate", model["canonical_rules"])
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])
        self.assertFalse(model["hard_failure_override_executed"])

    def test_b20_suspected_hard_failure_never_overrides_anti_flap(self):
        model = accel.build_hard_failure_override_anti_flap_arbitration(
            hard_failure_policy_windows={
                "schema_version": "v7.b2.hard-failure-policy-windows.v1",
                "rows": [{
                    "object": "awg3",
                    "risk_class": "SUSPECTED_HARD_FAILURE",
                    "hard_failure_classification": "HARD_FAILURE_SUSPECTED",
                    "selected_action_class": "single-user governed candidate failover",
                    "blockers": ["anti_flap_blocks_recent_oscillation"],
                }],
            },
            anti_flapping={"schema_version": "v7.routing-foundation.anti-flapping.v1", "summary": {"blocked_users": 1}},
            hysteresis_state_change_cost_mapping={"schema_version": "v7.b19-hysteresis-state-change-cost-mapping.v1"},
            generated_at="2026-06-25T00:00:00+00:00",
        )

        row = model["rows"][0]
        self.assertEqual(row["arbitration_result"], "ANTI_FLAP_HOLDS_CONFIRMATION_REQUIRED")
        self.assertEqual(row["anti_flap_result"], "HOLD")
        self.assertIn("hard_failure_confirmation_required", row["remaining_blockers"])
        self.assertEqual(model["summary"]["override_candidates"], 0)
        self.assertEqual(model["summary"]["anti_flap_holds"], 1)
        self.assertFalse(model["hard_failure_override_executed"])
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])

    def test_b21_per_user_routing_control_mode_normalizes_existing_fields_read_only(self):
        model = accel.build_per_user_routing_control_mode(
            decision_surface={
                "users": [
                    {
                        "user": "10.7.0.2",
                        "current_channel": "vless",
                        "recommended_channel": "awg0",
                        "routing_control_mode": "AUTO",
                    },
                    {
                        "user": "10.7.0.3",
                        "current_channel": "awg1",
                        "recommended_channel": "awg2",
                        "raw": {"manual_only": "1", "group": "vip"},
                    },
                    {
                        "user": "10.7.0.4",
                        "current_channel": "awg3",
                        "recommended_channel": "awg0",
                        "pinned_channel": "awg3",
                    },
                ]
            },
            org_cohort_identity_policy_integration={"schema_version": "v7.b11.org-cohort-identity-policy-integration.v1"},
            hard_failure_override_anti_flap_arbitration={"schema_version": "v7.b20-hard-failure-override-anti-flap-arbitration.v1"},
            generated_at="2026-06-25T00:00:00+00:00",
        )

        self.assertEqual(model["schema_version"], "v7.b21-per-user-routing-control-mode.v1")
        self.assertEqual(model["backlog_item"], "B21")
        by_user = {row["user"]: row for row in model["rows"]}
        self.assertEqual(by_user["10.7.0.2"]["routing_control_mode"], "AUTO")
        self.assertEqual(by_user["10.7.0.2"]["mode_source_status"], "EXISTS_COMPLETE")
        self.assertTrue(by_user["10.7.0.2"]["planner_recommendation_allowed"])
        self.assertEqual(by_user["10.7.0.3"]["routing_control_mode"], "MANUAL")
        self.assertEqual(by_user["10.7.0.3"]["mode_source_status"], "EXISTS_UNDER_OTHER_NAME")
        self.assertTrue(by_user["10.7.0.3"]["planner_move_blocked_by_mode"])
        self.assertEqual(by_user["10.7.0.4"]["routing_control_mode"], "PINNED")
        self.assertIn("recommended_channel_differs_from_pinned_channel", by_user["10.7.0.4"]["blockers"])
        self.assertEqual(model["summary"]["auto"], 1)
        self.assertEqual(model["summary"]["manual"], 1)
        self.assertEqual(model["summary"]["pinned"], 1)
        self.assertEqual(model["summary"]["runtime_actions_created"], 0)
        self.assertFalse(model["registry_written"])
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])
        self.assertFalse(model["new_owner_created"])

    def test_b21_inventory_exposes_per_user_routing_control_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-25T00:00:00+00:00",
            )

        model = inventory["per_user_routing_control_mode"]
        self.assertEqual(model["schema_version"], "v7.b21-per-user-routing-control-mode.v1")
        self.assertEqual(model["backlog_item"], "B21")
        self.assertEqual(model["summary"]["users_seen"], 2)
        self.assertEqual(model["summary"]["missing_explicit_mode"], 2)
        self.assertEqual(model["omp_output"]["b21_status"], "DONE_READ_ONLY_PER_USER_ROUTING_CONTROL_MODE")
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])

    def test_c1_fail_open_fail_closed_action_class_behavior_is_read_only(self):
        model = accel.build_fail_open_fail_closed_action_class_behavior(
            action_class_runtime_enablement={
                "schema_version": "v7.action-class-runtime-enablement.v1",
                "action_classes": [
                    {
                        "action_class": "single-user governed candidate failover",
                        "runtime_state": "GOVERNED_ONLY",
                        "missing_evidence": ["authority_not_granted"],
                    },
                    {
                        "action_class": "channel hard-fail failover",
                        "runtime_state": "GOVERNED_ONLY",
                    },
                ],
            },
            runtime_eligibility_arbitration={
                "schema_version": "v7.a6-runtime-eligibility-arbitration.v1",
                "gate_rows": [
                    {"gate": "runtime_apply", "state": "STOP"},
                    {"gate": "authority", "state": "STOP"},
                ],
            },
            per_user_routing_control_mode={
                "schema_version": "v7.b21-per-user-routing-control-mode.v1",
                "summary": {"manual": 1, "pinned": 1},
            },
            hard_failure_override_anti_flap_arbitration={
                "schema_version": "v7.b20-hard-failure-override-anti-flap-arbitration.v1",
                "summary": {"override_candidates": 1},
            },
            stale_read_mutation_blocking={
                "schema_version": "v7.b17-stale-read-mutation-blocking.v1",
                "stale_domains": ["capacity"],
            },
            owner_issued_version_lease_pattern={
                "schema_version": "v7.b18-owner-issued-version-lease-pattern.v1",
                "summary": {"pattern_missing": 1},
            },
            generated_at="2026-06-25T00:00:00+00:00",
        )

        self.assertEqual(model["schema_version"], "v7.c1-fail-open-fail-closed-action-class-behavior.v1")
        self.assertEqual(model["backlog_item"], "C1")
        by_class = {row["action_class"]: row for row in model["rows"]}
        single = by_class["single-user governed candidate failover"]
        self.assertEqual(single["runtime_apply_behavior"], "FAIL_CLOSED")
        self.assertIn("read_only_diagnosis", single["fail_open_allowed"])
        self.assertIn("authority_not_granted", single["fail_closed_conditions"])
        self.assertIn("manual_or_pinned_user_mode_present", single["fail_closed_conditions"])
        hard_fail = by_class["channel hard-fail failover"]
        self.assertIn("authority_review_candidate_only", hard_fail["fail_open_allowed"])
        self.assertFalse(hard_fail["hard_failure_override_context"]["override_execution_allowed"])
        self.assertEqual(model["summary"]["runtime_actions_created"], 0)
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])
        self.assertFalse(model["new_owner_created"])

    def test_c1_inventory_exposes_fail_open_fail_closed_behavior(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-25T00:00:00+00:00",
            )

        model = inventory["fail_open_fail_closed_action_class_behavior"]
        self.assertEqual(model["schema_version"], "v7.c1-fail-open-fail-closed-action-class-behavior.v1")
        self.assertEqual(model["backlog_item"], "C1")
        self.assertEqual(model["summary"]["action_classes_seen"], len(accel.ACTION_CLASS_LADDER))
        self.assertEqual(
            model["omp_output"]["c1_status"],
            "DONE_READ_ONLY_FAIL_OPEN_FAIL_CLOSED_ACTION_CLASS_BEHAVIOR",
        )
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])

    def test_c6_bounded_stale_allowance_by_action_class_is_read_only(self):
        freshness = accel.build_freshness_actionability({
            "service-scores": {"freshness_state": "STALE", "stop_required": True, "runtime_behavior": "STOP"},
            "channel-service-scores": {"freshness_state": "FRESH", "stop_required": False, "runtime_behavior": "READ"},
        })
        windows = accel.build_action_class_freshness_windows(freshness)
        runtime = {
            "schema_version": "v7.a6-runtime-eligibility-arbitration.v1",
            "gate_rows": [{"gate": "freshness", "state": "STOP", "owner": "freshness_actionability"}],
        }
        stale = accel.build_stale_read_mutation_blocking(
            freshness_actionability=freshness,
            runtime_eligibility_arbitration=runtime,
        )
        lease = accel.build_owner_issued_version_lease_pattern(
            freshness_actionability=freshness,
            action_class_freshness_windows=windows,
            stale_read_mutation_blocking=stale,
        )
        fail_behavior = accel.build_fail_open_fail_closed_action_class_behavior(
            runtime_eligibility_arbitration=runtime,
            stale_read_mutation_blocking=stale,
            owner_issued_version_lease_pattern=lease,
        )
        model = accel.build_bounded_stale_allowance_by_action_class(
            freshness_actionability=freshness,
            action_class_freshness_windows=windows,
            stale_read_mutation_blocking=stale,
            owner_issued_version_lease_pattern=lease,
            fail_open_fail_closed_action_class_behavior=fail_behavior,
            runtime_eligibility_arbitration=runtime,
            generated_at="2026-06-25T00:00:00+00:00",
        )

        self.assertEqual(model["schema_version"], "v7.c6-bounded-stale-allowance-by-action-class.v1")
        self.assertEqual(model["backlog_item"], "C6")
        self.assertEqual(model["decision"]["bounded_stale_mutation_allowance_seconds"], 0)
        self.assertTrue(model["decision"]["stale_evidence_observation_allowed"])
        self.assertTrue(model["decision"]["stale_evidence_engineering_report_allowed"])
        self.assertFalse(model["decision"]["stale_evidence_mutation_allowed"])
        self.assertTrue(model["decision"]["fresh_evidence_required_before_mutation"])
        self.assertGreaterEqual(model["summary"]["action_classes"], 1)
        self.assertEqual(model["summary"]["stale_mutation_allowed"], 0)
        self.assertTrue(all(row["stale_read_allowed_for_observation"] for row in model["rows"]))
        self.assertTrue(all(row["stale_read_allowed_for_mutation"] is False for row in model["rows"]))
        self.assertTrue(all(row["bounded_stale_mutation_allowance_seconds"] == 0 for row in model["rows"]))
        self.assertTrue(all(row["fresh_evidence_required_before_mutation"] for row in model["rows"]))
        self.assertTrue(any(
            "runtime_eligibility_freshness_gate_stop" in row["mutation_blockers"]
            for row in model["rows"]
        ))
        self.assertIn(
            "C7_POOL_MAX_EJECTION_MINIMUM_HEALTH_CAPACITY_BLAST_BOUNDS",
            model["omp_output"]["unlocked_capability"],
        )
        self.assertIn("mutation_from_stale_read", model["omp_output"]["blocked_later_steps"])
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])
        self.assertFalse(model["threshold_values_changed"])
        self.assertFalse(model["formula_changed"])
        self.assertFalse(model["new_owner_created"])

    def test_c6_inventory_exposes_bounded_stale_allowance(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-25T00:00:00+00:00",
            )

        model = inventory["bounded_stale_allowance_by_action_class"]
        self.assertEqual(model["schema_version"], "v7.c6-bounded-stale-allowance-by-action-class.v1")
        self.assertEqual(model["backlog_item"], "C6")
        self.assertEqual(
            model["omp_output"]["c6_status"],
            "DONE_READ_ONLY_BOUNDED_STALE_ALLOWANCE_BY_ACTION_CLASS",
        )
        self.assertEqual(model["summary"]["action_classes"], len(accel.ACTION_CLASS_LADDER))
        self.assertEqual(model["summary"]["stale_mutation_allowed"], 0)
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])

    def test_c7_pool_health_capacity_blast_bounds_maps_proxy_semantics_read_only(self):
        model = accel.build_pool_health_capacity_blast_bounds(
            service_pool_cohort_blast_radius_scope={
                "schema_version": "v7.b14-service-pool-cohort-blast-radius-scope.v1",
                "rows": [{
                    "user": "10.7.0.2",
                    "target_channel": "awg0",
                    "pool_scope": {
                        "pool": "awg0",
                        "capacity_decision": "capacity_available",
                        "projected_load": {"users": 1, "soft_limit": 5, "hard_limit": 10},
                    },
                    "service_scope": {"fit_verdict": "FIT", "required_services": ["telegram"]},
                    "blast_radius_scope": {"beyond_one_user_certified": True},
                    "action_class_scope": {
                        "current_action_class": "two-user governed candidate failover",
                        "stage_certification_state": "NEXT_ACTION_CLASS_STAGE_CERTIFIED_FOR_AUTHORITY_REVIEW_READ_ONLY",
                    },
                    "blockers": [],
                }],
            },
            class_level_blast_radius_certification={
                "schema_version": "v7.a5-class-level-blast-radius-certification.v1",
                "beyond_one_user_certified": True,
                "max_historical_certified_blast_radius_users": 4,
            },
            next_action_class_stage_certification={
                "schema_version": "v7.b12-next-action-class-stage-certification.v1",
                "next_stage": {
                    "stage_certification_state": "NEXT_ACTION_CLASS_STAGE_CERTIFIED_FOR_AUTHORITY_REVIEW_READ_ONLY",
                    "authority_review_required": True,
                },
            },
            bounded_stale_allowance_by_action_class={
                "schema_version": "v7.c6-bounded-stale-allowance-by-action-class.v1",
                "decision": {
                    "stale_evidence_mutation_allowed": False,
                    "fresh_evidence_required_before_mutation": True,
                },
            },
            action_class_freshness_windows={
                "schema_version": "v7.action-class-freshness-windows.v1",
                "rows": [{
                    "action_class": "two-user governed candidate failover",
                    "freshness_windows": {"capacity": 600, "service": 600},
                }],
            },
            generated_at="2026-06-25T00:00:00+00:00",
        )

        self.assertEqual(model["schema_version"], "v7.c7-pool-health-capacity-blast-bounds.v1")
        self.assertEqual(model["backlog_item"], "C7")
        row = model["rows"][0]
        self.assertEqual(row["mapping_state"], "POOL_HEALTH_CAPACITY_BLAST_BOUNDS_MAPPED_READ_ONLY")
        self.assertEqual(row["v7_max_ejection_bound"]["max_ejection_users_read_model"], 2)
        self.assertEqual(row["v7_minimum_health_bound"]["minimum_health_state"], "PASS")
        self.assertEqual(row["freshness_bound"]["freshness_windows"]["capacity"], 600)
        self.assertIn("max_ejection", model["semantic_mapping"])
        self.assertEqual(model["summary"]["threshold_changes"], 0)
        self.assertEqual(model["summary"]["formula_changes"], 0)
        self.assertEqual(model["omp_output"]["unlocked_capability"], "IMPLEMENTATION_COMPLETE")
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])
        self.assertFalse(model["blast_radius_expanded"])
        self.assertFalse(model["threshold_values_changed"])
        self.assertFalse(model["formula_changed"])
        self.assertFalse(model["new_owner_created"])

    def test_c7_inventory_exposes_pool_health_capacity_blast_bounds(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-25T00:00:00+00:00",
            )

        model = inventory["pool_health_capacity_blast_bounds"]
        self.assertEqual(model["schema_version"], "v7.c7-pool-health-capacity-blast-bounds.v1")
        self.assertEqual(model["backlog_item"], "C7")
        self.assertEqual(
            model["omp_output"]["c7_status"],
            "DONE_READ_ONLY_POOL_HEALTH_CAPACITY_BLAST_BOUNDS_MAPPED",
        )
        self.assertEqual(model["summary"]["runtime_actions_created"], 0)
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])
        self.assertFalse(model["blast_radius_expanded"])

    def test_c2_probabilistic_suspicion_is_advisory_only(self):
        shadow = shadow_autonomy.build_shadow_autonomy_model(
            {
                "users": [{
                    "user": "10.7.0.2",
                    "current_channel": "vless",
                    "recommended_channel": "awg0",
                    "recommendation": "move_recommended",
                    "confidence": 0.42,
                    "risk": 61,
                    "trust": 30,
                    "prediction": {"confidence": 0.2},
                    "blockers": ["freshness_recheck_required"],
                }]
            },
            now="2026-06-25T00:00:00+00:00",
        )
        model = accel.build_probabilistic_suspicion_advisory_evidence(
            shadow_model=shadow,
            source_confidence_inventory={
                "schema_version": "v7.source-confidence-inventory.v1",
                "sources": [{
                    "source": "prediction",
                    "confidence": 39.5,
                    "owner": "admin_core.intelligence_workers",
                }],
            },
            degradation_signal_policy_mapping={
                "schema_version": "v7.b4.degradation-signal-policy-mapping.v1",
                "evidence_rows": [{
                    "object": "awg0",
                    "source": "quality",
                    "owner": "tools/v7-egress-quality-compact",
                    "signal_family": "latency",
                    "canonical_policy_result": "SOFT_DEGRADATION",
                    "requires_attribution_before_action": True,
                }],
            },
            observed_degradation_attribution={
                "schema_version": "v7.b5.observed-degradation-attribution.v1",
                "rows": [{
                    "object": "awg0",
                    "attribution_state": "ACTIVE_ONLY_PASSIVE_OUTCOME_PENDING",
                }],
            },
            metric_reliability_certification={
                "schema_version": "v7.b13-metric-reliability-certification.v1",
                "summary": {"positive_promotion_allowed": False},
            },
            fail_open_fail_closed_action_class_behavior={
                "schema_version": "v7.c1-fail-open-fail-closed-action-class-behavior.v1",
                "summary": {"fail_closed_runtime_apply_classes": 9},
            },
            generated_at="2026-06-25T00:00:00+00:00",
        )

        self.assertEqual(model["schema_version"], "v7.c2-probabilistic-suspicion-advisory-evidence.v1")
        self.assertEqual(model["backlog_item"], "C2")
        self.assertEqual(model["omp_output"]["c2_status"], "DONE_READ_ONLY_PROBABILISTIC_SUSPICION_ADVISORY_EVIDENCE")
        self.assertGreaterEqual(model["summary"]["advisory_evidence_rows"], 3)
        self.assertEqual(model["summary"]["direct_blocking_rows"], 0)
        self.assertEqual(model["summary"]["direct_execution_rows"], 0)
        self.assertIn("probabilistic_suspicion_is_advisory_evidence_only", model["canonical_rules"])
        self.assertTrue(all(row["direct_blocking_power"] == "NONE" for row in model["rows"]))
        self.assertTrue(all(row["direct_execution_power"] == "NONE" for row in model["rows"]))
        self.assertTrue(all(row["runtime_apply_allowed"] is False for row in model["rows"]))
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])
        self.assertFalse(model["synthetic_evidence_created"])
        self.assertFalse(model["threshold_values_changed"])
        self.assertFalse(model["formula_changed"])
        self.assertFalse(model["new_owner_created"])

    def test_c2_inventory_exposes_probabilistic_suspicion_advisory_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-25T00:00:00+00:00",
            )

        model = inventory["probabilistic_suspicion_advisory_evidence"]
        self.assertEqual(model["schema_version"], "v7.c2-probabilistic-suspicion-advisory-evidence.v1")
        self.assertEqual(model["backlog_item"], "C2")
        self.assertEqual(
            model["omp_output"]["c2_status"],
            "DONE_READ_ONLY_PROBABILISTIC_SUSPICION_ADVISORY_EVIDENCE",
        )
        self.assertEqual(model["summary"]["direct_blocking_rows"], 0)
        self.assertEqual(model["summary"]["direct_execution_rows"], 0)
        self.assertTrue(model["read_only"])
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["authority_expanded"])

    def test_b16_rollback_authority_certification_is_read_only_authority_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[{
                    "recommendation_id": "r1",
                    "decision_id": "decision-1",
                    "packet_id": "p1",
                    "apply_result": "success",
                    "post_action_verification": {"status": "passed"},
                    "service_outcome": {"telegram": "ok"},
                    "user_outcome": {"user": "10.7.0.2"},
                    "learning_record": {"stored": True},
                    "outcome_observed_at": "2026-06-24T00:00:00+00:00",
                    "blast_radius": 1,
                    "selected_move_count": 1,
                    "user": "10.7.0.2",
                    "target": "awg0",
                    "service_delta": 5,
                    "prediction_delta": 3,
                }],
                generated_at="2026-06-25T00:00:00+00:00",
            )

        certification = inventory["rollback_authority_certification"]
        self.assertEqual(certification["schema_version"], "v7.b16-rollback-authority-certification.v1")
        self.assertEqual(certification["backlog_item"], "B16")
        self.assertEqual(certification["certification_state"], "CERTIFIED_FOR_AUTHORITY_REVIEW_ONLY")
        gates = {row["metric"]: row["state"] for row in certification["gate_rows"]}
        self.assertEqual(gates["rollback_evidence"], "PASS")
        self.assertEqual(gates["verification_reliability"], "PASS")
        self.assertEqual(gates["no_rollback_observed"], "PASS")
        self.assertEqual(gates["metric_reliability"], "PASS")
        self.assertEqual(gates["runtime_eligibility"], "PASS")
        self.assertEqual(gates["authority"], "STOP")
        self.assertEqual(gates["runtime_apply"], "STOP")
        self.assertTrue(certification["evidence_ready_for_authority_review"])
        self.assertFalse(certification["automatic_rollback_authority_granted"])
        self.assertFalse(certification["automatic_rollback_execution_allowed"])
        self.assertEqual(certification["authority_stop_gates"], ["authority", "runtime_apply"])
        self.assertEqual(
            certification["omp_output"]["next_safe_action"],
            "continue to Runtime Capability Maturation Program RT2-S1 measurement and observability",
        )
        self.assertFalse(certification["runtime_mutation_performed"])
        self.assertFalse(certification["rollback_executed"])
        self.assertFalse(certification["apply_executed"])
        self.assertEqual(certification["users_moved"], 0)
        self.assertFalse(certification["authority_expanded"])
        self.assertFalse(certification["new_owner_created"])

    def test_b16_rollback_authority_certification_blocks_missing_mandatory_evidence(self):
        certification = accel.build_rollback_authority_certification(
            floor_forensics={"rollback_and_blast": {"rollback_records_seen": 0, "rollback_confidence": 0.0}},
            decision_outcome_closure={"closure_state": "PARTIAL"},
            decision_outcome_learning={"effectiveness": {"rollback_rate": 0.0}},
            runtime_eligibility_arbitration={"schema_version": "missing", "runtime_execute_decision": "UNKNOWN"},
            metric_reliability_certification={"schema_version": "missing", "blocking_recommendation_certified": False},
            generated_at="2026-06-25T00:00:00+00:00",
        )

        self.assertEqual(certification["certification_state"], "NOT_CERTIFIED_MANDATORY_ROLLBACK_GATE_FAILED")
        self.assertFalse(certification["evidence_ready_for_authority_review"])
        self.assertIn("rollback_evidence", certification["mandatory_stop_gates"])
        self.assertIn("verification_reliability", certification["mandatory_stop_gates"])
        self.assertIn("metric_reliability", certification["mandatory_stop_gates"])
        self.assertIn("runtime_eligibility", certification["mandatory_stop_gates"])
        self.assertFalse(certification["automatic_rollback_authority_granted"])
        self.assertFalse(certification["automatic_rollback_execution_allowed"])
        self.assertFalse(certification["runtime_mutation_performed"])
        self.assertFalse(certification["authority_expanded"])

    def test_rt2_s5_certified_concurrency_ladder_closes_serial_only_stop_safe(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[{
                    "recommendation_id": "r1",
                    "decision_id": "decision-1",
                    "packet_id": "p1",
                    "apply_result": "success",
                    "post_action_verification": {"status": "passed"},
                    "service_outcome": {"telegram": "ok"},
                    "user_outcome": {"user": "10.7.0.2"},
                    "learning_record": {"stored": True},
                    "outcome_observed_at": "2026-06-24T00:00:00+00:00",
                    "blast_radius": 1,
                    "selected_move_count": 1,
                    "user": "10.7.0.2",
                    "target": "awg0",
                    "service_delta": 5,
                    "prediction_delta": 3,
                }],
                generated_at="2026-06-25T00:00:00+00:00",
            )

        ladder = inventory["rt2_s5_certified_concurrency_ladder"]
        self.assertEqual(ladder["schema_version"], "v7.rt2-s5-certified-concurrency-ladder.v1")
        self.assertEqual(ladder["omp_workstream"], "RT2-S5")
        self.assertEqual(ladder["certification_state"], "DONE_READ_ONLY_CONCURRENCY_LADDER_OWNER_MAPPED")
        self.assertEqual(ladder["certification_verdict"], "STOP_SAFE_CONCURRENCY_NOT_ENABLED")
        self.assertEqual(ladder["certified_concurrency_level"], "SERIAL_ONLY_READ_ONLY")
        self.assertTrue(ladder["completion_criteria_met"])
        self.assertTrue(ladder["rt2_s6_unlocked"])
        levels = {row["level"]: row for row in ladder["concurrency_levels"]}
        self.assertEqual(levels["L0_SERIAL_ONLY"]["status"], "CERTIFIED_READ_ONLY")
        self.assertEqual(levels["L1_TWO_USER_OR_TWO_ACTION"]["status"], "STOP_SAFE_AUTHORITY_AND_CAPACITY_REQUIRED")
        self.assertEqual(levels["L2_SMALL_BATCH_OR_POOL"]["status"], "STOP_SAFE_NO_SILENT_BLAST_EXPANSION")
        gates = {row["metric"]: row["state"] for row in ladder["gate_rows"]}
        self.assertEqual(gates["governed_execution_coordination"], "PASS")
        self.assertEqual(gates["runtime_eligibility"], "PASS")
        self.assertEqual(gates["verification_capacity"], "PASS")
        self.assertEqual(gates["rollback_capacity"], "PASS")
        self.assertEqual(gates["authority_envelope"], "STOP_SAFE")
        self.assertEqual(gates["runtime_apply"], "STOP_SAFE")
        self.assertIn("RT2-S6_EVIDENCE_BASED_CONTINUOUS_IMPROVEMENT", ladder["omp_output"]["unlocked_capability"])
        self.assertFalse(ladder["concurrency_enabled"])
        self.assertFalse(ladder["runtime_mutation_performed"])
        self.assertFalse(ladder["apply_executed"])
        self.assertEqual(ladder["users_moved"], 0)
        self.assertFalse(ladder["authority_expanded"])
        self.assertFalse(ladder["new_runtime_created"])

    def test_rt2_s5_certified_concurrency_ladder_blocks_missing_base_evidence(self):
        ladder = accel.build_rt2_s5_certified_concurrency_ladder(
            action_class_runtime_enablement={},
            class_level_blast_radius_certification={},
            runtime_eligibility_arbitration={},
            metric_reliability_certification={},
            rollback_authority_certification={},
            anti_flapping={"summary": {"blocked_users": 1}},
            rt2_s4_governed_execution_coordination={"status": "PARTIAL"},
            generated_at="2026-06-25T00:00:00+00:00",
        )

        self.assertEqual(ladder["certification_state"], "STOP_SAFE_BASE_EVIDENCE_INCOMPLETE")
        self.assertEqual(ladder["certified_concurrency_level"], "NONE_STOP_SAFE")
        self.assertFalse(ladder["completion_criteria_met"])
        self.assertFalse(ladder["rt2_s6_unlocked"])
        self.assertIn("governed_execution_coordination", ladder["stop_metrics"])
        self.assertIn("runtime_eligibility", ladder["stop_metrics"])
        self.assertIn("verification_capacity", ladder["stop_metrics"])
        self.assertIn("rollback_capacity", ladder["stop_metrics"])
        self.assertFalse(ladder["concurrency_enabled"])
        self.assertFalse(ladder["runtime_mutation_performed"])
        self.assertFalse(ladder["authority_expanded"])

    def test_rt2_s6_evidence_based_continuous_improvement_returns_to_b1_advisory_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[{
                    "recommendation_id": "r1",
                    "decision_id": "decision-1",
                    "packet_id": "p1",
                    "apply_result": "success",
                    "post_action_verification": {"status": "passed"},
                    "service_outcome": {"telegram": "ok"},
                    "user_outcome": {"user": "10.7.0.2"},
                    "learning_record": {"stored": True},
                    "outcome_observed_at": "2026-06-24T00:00:00+00:00",
                    "blast_radius": 1,
                    "selected_move_count": 1,
                    "user": "10.7.0.2",
                    "target": "awg0",
                    "service_delta": 5,
                    "prediction_delta": 3,
                }],
                generated_at="2026-06-25T00:00:00+00:00",
            )

        s6 = inventory["rt2_s6_evidence_based_continuous_improvement"]
        self.assertEqual(s6["schema_version"], "v7.rt2-s6-evidence-based-continuous-improvement.v1")
        self.assertEqual(s6["omp_workstream"], "RT2-S6")
        self.assertEqual(s6["certification_state"], "DONE_READ_ONLY_OWNER_MAPPED_RECOMMENDATION")
        self.assertEqual(s6["recommendation_verdict"], "OWNER_MAPPED_RECOMMENDATION")
        self.assertTrue(s6["completion_criteria_met"])
        self.assertTrue(s6["rt2_graduated"])
        self.assertEqual(s6["next_omp_step"], "B1_AGGREGATE_LIVENESS_EVIDENCE_BY_SOURCE_FAMILY_AND_CONFIDENCE")
        recommendation = s6["recommendation_rows"][0]
        self.assertEqual(recommendation["canonical_owner"], "docs/programs/V7_IMPLEMENTATION_BACKLOG.md#B1")
        self.assertIn("admin_core/intelligence_workers.py", recommendation["implementation_owners"])
        gates = {row["metric"]: row["state"] for row in s6["evidence_rows"]}
        self.assertEqual(gates["safe_execution_limit"], "PASS")
        self.assertEqual(gates["outcome_leverage"], "PASS")
        self.assertEqual(gates["metric_reliability"], "PASS")
        self.assertEqual(gates["authority_boundary"], "STOP_SAFE")
        self.assertTrue(s6["advisory_only"])
        self.assertFalse(s6["automatic_recommendation_enabled"])
        self.assertFalse(s6["direct_implementation_started"])
        self.assertFalse(s6["runtime_mutation_performed"])
        self.assertFalse(s6["apply_executed"])
        self.assertEqual(s6["users_moved"], 0)
        self.assertFalse(s6["authority_expanded"])
        self.assertFalse(s6["new_owner_created"])

    def test_rt2_s6_evidence_based_continuous_improvement_blocks_missing_mandatory_evidence(self):
        s6 = accel.build_rt2_s6_evidence_based_continuous_improvement(
            outcome_leverage_model={"activities_ranked": []},
            maximum_reality_knowledge_extraction={"final_verdict": "UNKNOWN"},
            rt2_s5_certified_concurrency_ladder={"certification_state": "STOP_SAFE_BASE_EVIDENCE_INCOMPLETE"},
            routing_recommendation_readiness={},
            metric_reliability_certification={"schema_version": "missing", "blocking_recommendation_certified": False},
            decision_outcome_learning={},
            generated_at="2026-06-25T00:00:00+00:00",
        )

        self.assertEqual(s6["certification_state"], "STOP_SAFE_RECOMMENDATION_EVIDENCE_INCOMPLETE")
        self.assertEqual(s6["recommendation_verdict"], "MISSING_EVIDENCE_STOP_SAFE")
        self.assertFalse(s6["completion_criteria_met"])
        self.assertFalse(s6["rt2_graduated"])
        self.assertIn("safe_execution_limit", s6["mandatory_stop"])
        self.assertIn("outcome_leverage", s6["mandatory_stop"])
        self.assertIn("metric_reliability", s6["mandatory_stop"])
        self.assertFalse(s6["runtime_mutation_performed"])
        self.assertFalse(s6["direct_implementation_started"])
        self.assertFalse(s6["authority_expanded"])

    def test_autonomous_routing_evolution_program_survives_refresh_rebuild(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            first = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-25T00:00:00+00:00",
            )
            second = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=json.loads(json.dumps(self.decision_surface(), sort_keys=True)),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-25T00:05:00+00:00",
            )

        first_program = first["autonomous_routing_evolution_program"]
        second_program = second["autonomous_routing_evolution_program"]
        self.assertEqual(first_program["phase_status"], second_program["phase_status"])
        self.assertEqual(first_program["tier_2_distance"], second_program["tier_2_distance"])
        self.assertEqual(first_program["exact_stop_reason"], second_program["exact_stop_reason"])
        self.assertFalse(second_program["runtime_mutation_performed"])
        self.assertEqual(second_program["users_moved"], 0)
        self.assertFalse(second_program["apply_executed"])

    def test_maximum_reality_knowledge_extraction_classifies_current_limits(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-25T00:00:00+00:00",
            )

        extraction = inventory["maximum_reality_knowledge_extraction"]
        self.assertEqual(
            extraction["schema_version"],
            "v7.autonomy-trust.maximum-reality-knowledge-extraction.v1",
        )
        classes = {row["item"]: row["classification"] for row in extraction["knowledge_limit_items"]}
        self.assertEqual(classes["service_outcomes"], "OBTAINABLE_NOW")
        self.assertEqual(classes["missing_candidate_outcomes"], "OBTAINABLE_AFTER_GOVERNED_ACTION")
        self.assertEqual(classes["client_telemetry"], "REQUIRES_NEW_ARCHITECTURE")
        self.assertEqual(
            extraction["physical_reality_limit"]["missing_candidate_outcomes"],
            2,
        )
        self.assertEqual(
            extraction["physical_reality_limit"]["obtainable_after_governed_action_count"],
            2,
        )
        self.assertEqual(
            extraction["maximum_current_suitability"]["converted_missing_candidate_outcomes_at_max"],
            2,
        )
        self.assertGreaterEqual(
            extraction["maximum_current_suitability"]["maximum_possible_without_more_users_channels_formula_or_floor_changes"],
            extraction["maximum_current_suitability"]["current"],
        )
        self.assertIn("prediction_outcome_cycle", extraction["highest_leverage_now"])
        self.assertFalse(extraction["runtime_mutation_performed"])
        self.assertEqual(extraction["users_moved"], 0)
        self.assertFalse(extraction["apply_executed"])
        self.assertFalse(extraction["autonomy_enabled"])

    def test_maximum_reality_knowledge_extraction_survives_refresh_rebuild(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            first = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-25T00:00:00+00:00",
            )
            second = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=json.loads(json.dumps(self.decision_surface(), sort_keys=True)),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-25T00:05:00+00:00",
            )

        first_extraction = first["maximum_reality_knowledge_extraction"]
        second_extraction = second["maximum_reality_knowledge_extraction"]
        self.assertEqual(first_extraction["classification_summary"], second_extraction["classification_summary"])
        self.assertEqual(first_extraction["physical_reality_limit"], second_extraction["physical_reality_limit"])
        self.assertEqual(first_extraction["maximum_current_suitability"], second_extraction["maximum_current_suitability"])
        self.assertEqual(second_extraction["automatic_cycle_completion"]["new_cycle_automation_level"], "FULLY_AUTONOMOUS")
        self.assertTrue(second_extraction["automatic_cycle_completion"]["automatic_rerun_works"])
        self.assertFalse(second_extraction["runtime_mutation_performed"])
        self.assertEqual(second_extraction["users_moved"], 0)
        self.assertFalse(second_extraction["apply_executed"])

    def test_final_architecture_certification_covers_core_classes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            inventory = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-25T00:00:00+00:00",
            )

        certification = inventory["final_autonomous_routing_architecture_certification"]
        self.assertEqual(
            certification["schema_version"],
            "v7.autonomy-trust.final-autonomous-routing-architecture-certification.v1",
        )
        self.assertEqual(
            certification["final_verdict"],
            "ARCHITECTURE_COMPLETE_WITH_FUTURE_OPTIONAL_EXTENSIONS",
        )
        self.assertEqual(certification["fundamental_missing_classes"], [])
        knowledge = {row["item"]: row for row in certification["knowledge_source_completeness"]}
        for item in [
            "Channel Knowledge",
            "Service Knowledge",
            "User Knowledge",
            "Decision Knowledge",
            "Outcome Knowledge",
            "Learning Knowledge",
            "Suitability Knowledge",
            "Prediction Knowledge",
            "Safety / Blast / Rollback Knowledge",
        ]:
            self.assertIn(item, knowledge)
            self.assertNotEqual(knowledge[item]["status"], "MISSING")
        self.assertEqual(knowledge["Client Observation Knowledge"]["status"], "PARTIAL")
        decisions = {row["item"]: row["status"] for row in certification["decision_completeness"]}
        for item in ["KEEP", "MOVE", "FAILOVER", "DRAIN", "WAIT", "ASK_OPERATOR", "NO_ACTION", "SELF_STOP", "SELF_LIMIT"]:
            self.assertEqual(decisions[item], "EXISTS")
        self.assertEqual(decisions["QUARANTINE"], "PARTIAL")
        self.assertEqual(decisions["RECOVER"], "PARTIAL")
        self.assertEqual(certification["lifecycle_status_by_stage"]["observation"], "EXISTS")
        self.assertEqual(certification["lifecycle_status_by_stage"]["learning"], "EXISTS")
        self.assertEqual(certification["lifecycle_status_by_stage"]["aging"], "PARTIAL")
        self.assertEqual(certification["architecture_limit"], "REAL_WORLD_EXPERIENCE_AND_AUTHORITY")
        self.assertEqual(
            certification["next_program"],
            "GOVERNED_CANDIDATE_OUTCOME_EXECUTION_AND_CLOSURE",
        )
        self.assertFalse(certification["runtime_mutation_performed"])
        self.assertEqual(certification["users_moved"], 0)
        self.assertFalse(certification["apply_executed"])
        self.assertFalse(certification["autonomy_enabled"])

    def test_final_architecture_certification_survives_refresh_rebuild(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.populate_snapshots(root)
            first = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=self.decision_surface(),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-25T00:00:00+00:00",
            )
            second = accel.build_acceleration_inventory(
                snapshot_root=root,
                decision_surface=json.loads(json.dumps(self.decision_surface(), sort_keys=True)),
                shadow_history=[],
                decision_records=[],
                generated_at="2026-06-25T00:05:00+00:00",
            )

        first_cert = first["final_autonomous_routing_architecture_certification"]
        second_cert = second["final_autonomous_routing_architecture_certification"]
        for key in [
            "knowledge_source_summary",
            "decision_summary",
            "lifecycle_summary",
            "routing_summary",
            "fundamental_missing_classes",
            "partial_classes",
            "final_verdict",
        ]:
            self.assertEqual(first_cert[key], second_cert[key])
        self.assertEqual(
            second_cert["duplication_audit"]["merged_through_existing_owner"],
            "admin_core.autonomy_trust_acceleration",
        )
        self.assertEqual(second_cert["autonomy_cycle_completeness"]["cycle_count"], 12)
        self.assertFalse(second_cert["runtime_mutation_performed"])
        self.assertEqual(second_cert["users_moved"], 0)
        self.assertFalse(second_cert["apply_executed"])


    def test_l7_l8_passport_deduplicates_existing_owner_records_and_closes_m1_m3_contract(self):
        operation_id = "runtime_autoswitch_material_1"
        base = {
            "_v7_evidence_source_path": "/opt/v7/egress/state/execution-events.jsonl",
            "audit_reference": operation_id,
            "feedback_id": "execfb_material_1",
            "decision_id": "execfb_material_1",
            "packet_id": "packet_material_1",
            "recommendation_id": "recommendation_material_1",
            "user": "10.7.0.5",
            "source_channel": "awg0",
            "target_channel": "vless",
            "outcome_observed_at": "2026-07-19T00:00:00+00:00",
            "outcome_quality": {
                "outcome_quality": "SUCCESS",
                "terminal_outcome_classification": "SUCCESS",
            },
            "execution_outcome": {"success": True, "applied": True},
            "verification_result": {"verification_passed": True},
            "stability_window_seconds": 3600,
            "decision_trace_id": "trace_material_1",
            "input_snapshot_identity": "snapshot_material_1",
            "expected_terminal": "SUCCESS",
            "learning_record": {"learning_record_id": "learn_material_1"},
        }
        duplicate = {
            **base,
            "_v7_evidence_source_path": "/opt/v7/egress/state/closure-records.jsonl",
            "schema_version": "v7.execution-feedback-closure.v1",
            "closure_state": "CLOSED",
        }

        model = accel.build_l7_l8_outcome_evidence_program(
            [base, duplicate],
            generated_at="2026-07-19T01:00:00+00:00",
        )

        self.assertEqual(model["mission_results"]["M1"]["status"], "COMPLETE_CONSUMED")
        self.assertEqual(len(model["outcome_evidence_passports"]), 1)
        passport = model["outcome_evidence_passports"][0]
        self.assertEqual(passport["record_count"], 2)
        self.assertEqual(passport["operation_id"], operation_id)
        self.assertEqual(passport["evidence_class"], "CONTROLLED_PRODUCTION")
        self.assertTrue(passport["completeness"]["core_complete"])
        self.assertTrue(passport["completeness"]["temporal_complete"])
        self.assertTrue(passport["completeness"]["replay_complete"])
        self.assertEqual(passport["eligibility"], "ELIGIBLE_FOR_CALIBRATION")
        self.assertEqual(model["opportunity_denominator"]["counts"]["ACTION"], 1)
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["authority_expanded"])
        self.assertEqual(model["users_moved"], 0)

    def test_l7_l8_program_records_exact_temporal_and_replay_residuals(self):
        model = accel.build_l7_l8_outcome_evidence_program([{
            "_v7_evidence_source_path": "/opt/v7/events/switch-history.jsonl",
            "operation": {"operation_id": "runtime_autoswitch_incomplete", "terminal_state": "APPLIED"},
            "selected_moves": [{"user_ip": "10.7.0.5", "current_egress": "awg0", "recommended_egress": "vless"}],
            "outcome_status": "success",
            "created_at": "2026-07-19T00:00:00+00:00",
        }])

        passport = model["outcome_evidence_passports"][0]
        self.assertIn("accepted_request", passport["completeness"]["missing_temporal_fields"])
        self.assertIn("delayed_5m_observation", passport["completeness"]["missing_temporal_fields"])
        self.assertIn("decision_trace_id", passport["completeness"]["missing_replay_fields"])
        self.assertEqual(model["mission_results"]["M6"]["status"], "INSUFFICIENT_EVIDENCE")
        self.assertEqual(model["mission_results"]["M7"]["authority_recommendation"], "INSUFFICIENT_EVIDENCE")
        self.assertEqual(model["mission_results"]["M8"]["status"], "MISSION_NOT_REQUIRED_BY_AUTHORITY_VERDICT")

    def test_l7_l8_opportunity_denominator_preserves_non_action_terminals(self):
        records = [
            {"decision_id": "stay-1", "action": "STAY", "user": "u1", "channel": "awg0"},
            {"decision_id": "stop-1", "terminal_state": "STOP_SAFE", "user": "u2", "channel": "awg1"},
            {"decision_id": "blocked-1", "status": "BLOCKED", "user": "u3", "channel": "awg2"},
            {"recommendation_id": "missed-1", "user": "u4", "channel": "awg3"},
            {"decision_id": "none-1", "reason": "NO_SAFE_CANDIDATE", "user": "u5"},
        ]
        model = accel.build_l7_l8_outcome_evidence_program(records)
        counts = model["opportunity_denominator"]["counts"]
        self.assertEqual(counts["STAY"], 1)
        self.assertEqual(counts["STOP_SAFE"], 1)
        self.assertEqual(counts["BLOCKED"], 1)
        self.assertEqual(counts["MISSED"], 1)
        self.assertEqual(counts["NO_CANDIDATE"], 1)
        self.assertEqual(counts["ACTION"], 0)
        self.assertFalse(model["new_storage_created"])
        self.assertFalse(model["new_truth_source_created"])


if __name__ == "__main__":
    unittest.main()
