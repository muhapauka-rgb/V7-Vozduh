"""Routing Brain advisory integration for V7.

The brain connects RI.1 intelligence models to planner-facing advice without
owning runtime decisions. Runtime Planner decides, Governance authorizes,
Runtime executes, Audit/Closure record.
"""

from __future__ import annotations

import statistics
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
FEEDBACK_SCHEMA = "ri2.routing-brain-feedback.v1"


ADVISORY_CONTRACT = {
    "schema_version": "ri2.intelligence-advisory-contract.v1",
    "may_output": [
        "service_suitability_advice",
        "user_service_weight_advice",
        "degradation_trend_advice",
        "execution_trust_advice",
        "dynamic_blast_radius_advice",
        "candidate_explanation_advice",
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
    {"stage": "runtime_planner", "owner": "tools/v7-users-autoswitch", "classification": "DO_NOT_TOUCH_DECISION_LOGIC"},
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
