# BLOCK P4.A First Controlled Runtime Action Design Report

Project: V7 Vozduh
Program: P4
Block: P4.A
Mode: Architecture / Discovery / Action Design

## 1. Reality Audit

Created: `P4A_REALITY_AUDIT.md`

Existing operator execution, approval center, execution contracts, candidate workflow, readiness, dry-run, verification, rollback preview, governance preview, rehearsal preview and packet concepts were found and classified for reuse.

## 2. Conflict Audit

Created: `P4A_IMPLEMENTATION_CONFLICT_AUDIT.md`

Equivalent governance and packet functionality already exists. P4.A does not create a parallel packet system, execution engine, rollback executor, verification store or approval queue.

## 3. Truth Source Audit

Created: `P4A_TRUTH_SOURCE_AUDIT.md`

No truth-source conflict requires stopping. P4.A documents are design references only.

## 4. Runtime Audit

Created: `P4A_RUNTIME_AUDIT.md`

The first action must trust fresh runtime state, registry hashes, empty selected moves, health, capacity, trust, candidate/action validity, dry-run verification, rollback preview and audit/event observability.

## 5. First Action Candidate Review

Created: `P4A_FIRST_ACTION_CANDIDATE_REVIEW.md`

Selected first action:

`ZERO_MOVE_GOVERNANCE_STATE_TRANSITION`

This is an append-only governed runtime marker with zero user movement, zero route change, zero autoswitch apply, zero rollback execution, zero deploy and zero systemd change.

## 6. Action Scope

Created: `P4A_ACTION_SCOPE_MODEL.md`

Scope: `runtime_governance.zero_move_state_transition`

Blast radius: governance/audit record only.

## 7. Action Packet Design

Created: `P4A_ACTION_PACKET_DESIGN.md`

Packet design reuses existing approval id, packet id, operation id, approvals, TTL, expected hashes, rollback manifest, runtime recheck, replay denial and audit append concepts.

## 8. Approval Design

Created: `P4A_APPROVAL_DESIGN.md`

Requires independent `approval_author` and `approval_reviewer`, short TTL, invalidation on changed facts, and re-approval on any invalidation.

## 9. Runtime Recheck

Created: `P4A_PREACTION_RECHECK.md`

Immediate pre-action recheck aborts on any changed, stale, missing, invalid, expired, mismatched or unknown state.

## 10. Abort Matrix

Created: `P4A_ABORT_MATRIX.md`

Abort matrix covers packet expiry, approval conflicts, registry mismatches, selected moves, health, capacity, trust, scope, dry-run verification, rollback preview, observation and replay.

## 11. Rollback Preview

Created: `P4A_ROLLBACK_PREVIEW_DESIGN.md`

Rollback for the selected first action is a compensating append-only governance record. No rollback execution is performed or designed for P4.A.

## 12. Observation Plan

Created: `P4A_OBSERVATION_PLAN.md`

Observation covers before/during/after checkpoints, replay denial, unchanged runtime facts and bounded existing retention.

## 13. Admin Surface

Created: `P4A_ADMIN_SURFACE_REVIEW.md`

Use existing Execution Drawer, Approval Center, Checks, Logs and Operator surfaces. No new top-level section.

## 14. Fail Closed Certification

Created: `P4A_FAIL_CLOSED_CERTIFICATION.md`

Unknown, missing, stale, expired, mismatched, invalid, inconclusive, blocked, replayed or widened scope states all abort.

## 15. Readiness Review

Created: `P4A_READINESS_REVIEW.md`

Status: `READY_WITH_BLOCKERS`

First Controlled Runtime Action Specification can begin.

## 16. Remaining Risks

- Future implementation could bypass the existing operator execution validator.
- A governance marker could be over-described as traffic-affecting runtime success.
- Append-only compensation must be clearly presented as compensation, not deletion.
- UI controls could accidentally expose execute/apply too early.
- Runtime action authority remains uncertified until a later explicit block.

## 17. Recommendation For P4.B

Proceed to First Controlled Runtime Action Specification.

P4.B should specify the exact packet schema, exact expected hashes, exact approval text, exact recheck algorithm, exact append-only governance record, exact replay denial test, exact observation evidence, and exact fail-closed tests.

P4.B must still avoid execution unless explicitly authorized.

## Required Verdicts

`reality_audit_complete=true`

`implementation_conflict_audit_complete=true`

`truth_source_audit_complete=true`

`runtime_audit_complete=true`

`first_action_candidate_defined=true`

`action_scope_defined=true`

`action_packet_defined=true`

`approval_defined=true`

`preaction_recheck_defined=true`

`abort_matrix_defined=true`

`rollback_preview_defined=true`

`observation_plan_defined=true`

`fail_closed_certified=true`

`safe_to_continue_to_first_controlled_runtime_action_specification=true`

## Safety Verdict

`runtime_mutation_performed=false`

`routing_changed=false`

`users_moved=false`

`autoswitch_apply_run=false`

`rollback_executed=false`

`execution_engine_implemented=false`

`runtime_hooks_with_authority=false`

`deploy_performed=false`

`systemd_changed=false`

## Stop Condition

P4.A design complete.

Action implementation was not started.

