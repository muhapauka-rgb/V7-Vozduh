"""Routing Brain advisory integration for V7.

The brain connects RI.1 intelligence models to planner-facing advice without
owning runtime decisions. Runtime Planner decides, Governance authorizes,
Runtime executes, Audit/Closure record.
"""

from __future__ import annotations

import statistics
from time import perf_counter as time_perf
from dataclasses import dataclass, field
from typing import Any

from admin_core.routing_intelligence import (
    DynamicBlastRadiusModel,
    ExecutionTrustModel,
    PredictiveFoundation,
    ServiceHistoryStore,
    ServiceIntelligenceEngine,
    UserServiceWeights,
    as_float,
    clamp,
    normalize_services,
)


ROUTING_BRAIN_SCHEMA = "ri2.routing-brain-advisory.v1"
RI3_CANDIDATE_ADVISORY_SCHEMA = "ri3.candidate-advisory-score.v1"
FEEDBACK_SCHEMA = "ri2.routing-brain-feedback.v1"
HISTORY_WINDOWS = ("1h", "24h", "7d", "30d")
HISTORY_WINDOW_WEIGHTS = {
    "1h": 0.40,
    "24h": 0.30,
    "7d": 0.20,
    "30d": 0.10,
}


ADVISORY_CONTRACT = {
    "schema_version": "ri3.intelligence-advisory-contract.v1",
    "may_output": [
        "service_suitability_advice",
        "user_service_weight_advice",
        "degradation_trend_advice",
        "execution_trust_advice",
        "dynamic_blast_radius_advice",
        "candidate_explanation_advice",
        "candidate_ranking_score_part",
        "service_history_score",
        "weighted_service_score",
        "execution_trust_score",
        "service_confidence_score",
        "degradation_risk_score",
    ],
    "may_not": [
        "move_users",
        "bypass_planner",
        "bypass_governance",
        "write_selected_moves_directly",
        "approve_execution",
        "mutate_runtime_state",
    ],
    "decision_owners": {
        "routing_intelligence": "advice_only",
        "runtime_planner": "final_routing_decision_owner",
        "governance": "execution_authorization_owner",
        "runtime": "execution_owner",
        "audit_closure": "record_owner",
    },
    "planner_influence_rules": {
        "scope": "eligible_candidates_only",
        "score_part": "bounded_advisory_input",
        "may_create_candidates": False,
        "may_change_hard_gates": False,
        "may_change_reservation": False,
        "may_change_governance": False,
        "may_change_runtime_execution": False,
    },
}


ROUTING_BRAIN_MAP = [
    {"stage": "raw_runtime_data", "owner": "runtime_truth_files", "classification": "REUSE"},
    {"stage": "service_history", "owner": "RI.1 ServiceHistoryStore", "classification": "EXTEND"},
    {"stage": "service_intelligence", "owner": "RI.1 ServiceIntelligenceEngine", "classification": "EXTEND"},
    {"stage": "user_service_weights", "owner": "RI.1 UserServiceWeights", "classification": "EXTEND"},
    {"stage": "service_suitability", "owner": "runtime_planner_decision / RI_advice", "classification": "MERGE_AS_ADVICE"},
    {"stage": "execution_trust", "owner": "RI.1 ExecutionTrustModel", "classification": "EXTEND"},
    {"stage": "dynamic_blast_radius_recommendation", "owner": "RI.1 DynamicBlastRadiusModel", "classification": "EXTEND_AS_ADVICE"},
    {"stage": "planner_advisory_context", "owner": "RI.2 RoutingBrain", "classification": "EXTEND"},
    {"stage": "runtime_planner", "owner": "tools/v7-users-autoswitch", "classification": "EXTEND_RANKING_ONLY"},
    {"stage": "governance_packet", "owner": "operator/governance modules", "classification": "DO_NOT_TOUCH"},
    {"stage": "execution", "owner": "runtime execution tools", "classification": "DO_NOT_TOUCH"},
    {"stage": "audit", "owner": "audit/operation stores", "classification": "REUSE_AS_FEEDBACK_INPUT"},
    {"stage": "closure", "owner": "closure workflow", "classification": "REUSE_AS_FEEDBACK_INPUT"},
    {"stage": "history_feedback", "owner": "RI feedback envelope", "classification": "DEFINE_ONLY"},
]


def routing_brain_map() -> dict[str, Any]:
    return {
        "schema_version": "ri2.routing-brain-map.v1",
        "chain": ROUTING_BRAIN_MAP,
        "contract": ADVISORY_CONTRACT,
        "single_source_of_truth": {
            "runtime_truth": "existing runtime state files",
            "routing_decision": "runtime planner",
            "execution_authorization": "governance",
            "runtime_execution": "runtime execution tools",
            "history_feedback": "audit/closure/service health as inputs, no autonomous learning",
        },
    }


@dataclass
class RoutingBrain:
    service_matrix: dict[str, Any] = field(default_factory=dict)
    quality_summary: dict[str, Any] = field(default_factory=dict)
    service_preferences: dict[str, Any] = field(default_factory=dict)
    audit_records: list[dict[str, Any]] = field(default_factory=list)

    def candidate_advisory_scores(
        self,
        *,
        total_users: int,
        affected_users: int,
        required_services: list[str] | None = None,
        user_id: str = "",
        candidate_targets: list[str] | None = None,
    ) -> dict[str, Any]:
        """Return bounded advisory score parts for planner ranking.

        This contract intentionally has no candidate creation, selected-move,
        approval, apply, or runtime mutation fields. The planner may consume the
        bounded `score_part` only after its own hard gates mark a candidate
        eligible.
        """
        started = time_perf()
        required = normalize_services(required_services or self.service_preferences.get("required_services") or [])
        targets = [str(item) for item in (candidate_targets or []) if str(item)]
        history = ServiceHistoryStore.from_runtime_inputs(self.service_matrix, self.quality_summary)
        weights = UserServiceWeights.from_service_preferences(self.service_preferences, required)
        user_weights = weights.for_user(user_id, required) if user_id else weights.defaults
        engine = ServiceIntelligenceEngine(history)
        trust = ExecutionTrustModel.from_records(self.audit_records)
        trust_score = clamp(as_float(trust.get("score")), 0.0, 100.0)
        target_scores: dict[str, Any] = {}

        for target in targets:
            unweighted_windows: dict[str, Any] = {}
            weighted_windows: dict[str, Any] = {}
            service_history_score = 0.0
            weighted_service_score = 0.0
            confidence_values: list[float] = []
            one_hour_weighted = 0.0
            baseline_values: list[float] = []

            for window in HISTORY_WINDOWS:
                window_weight = HISTORY_WINDOW_WEIGHTS.get(window, 0.0)
                unweighted = engine.score_target(target, required_services=required, window=window)
                weighted = engine.score_target(
                    target,
                    required_services=required,
                    service_weights=user_weights,
                    window=window,
                )
                unweighted_score = clamp(as_float(unweighted.get("aggregate_score")), 0.0, 100.0)
                weighted_score = clamp(as_float(weighted.get("aggregate_score")), 0.0, 100.0)
                service_history_score += unweighted_score * window_weight
                weighted_service_score += weighted_score * window_weight
                unweighted_windows[window] = unweighted
                weighted_windows[window] = weighted
                if window == "1h":
                    one_hour_weighted = weighted_score
                else:
                    baseline_values.append(weighted_score)
                for row in weighted.get("per_service", []):
                    confidence_values.append(clamp(as_float(row.get("confidence")), 0.0, 1.0))

            service_confidence_score = statistics.mean(confidence_values) * 100.0 if confidence_values else 0.0
            baseline = statistics.mean(baseline_values) if baseline_values else one_hour_weighted
            degradation_delta = max(0.0, baseline - one_hour_weighted)
            degradation_risk = clamp(
                ((100.0 - weighted_service_score) * 0.45)
                + (degradation_delta * 0.35)
                + ((100.0 - service_confidence_score) * 0.20)
            )
            advisory_score = clamp(
                (service_history_score * 0.25)
                + (weighted_service_score * 0.35)
                + (trust_score * 0.15)
                + (service_confidence_score * 0.15)
                + ((100.0 - degradation_risk) * 0.10)
            )
            score_part = round((advisory_score - 50.0) * 2.0, 3)
            score_part = round(max(-100.0, min(100.0, score_part)), 3)
            recommendation = "neutral"
            if score_part >= 25:
                recommendation = "prefer"
            elif score_part <= -25:
                recommendation = "deprioritize"
            target_scores[target] = {
                "schema_version": RI3_CANDIDATE_ADVISORY_SCHEMA,
                "target": target,
                "score_part": score_part,
                "advisory_score": round(advisory_score, 3),
                "service_history_score": round(service_history_score, 3),
                "weighted_service_score": round(weighted_service_score, 3),
                "execution_trust_score": round(trust_score, 3),
                "service_confidence_score": round(service_confidence_score, 3),
                "degradation_risk_score": round(degradation_risk, 3),
                "recommendation": recommendation,
                "windows": {
                    "unweighted": {
                        window: {
                            "aggregate_score": unweighted_windows[window].get("aggregate_score", 0.0),
                            "verdict": unweighted_windows[window].get("verdict", "UNKNOWN"),
                        }
                        for window in HISTORY_WINDOWS
                    },
                    "weighted": {
                        window: {
                            "aggregate_score": weighted_windows[window].get("aggregate_score", 0.0),
                            "verdict": weighted_windows[window].get("verdict", "UNKNOWN"),
                        }
                        for window in HISTORY_WINDOWS
                    },
                },
                "user_service_weights": user_weights,
                "explainability": [
                    f"service_history_score={round(service_history_score, 3)}",
                    f"weighted_service_score={round(weighted_service_score, 3)}",
                    f"execution_trust_score={round(trust_score, 3)}",
                    f"service_confidence_score={round(service_confidence_score, 3)}",
                    f"degradation_risk_score={round(degradation_risk, 3)}",
                    "planner_may_use_score_part_only_after_candidate_is_eligible",
                ],
                "authority": {
                    "routing_intelligence": "advice_only",
                    "candidate_creation": "forbidden",
                    "hard_gate_override": "forbidden",
                    "governance_authority": "none",
                    "runtime_execution_authority": "none",
                },
            }

        aggregate_scores = [as_float(row.get("advisory_score")) for row in target_scores.values()]
        service_risk = clamp(100.0 - (statistics.mean(aggregate_scores) if aggregate_scores else 0.0))
        platform_health = clamp(statistics.mean(aggregate_scores) if aggregate_scores else 0.0)
        blast = DynamicBlastRadiusModel.recommend(
            total_users=total_users,
            affected_users=affected_users,
            execution_trust=trust_score,
            service_risk=service_risk,
            platform_health=platform_health,
        )
        elapsed = round((time_perf() - started) * 1000.0, 3)
        return {
            "schema_version": "ri3.candidate-advisory-scores.v1",
            "mode": "planner_ranking_advice",
            "planner_influence_active": True,
            "planner_decision_owner": "tools/v7-users-autoswitch",
            "execution_authority": "none",
            "selected_moves_write_authority": "none",
            "contract": ADVISORY_CONTRACT,
            "candidate_scores": target_scores,
            "execution_trust": trust,
            "dynamic_blast_radius_advice": blast,
            "performance": {
                "candidate_count": len(targets),
                "history_windows": list(HISTORY_WINDOWS),
                "latency_ms": elapsed,
                "runtime_path": "planner_in_process_bounded_read_model",
            },
        }

    def advisory_context(
        self,
        *,
        total_users: int,
        affected_users: int,
        required_services: list[str] | None = None,
        user_id: str = "",
        candidate_targets: list[str] | None = None,
        window: str = "1h",
    ) -> dict[str, Any]:
        required = normalize_services(required_services or self.service_preferences.get("required_services") or [])
        history = ServiceHistoryStore.from_runtime_inputs(self.service_matrix, self.quality_summary)
        weights = UserServiceWeights.from_service_preferences(self.service_preferences, required)
        user_weights = weights.for_user(user_id, required) if user_id else weights.defaults
        engine = ServiceIntelligenceEngine(history)
        all_scores = engine.score_all_targets(required_services=required, service_weights=user_weights, window=window)
        if candidate_targets:
            wanted = {str(item) for item in candidate_targets}
            service_scores = {target: score for target, score in all_scores.items() if target in wanted}
        else:
            service_scores = all_scores
        aggregate_scores = [as_float(row.get("aggregate_score")) for row in service_scores.values()]
        confidences = [
            as_float(service.get("confidence"))
            for row in service_scores.values()
            for service in row.get("per_service", [])
        ]
        service_history_score = statistics.mean(aggregate_scores) if aggregate_scores else 0.0
        intelligence_confidence = statistics.mean(confidences) if confidences else 0.0
        trust = ExecutionTrustModel.from_records(self.audit_records)
        service_risk = clamp(100.0 - service_history_score)
        platform_health = clamp(service_history_score)
        blast = DynamicBlastRadiusModel.recommend(
            total_users=total_users,
            affected_users=affected_users,
            execution_trust=as_float(trust.get("score")),
            service_risk=service_risk,
            platform_health=platform_health,
        )
        prediction = PredictiveFoundation.analyze_service_trends(history)
        return {
            "schema_version": ROUTING_BRAIN_SCHEMA,
            "mode": "planner_advisory_context",
            "intelligence_present": bool(self.service_matrix or self.quality_summary or self.service_preferences or self.audit_records),
            "intelligence_confidence": round(clamp(intelligence_confidence, 0.0, 1.0), 3),
            "service_history_score": round(clamp(service_history_score), 3),
            "weighted_service_score": round(clamp(service_history_score), 3),
            "execution_trust_score": trust.get("score", 0.0),
            "recommended_blast_radius": blast.get("recommended_budget", 0),
            "intelligence_used_for_explanation": True,
            "planner_influence_active": False,
            "planner_decision_owner": "tools/v7-users-autoswitch",
            "execution_authority": "none",
            "selected_moves_write_authority": "none",
            "authority": {
                "routing_intelligence": "advice_only",
                "planner_decision_owner": "tools/v7-users-autoswitch",
                "governance_authority": "unchanged",
                "execution_authority": "none",
                "selected_moves_write_authority": "none",
            },
            "contract": ADVISORY_CONTRACT,
            "service_scores": service_scores,
            "user_service_weights": user_weights,
            "execution_trust": trust,
            "dynamic_blast_radius_advice": blast,
            "predictive_foundation": {
                "prediction_enabled": prediction.get("prediction_enabled", False),
                "examples": prediction.get("examples", [])[:25],
            },
        }

    @staticmethod
    def feedback_envelope(
        *,
        operation_result: dict[str, Any] | None = None,
        rollback_result: dict[str, Any] | None = None,
        audit_result: dict[str, Any] | None = None,
        closure_result: dict[str, Any] | None = None,
        service_health_after: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return {
            "schema_version": FEEDBACK_SCHEMA,
            "mode": "feedback_definition_only",
            "autonomous_learning_enabled": False,
            "runtime_state_mutation": False,
            "feeds": {
                "execution_result": operation_result or {},
                "rollback_result": rollback_result or {},
                "audit_result": audit_result or {},
                "closure_result": closure_result or {},
                "service_health_after_movement": service_health_after or {},
            },
            "future_inputs": [
                "ServiceHistoryStore",
                "ExecutionTrustModel",
                "DynamicBlastRadiusModel",
            ],
        }
