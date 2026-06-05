"""Canonical governed execution pipeline contracts for operator movement.

This module is intentionally pure. It defines the contract, lifecycle, and
decision/action matrix that bridge recommendations to the existing governed
execution owner. It does not invoke shell commands or write runtime state.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any


SCHEMA_VERSION = "v7.operator-governed-execution-pipeline.v1"
CANONICAL_PLANNER = "tools/v7-users-autoswitch"
CANONICAL_PACKET_OWNER = "admin_core/operator_execution.py"
CANONICAL_PACKET_TOOL = "tools/v7-operator-execution-packet"
CANONICAL_RUNTIME_EXECUTOR = "tools/v7-users-autoswitch --apply --verify"
CANONICAL_ROLLBACK_EXECUTOR = "tools/v7-users-autoswitch --rollback-packet --apply --verify"

REQUIRED_RECOMMENDATION_FIELDS = [
    "user",
    "current_channel",
    "recommended_channel",
    "confidence",
    "trust",
    "prediction",
    "risk",
    "rollback_plan",
    "snapshot_generation",
    "source_hashes",
    "reason_summary",
]

EXECUTION_STATES = [
    "EXECUTION_READY",
    "EXECUTION_BLOCKED",
    "EXECUTION_RUNNING",
    "EXECUTION_SUCCESS",
    "EXECUTION_PARTIAL",
    "EXECUTION_FAILED",
    "ROLLBACK_REQUIRED",
    "ROLLBACK_RUNNING",
    "ROLLBACK_SUCCESS",
    "ROLLBACK_FAILED",
]


def stable_hash(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def recommendation_execution_contract(row: dict[str, Any]) -> dict[str, Any]:
    """Convert an operator recommendation row into an execution candidate.

    The returned candidate is not executable by itself. It is the canonical
    payload that must be turned into an approval packet and then consumed by the
    existing restore-barrier/governed apply chain.
    """
    user = str(row.get("user") or row.get("ip") or "")
    current = str(row.get("current_channel") or row.get("current") or "")
    target = str(row.get("recommended_channel") or row.get("target") or "")
    source_hashes = {
        "recommendation_hash": str(row.get("recommendation_hash") or ""),
        "source_hash": str(row.get("source_hash") or ""),
    }
    candidate = {
        "schema_version": "v7.recommendation-execution-candidate.v1",
        "user": user,
        "current_channel": current,
        "recommended_channel": target,
        "confidence": row.get("confidence", 0.0),
        "trust": row.get("trust", 0.0),
        "prediction": row.get("prediction") if isinstance(row.get("prediction"), dict) else {},
        "risk": row.get("risk", 0.0),
        "rollback_plan": {
            "required": True,
            "rollback_target": current,
            "owner": CANONICAL_PACKET_OWNER,
            "executor": CANONICAL_ROLLBACK_EXECUTOR,
        },
        "snapshot_generation": {
            "required": True,
            "fresh_execution_time_recheck_required": True,
            "restore_barrier_required": True,
        },
        "source_hashes": source_hashes,
        "reason_summary": list(row.get("reasons") or [])[:8],
        "approval_packet_required": True,
        "execution_candidate": bool(user and current and target and current != target),
        "execution_allowed_now": False,
        "runtime_mutation_performed": False,
        "next_required_state": "APPROVAL_PACKET_REQUIRED",
    }
    candidate["candidate_hash"] = stable_hash({
        "user": user,
        "current_channel": current,
        "recommended_channel": target,
        "source_hashes": source_hashes,
    })[:24]
    return candidate


def approval_packet_lifecycle() -> list[dict[str, Any]]:
    return [
        {
            "state": "PACKET_CREATED",
            "condition": "operator selects a recommendation or batch preview",
            "decision": "create approval packet candidate",
            "action": "generate packet from canonical recommendation contract",
            "executor": CANONICAL_PACKET_TOOL,
            "trigger": "operator explicit approval intent",
            "evidence": ["packet json", "candidate hash", "source hashes"],
            "blocked_actions": ["runtime apply", "direct user-switch"],
            "next_state": "PACKET_VALIDATING",
        },
        {
            "state": "PACKET_VALIDATING",
            "condition": "packet exists and has dual approval metadata",
            "decision": "validate schema, ttl, budget, rollback manifest and selected move hash",
            "action": "run packet validation and execution-time recheck",
            "executor": CANONICAL_PACKET_OWNER,
            "trigger": "packet submit",
            "evidence": ["validation result", "recheck result", "audit record"],
            "blocked_actions": ["runtime apply when invalid", "restore barrier write when mismatch"],
            "next_state": "PACKET_APPROVED" ,
        },
        {
            "state": "PACKET_REJECTED",
            "condition": "packet invalid, expired, replayed, mismatched, or manually rejected",
            "decision": "deny execution",
            "action": "write denial audit and closure",
            "executor": CANONICAL_PACKET_OWNER,
            "trigger": "validation failure or operator rejection",
            "evidence": ["denial audit", "closure record", "reason list"],
            "blocked_actions": ["restore barrier write", "runtime apply", "rollback execution"],
            "next_state": "EXECUTION_BLOCKED",
        },
        {
            "state": "PACKET_APPROVED",
            "condition": "dual approval, valid ttl, matching generation and rollback manifest",
            "decision": "create restore-barrier clearance only",
            "action": "write generation-bound restore-barrier clearance",
            "executor": CANONICAL_PACKET_OWNER,
            "trigger": "approved packet runtime action",
            "evidence": ["restore barrier clearance", "rollback binding", "execution readiness closure"],
            "blocked_actions": ["direct user-switch", "apply without fresh recheck"],
            "next_state": "EXECUTION_READY",
        },
        {
            "state": "PACKET_EXECUTED",
            "condition": "fresh recheck passes and governed apply succeeds",
            "decision": "verify and close execution",
            "action": "write audit, outcome, trust input, prediction input and recommendation quality input",
            "executor": CANONICAL_RUNTIME_EXECUTOR,
            "trigger": "separate approved governed apply invocation",
            "evidence": ["apply result", "verification result", "audit", "closure"],
            "blocked_actions": ["replay apply", "unbounded batch continuation"],
            "next_state": "EXECUTION_SUCCESS",
        },
    ]


def execution_recheck_policy() -> dict[str, Any]:
    return {
        "schema_version": "v7.execution-recheck-policy.v1",
        "immediate_before_execution": [
            "production_truth",
            "snapshot_gate",
            "current_channel",
            "target_channel",
            "health",
            "capacity",
            "prediction",
            "trust",
            "restore_barrier",
            "rollback_packet",
        ],
        "if_any_mismatch": "STOP_EXECUTION",
        "evidence": ["truth check", "snapshot hashes", "selected move hash", "rollback packet hash"],
        "runtime_mutation_before_pass": False,
    }


def governed_apply_policy() -> dict[str, Any]:
    return {
        "schema_version": "v7.governed-apply-policy.v1",
        "executor": CANONICAL_RUNTIME_EXECUTOR,
        "who_may_invoke": ["approved operator execution owner", "future bounded autonomy via same owner only"],
        "required_before_invoke": [
            "approval packet valid",
            "restore barrier clearance active",
            "rollback packet bound",
            "fresh execution-time recheck PASS",
            "audit path available",
            "closure path available",
        ],
        "blocks_execution": [
            "missing packet",
            "expired packet",
            "stale production truth",
            "snapshot mismatch",
            "current channel mismatch",
            "capacity or health blocker",
            "trust or prediction blocker",
            "restore barrier mismatch",
            "rollback packet missing",
            "direct user-switch attempt",
        ],
    }


def verification_policy() -> dict[str, Any]:
    return {
        "schema_version": "v7.execution-verification-policy.v1",
        "verify_after_execution": [
            "channel_changed",
            "route_healthy",
            "services_healthy",
            "risk_acceptable",
            "prediction_outcome",
            "trust_impact",
        ],
        "results": {
            "success": "write success audit, closure, trust positive input, prediction quality input",
            "partial_success": "stop further moves, write partial audit, require operator review",
            "failure": "write failure audit and evaluate rollback_required",
            "rollback_required": "enter ROLLBACK_REQUIRED and execute rollback policy only",
        },
    }


def rollback_policy() -> dict[str, Any]:
    return {
        "schema_version": "v7.rollback-policy.v1",
        "rollback_trigger": ["verification failure", "partial execution outside tolerance", "operator stop", "service health regression"],
        "rollback_authority": CANONICAL_PACKET_OWNER,
        "rollback_executor": CANONICAL_ROLLBACK_EXECUTOR,
        "required_before_rollback": ["rollback packet valid", "rollback target still known", "audit path available"],
        "verification": ["channel restored", "route healthy", "services recovered", "closure written"],
        "blocked_actions": ["ad hoc v7-user-switch rollback", "rollback without packet", "second rollback owner"],
    }


def execution_action_matrix() -> list[dict[str, Any]]:
    rows = {
        "EXECUTION_READY": ("approved packet and fresh recheck pass", "execute or wait", "invoke governed apply only", CANONICAL_RUNTIME_EXECUTOR, "operator approved apply", "readiness closure", ["direct user-switch"], "EXECUTION_RUNNING"),
        "EXECUTION_BLOCKED": ("any required gate unknown or failed", "stop", "write denial/closure and surface blockers", CANONICAL_PACKET_OWNER, "gate failure", "denial audit", ["apply", "direct user-switch"], "PACKET_REJECTED"),
        "EXECUTION_RUNNING": ("governed apply started", "monitor", "collect runtime result and verification data", CANONICAL_RUNTIME_EXECUTOR, "apply process active", "apply log", ["second apply", "new packet"], "EXECUTION_SUCCESS"),
        "EXECUTION_SUCCESS": ("movement verified and services healthy", "close success", "write audit, closure, trust and prediction inputs", CANONICAL_PACKET_OWNER, "verification pass", "success closure", ["rollback unless new incident"], "CLOSED"),
        "EXECUTION_PARTIAL": ("some moves verified and some uncertain", "contain", "stop remaining moves and require operator review", CANONICAL_PACKET_OWNER, "verification partial", "partial audit", ["continue batch"], "ROLLBACK_REQUIRED"),
        "EXECUTION_FAILED": ("apply failed or verification failed", "evaluate rollback", "write failure audit and bind rollback packet", CANONICAL_PACKET_OWNER, "verification failure", "failure audit", ["new apply"], "ROLLBACK_REQUIRED"),
        "ROLLBACK_REQUIRED": ("rollback trigger true", "rollback", "validate rollback packet", CANONICAL_PACKET_OWNER, "rollback decision", "rollback readiness", ["ad hoc rollback"], "ROLLBACK_RUNNING"),
        "ROLLBACK_RUNNING": ("rollback packet executing", "monitor", "run governed rollback executor and verify", CANONICAL_ROLLBACK_EXECUTOR, "approved rollback", "rollback log", ["forward apply"], "ROLLBACK_SUCCESS"),
        "ROLLBACK_SUCCESS": ("rollback verified", "close rollback", "write rollback success audit and closure", CANONICAL_PACKET_OWNER, "rollback verification pass", "rollback closure", ["replay rollback"], "CLOSED"),
        "ROLLBACK_FAILED": ("rollback failed or unverifiable", "escalate", "write blocker, freeze further movement and require manual incident handling", CANONICAL_PACKET_OWNER, "rollback verification failure", "incident blocker", ["all future apply"], "BLOCKER"),
    }
    keys = ["condition", "decision", "action", "executor", "trigger", "written_evidence", "blocked_actions", "next_state"]
    return [{"state": state, **dict(zip(keys, values))} for state, values in rows.items()]


def audit_closure_certification() -> dict[str, Any]:
    return {
        "schema_version": "v7.audit-closure-certification.v1",
        "required_for_every_state": ["audit", "evidence", "closure", "outcome", "trust input", "prediction input", "recommendation quality input"],
        "certified_existing_writers": [CANONICAL_PACKET_OWNER, "admin/v7-admin-api audit_admin for blocked attempts"],
        "gap": "final runtime apply outcome must append trust/prediction/recommendation quality records when governed apply is enabled",
    }


def batch_execution_governance_model() -> dict[str, Any]:
    return {
        "schema_version": "v7.batch-execution-governance-model.v1",
        "batch_preview": "read-only from operator decision surface",
        "blast_radius": "must be bounded by packet selected_move_budget",
        "approval": "dual approval required",
        "execution": "same governed apply path, no batch-specific executor",
        "verification": "per-user and aggregate verification",
        "rollback": "operation-scoped rollback packet for every selected move",
        "audit": "one operation audit plus per-user evidence",
        "closure": "success, partial, failure, or rollback closure",
        "execution_allowed_now": False,
    }


def autonomy_execution_integration_model() -> dict[str, Any]:
    return {
        "schema_version": "v7.autonomy-execution-integration-model.v1",
        "required_answer": "Autonomy must call existing governed execution path.",
        "forbidden": "Autonomy must not create a second execution system.",
        "integration": [
            "autonomy may produce recommendation candidates only",
            "same approval packet schema",
            "same execution-time recheck",
            "same restore barrier",
            "same rollback packet",
            "same governed apply",
            "same audit and closure",
        ],
    }


def direct_user_switch_blocker(user: str, target: str, actor: str = "") -> dict[str, Any]:
    return {
        "action": "user_switch",
        "status": "blocked",
        "error": "governed_execution_pipeline_required",
        "message": "Direct user movement is disabled. Use recommendation approval packet and governed apply.",
        "user": user,
        "target": target,
        "actor": actor,
        "execution_allowed_now": False,
        "runtime_mutation_performed": False,
        "users_moved": False,
        "autoswitch_apply_run": False,
        "required_path": [
            "recommendation",
            "approval_packet",
            "execution_time_recheck",
            "restore_barrier",
            "rollback_packet",
            "governance",
            "v7-users-autoswitch --apply --verify",
            "verification",
            "audit",
            "closure",
        ],
    }


def pipeline_certification() -> dict[str, Any]:
    matrix = execution_action_matrix()
    return {
        "schema_version": SCHEMA_VERSION,
        "single_execution_path": {
            "planner": CANONICAL_PLANNER,
            "approval_packet": CANONICAL_PACKET_TOOL,
            "packet_owner": CANONICAL_PACKET_OWNER,
            "runtime_apply": CANONICAL_RUNTIME_EXECUTOR,
            "rollback": CANONICAL_ROLLBACK_EXECUTOR,
            "direct_user_switch_allowed": False,
        },
        "recommendation_execution_contract": REQUIRED_RECOMMENDATION_FIELDS,
        "approval_packet_lifecycle": approval_packet_lifecycle(),
        "execution_recheck_policy": execution_recheck_policy(),
        "governed_apply_policy": governed_apply_policy(),
        "verification_policy": verification_policy(),
        "rollback_policy": rollback_policy(),
        "execution_action_matrix": matrix,
        "audit_closure_certification": audit_closure_certification(),
        "batch_execution_governance_model": batch_execution_governance_model(),
        "autonomy_execution_integration_model": autonomy_execution_integration_model(),
        "duplication_audit": {
            "second_execution_path_created": False,
            "second_planner_created": False,
            "second_governance_created": False,
            "second_rollback_created": False,
            "second_approval_system_created": False,
            "second_truth_source_created": False,
        },
        "final_verdicts": {
            "single_execution_path_certified": True,
            "recommendation_execution_contract_defined": True,
            "approval_packet_lifecycle_defined": True,
            "execution_recheck_defined": True,
            "governed_apply_policy_defined": True,
            "verification_policy_defined": True,
            "rollback_policy_defined": True,
            "execution_action_matrix_complete": all(
                all(key in row and row[key] not in ("", [], None) for key in [
                    "condition",
                    "decision",
                    "action",
                    "executor",
                    "trigger",
                    "written_evidence",
                    "blocked_actions",
                    "next_state",
                ])
                for row in matrix
            ),
            "audit_closure_certified": True,
            "operator_approval_ready": False,
            "bounded_autonomy_ready": False,
            "production_autonomy_ready": False,
            "new_truth_sources_created": False,
            "duplicate_systems_created": False,
            "runtime_mutation_performed": False,
            "users_moved": False,
            "autoswitch_apply_run": False,
            "SAFE_NEXT_STEP": "implement_operator_packet_creation_ui_and_final_apply_outcome_feedback",
        },
    }
