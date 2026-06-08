import unittest
from pathlib import Path

from admin_core import operator_execution_pipeline as pipeline


ROOT = Path(__file__).resolve().parents[2]
ADMIN_API = ROOT / "admin" / "v7-admin-api"


class OperatorExecutionPipelineTest(unittest.TestCase):
    def recommendation_row(self):
        return {
            "user": "10.7.0.3",
            "current_channel": "awg0",
            "recommended_channel": "awg3",
            "confidence": 0.91,
            "trust": 88.0,
            "prediction": {"available": True, "confidence": 0.82},
            "risk": 3.2,
            "recommendation_hash": "rec-hash",
            "source_hash": "source-hash",
            "reasons": ["best available channel has higher advisory suitability"],
        }

    def test_recommendation_execution_contract_has_required_fields(self):
        contract = pipeline.recommendation_execution_contract(self.recommendation_row())

        for field in pipeline.REQUIRED_RECOMMENDATION_FIELDS:
            self.assertIn(field, contract)
        self.assertTrue(contract["execution_candidate"])
        self.assertFalse(contract["execution_allowed_now"])
        self.assertFalse(contract["runtime_mutation_performed"])
        self.assertEqual(contract["rollback_plan"]["rollback_target"], "awg0")
        self.assertEqual(contract["next_required_state"], "APPROVAL_PACKET_REQUIRED")

    def test_execution_action_matrix_satisfies_rule_16(self):
        required = {
            "condition",
            "decision",
            "action",
            "executor",
            "trigger",
            "written_evidence",
            "blocked_actions",
            "next_state",
        }
        matrix = pipeline.execution_action_matrix()

        self.assertEqual({row["state"] for row in matrix}, set(pipeline.EXECUTION_STATES))
        for row in matrix:
            with self.subTest(state=row["state"]):
                self.assertTrue(required.issubset(row))
                for key in required:
                    self.assertTrue(row[key], f"{row['state']} missing {key}")

    def test_pipeline_certification_is_single_path_and_non_mutating(self):
        cert = pipeline.pipeline_certification()
        verdicts = cert["final_verdicts"]

        self.assertTrue(verdicts["single_execution_path_certified"])
        self.assertTrue(verdicts["execution_action_matrix_complete"])
        self.assertFalse(verdicts["new_truth_sources_created"])
        self.assertFalse(verdicts["duplicate_systems_created"])
        self.assertFalse(verdicts["runtime_mutation_performed"])
        self.assertFalse(verdicts["users_moved"])
        self.assertFalse(verdicts["autoswitch_apply_run"])
        self.assertFalse(cert["single_execution_path"]["direct_user_switch_allowed"])
        self.assertEqual(cert["single_execution_path"]["runtime_apply"], pipeline.CANONICAL_RUNTIME_EXECUTOR)
        self.assertTrue(verdicts["execution_loop_readiness_foundation_complete"])
        self.assertIn("execution_loop_readiness_foundation", cert)

    def test_execution_loop_readiness_foundation_extracts_stage_timing(self):
        foundation = pipeline.execution_loop_readiness_foundation(
            planner_result={"stage": "planner", "elapsed_ms": 12.5, "operation": {"selected_move_count": 2}},
            contracts=[
                {"contract_id": "contract-1", "stage": "packet", "duration_ms": 4, "affected_users": ["10.0.0.3", "10.0.0.6"]},
                {"contract_id": "contract-1", "stage": "restore_barrier", "elapsed_sec": 0.25},
            ],
            events=[
                {"event_id": "apply-1", "event_type": "APPLY_COMPLETED", "duration_ms": 100, "completed_at": "2026-06-08T10:00:03Z"},
                {"event_id": "verify-1", "event_type": "VERIFICATION_COMPLETED", "duration_ms": 30, "completed_at": "2026-06-08T10:00:04Z"},
                {"event_id": "feedback-1", "event_type": "FEEDBACK_MATERIALIZED", "duration_ms": 20, "completed_at": "2026-06-08T10:00:05Z"},
                {"event_id": "closure-1", "event_type": "CLOSURE_CLOSED", "duration_ms": 10, "completed_at": "2026-06-08T10:00:06Z"},
            ],
        )
        metrics = foundation["performance_audit"]["requested_metrics"]

        self.assertTrue(foundation["read_only"])
        self.assertFalse(foundation["execution_allowed_now"])
        self.assertFalse(foundation["routing_behavior_changed"])
        self.assertEqual(foundation["users_moved"], 0)
        self.assertFalse(foundation["apply_executed"])
        self.assertEqual(metrics["planner_duration_ms"]["value"], 12.5)
        self.assertEqual(metrics["packet_duration_ms"]["value"], 4)
        self.assertEqual(metrics["restore_barrier_duration_ms"]["value"], 250.0)
        self.assertEqual(metrics["apply_duration_ms"]["value"], 100)
        self.assertEqual(metrics["verification_duration_ms"]["value"], 30)
        self.assertEqual(metrics["feedback_duration_ms"]["value"], 20)
        self.assertEqual(metrics["closure_duration_ms"]["value"], 10)
        self.assertEqual(metrics["total_duration_ms"]["value"], 426.5)
        self.assertEqual(metrics["per_user_duration_ms"]["value"], 213.25)
        self.assertEqual(foundation["execution_observability"]["latest_success_ref"], "closure-1")
        self.assertTrue(foundation["readiness_certification"]["operator_approval_ready"])

    def test_execution_loop_foundation_reuses_existing_owners(self):
        foundation = pipeline.execution_loop_readiness_foundation()
        owners = {row["stage"]: row["owner"] for row in foundation["execution_chain_audit"]}

        self.assertEqual(owners["planner"], pipeline.CANONICAL_PLANNER)
        self.assertEqual(owners["packet"], pipeline.CANONICAL_PACKET_TOOL)
        self.assertEqual(owners["restore_barrier"], pipeline.CANONICAL_PACKET_OWNER)
        self.assertEqual(owners["apply"], pipeline.CANONICAL_RUNTIME_EXECUTOR)
        self.assertEqual(owners["feedback"], pipeline.CANONICAL_FEEDBACK_OWNER)
        self.assertFalse(foundation["runtime_execution_changes"])
        self.assertFalse(foundation["autonomy_enabled"])

    def test_operator_execution_dashboard_model_is_read_only_and_operator_visible(self):
        readiness = pipeline.execution_loop_readiness_foundation(
            contracts=[
                {"contract_id": "contract-1", "stage": "packet", "duration_ms": 8, "affected_users": ["10.0.0.3"], "created_at": "2026-06-08T10:00:00Z"},
            ],
            events=[
                {"event_id": "verify-1", "event_type": "VERIFICATION_COMPLETED", "duration_ms": 44, "completed_at": "2026-06-08T10:00:01Z"},
            ],
        )
        dashboard = pipeline.execution_operator_dashboard_model(
            readiness=readiness,
            decision_surface={
                "shadow_autonomy": {
                    "mode": "shadow_only",
                    "current_decisions": [{"decision_id": "shadow-1", "user": "10.0.0.3"}],
                    "decision_history": [{"decision_id": "shadow-0", "user": "10.0.0.2"}],
                    "comparison_history": [{"decision_id": "shadow-0", "operator_agreed": True}],
                    "quality": {"decisions_total": 1, "agreement_rate": 1.0, "override_rate": 0.0},
                    "confidence": {"earned_confidence": 82.5},
                    "observation_window": {"comparisons_observed": 1, "enough_comparisons": False},
                    "disagreement_analysis": {"disagreements_total": 0, "primary_disagreement_reason": "NONE"},
                    "confidence_evolution": {"trend": "STABLE"},
                    "operator_behavior": {"behavior_pattern": "MOSTLY_AGREEING"},
                    "autonomy_evidence": {"evidence_targets_met": False, "missing_targets": ["minimum_comparisons"]},
                    "autonomy_readiness": {"closest_stage": "SHADOW_ONLY", "bounded_autonomy_ready": False},
                    "gap_analysis": {"single_blocker": "SHADOW_OBSERVATION_EVIDENCE_BELOW_MINIMUM"},
                },
                "channels": [
                    {"channel": "vless", "channel_state": "Trusted", "channel_state_source": "trust-evolution-summaries"},
                    {"channel": "awg0", "channel_state": "Recovery", "channel_state_source": "trust-evolution-summaries"},
                ],
                "users": [{"user": "10.0.0.3"}],
                "batch_preview": {"users_to_move": [{"user": "10.0.0.3"}], "blast_radius": {"users": 1}},
                "snapshot_statuses": {"trust-summaries": {"status": "OK"}, "prediction-summaries": {"status": "STALE"}},
            },
            execution_summary={"summary": {"health": "OK", "contracts_total": 1, "events_total": 1}},
        )

        self.assertEqual(dashboard["schema_version"], "v7.operator-execution-dashboard.v1")
        self.assertTrue(dashboard["read_only"])
        self.assertFalse(dashboard["execution_allowed_now"])
        self.assertFalse(dashboard["routing_behavior_changed"])
        self.assertEqual(dashboard["users_moved"], 0)
        self.assertFalse(dashboard["apply_executed"])
        self.assertFalse(dashboard["autonomy_enabled"])
        self.assertEqual(dashboard["current_authority"]["execution_owner"], pipeline.CANONICAL_RUNTIME_EXECUTOR)
        self.assertEqual(dashboard["current_authority"]["allowed_budget"], 1)
        self.assertEqual(len(dashboard["timeline"]), 7)
        self.assertIn("packet_duration_ms", dashboard["performance"]["available_metrics"])
        self.assertEqual(dashboard["performance"]["bottleneck"], "NONE")
        self.assertEqual(dashboard["performance"]["current_stage"], "verification")
        self.assertTrue(dashboard["operator_approval_review"]["operator_approval_ready"])
        self.assertEqual(dashboard["pool_status"]["channels_total"], 2)
        self.assertEqual(dashboard["planner_status"]["candidate_moves_total"], 1)
        self.assertEqual(dashboard["snapshot_status"]["state"], "REVIEW_REQUIRED")
        self.assertIn("prediction-summaries", dashboard["snapshot_status"]["non_ready_families"])
        self.assertFalse(dashboard["shadow_autonomy"]["enabled"])
        self.assertEqual(dashboard["shadow_autonomy"]["decisions_total"], 1)
        self.assertEqual(dashboard["shadow_autonomy"]["agreement_rate"], 1.0)
        self.assertEqual(dashboard["shadow_autonomy"]["operator_behavior"]["behavior_pattern"], "MOSTLY_AGREEING")
        self.assertFalse(dashboard["shadow_autonomy"]["autonomy_readiness"]["bounded_autonomy_ready"])
        self.assertFalse(dashboard["shadow_autonomy"]["apply_executed"])
        self.assertFalse(dashboard["shadow_autonomy"]["autonomy_enabled"])
        self.assertFalse(dashboard["reuse"]["new_dashboard_created"])
        self.assertFalse(dashboard["reuse"]["parallel_observability_created"])

    def test_execution_dashboard_detects_slow_path_without_runtime_mutation(self):
        readiness = pipeline.execution_loop_readiness_foundation(
            contracts=[
                {"contract_id": "contract-1", "stage": "packet", "duration_ms": 8, "affected_users": ["10.0.0.3", "10.0.0.6"]},
            ],
            events=[
                {"event_id": "apply-1", "event_type": "APPLY_COMPLETED", "duration_ms": 65000, "completed_at": "2026-06-08T10:00:01Z"},
                {"event_id": "verify-1", "event_type": "VERIFICATION_FAILED", "duration_ms": 200, "completed_at": "2026-06-08T10:00:02Z"},
                {"event_id": "rollback-1", "event_type": "ROLLBACK_COMPLETED", "duration_ms": 100, "completed_at": "2026-06-08T10:00:03Z"},
            ],
        )
        dashboard = pipeline.execution_operator_dashboard_model(readiness=readiness)

        self.assertTrue(dashboard["performance"]["slow_path_detected"])
        self.assertEqual(dashboard["performance"]["bottleneck"], "apply_duration_ms")
        self.assertEqual(dashboard["performance"]["latest_failure_ref"], "verify-1")
        self.assertEqual(dashboard["performance"]["latest_rollback_ref"], "rollback-1")
        self.assertFalse(dashboard["execution_allowed_now"])
        self.assertEqual(dashboard["users_moved"], 0)
        self.assertFalse(dashboard["apply_executed"])
        self.assertFalse(dashboard["autonomy_enabled"])

    def test_autonomous_dry_run_simulates_canary_without_runtime_mutation(self):
        decision_surface = {
            "users_by_ip": {
                "10.0.0.3": {
                    "user": "10.0.0.3",
                    "current_channel": "awg3",
                    "recommended_channel": "vless",
                    "confidence": 0.91,
                    "trust": 88.0,
                    "prediction": {"confidence": 0.82},
                    "risk": 2.5,
                    "recommendation_hash": "rec-1",
                    "source_hash": "source-1",
                    "reasons": ["vless has better service suitability"],
                },
            },
            "batch_preview": {
                "users_to_move": [
                    {"user": "10.0.0.3", "from": "awg3", "to": "vless", "confidence": 0.91, "risk": 2.5, "recommendation_hash": "rec-1"},
                ],
            },
            "snapshot_statuses": {"service-scores": {"status": "OK"}, "trust-summaries": {"status": "FRESH"}},
        }

        model = pipeline.autonomous_dry_run_model(decision_surface=decision_surface, max_users=1)

        self.assertTrue(model["autonomous_dry_run"])
        self.assertTrue(model["canary_autonomy_ready"])
        self.assertEqual(model["single_blocker"], "NONE")
        self.assertEqual(model["candidate_count"], 1)
        self.assertEqual(model["simulated_apply"]["selected_users_count"], 1)
        self.assertEqual(model["simulated_apply"]["would_move"][0]["user"], "10.0.0.3")
        self.assertEqual(model["simulated_apply"]["would_move"][0]["rollback_target"], "awg3")
        self.assertFalse(model["execution_allowed_now"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["routing_changed"])
        self.assertFalse(model["rollback_executed"])
        self.assertFalse(model["autonomy_enabled"])

    def test_autonomous_dry_run_hard_stops_on_snapshot_mismatch(self):
        decision_surface = {
            "users_by_ip": {
                "10.0.0.3": {"current_channel": "awg3", "recommended_channel": "vless", "confidence": 0.91, "trust": 88.0},
            },
            "batch_preview": {
                "users_to_move": [{"user": "10.0.0.3", "from": "awg3", "to": "vless", "confidence": 0.91}],
            },
            "snapshot_statuses": {
                "service-scores": {
                    "status": "STALE",
                    "validation_errors": ["source_hash_mismatch:service-scores:service_matrix"],
                },
            },
        }

        model = pipeline.autonomous_dry_run_model(decision_surface=decision_surface, max_users=1)
        blockers = model["safety_gates"]["hard_stop_blockers"]

        self.assertFalse(model["canary_autonomy_ready"])
        self.assertIn("snapshot_mismatch:service-scores", blockers)
        self.assertIn("source_drift:service-scores", blockers)
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["rollback_executed"])

    def test_autonomous_dry_run_accepts_operator_surface_snapshot_contract(self):
        decision_surface = {
            "users_by_ip": {
                "10.0.0.3": {
                    "current_channel": "awg3",
                    "recommended_channel": "vless",
                    "confidence": 0.91,
                    "trust": 88.0,
                    "prediction": {"confidence": 0.82},
                    "risk": 2.5,
                },
            },
            "batch_preview": {
                "users_to_move": [{"user": "10.0.0.3", "from": "awg3", "to": "vless", "confidence": 0.91}],
            },
            "snapshot_statuses": {
                "service-scores": {
                    "status": "OK",
                    "validation_ok": True,
                    "freshness_state": "FRESH",
                    "runtime_behavior": "ALLOW",
                    "stop_required": False,
                    "validation_errors": [],
                },
                "trust-summaries": {
                    "status": "OK",
                    "validation_ok": True,
                    "freshness_state": "FRESH",
                    "runtime_behavior": "ALLOW",
                    "stop_required": False,
                    "validation_errors": [],
                },
            },
        }

        model = pipeline.autonomous_dry_run_model(decision_surface=decision_surface, max_users=1)

        self.assertTrue(model["canary_autonomy_ready"])
        self.assertEqual(model["safety_gates"]["hard_stop_blockers"], [])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)

    def test_autonomous_dry_run_blocks_low_trust_and_prediction_confidence(self):
        decision_surface = {
            "users_by_ip": {
                "10.0.0.3": {
                    "current_channel": "awg3",
                    "recommended_channel": "awg0",
                    "confidence": 0.458,
                    "trust": 3.15,
                    "prediction": {"confidence": 0.386},
                    "risk": 3.387,
                },
            },
            "batch_preview": {
                "users_to_move": [
                    {"user": "10.0.0.3", "from": "awg3", "to": "awg0", "confidence": 0.458, "risk": 3.387},
                ],
            },
            "snapshot_statuses": {
                "service-scores": {"status": "OK", "validation_ok": True, "freshness_state": "FRESH", "stop_required": False},
                "trust-summaries": {"status": "OK", "validation_ok": True, "freshness_state": "FRESH", "stop_required": False},
                "prediction-summaries": {"status": "OK", "validation_ok": True, "freshness_state": "FRESH", "stop_required": False},
            },
        }

        model = pipeline.autonomous_dry_run_model(decision_surface=decision_surface, max_users=1)
        blockers = model["safety_gates"]["hard_stop_blockers"]
        floor = model["safety_gates"]["candidate_floor_evaluation"][0]

        self.assertFalse(model["canary_autonomy_ready"])
        self.assertIn("confidence_too_low", blockers)
        self.assertIn("trust_too_low", blockers)
        self.assertIn("prediction_confidence_too_low", blockers)
        self.assertEqual(floor["confidence"], 45.8)
        self.assertEqual(floor["trust"], 3.15)
        self.assertEqual(floor["prediction_confidence"], 38.6)
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)

    def test_autonomous_dry_run_can_use_outcome_evidence_without_lowering_floors(self):
        decision_surface = {
            "users_by_ip": {
                "10.0.0.3": {
                    "current_channel": "awg3",
                    "recommended_channel": "awg0",
                    "confidence": 0.458,
                    "trust": 3.15,
                    "prediction": {"confidence": 0.386},
                    "risk": 3.387,
                },
            },
            "batch_preview": {
                "users_to_move": [
                    {"user": "10.0.0.3", "from": "awg3", "to": "awg0", "confidence": 0.458, "risk": 3.387},
                ],
            },
            "trust_evolution_advice": {
                "available": True,
                "live_calibrated": True,
                "decision_confidence": 88,
                "prediction_confidence": 86,
                "service_confidence": 82,
                "suitability_confidence": 79,
                "rollback_confidence": 91,
                "blast_radius_confidence": 85,
                "candidate_outcomes_count": 8,
                "prediction_actuals_count": 8,
                "service_actuals_count": 8,
            },
            "snapshot_statuses": {
                "service-scores": {"status": "OK", "validation_ok": True, "freshness_state": "FRESH", "stop_required": False},
                "trust-summaries": {"status": "OK", "validation_ok": True, "freshness_state": "FRESH", "stop_required": False},
                "prediction-summaries": {"status": "OK", "validation_ok": True, "freshness_state": "FRESH", "stop_required": False},
            },
        }

        model = pipeline.autonomous_dry_run_model(decision_surface=decision_surface, max_users=1)
        floor = model["safety_gates"]["candidate_floor_evaluation"][0]
        adjustment = model["candidates"][0]["outcome_evidence_adjustment"]

        self.assertTrue(model["outcome_driven_evidence"]["applied"])
        self.assertTrue(model["canary_autonomy_ready"])
        self.assertEqual(model["single_blocker"], "NONE")
        self.assertGreaterEqual(floor["confidence"], pipeline.AUTONOMY_CANARY_CONFIDENCE_FLOOR)
        self.assertGreaterEqual(floor["trust"], pipeline.AUTONOMY_CANARY_TRUST_FLOOR)
        self.assertGreaterEqual(floor["prediction_confidence"], pipeline.AUTONOMY_CANARY_PREDICTION_CONFIDENCE_FLOOR)
        self.assertEqual(floor["rollback_confidence"], 91)
        self.assertEqual(adjustment["before"]["confidence"], 45.8)
        self.assertGreaterEqual(adjustment["after"]["confidence"], 70)
        self.assertFalse(adjustment["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["autonomy_enabled"])

    def test_autonomous_dry_run_exposes_engine_trace_and_reachability(self):
        decision_surface = {
            "users_by_ip": {
                "10.0.0.3": {
                    "current_channel": "awg3",
                    "recommended_channel": "awg0",
                    "confidence": 0.458,
                    "trust": 3.15,
                    "prediction": {"confidence": 0.396},
                    "risk": 3.387,
                },
            },
            "batch_preview": {
                "users_to_move": [
                    {"user": "10.0.0.3", "from": "awg3", "to": "awg0", "confidence": 0.458, "risk": 3.387},
                ],
            },
            "trust_evolution_advice": {
                "available": True,
                "live_calibrated": True,
                "decision_confidence": 35,
                "prediction_confidence": 36.604,
                "service_confidence": 37,
                "suitability_confidence": 38,
                "rollback_confidence": 0,
                "blast_radius_confidence": 20,
                "candidate_outcomes_count": 67,
                "prediction_actuals_count": 21,
                "service_actuals_count": 21,
                "rollback_validation_status": "NO_ROLLBACK_OUTCOMES",
            },
            "snapshot_statuses": {
                "service-scores": {"status": "OK", "validation_ok": True, "freshness_state": "FRESH", "stop_required": False},
                "trust-summaries": {"status": "OK", "validation_ok": True, "freshness_state": "FRESH", "stop_required": False},
                "prediction-summaries": {"status": "OK", "validation_ok": True, "freshness_state": "FRESH", "stop_required": False},
            },
        }

        model = pipeline.autonomous_dry_run_model(decision_surface=decision_surface, max_users=1)
        trace = model["engine_trace"]

        self.assertEqual(trace["confidence_engine_trace"]["candidate_confidence"], 45.8)
        self.assertEqual(trace["prediction_engine_trace"]["production_formula"], "mean(matched_forecast_accuracy) * mean(forecast_confidence)")
        self.assertEqual(trace["rollback_confidence_trace"]["validation_status"], "NO_ROLLBACK_OUTCOMES")
        self.assertIn("rollback_validation_evidence_missing_or_not_scored", trace["evidence_flow_audit"]["missing_links"])
        self.assertEqual(trace["reachability_model"]["gaps"]["confidence"], 24.2)
        self.assertEqual(trace["time_to_floor_analysis"]["additional_rollback_validations_needed"], 1)
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["autonomy_enabled"])

    def test_autonomous_dry_run_ignores_uncalibrated_outcome_evidence(self):
        decision_surface = {
            "users_by_ip": {
                "10.0.0.3": {
                    "current_channel": "awg3",
                    "recommended_channel": "awg0",
                    "confidence": 0.458,
                    "trust": 3.15,
                    "prediction": {"confidence": 0.386},
                    "risk": 3.387,
                },
            },
            "batch_preview": {
                "users_to_move": [
                    {"user": "10.0.0.3", "from": "awg3", "to": "awg0", "confidence": 0.458, "risk": 3.387},
                ],
            },
            "trust_evolution_advice": {
                "available": True,
                "live_calibrated": False,
                "decision_confidence": 99,
                "prediction_confidence": 99,
                "service_confidence": 99,
                "suitability_confidence": 99,
                "rollback_confidence": 99,
                "blast_radius_confidence": 99,
                "candidate_outcomes_count": 8,
                "prediction_actuals_count": 8,
                "service_actuals_count": 8,
            },
            "snapshot_statuses": {
                "service-scores": {"status": "OK", "validation_ok": True, "freshness_state": "FRESH", "stop_required": False},
                "trust-summaries": {"status": "OK", "validation_ok": True, "freshness_state": "FRESH", "stop_required": False},
                "prediction-summaries": {"status": "OK", "validation_ok": True, "freshness_state": "FRESH", "stop_required": False},
            },
        }

        model = pipeline.autonomous_dry_run_model(decision_surface=decision_surface, max_users=1)
        blockers = model["safety_gates"]["hard_stop_blockers"]
        floor = model["safety_gates"]["candidate_floor_evaluation"][0]

        self.assertFalse(model["outcome_driven_evidence"]["applied"])
        self.assertFalse(model["canary_autonomy_ready"])
        self.assertIn("confidence_too_low", blockers)
        self.assertIn("trust_too_low", blockers)
        self.assertIn("prediction_confidence_too_low", blockers)
        self.assertEqual(floor["confidence"], 45.8)
        self.assertEqual(floor["trust"], 3.15)
        self.assertEqual(floor["prediction_confidence"], 38.6)
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["autonomy_enabled"])

    def test_autonomous_dry_run_reuses_existing_owners(self):
        model = pipeline.autonomous_dry_run_model(decision_surface={}, max_users=1)
        owners = model["owner_reuse_audit"]

        self.assertTrue(owners["owners_reused"])
        self.assertEqual(owners["planner"], pipeline.CANONICAL_PLANNER)
        self.assertEqual(owners["packet_owner"], pipeline.CANONICAL_PACKET_OWNER)
        self.assertEqual(owners["rollback_model"], pipeline.CANONICAL_PACKET_OWNER)
        self.assertFalse(owners["new_planner_created"])
        self.assertFalse(owners["new_execution_path_created"])
        self.assertFalse(owners["new_truth_source_created"])
        self.assertEqual(model["single_blocker"], "no_canary_candidate_available")

    def test_operator_dashboard_exposes_autonomous_dry_run(self):
        dashboard = pipeline.execution_operator_dashboard_model(
            decision_surface={
                "users_by_ip": {
                    "10.0.0.3": {
                        "current_channel": "awg3",
                        "recommended_channel": "vless",
                        "confidence": 0.91,
                        "trust": 88.0,
                    },
                },
                "batch_preview": {
                    "users_to_move": [{"user": "10.0.0.3", "from": "awg3", "to": "vless", "confidence": 0.91}],
                    "blast_radius": {"users": 1},
                },
                "snapshot_statuses": {"service-scores": {"status": "OK"}},
            }
        )

        self.assertIn("autonomous_dry_run", dashboard)
        self.assertTrue(dashboard["autonomous_dry_run"]["autonomous_dry_run"])
        self.assertFalse(dashboard["autonomous_dry_run"]["apply_executed"])
        self.assertEqual(dashboard["autonomous_dry_run"]["users_moved"], 0)
        self.assertFalse(dashboard["autonomous_dry_run"]["autonomy_enabled"])

    def test_direct_user_switch_blocker_is_fail_closed(self):
        blocked = pipeline.direct_user_switch_blocker("10.7.0.3", "awg3", "operator-a")

        self.assertEqual(blocked["status"], "blocked")
        self.assertEqual(blocked["error"], "governed_execution_pipeline_required")
        self.assertFalse(blocked["execution_allowed_now"])
        self.assertFalse(blocked["runtime_mutation_performed"])
        self.assertFalse(blocked["users_moved"])
        self.assertFalse(blocked["autoswitch_apply_run"])
        self.assertIn("v7-users-autoswitch --apply --verify", blocked["required_path"])

    def test_module_does_not_import_or_call_runtime_execution(self):
        source = Path(pipeline.__file__).read_text(encoding="utf-8")

        self.assertNotIn("subprocess", source)
        self.assertNotIn("run_action", source)
        self.assertNotIn("os.system", source)

    def test_admin_user_switch_endpoint_no_longer_calls_direct_switch(self):
        source = ADMIN_API.read_text(encoding="utf-8")
        marker = 'elif path == "/api/actions/user-switch":'
        start = source.index(marker)
        end = source.index('elif path == "/api/actions/users-rebalance-dry-run":', start)
        handler = source[start:end]

        self.assertIn("governed_user_switch_blocker_response", handler)
        self.assertNotIn("run_action([\"v7-user-switch\"", handler)
        self.assertNotIn("proxy_runtime_switch_user_egress", handler)

    def test_admin_operator_dashboard_reuses_existing_operator_surface(self):
        source = ADMIN_API.read_text(encoding="utf-8")

        self.assertIn('id="operatorExecutionDashboard"', source)
        self.assertIn('id="operatorExecutionLoopTimeline"', source)
        self.assertIn('id="operatorExecutionPerformance"', source)
        self.assertIn('id="operatorAutonomousDryRun"', source)
        self.assertIn("renderOperatorExecutionDashboard(operatorView.execution_dashboard || {})", source)
        self.assertIn("renderOperatorAutonomousDryRun", source)
        self.assertIn("/api/operator/autonomous-dry-run", source)
        self.assertIn("shadow_autonomy_response(decision_surface=surface, record=False)", source)
        self.assertIn("execution_dashboard_response()", source)
        self.assertIn("Доверие и восстановление", source)
        self.assertIn("openOperatorFocusedFix", source)
        self.assertIn("Исправить это", source)
        self.assertIn("closure_duration_ms:'Закрытие'", source)
        self.assertIn("approval готов", source)
        self.assertIn("openChannelStateDrawer", source)
        self.assertIn('id="operatorShadowAutonomy"', source)
        self.assertIn("renderOperatorShadowAutonomy", source)
        self.assertIn("/api/actions/shadow-autonomy-compare", source)
        self.assertIn("Shadow-наблюдение", source)
        self.assertIn("Качество решений", source)
        self.assertIn("Несогласия", source)
        self.assertNotIn("/api/actions/execution-apply", source)


if __name__ == "__main__":
    unittest.main()
