# PROGRAM Z6.5 Gate 0 State Discovery

Project: V7 Vozduh
Program: Z6.5 - Runtime Operation Lifecycle Design
Mode: READ ONLY
Date: 2026-06-02

## Constraint

Lifecycle semantics only. No implementation, APIs, storage, runtime mutations, deploy, autoswitch apply, user movement, routing mutation, service restart, systemd/timer modification, cleanup, merge, or force push.

## Ownership Anchors Reused

| Area | Owner |
|---|---|
| Runtime owner | `tools/v7-users-autoswitch` |
| Scheduler | `systemd/v7-users-autoswitch.timer/service` |
| Audit owner | `tools/runtime-support/v7-audit-log` |
| Closure owner | `admin/v7-admin-api` + `admin_core/operator_observability.py` |
| Existing partial orchestrator | `tools/v7-users-autoswitch` |

## Existing State Concepts

| State / Concept Set | Values | Where Used | Owner | Purpose | Status |
|---|---|---|---|---|---|
| Execution contract statuses | `DRAFT`, `PRECHECKED`, `APPROVED`, `SCHEDULED`, `VALIDATED`, `RECHECKED`, `EXECUTING`, `VERIFYING`, `OBSERVING`, `ROLLBACK_READY`, `ROLLING_BACK`, `COMPLETED`, `FAILED_CLOSED`, `ROLLED_BACK`, `REPLAY_DENIED`, `CANCELLED`, `EXPIRED` | `admin/v7-admin-api` execution contract model | Admin read model | Preview execution lifecycle vocabulary | REUSE / EXTEND |
| Execution event types | `EXECUTION_CREATED`, `EXECUTION_CONTRACT_CREATED`, `EXECUTION_VALIDATED`, `EXECUTION_STARTED`, `EXECUTION_COMPLETED`, `EXECUTION_FAILED`, `VERIFICATION_STARTED`, `VERIFICATION_COMPLETED`, `VERIFICATION_FAILED`, `ROLLBACK_CREATED`, `ROLLBACK_STARTED`, `ROLLBACK_COMPLETED`, `ROLLBACK_FAILED`, `REPLAY_DENIED` | `admin/v7-admin-api` execution event model | Admin read model | Event vocabulary for execution and rollback | REUSE / EXTEND |
| Closure states | `OPEN`, `VERIFIED`, `CLOSED`, `EXPIRED` | Admin closure model | Admin/operator closure owner | Closure lifecycle | REUSE |
| Freshness states | `FRESH`, `STALE`, `EXPIRED`, `UNKNOWN` | Admin operational metadata | Admin read model | Evidence freshness, not operation terminal state | REUSE as metadata |
| Evidence statuses | `OPEN`, `OBSERVING`, `VERIFIED`, `CLOSED`, `STALE` | Evidence bundle model | Admin evidence model | Evidence state | REUSE as evidence only |
| Proposal statuses | `DRAFT`, `OBSERVED`, `ACTIVE`, `REVIEW_REQUIRED`, `EXPIRED`, `SUPERSEDED`, `CLOSED` | Proposal model | Admin proposal/read model | Proposal lifecycle, not runtime execution | REUSE as pre-operation input |
| Gate/check statuses | `PASS`, `FAIL`, `REVIEW_REQUIRED`, `UNKNOWN`, plus `READY`, `READY_WITH_REVIEW`, `NOT_READY`, `BLOCKED` | Admin execution gates/candidates/readiness | Admin read model | Validation/admission evidence | REUSE as gate result, not operation terminal |
| Operator execution verdicts | `PACKET_VALID`, `DENY_PACKET_INVALID`, `DENY_STALE_RUNTIME`, `DENY_HASH_MISMATCH`, `ALLOW_RECORD_ONLY`, `DENY_REPLAY`, `DENY_RUNTIME_ACTION_UNSUPPORTED` | `admin_core/operator_execution.py` | Operator execution support | Zero-move packet validation/recheck verdicts | REUSE as supporting verdicts |
| Autoswitch apply result | `applied=false` with reasons `dry_run`, `autoswitch_disabled_by_policy`, `mode_observe_blocks_apply`, `no_selected_moves`; or `applied=true` with per-move `rc`, `verify_rc`, `rollback_rc` | `tools/v7-users-autoswitch` | Runtime owner | Runtime outcome from plan/apply | REUSE / EXTEND |
| Restore barrier statuses | active, expired, cleared, post-TTL blocking, generation clearance ok/fail, budget exceeded, selected-move hash/count mismatch | `tools/v7-users-autoswitch`, Admin adapters, restore-settle evidence | Runtime owner + Admin visibility | Runtime execution blocker/admission condition | REUSE |
| Historical operation states | `HISTORICAL`, `SAFE`, `CONDITIONAL`, `BLOCKED`, `STALE`, report-specific statuses | `admin_core/operator_observability.py` | Operator observability | Historical timeline/read-only evidence | REUSE as historical evidence |

## Gate 0 Classification

| Lifecycle Concept | Classification | Reason |
|---|---|---|
| Execution contract status vocabulary | REUSE / EXTEND | Strongest existing operation-state vocabulary, but currently preview/read-only. |
| Closure state vocabulary | REUSE | Existing closure truth model; keep distinct from runtime terminal state. |
| Proposal status vocabulary | REUSE | Pre-operation proposal input, not runtime operation state. |
| Evidence status vocabulary | REUSE | Evidence lifecycle only. |
| Gate/check statuses | REUSE | Admission/readiness checks only. |
| Autoswitch apply result reasons | REUSE / EXTEND | Runtime owner outcome source; must map into operation lifecycle. |
| Operator execution verdicts | REUSE | Supporting runtime recheck/governance verdicts, not global lifecycle states. |
| Historical report states | DO NOT TOUCH / REUSE AS EVIDENCE | Historical lineage, not active lifecycle truth. |
| New duplicate state vocabulary | REPLACE = NO | Forbidden by Z6.5; target states must derive from existing concepts. |

