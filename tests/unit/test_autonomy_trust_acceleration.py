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
            {"recommendation_hash": "r1", "selected_moves": [{"user": "10.7.0.2", "target": "awg0"}], "status": "preview_only"}
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
            "routing_recommendation_readiness",
            "decision_outcome_learning",
        ):
            self.assertIn(key, inventory)
            self.assertFalse(inventory[key]["runtime_mutation_performed"])
            self.assertFalse(inventory[key]["apply_executed"])
            self.assertEqual(inventory[key]["users_moved"], 0)
        self.assertIn("decision_effectiveness", inventory)
        self.assertEqual(inventory["decision_effectiveness"]["recommendation_correct_rate"], 1.0)
        self.assertEqual(inventory["knowledge_growth"]["knowledge_gained"], 1)

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

    def test_action_class_runtime_enablement_exposes_current_path_without_authority(self):
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
        self.assertEqual(enablement["schema_version"], "v7.action-class-runtime-enablement.v1")
        self.assertEqual(enablement["path_status"], "PARTIAL")
        self.assertEqual(enablement["semantic_reuse_audit"]["semantic_coverage_percent"], 78)
        self.assertFalse(enablement["semantic_reuse_audit"]["need_new_owner"])
        self.assertEqual(enablement["semantic_reuse_audit"]["duplicate_detector_result"], "NO_DUPLICATE_OWNER_CREATED")
        self.assertEqual(enablement["current_action_class"], "single-user governed candidate failover")
        self.assertEqual(enablement["current_state"], "GOVERNED_ONLY")
        self.assertEqual(enablement["next_promotion_target"], "CERTIFIED_FOR_CLASS_APPROVAL")
        self.assertFalse(enablement["runtime_capability_view"]["runtime_can_execute_automatically"])
        self.assertFalse(enablement["runtime_capability_view"]["runtime_apply_allowed_now"])
        self.assertEqual(enablement["enablement_readiness"]["stop_condition_if_promoted"], "AUTHORITY_BOUNDARY")
        self.assertIn("class-level authority_policy_approval", enablement["enablement_readiness"]["missing_evidence"])
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
        self.assertFalse(enablement["autonomy_enabled"])
        self.assertFalse(enablement["new_planner_created"])
        self.assertFalse(enablement["new_governance_created"])
        self.assertFalse(enablement["new_execution_path_created"])
        self.assertFalse(enablement["new_truth_source_created"])

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


if __name__ == "__main__":
    unittest.main()
