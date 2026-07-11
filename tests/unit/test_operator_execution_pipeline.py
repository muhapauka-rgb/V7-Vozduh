import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from admin_core import operator_execution
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
            "ctr_governance_evidence": {
                "schema_version": "v7.ctr.governance-evidence.v1",
                "channel": "awg3",
                "state": "RECOVERING",
                "reason": "Канал восстанавливается.",
                "recovery_state": "IN_PROGRESS",
                "recovery_path": "После подтверждения вернётся в WATCH или TRUSTED.",
                "blocked_actions": "Нельзя расширять нагрузку автоматически.",
                "recommended_action": "Дождаться стабильности.",
                "review_required": True,
                "approval_authority": "none",
                "denial_authority": "none",
                "packet_preview": {
                    "ctr_state": "RECOVERING",
                    "ctr_confidence": 0.8,
                    "ctr_review_status": "REVIEW_REQUIRED",
                    "ctr_review_reason": "Канал ещё восстанавливается.",
                    "ctr_recovery_state": "IN_PROGRESS",
                    "ctr_recovery_path": "После подтверждения вернётся в WATCH или TRUSTED.",
                    "ctr_blocked_actions": "Нельзя расширять нагрузку автоматически.",
                    "ctr_recommended_action": "Дождаться стабильности.",
                    "emergency_only": False,
                },
            },
            "review_required": True,
            "review_required_reasons": ["ctr_state_requires_operator_review"],
            "review_category": "recovery_review",
            "review_severity": "medium",
            "review_recommendation": "Дождаться стабильности.",
            "review_warning": "Не расширять нагрузку автоматически.",
            "review_next_action": "Проверить recovery state.",
            "emergency_only": False,
        }

    def governed_canary_surface(self, *, target="awg0", recommendation_hash="rec-canary-1", source_hash="source-canary-1"):
        return {
            "controlled_execution_source_hashes": {
                "users_registry": "users-canary-hash",
                "egress_registry": "egress-canary-hash",
            },
            "controlled_execution_snapshot_bundle_hash": "snapshot-canary-hash",
            "users_by_ip": {
                "10.7.0.5": {
                    "user": "10.7.0.5",
                    "current_channel": "vless",
                    "recommended_channel": target,
                    "confidence": 0.458,
                    "trust": 54.115,
                    "prediction": {"confidence": 0.35514},
                    "risk": 3.2,
                    "recommendation_hash": recommendation_hash,
                    "source_hash": source_hash,
                    "reasons": ["planner selected one-user governed canary"],
                },
            },
            "batch_preview": {
                "users_to_move": [
                    {
                        "user": "10.7.0.5",
                        "from": "vless",
                        "to": target,
                        "confidence": 0.458,
                        "risk": 3.2,
                        "recommendation_hash": recommendation_hash,
                    },
                ],
                "knowledge_decision_readiness": {
                    "routing_recommendation_readiness": "READY_FOR_REVIEW",
                    "blockers": [],
                    "decision_effectiveness": {"recommendation_correct_rate": 1.0},
                    "knowledge_growth": {"knowledge_gained": 1},
                },
            },
            "knowledge_decision_overlay": {
                "service_user_sla_fit": {"rows": [], "blockers": []},
                "freshness_actionability": {"domains": {}, "blockers": []},
                "recovery_admission": {"rows": [], "blockers": []},
                "anti_flapping": {"rows": [], "blockers": []},
                "decision_effectiveness": {"recommendation_correct_rate": 1.0},
                "routing_recommendation_readiness": {"readiness": "READY_FOR_REVIEW", "blockers": []},
            },
            "knowledge_quality_read_model": {"schema_version": "v7.knowledge-quality-read-model.v1"},
            "snapshot_statuses": {
                "service-scores": {"status": "OK", "validation_ok": True, "freshness_state": "FRESH", "stop_required": False},
                "trust-summaries": {"status": "OK", "validation_ok": True, "freshness_state": "FRESH", "stop_required": False},
                "prediction-summaries": {"status": "OK", "validation_ok": True, "freshness_state": "FRESH", "stop_required": False},
            },
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
        self.assertTrue(contract["review_required"])
        self.assertIn("ctr_state_requires_operator_review", contract["review_required_reasons"])
        self.assertEqual(contract["review_category"], "recovery_review")
        self.assertEqual(contract["review_severity"], "medium")
        self.assertEqual(contract["packet_evidence_preview"]["ctr_state"], "RECOVERING")
        self.assertEqual(contract["ctr_governance_evidence"]["state"], "RECOVERING")
        self.assertEqual(contract["ctr_authority"]["approval_authority"], "none")
        self.assertEqual(contract["ctr_authority"]["runtime_execution_authority"], "none")
        self.assertFalse(contract["ctr_authority"]["packet_authority_changed"])

    def test_autonomy_candidate_selection_review_finds_better_candidate_without_mutation(self):
        decision_surface = {
            "users_by_ip": {
                "10.7.0.16": {
                    "user": "10.7.0.16",
                    "current_channel": "vless",
                    "recommended_channel": "awg3",
                    "confidence": 0.42,
                    "trust": 35,
                    "prediction": {"confidence": 0.39},
                    "risk": 8,
                    "recommendation_hash": "weak-rec",
                    "source_hash": "weak-source",
                },
                "10.7.0.17": {
                    "user": "10.7.0.17",
                    "current_channel": "vless",
                    "recommended_channel": "awg3",
                    "confidence": 0.91,
                    "trust": 88,
                    "prediction": {"confidence": 0.86},
                    "risk": 3,
                    "recommendation_hash": "strong-rec",
                    "source_hash": "strong-source",
                },
            },
            "batch_preview": {
                "users_to_move": [
                    {"user": "10.7.0.16", "from": "vless", "to": "awg3", "confidence": 0.42, "risk": 8},
                    {"user": "10.7.0.17", "from": "vless", "to": "awg3", "confidence": 0.91, "risk": 3},
                ]
            },
        }

        review = pipeline.autonomy_candidate_selection_review_model(decision_surface=decision_surface)

        self.assertEqual(review["candidate_count"], 2)
        self.assertEqual(review["current_candidate"]["user"], "10.7.0.16")
        self.assertEqual(review["best_candidate"]["user"], "10.7.0.17")
        self.assertTrue(review["better_candidate_exists"])
        self.assertFalse(review["current_candidate_is_best"])
        self.assertEqual(review["selection_model_health"]["state"], "BETTER_CANDIDATE_AVAILABLE")
        self.assertEqual(review["top_candidates"]["combined_readiness"][0]["user"], "10.7.0.17")
        self.assertEqual(review["top_candidates"]["confidence"][0]["user"], "10.7.0.17")
        self.assertEqual(review["top_candidates"]["trust"][0]["user"], "10.7.0.17")
        self.assertEqual(review["top_candidates"]["prediction"][0]["user"], "10.7.0.17")
        self.assertEqual(review["current_candidate"]["floor_distance"]["confidence"], 28.0)
        self.assertEqual(review["current_candidate"]["floor_distance"]["trust"], 35.0)
        self.assertEqual(review["current_candidate"]["floor_distance"]["prediction_confidence"], 31.0)
        self.assertTrue(review["best_candidate"]["passes_autonomy_floors"])
        self.assertTrue(review["read_only"])
        self.assertFalse(review["runtime_mutation_performed"])
        self.assertFalse(review["apply_executed"])
        self.assertEqual(review["users_moved"], 0)
        self.assertFalse(review["autonomy_enabled"])

    def test_autonomy_candidate_selection_review_preserves_current_best_ties(self):
        decision_surface = {
            "users_by_ip": {
                "10.7.0.16": {
                    "user": "10.7.0.16",
                    "current_channel": "vless",
                    "recommended_channel": "awg3",
                    "confidence": 0.45,
                    "trust": 34,
                    "prediction": {"confidence": 0.39},
                    "risk": 3,
                },
                "10.7.0.17": {
                    "user": "10.7.0.17",
                    "current_channel": "vless",
                    "recommended_channel": "awg3",
                    "confidence": 0.45,
                    "trust": 34,
                    "prediction": {"confidence": 0.39},
                    "risk": 3,
                },
            },
            "batch_preview": {
                "users_to_move": [
                    {"user": "10.7.0.16", "from": "vless", "to": "awg3", "confidence": 0.45, "risk": 3},
                    {"user": "10.7.0.17", "from": "vless", "to": "awg3", "confidence": 0.45, "risk": 3},
                ]
            },
        }

        review = pipeline.autonomy_candidate_selection_review_model(decision_surface=decision_surface)

        self.assertEqual(review["candidate_count"], 2)
        self.assertEqual(review["current_candidate"]["user"], "10.7.0.16")
        self.assertEqual(review["best_candidate"]["user"], "10.7.0.16")
        self.assertTrue(review["current_candidate_is_best"])
        self.assertFalse(review["better_candidate_exists"])
        self.assertEqual(review["selection_model_health"]["state"], "CURRENT_BEST")
        self.assertTrue(review["selection_model_health"]["could_select_weaker_candidate_when_scores_differ"])

    def test_autonomy_confidence_component_review_traces_pool_root_cause(self):
        decision_surface = {
            "trust_evolution_advice": {
                "available": True,
                "live_calibrated": True,
                "candidate_outcomes_count": 67,
                "prediction_actuals_count": 21,
                "service_actuals_count": 21,
                "decision_confidence": 50,
                "service_confidence": 38,
                "suitability_confidence": 28,
                "prediction_confidence": 39,
                "blast_radius_confidence": 20,
                "rollback_confidence": 100,
                "rollback_validation_status": "VALIDATED",
            },
            "users_by_ip": {
                "10.7.0.16": {
                    "user": "10.7.0.16",
                    "current_channel": "vless",
                    "recommended_channel": "awg3",
                    "confidence": 0.45,
                    "trust": 3,
                    "prediction": {"confidence": 0.39},
                    "risk": 3,
                },
                "10.7.0.17": {
                    "user": "10.7.0.17",
                    "current_channel": "vless",
                    "recommended_channel": "awg3",
                    "confidence": 0.45,
                    "trust": 3,
                    "prediction": {"confidence": 0.39},
                    "risk": 3,
                },
            },
            "batch_preview": {
                "users_to_move": [
                    {"user": "10.7.0.16", "from": "vless", "to": "awg3", "confidence": 0.45, "risk": 3},
                    {"user": "10.7.0.17", "from": "vless", "to": "awg3", "confidence": 0.45, "risk": 3},
                ]
            },
        }

        review = pipeline.autonomy_confidence_component_review_model(decision_surface=decision_surface)

        self.assertTrue(review["read_only"])
        self.assertEqual(review["candidate_pool_analysis"]["candidate_count"], 2)
        self.assertEqual(len(review["candidate_pool_analysis"]["top_candidates"]), 2)
        components = {row["component"]: row for row in review["confidence_component_trace"]}
        self.assertEqual(components["blast_radius_confidence"]["distance_to_floor"], 50.0)
        self.assertEqual(components["suitability_confidence"]["distance_to_floor"], 42.0)
        self.assertEqual(components["service_confidence"]["distance_to_floor"], 32.0)
        self.assertEqual(components["prediction_confidence"]["distance_to_floor"], 31.0)
        self.assertEqual(components["decision_confidence"]["distance_to_floor"], 20.0)
        self.assertEqual(components["rollback_confidence"]["distance_to_floor"], 0.0)
        self.assertEqual(review["pool_wide_root_cause"]["primary_limiting_component"], "blast_radius_confidence")
        self.assertTrue(review["pool_wide_root_cause"]["pool_wide_issue"])
        self.assertFalse(review["pool_wide_root_cause"]["candidate_specific_issue"])
        self.assertIn("decision_confidence", review["component_weighting"]["confidence_score_inputs"])
        self.assertIn("blast_radius_confidence", review["component_weighting"]["trust_score_inputs"])
        reachability = {row["component"]: row for row in review["component_reachability_review"]}
        self.assertIn("matched forecast actuals", reachability["prediction_confidence"]["required_evidence"])
        self.assertTrue(reachability["service_confidence"]["reachable_without_floor_reduction"])
        self.assertFalse(review["model_health_review"]["floor_reduction_required"])
        self.assertFalse(review["runtime_mutation_performed"])
        self.assertFalse(review["apply_executed"])
        self.assertEqual(review["users_moved"], 0)
        self.assertFalse(review["autonomy_enabled"])

    def test_autonomy_confidence_component_review_marks_healthy_components(self):
        decision_surface = {
            "trust_evolution_advice": {
                "available": True,
                "live_calibrated": True,
                "candidate_outcomes_count": 10,
                "prediction_actuals_count": 10,
                "service_actuals_count": 10,
                "decision_confidence": 80,
                "service_confidence": 82,
                "suitability_confidence": 84,
                "prediction_confidence": 86,
                "blast_radius_confidence": 88,
                "rollback_confidence": 100,
                "rollback_validation_status": "VALIDATED",
            },
            "users_by_ip": {
                "10.7.0.16": {
                    "user": "10.7.0.16",
                    "current_channel": "vless",
                    "recommended_channel": "awg3",
                    "confidence": 0.9,
                    "trust": 90,
                    "prediction": {"confidence": 0.9},
                    "risk": 1,
                },
            },
            "batch_preview": {
                "users_to_move": [
                    {"user": "10.7.0.16", "from": "vless", "to": "awg3", "confidence": 0.9, "risk": 1},
                ]
            },
        }

        review = pipeline.autonomy_confidence_component_review_model(decision_surface=decision_surface)

        self.assertEqual(review["pool_wide_root_cause"]["primary_limiting_component"], "NONE")
        self.assertFalse(review["pool_wide_root_cause"]["pool_wide_issue"])
        for component in review["model_health_review"]["components"]:
            with self.subTest(component=component["component"]):
                self.assertTrue(component["healthy"])
                self.assertEqual(component["health_state"], "HEALTHY")
                self.assertFalse(component["misweighted"])
        self.assertFalse(review["component_weighting"]["floors_lowered"])
        self.assertFalse(review["component_weighting"]["weights_changed"])

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
        self.assertTrue(verdicts["operator_approved_controller_preview_ready"])
        self.assertTrue(cert["operator_approved_execution_controller"]["preview_only"])

    def test_operator_approved_controller_approve_preview_reuses_existing_owners(self):
        model = pipeline.operator_approved_execution_controller_preview("APPROVE")
        owners = model["owner_reuse"]
        step_names = [row["name"] for row in model["steps"]]

        self.assertEqual(model["decision"], "APPROVE")
        self.assertTrue(model["preview_only"])
        self.assertFalse(model["execution_allowed_now"])
        self.assertFalse(model["runtime_mutation_performed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["autonomy_enabled"])
        self.assertEqual(owners["planner"], pipeline.CANONICAL_PLANNER)
        self.assertEqual(owners["packet"], pipeline.CANONICAL_PACKET_TOOL)
        self.assertEqual(owners["restore_barrier"], pipeline.CANONICAL_PACKET_OWNER)
        self.assertEqual(owners["apply"], pipeline.CANONICAL_RUNTIME_EXECUTOR)
        self.assertEqual(owners["feedback"], pipeline.CANONICAL_FEEDBACK_OWNER)
        self.assertEqual(step_names, [
            "fresh_planner",
            "packet",
            "runtime_recheck",
            "restore_barrier",
            "apply",
            "verify",
            "rollback_readiness",
            "feedback",
            "closure",
            "trust_refresh",
        ])
        self.assertTrue(model["final_certification"]["operator_reduced_to_approve_reject"])
        for value in model["no_bypass_certification"].values():
            self.assertFalse(value)

    def test_operator_approved_controller_reject_preview_closure_only(self):
        model = pipeline.operator_approved_execution_controller_preview("REJECT")

        self.assertEqual(model["decision"], "REJECT")
        self.assertEqual(model["terminal_preview_state"], "REJECTED_CLOSURE_ONLY")
        self.assertTrue(model["closure_only"])
        self.assertEqual([row["name"] for row in model["steps"]], ["reject_closure"])
        self.assertEqual(model["steps"][0]["owner"], pipeline.CANONICAL_FEEDBACK_OWNER)
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)
        self.assertFalse(model["routing_changed"])
        self.assertIn("governed apply", model["blocked_actions"])

    def test_rt2_s4_governed_execution_coordination_owner_maps_terminal_path(self):
        s4 = pipeline.rt2_s4_governed_execution_coordination(
            rt2_s3_delta={"status": "DONE_READ_ONLY_DELTA_OWNER_MAPPED"},
        )

        rows = {row["stage"]: row for row in s4["coordination_rows"]}
        self.assertEqual(s4["schema_version"], "v7.rt2-s4-governed-execution-coordination.v1")
        self.assertEqual(s4["status"], "DONE_READ_ONLY_GOVERNED_EXECUTION_COORDINATION_OWNER_MAPPED")
        self.assertTrue(s4["completion_criteria_met"])
        for stage in [
            "packet",
            "runtime_recheck",
            "restore_barrier",
            "apply",
            "verify",
            "rollback_readiness",
            "feedback",
            "closure",
        ]:
            self.assertIn(stage, rows)
            self.assertEqual(rows[stage]["status"], "OWNER_MAPPED")
            self.assertFalse(rows[stage]["runtime_mutation_performed_now"])
        self.assertEqual(rows["packet"]["owner"], pipeline.CANONICAL_PACKET_TOOL)
        self.assertEqual(rows["restore_barrier"]["owner"], pipeline.CANONICAL_PACKET_OWNER)
        self.assertEqual(rows["apply"]["owner"], pipeline.CANONICAL_RUNTIME_EXECUTOR)
        self.assertEqual(rows["feedback"]["owner"], pipeline.CANONICAL_FEEDBACK_OWNER)
        self.assertEqual(s4["terminal_classification"]["closure_owner"], pipeline.CANONICAL_FEEDBACK_OWNER)
        self.assertTrue(s4["terminal_classification"]["terminal_classification_ready"])
        self.assertEqual(
            s4["terminal_classification"]["containment_forward_fix_schema"],
            "v7.b15-containment-forward-fix-classification.v1",
        )
        b15 = s4["source_models"]["containment_forward_fix_classification"]
        self.assertEqual(b15["backlog_item"], "B15")
        self.assertTrue(b15["read_only"])
        self.assertFalse(b15["runtime_mutation_performed"])
        self.assertFalse(b15["apply_executed"])
        self.assertFalse(b15["rollback_executed"])
        self.assertEqual(b15["users_moved"], 0)
        self.assertEqual(s4["unlocked_capability"], "RT2-S5_CERTIFIED_CONCURRENCY_LADDER")
        self.assertEqual(s4["missing_stages"], [])
        self.assertEqual(s4["ownerless_stages"], [])

    def test_rt2_s4_governed_execution_coordination_remains_read_only(self):
        s4 = pipeline.rt2_s4_governed_execution_coordination()

        self.assertTrue(s4["read_only"])
        self.assertTrue(s4["preview_only"])
        self.assertFalse(s4["safety"]["runtime_behavior_changed"])
        self.assertFalse(s4["safety"]["runtime_apply_allowed_now"])
        self.assertFalse(s4["safety"]["restore_barrier_written_now"])
        self.assertFalse(s4["safety"]["apply_executed"])
        self.assertFalse(s4["safety"]["rollback_executed"])
        self.assertFalse(s4["safety"]["feedback_written_now"])
        self.assertFalse(s4["safety"]["closure_written_now"])
        self.assertEqual(s4["safety"]["users_moved"], 0)
        self.assertFalse(s4["safety"]["authority_expanded"])
        self.assertFalse(s4["safety"]["concurrency_enabled"])
        self.assertFalse(s4["safety"]["queue_daemon_created"])
        self.assertFalse(s4["safety"]["new_execution_path_created"])
        self.assertIn("RT2-S6_EVIDENCE_BASED_CONTINUOUS_IMPROVEMENT", s4["still_blocked"])
        self.assertIn("runtime_apply", s4["still_blocked"])
        self.assertIn("concurrency", s4["still_blocked"])
        self.assertTrue(s4["idempotency_and_loop_controls"]["planner_regeneration_after_approval_blocked"])
        self.assertFalse(s4["idempotency_and_loop_controls"]["queue_daemon_created"])

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

    def test_rt2_s1_measurement_observability_foundation_owner_maps_required_fields(self):
        foundation = pipeline.rt2_s1_measurement_observability_foundation(
            planner_result={"stage": "planner", "duration_ms": 15, "operation": {"selected_move_count": 2}},
            contracts=[
                {"contract_id": "contract-1", "stage": "packet", "duration_ms": 5, "affected_users": ["10.0.0.3", "10.0.0.6"]},
                {"contract_id": "contract-1", "stage": "restore_barrier", "duration_ms": 10},
            ],
            events=[
                {"event_id": "apply-1", "event_type": "APPLY_COMPLETED", "duration_ms": 65000, "completed_at": "2026-06-08T10:00:01Z"},
                {"event_id": "verify-1", "event_type": "VERIFICATION_FAILED", "duration_ms": 200, "completed_at": "2026-06-08T10:00:02Z"},
                {"event_id": "rollback-1", "event_type": "ROLLBACK_COMPLETED", "duration_ms": 300, "completed_at": "2026-06-08T10:00:03Z"},
                {"event_id": "feedback-1", "event_type": "FEEDBACK_MATERIALIZED", "duration_ms": 20, "completed_at": "2026-06-08T10:00:04Z"},
                {"event_id": "closure-1", "event_type": "CLOSURE_CLOSED", "duration_ms": 10, "completed_at": "2026-06-08T10:00:05Z"},
            ],
        )

        rows = {row["category"]: row for row in foundation["measurement_rows"]}
        self.assertEqual(foundation["schema_version"], "v7.rt2-s1-measurement-observability-foundation.v1")
        self.assertEqual(foundation["workstream"], "RT2-S1")
        self.assertEqual(foundation["status"], "DONE_READ_ONLY_MEASUREMENT_OWNER_MAPPED")
        self.assertTrue(foundation["completion_criteria_met"])
        self.assertEqual(rows["runtime_time"]["status"], "OBSERVED")
        self.assertEqual(rows["reaction_latency"]["status"], "OBSERVED")
        self.assertEqual(rows["dependency_topology"]["status"], "OBSERVED")
        self.assertEqual(rows["time_to_safe_recovery"]["status"], "PARTIAL_OWNER_MAPPED")
        self.assertEqual(foundation["source_models"]["dashboard_performance"]["bottleneck"], "apply_duration_ms")
        self.assertEqual(foundation["unlocked_capability"], "RT2-S2_WORLD_READINESS_MATURATION")
        self.assertIn("RT2-S3_DESIRED_STATE_DELTA", foundation["still_blocked"])
        self.assertFalse(foundation["safety"]["dashboard_can_approve"])
        self.assertFalse(foundation["safety"]["runtime_apply_allowed_now"])
        self.assertFalse(foundation["safety"]["authority_expanded"])
        self.assertEqual(foundation["safety"]["users_moved"], 0)
        self.assertFalse(foundation["safety"]["new_owner_created"])

    def test_rt2_s1_measurement_observability_foundation_marks_missing_fields_with_owner(self):
        foundation = pipeline.rt2_s1_measurement_observability_foundation()
        rows = {row["category"]: row for row in foundation["measurement_rows"]}

        self.assertEqual(foundation["status"], "DONE_READ_ONLY_MEASUREMENT_OWNER_MAPPED")
        self.assertTrue(foundation["completion_criteria_met"])
        self.assertEqual(rows["runtime_time"]["status"], "OWNER_MAPPED_MISSING")
        self.assertEqual(rows["reaction_latency"]["status"], "OWNER_MAPPED_MISSING")
        self.assertEqual(rows["time_to_safe_recovery"]["status"], "OWNER_MAPPED_MISSING")
        self.assertIn("runtime_time", foundation["owner_mapped_missing_categories"])
        self.assertEqual(foundation["unmapped_categories"], [])
        self.assertFalse(foundation["safety"]["synthetic_metrics_created"])
        self.assertFalse(foundation["safety"]["runtime_behavior_changed"])

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
        evidence = model["autonomy_specific_evidence"]
        self.assertEqual(evidence["autonomous_trigger_evidence"]["status"], "READY_FOR_CANARY_REVIEW")
        self.assertEqual(evidence["autonomous_rollback_decision_evidence"]["status"], "SIMULATED_ROLLBACK_READY")
        self.assertEqual(evidence["operator_free_apply_evidence"]["status"], "NOT_CERTIFIED_BY_DESIGN")
        self.assertTrue(evidence["canary_autonomy_ready"])
        self.assertIn("operator_free_apply_not_certified", evidence["current_missing_evidence"])
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
        evidence = model["autonomy_specific_evidence"]
        self.assertEqual(evidence["self_stop_evidence"]["status"], "PROVEN_STOPPED")
        self.assertIn("snapshot_mismatch:service-scores", evidence["self_stop_evidence"]["hard_stop_blockers"])
        self.assertFalse(evidence["operator_free_apply_evidence"]["proved"])
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
        tier_review = model["safety_gates"]["risk_tier_review"]
        self.assertEqual(tier_review["nearest_reachable_tier"], "TIER_1")
        self.assertEqual(tier_review["nearest_reachable_status"], "MARGINAL_OPERATOR_REVIEW")
        self.assertEqual(tier_review["autonomous_one_user_status"], "NO_GO")
        self.assertTrue(tier_review["operator_canary_marginal_allowed"])
        self.assertFalse(model["apply_executed"])
        self.assertEqual(model["users_moved"], 0)

    def test_risk_tier_review_does_not_allow_operator_canary_past_absolute_blockers(self):
        review = pipeline.autonomy_risk_tier_review(
            candidate_floor_evaluation=[{
                "confidence": 45.8,
                "trust": 54.1,
                "prediction_confidence": 35.3,
                "rollback_confidence": 100.0,
            }],
            blockers=["confidence_too_low", "packet_mismatch"],
        )

        tiers = {row["tier"]: row for row in review["tiers"]}

        self.assertEqual(tiers["TIER_1"]["status"], "NO_GO")
        self.assertIn("packet_mismatch", review["non_negotiable_blockers"])
        self.assertFalse(review["operator_canary_marginal_allowed"])
        self.assertFalse(review["apply_executed"])
        self.assertEqual(review["users_moved"], 0)

    def test_risk_tier_model_keeps_higher_autonomy_floors_above_canary_floor(self):
        model = pipeline.autonomy_risk_tier_floor_model()
        tiers = {row["tier"]: row for row in model["tier_semantics"]}

        self.assertEqual(tiers["TIER_1"]["floor_mode"], "advisory_gap_visible")
        self.assertEqual(tiers["TIER_3"]["floors"]["confidence"], pipeline.AUTONOMY_CANARY_CONFIDENCE_FLOOR)
        self.assertGreater(tiers["TIER_4"]["floors"]["confidence"], tiers["TIER_3"]["floors"]["confidence"])
        self.assertGreater(tiers["TIER_6"]["floors"]["confidence"], tiers["TIER_4"]["floors"]["confidence"])
        self.assertFalse(model["floor_change_performed"])
        self.assertFalse(model["autonomy_enabled"])

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
        evidence = model["autonomy_specific_evidence"]
        self.assertEqual(evidence["autonomous_trigger_evidence"]["status"], "BLOCKED")
        self.assertEqual(evidence["autonomy_confidence_evidence"]["status"], "FLOORS_NOT_MET")
        self.assertIn("autonomy_confidence_floor_evidence_missing", evidence["current_missing_evidence"])
        self.assertLess(evidence["autonomy_specific_evidence_score"], 100)
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

    def test_event_consumer_readonly_certifies_preview_lifecycle_without_apply(self):
        decision_surface = {
            "users_by_ip": {
                "10.0.0.3": {
                    "user": "10.0.0.3",
                    "current_channel": "awg3",
                    "recommended_channel": "wireguard-1779454504-c43409",
                    "confidence": 0.91,
                    "trust": 88.0,
                    "prediction": {"confidence": 0.82},
                    "risk": 2.0,
                    "recommendation_hash": "rec-event-1",
                    "source_hash": "source-event-1",
                },
            },
            "batch_preview": {
                "users_to_move": [
                    {
                        "user": "10.0.0.3",
                        "from": "awg3",
                        "to": "wireguard-1779454504-c43409",
                        "confidence": 0.91,
                        "risk": 2.0,
                        "recommendation_hash": "rec-event-1",
                    },
                ],
            },
            "snapshot_statuses": {
                "service-scores": {"status": "OK", "validation_ok": True, "freshness_state": "FRESH", "stop_required": False},
                "trust-summaries": {"status": "OK", "validation_ok": True, "freshness_state": "FRESH", "stop_required": False},
                "prediction-summaries": {"status": "OK", "validation_ok": True, "freshness_state": "FRESH", "stop_required": False},
            },
        }

        first = pipeline.event_consumer_readonly_certification_model(
            events=[
                {
                    "source": "service_matrix",
                    "channel": "awg3",
                    "message": "Telegram failed",
                    "updated_at": "2026-06-23T00:00:00Z",
                    "confidence": 0.91,
                }
            ],
            decision_surface=decision_surface,
            now="2026-06-23T00:01:00Z",
        )
        rebuilt = pipeline.event_consumer_readonly_certification_model(
            events=list(first["event_consumer"]["events"]),
            decision_surface=dict(decision_surface),
            now="2026-06-23T00:02:00Z",
        )

        self.assertEqual(first["final_verdict"], "EVENT_CONSUMER_CERTIFIED")
        self.assertTrue(first["event_consumer_certified"])
        self.assertTrue(all(row["ready"] for row in first["chain_completeness"]))
        self.assertEqual(first["event_consumer"]["planner_preview_event_count"], 1)
        self.assertEqual(first["planner_preview"]["candidate_count"], 1)
        self.assertTrue(first["packet_preview"]["would_prepare_packet"])
        self.assertEqual(first["restore_barrier_preview"]["readiness"], "READY_FOR_REVIEW")
        self.assertEqual(first["rollback_preview"]["rollback_decision"], "ROLLBACK_NOT_REQUIRED_IN_SIMULATION")
        self.assertTrue(first["feedback_preview"]["preview_only"])
        self.assertTrue(first["learning_preview"]["preview_only"])
        self.assertTrue(first["learning_preview"]["observed_outcome_primary"])
        self.assertFalse(first["apply_executed"])
        self.assertEqual(first["users_moved"], 0)
        self.assertFalse(first["autonomy_enabled"])
        self.assertFalse(first["synthetic_events_created"])
        self.assertFalse(first["synthetic_evidence_created"])
        self.assertEqual(
            first["event_consumer"]["events"][0]["event_id"],
            rebuilt["event_consumer"]["events"][0]["event_id"],
        )

    def test_governed_canary_cycle_reaches_authority_boundary_with_low_autonomy_floors(self):
        decision_surface = self.governed_canary_surface()

        cycle = pipeline.governed_canary_knowledge_gated_dry_run_cycle(
            events=[],
            decision_surface=decision_surface,
            max_users=1,
            now="2026-06-24T16:00:00Z",
        )
        rebuilt = pipeline.governed_canary_knowledge_gated_dry_run_cycle(
            events=[],
            decision_surface=decision_surface,
            max_users=1,
            now="2026-06-24T16:00:00Z",
        )

        self.assertEqual(cycle["stop_reason"], "AUTHORITY_BOUNDARY")
        self.assertEqual(cycle["event_source"], "CURRENT_STATE_PREVIEW")
        self.assertEqual(cycle["target"], "awg0")
        self.assertEqual(cycle["candidate"]["user"], "10.7.0.5")
        self.assertEqual(cycle["packet_preview"]["status"], "PACKET_PREVIEW_READY")
        dry_run_generation = (((cycle["dry_run"].get("safety") or {}).get("generation") or {}).get("planner_generation_id") or "")
        if dry_run_generation:
            self.assertEqual(cycle["packet_preview"]["authority_generation"], dry_run_generation)
        else:
            self.assertTrue(cycle["packet_preview"]["authority_generation"])
        self.assertIn("source_hashes", cycle["packet_preview"])
        self.assertIn("snapshot_bundle_hash", cycle["packet_preview"])
        self.assertEqual(cycle["restore_status"]["status"], "RESTORE_AND_ROLLBACK_PREVIEW_READY")
        self.assertEqual(cycle["verification_plan"]["status"], "VERIFICATION_PLAN_READY")
        self.assertEqual(cycle["outcome_closure_plan"]["status"], "OUTCOME_CLOSURE_PLAN_READY")
        self.assertEqual(cycle["learning_path"]["status"], "LEARNING_PATH_CONNECTED")
        self.assertEqual(cycle["next_action"], "EXPLICIT_OPERATOR_APPROVAL_REQUIRED_FOR_THIS_PACKET")
        self.assertFalse(cycle["manual_prompting_required_before_boundary"])
        self.assertFalse(cycle["non_authority_stop_requires_fix"])
        self.assertEqual(cycle["final_verdict"], "AUTONOMOUS_DRY_RUN_CYCLE_REACHES_AUTHORITY_BOUNDARY")
        approval_prompt = cycle["approval_prompt"]
        self.assertEqual(approval_prompt["status"], "APPROVAL_PROMPT_READY")
        self.assertEqual(approval_prompt["packet_preview_id"], cycle["packet_preview"]["packet_id"])
        self.assertEqual(approval_prompt["operation_id"], cycle["packet_preview"]["operation_id"])
        self.assertEqual(approval_prompt["selected_move_hash"], cycle["packet_preview"]["selected_move_hash"])
        self.assertEqual(approval_prompt["user"], "10.7.0.5")
        self.assertEqual(approval_prompt["current_channel"], "vless")
        self.assertEqual(approval_prompt["target_channel"], "awg0")
        self.assertEqual(approval_prompt["rollback_target"], "vless")
        self.assertEqual(
            approval_prompt["rollback_manifest_id"],
            cycle["packet_preview"]["rollback_manifest_preview"]["rollback_manifest_id"],
        )
        self.assertEqual(approval_prompt["authority_tier"], cycle["decision"]["authority_tier"])
        self.assertEqual(approval_prompt["authority_status"], cycle["decision"]["authority_status"])
        self.assertIn("execute this exact governed packet", approval_prompt["allowed_action"])
        self.assertIn("move any other user", approval_prompt["forbidden_actions"])
        self.assertIn(cycle["packet_preview"]["packet_id"], approval_prompt["approval_command_text"])
        self.assertIn(cycle["packet_preview"]["operation_id"], approval_prompt["approval_command_text"])
        self.assertIn(cycle["packet_preview"]["selected_move_hash"], approval_prompt["approval_command_text"])
        self.assertFalse(approval_prompt["runtime_mutation_performed"])
        self.assertFalse(approval_prompt["restore_barrier_written_now"])
        self.assertFalse(approval_prompt["apply_executed"])
        self.assertEqual(approval_prompt["users_moved"], 0)
        break_glass = cycle["break_glass_authority_policy"]
        self.assertEqual(break_glass["schema_version"], "v7.c3-break-glass-authority-policy.v1")
        self.assertEqual(break_glass["policy_status"], "DEFINED_NOT_APPROVED_FOR_RUNTIME")
        self.assertEqual(
            break_glass["omp_output"]["c3_status"],
            "DONE_READ_ONLY_AUDITED_EXCEPTIONAL_OPERATOR_POLICY",
        )
        self.assertTrue(break_glass["definition"]["operator_policy_approval_required"])
        self.assertEqual(break_glass["definition"]["default_state"], "DISABLED")
        self.assertEqual(break_glass["definition"]["runtime_apply_permission"], "NOT_GRANTED")
        self.assertIn("probabilistic suspicion alone", break_glass["forbidden_triggers"])
        self.assertIn("Runtime apply enablement", break_glass["forbidden_effects"])
        self.assertIn("user movement without exact approved packet", break_glass["forbidden_effects"])
        self.assertFalse(break_glass["safety"]["break_glass_authority_granted_now"])
        self.assertFalse(break_glass["safety"]["runtime_apply_allowed_now"])
        self.assertFalse(break_glass["safety"]["automation_enabled"])
        self.assertFalse(break_glass["safety"]["authority_expanded"])
        self.assertEqual(break_glass["safety"]["users_moved"], 0)
        action_class = cycle["action_class_runtime_enablement"]
        self.assertEqual(action_class["schema_version"], "v7.action-class-runtime-enablement-preview.v1")
        self.assertEqual(action_class["current_action_class"], "single-user governed candidate failover")
        self.assertEqual(action_class["current_state"], "GOVERNED_ONLY")
        self.assertEqual(action_class["next_promotion_target"], "CERTIFIED_FOR_CLASS_APPROVAL")
        self.assertEqual(action_class["runtime_must_stop_at"], "AUTHORITY_BOUNDARY")
        self.assertFalse(action_class["runtime_can_execute_automatically"])
        self.assertFalse(action_class["runtime_apply_allowed_now"])
        self.assertEqual(action_class["packet_to_action_class_mapping"]["packet_id"], cycle["packet_preview"]["packet_id"])
        self.assertEqual(action_class["packet_to_action_class_mapping"]["operation_id"], cycle["packet_preview"]["operation_id"])
        self.assertEqual(action_class["packet_to_action_class_mapping"]["selected_move_hash"], cycle["packet_preview"]["selected_move_hash"])
        self.assertEqual(action_class["packet_to_action_class_mapping"]["subject"], ["10.7.0.5"])
        self.assertEqual(action_class["packet_to_action_class_mapping"]["target"], ["awg0"])
        self.assertFalse(action_class["authority_to_action_class_mapping"]["authority_expansion_performed"])
        self.assertFalse(action_class["runtime_mutation_performed"])
        self.assertFalse(action_class["restore_barrier_written_now"])
        self.assertFalse(action_class["apply_executed"])
        self.assertEqual(action_class["users_moved"], 0)
        self.assertFalse(action_class["authority_expanded"])
        self.assertFalse(action_class["new_planner_created"])
        self.assertFalse(action_class["new_governance_created"])
        self.assertFalse(action_class["new_execution_path_created"])
        self.assertFalse(action_class["new_truth_source_created"])
        self.assertFalse(cycle["safety"]["apply_executed"])
        self.assertEqual(cycle["safety"]["users_moved"], 0)
        self.assertFalse(cycle["safety"]["autonomy_enabled"])
        self.assertTrue(all(row["runtime_mutation_performed"] is False for row in cycle["cycle_steps"]))
        lifecycle = cycle["runtime_lifecycle_preview"]
        for field in [
            "lifecycle_id",
            "decision_id",
            "operation_id",
            "packet_id",
            "idempotency_key_fingerprint",
            "current_state_generation",
            "selected_move_hash",
            "runtime_stage",
            "stage_owner",
            "input_generation",
            "stop_reason",
            "authority_status",
            "packet_freshness",
            "duplicate_work_status",
            "loop_guard_status",
            "verification_status",
            "rollback_status",
            "outcome_status",
            "learning_status",
            "omp_notification_status",
        ]:
            self.assertIn(field, lifecycle)
        self.assertEqual(lifecycle["schema_version"], "v7.runtime-lifecycle-preview.v1")
        self.assertEqual(lifecycle["runtime_stage"], "AUTHORITY_CHECKED")
        self.assertEqual(lifecycle["stage_owner"], "OMP")
        self.assertEqual(lifecycle["stop_reason"], "AUTHORITY_BOUNDARY")
        self.assertEqual(lifecycle["packet_freshness"], "PACKET_PREVIEW_READY_CURRENT_INPUT")
        self.assertEqual(lifecycle["verification_status"], "VERIFICATION_PLAN_READY")
        self.assertEqual(lifecycle["rollback_status"], "RESTORE_AND_ROLLBACK_PREVIEW_READY")
        self.assertEqual(lifecycle["outcome_status"], "OUTCOME_CLOSURE_PLAN_READY")
        self.assertEqual(lifecycle["learning_status"], "LEARNING_PATH_CONNECTED")
        self.assertEqual(lifecycle["omp_notification_status"], "READY_TO_NOTIFY_OMP_WITH_STOP")
        self.assertEqual(lifecycle["duplicate_work_status"], "NO_DUPLICATE_WORK_DETECTED_READ_ONLY")
        self.assertEqual(lifecycle["loop_guard_status"], "NO_LOOP_DETECTED_READ_ONLY")
        self.assertEqual(lifecycle["operation_id"], cycle["packet_preview"]["operation_id"])
        self.assertEqual(lifecycle["packet_id"], cycle["packet_preview"]["packet_id"])
        self.assertEqual(lifecycle["selected_move_hash"], cycle["packet_preview"]["selected_move_hash"])
        self.assertEqual(
            lifecycle["idempotency_key_fingerprint"],
            rebuilt["runtime_lifecycle_preview"]["idempotency_key_fingerprint"],
        )
        self.assertFalse(lifecycle["runtime_mutation_performed"])
        self.assertFalse(lifecycle["restore_barrier_written_now"])
        self.assertFalse(lifecycle["apply_executed"])
        self.assertEqual(lifecycle["users_moved"], 0)
        self.assertFalse(lifecycle["rollback_executed"])
        self.assertFalse(lifecycle["learning_written_now"])

    def test_governed_canary_changed_packet_emits_fresh_approval_prompt(self):
        first = pipeline.governed_canary_knowledge_gated_dry_run_cycle(
            decision_surface=self.governed_canary_surface(target="awg0", recommendation_hash="rec-canary-1"),
            max_users=1,
            now="2026-06-24T16:00:00Z",
        )
        changed = pipeline.governed_canary_knowledge_gated_dry_run_cycle(
            decision_surface=self.governed_canary_surface(target="awg3", recommendation_hash="rec-canary-2", source_hash="source-canary-2"),
            max_users=1,
            now="2026-06-24T16:00:00Z",
        )

        self.assertEqual(first["stop_reason"], "AUTHORITY_BOUNDARY")
        self.assertEqual(changed["stop_reason"], "AUTHORITY_BOUNDARY")
        self.assertEqual(first["approval_prompt"]["status"], "APPROVAL_PROMPT_READY")
        self.assertEqual(changed["approval_prompt"]["status"], "APPROVAL_PROMPT_READY")
        self.assertNotEqual(first["packet_preview"]["packet_id"], changed["packet_preview"]["packet_id"])
        self.assertNotEqual(first["packet_preview"]["selected_move_hash"], changed["packet_preview"]["selected_move_hash"])
        self.assertNotEqual(first["approval_prompt"]["approval_command_text"], changed["approval_prompt"]["approval_command_text"])
        self.assertNotIn(first["packet_preview"]["packet_id"], changed["approval_prompt"]["approval_command_text"])
        self.assertIn(changed["packet_preview"]["packet_id"], changed["approval_prompt"]["approval_command_text"])
        self.assertEqual(changed["approval_prompt"]["target_channel"], "awg3")

    def test_same_semantic_governed_decision_keeps_committed_decision_id_when_packet_changes(self):
        first = pipeline.governed_canary_knowledge_gated_dry_run_cycle(
            decision_surface=self.governed_canary_surface(target="awg0", recommendation_hash="rec-canary-1", source_hash="source-canary-1"),
            max_users=1,
            now="2026-06-24T16:00:00Z",
        )
        refreshed = pipeline.governed_canary_knowledge_gated_dry_run_cycle(
            decision_surface=self.governed_canary_surface(target="awg0", recommendation_hash="rec-canary-2", source_hash="source-canary-2"),
            max_users=1,
            now="2026-06-24T16:02:00Z",
        )

        self.assertNotEqual(first["packet_preview"]["packet_id"], refreshed["packet_preview"]["packet_id"])
        self.assertEqual(first["candidate"]["candidate_hash"], refreshed["candidate"]["candidate_hash"])
        self.assertEqual(first["packet_preview"]["selected_move_hash"], refreshed["packet_preview"]["selected_move_hash"])
        self.assertEqual(first["packet_preview"]["decision_id"], refreshed["packet_preview"]["decision_id"])
        self.assertEqual(first["packet_preview"]["decision_commit"]["status"], "DECISION_COMMITTED")
        self.assertFalse(first["packet_preview"]["decision_commit"]["commit_is_execution_authority"])
        self.assertFalse(first["packet_preview"]["decision_commit"]["runtime_mutation_performed"])
        self.assertFalse(first["packet_preview"]["decision_commit"]["apply_executed"])
        self.assertEqual(first["packet_preview"]["decision_commit"]["users_moved"], 0)

    def test_material_governed_decision_change_creates_different_committed_decision_id(self):
        first = pipeline.governed_canary_knowledge_gated_dry_run_cycle(
            decision_surface=self.governed_canary_surface(target="awg0", recommendation_hash="rec-canary-1"),
            max_users=1,
            now="2026-06-24T16:00:00Z",
        )
        changed = pipeline.governed_canary_knowledge_gated_dry_run_cycle(
            decision_surface=self.governed_canary_surface(target="awg3", recommendation_hash="rec-canary-1"),
            max_users=1,
            now="2026-06-24T16:00:00Z",
        )

        self.assertNotEqual(first["packet_preview"]["selected_move_hash"], changed["packet_preview"]["selected_move_hash"])
        self.assertNotEqual(first["candidate"]["candidate_hash"], changed["candidate"]["candidate_hash"])
        self.assertNotEqual(first["packet_preview"]["decision_id"], changed["packet_preview"]["decision_id"])

    def test_committed_preview_cli_lease_creation_does_not_rerun_planner_selection(self):
        cycle = pipeline.governed_canary_knowledge_gated_dry_run_cycle(
            decision_surface=self.governed_canary_surface(target="awg0", recommendation_hash="rec-canary-1"),
            max_users=1,
            now="2026-06-24T16:00:00Z",
        )
        preview = cycle["packet_preview"]
        rollback_item = preview["rollback_manifest_preview"]["items"][0]
        tool = ROOT / "tools" / "v7-governed-canary-dry-run-cycle"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            preview_file = root / "preview.json"
            lease_file = root / "lease.json"
            preview_file.write_text(json.dumps({"packet_preview": preview}), encoding="utf-8")
            proc = subprocess.run(
                [
                    sys.executable,
                    str(tool),
                    "--create-execution-lease",
                    "--committed-preview-file",
                    str(preview_file),
                    "--execution-lease-file",
                    str(lease_file),
                    "--approved-packet-id",
                    preview["packet_id"],
                    "--approved-decision-id",
                    preview["decision_id"],
                    "--approved-operation-id",
                    preview["operation_id"],
                    "--approved-selected-move-hash",
                    preview["selected_move_hash"],
                    "--approved-user",
                    "10.7.0.5",
                    "--approved-source",
                    rollback_item["rollback_target"],
                    "--approved-target",
                    rollback_item["forward_target"],
                    "--approved-authority-generation",
                    preview["authority_generation"],
                    "--approved-source-bundle-hash",
                    preview["source_bundle_hash"],
                    "--approved-source-hashes-hash",
                    preview["source_bundle_hash"],
                    "--approved-snapshot-bundle-hash",
                    preview["snapshot_bundle_hash"],
                ],
                capture_output=True,
                text=True,
                timeout=20,
            )

            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            payload = json.loads(proc.stdout)
            self.assertTrue(payload["committed_preview_consumed"])
            self.assertFalse(payload["planner_rerun_before_lease"])
            self.assertFalse(payload["candidate_selection_rerun"])
            self.assertEqual(payload["execution_lease_create_result"]["verdict"], "EXECUTION_LEASE_WRITTEN")
            self.assertTrue(lease_file.exists())

    def test_execution_lease_blocks_planner_regeneration_when_plan_is_semantically_identical(self):
        first = pipeline.governed_canary_knowledge_gated_dry_run_cycle(
            decision_surface=self.governed_canary_surface(target="awg0", recommendation_hash="rec-canary-1"),
            max_users=1,
            now="2026-06-24T16:00:00Z",
        )
        lease = operator_execution.create_execution_lease_from_preview(
            first["packet_preview"],
            approval_author="operator-a",
            approval_reviewer="operator-b",
        )
        refreshed = pipeline.governed_canary_knowledge_gated_dry_run_cycle(
            decision_surface=self.governed_canary_surface(target="awg0", recommendation_hash="rec-canary-2", source_hash="source-canary-2"),
            execution_lease=lease,
            max_users=1,
            now="2026-06-24T16:01:00Z",
        )

        self.assertTrue(refreshed["execution_lease"]["active"])
        self.assertEqual(refreshed["packet_preview"]["packet_id"], first["packet_preview"]["packet_id"])
        self.assertEqual(refreshed["packet_preview"]["selected_move_hash"], first["packet_preview"]["selected_move_hash"])
        self.assertEqual(refreshed["packet_preview"]["allowed_targets"], ["awg0"])
        self.assertEqual(refreshed["approval_prompt"]["target_channel"], "awg0")
        self.assertFalse(refreshed["execution_lease"]["material_state_change"])
        self.assertEqual(refreshed["execution_lease"]["lease_keep_reason"], "no_material_state_change")
        self.assertTrue(refreshed["packet_preview"]["planner_regeneration_blocked_by_execution_lease"])
        self.assertTrue(refreshed["safety"]["planner_regeneration_blocked_by_execution_lease"])

    def test_execution_lease_invalidates_when_planner_target_changes_materially(self):
        first = pipeline.governed_canary_knowledge_gated_dry_run_cycle(
            decision_surface=self.governed_canary_surface(target="awg0", recommendation_hash="rec-canary-1"),
            max_users=1,
            now="2026-06-24T16:00:00Z",
        )
        lease = operator_execution.create_execution_lease_from_preview(
            first["packet_preview"],
            approval_author="operator-a",
            approval_reviewer="operator-b",
        )
        refreshed = pipeline.governed_canary_knowledge_gated_dry_run_cycle(
            decision_surface=self.governed_canary_surface(target="awg3", recommendation_hash="rec-canary-2", source_hash="source-canary-2"),
            execution_lease=lease,
            max_users=1,
            now="2026-06-24T16:01:00Z",
        )

        self.assertFalse(refreshed["execution_lease"]["active"])
        self.assertTrue(refreshed["execution_lease"]["material_state_change"])
        self.assertIn("target_channel", refreshed["execution_lease"]["changed_fields"])
        self.assertEqual(refreshed["packet_preview"]["allowed_targets"], ["awg3"])
        self.assertEqual(refreshed["approval_prompt"]["target_channel"], "awg3")

    def test_governed_canary_cycle_fails_non_authority_snapshot_stop(self):
        decision_surface = {
            "users_by_ip": {
                "10.7.0.5": {
                    "user": "10.7.0.5",
                    "current_channel": "vless",
                    "recommended_channel": "awg0",
                    "confidence": 0.9,
                    "trust": 90,
                    "prediction": {"confidence": 0.9},
                    "risk": 1.0,
                },
            },
            "batch_preview": {
                "users_to_move": [{"user": "10.7.0.5", "from": "vless", "to": "awg0", "confidence": 0.9}],
            },
            "snapshot_statuses": {
                "service-scores": {
                    "status": "STALE",
                    "validation_ok": False,
                    "freshness_state": "STALE",
                    "stop_required": True,
                    "validation_errors": ["source_hash_mismatch:service-scores:service_matrix"],
                },
            },
        }

        cycle = pipeline.governed_canary_knowledge_gated_dry_run_cycle(
            decision_surface=decision_surface,
            max_users=1,
        )

        self.assertEqual(cycle["stop_reason"], "MISSING_STATE_TRANSITION")
        self.assertTrue(cycle["non_authority_stop_requires_fix"])
        self.assertEqual(cycle["next_action"], "FIX_EXISTING_OWNER_GAP_AND_RERUN")
        self.assertEqual(cycle["final_verdict"], "AUTONOMOUS_DRY_RUN_CYCLE_BLOCKED")
        self.assertEqual(cycle["approval_prompt"]["status"], "NOT_EMITTED")
        self.assertNotIn("approval_command_text", cycle["approval_prompt"])
        self.assertFalse(cycle["safety"]["apply_executed"])
        self.assertEqual(cycle["safety"]["users_moved"], 0)
        self.assertFalse(cycle["approval_prompt"]["runtime_mutation_performed"])
        self.assertFalse(cycle["approval_prompt"]["restore_barrier_written_now"])
        self.assertFalse(cycle["approval_prompt"]["apply_executed"])
        self.assertEqual(cycle["approval_prompt"]["users_moved"], 0)

    def test_governed_canary_no_approval_prompt_for_unsafe_implementation_stop(self):
        cycle = pipeline.governed_canary_knowledge_gated_dry_run_cycle(
            decision_surface={
                "users_by_ip": {
                    "10.7.0.5": {
                        "user": "10.7.0.5",
                        "current_channel": "vless",
                        "recommended_channel": "awg0",
                        "confidence": 0.9,
                        "trust": 90,
                        "prediction": {"confidence": 0.9},
                        "risk": 1.0,
                    },
                },
                "batch_preview": {
                    "users_to_move": [{"user": "10.7.0.5", "from": "vless", "to": "awg0", "confidence": 0.9}],
                },
                "snapshot_statuses": {
                    "service-scores": {
                        "status": "STALE",
                        "validation_ok": False,
                        "freshness_state": "STALE",
                        "stop_required": True,
                        "validation_errors": ["source_hash_mismatch:service-scores:service_matrix"],
                    },
                },
            },
            max_users=1,
        )

        self.assertNotEqual(cycle["stop_reason"], "AUTHORITY_BOUNDARY")
        self.assertEqual(cycle["approval_prompt"]["status"], "NOT_EMITTED")
        self.assertNotIn("approval_command_text", cycle["approval_prompt"])
        self.assertFalse(cycle["approval_prompt"]["runtime_mutation_performed"])
        self.assertFalse(cycle["approval_prompt"]["apply_executed"])
        self.assertEqual(cycle["approval_prompt"]["users_moved"], 0)


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
                "trust_evolution_advice": {
                    "available": True,
                    "live_calibrated": True,
                    "candidate_outcomes_count": 22,
                    "prediction_actuals_count": 22,
                    "service_actuals_count": 22,
                    "governed_evidence_score": 100,
                    "inherited_execution_trust": 82,
                    "autonomy_specific_gap_score": 45,
                    "autonomy_boundary_cap": "OPERATOR_APPROVAL_READY",
                    "approval_autonomy_review_ready": True,
                    "bounded_autonomy_blockers": ["autonomous_trigger_not_certified"],
                    "operator_summary_ru": "Governed-история учитывается, автономия отдельно заблокирована.",
                },
                "snapshot_statuses": {"service-scores": {"status": "OK"}},
            }
        )

        self.assertIn("autonomous_dry_run", dashboard)
        trust = dashboard["trust_status"]
        self.assertEqual(trust["governed_evidence_score"], 100)
        self.assertEqual(trust["inherited_execution_trust"], 82)
        self.assertEqual(trust["autonomy_boundary_cap"], "OPERATOR_APPROVAL_READY")
        self.assertTrue(trust["approval_autonomy_review_ready"])
        self.assertIn("autonomous_trigger_not_certified", trust["bounded_autonomy_blockers"])
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
        self.assertIn("Пакет review", source)
        self.assertIn("operator_review_packet", source)
        self.assertIn("comparison_growth_projection", source)
        self.assertIn("read_jsonl_family_records(SHADOW_AUTONOMY_LOG_FILE", source)
        self.assertIn("COMPARISON_RECORD_TYPE", source)
        self.assertIn("Несогласия", source)
        self.assertIn("Переход к автономии", source)
        self.assertIn("inherited", source)
        self.assertIn("Governed-история учитывается", source)
        self.assertIn("Доказательства автономии", source)
        self.assertIn("Trigger:", source)
        self.assertNotIn("/api/actions/execution-apply", source)


if __name__ == "__main__":
    unittest.main()
