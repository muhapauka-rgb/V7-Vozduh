# BLOCK P4.B First Controlled Runtime Action Specification Report

Project: V7 Vozduh
Program: P4
Block: P4.B
Mode: Architecture / Specification / Safety Design

## 1. Reality Audit

Created: `P4B_REALITY_AUDIT.md`

Existing operator execution validation, runtime recheck, replay protection, append-only audit records, governance records, dry-run verification, approval preview, governance preview and rehearsal preview were found and marked for reuse.

## 2. Conflict Audit

Created: `P4B_IMPLEMENTATION_CONFLICT_AUDIT.md`

Equivalent functionality exists. P4.B specifies compatibility with existing operator execution concepts and creates no parallel packet, approval, replay, audit, governance, rollback or verification system.

## 3. Truth Source Audit

Created: `P4B_TRUTH_SOURCE_AUDIT.md`

No truth-source conflict requires stopping. P4.B files are specifications only.

## 4. Runtime Audit

Created: `P4B_RUNTIME_AUDIT.md`

The packet must freeze users registry hash, egress registry hash, selected moves hash/count, runtime snapshot hash, dry-run ids, health/capacity/trust refs, action design hash, rollback preview and observation refs.

## 5. Action Packet Spec

Created: `P4B_ACTION_PACKET_SPEC.md`

Specified `P4B_ZERO_MOVE_GOVERNANCE_ACTION_PACKET`, compatible with `e22.operator-execution-packet.v1`, using `ZERO_MOVEMENT_GENERATION_CLEARANCE_RECHECK` and `ZERO_MOVE_GOVERNANCE_STATE_TRANSITION`.

## 6. Approval Spec

Created: `P4B_APPROVAL_SPEC.md`

Specified approval text, exact scope, 900-second TTL, invalidation, renewal and rejection.

## 7. Runtime Recheck Spec

Created: `P4B_PREACTION_RECHECK_SPEC.md`

Specified exact recheck algorithm for schema, action, constraints, dual approval, expiry, hashes, health, capacity, trust, candidate/action validity, dry-run verification, rollback preview and observation availability.

## 8. Abort Spec

Created: `P4B_ABORT_SPEC.md`

Specified abort matrix with condition, detection, severity, reason, operator message and recovery path.

## 9. Rollback Preview Spec

Created: `P4B_ROLLBACK_PREVIEW_SPEC.md`

Rollback preview is `COMPENSATING_GOVERNANCE_RECORD_ONLY`; no rollback execution.

## 10. Observation Spec

Created: `P4B_OBSERVATION_SPEC.md`

Specified before, during, after and verification checkpoints, evidence collection and retention.

## 11. Replay Protection

Created: `P4B_REPLAY_PROTECTION_SPEC.md`

Specified replay, duplicate, expired packet and hash mismatch detection.

## 12. Fail Closed Certification

Created: `P4B_FAIL_CLOSED_CERTIFICATION.md`

Unknown, missing, stale, expired, invalid, mismatched, replay, blocked, duplicate, degraded and inconclusive states all abort.

## 13. Admin Surface Spec

Created: `P4B_ADMIN_SURFACE_SPEC.md`

Use existing Execution Drawer, Approval Center, Checks, Logs, Operator, Dry-Run Verification and Rollback Preview surfaces. No new top-level section.

## 14. Action Readiness

Created: `P4B_ACTION_READINESS_REVIEW.md`

Status: `READY_WITH_BLOCKERS`

First Controlled Runtime Action Certification may begin.

## 15. Remaining Risks

- Current compatible schema name is `e22.operator-execution-packet.v1`; P4.C should decide whether to retain it or define a wrapper.
- Current validator checks core hashes and selected moves; health/capacity/trust/dry-run verification checks need certification before implementation.
- A future implementation must avoid accidentally enabling broader runtime action modes.
- UI must not expose execute/apply controls during certification.

## 16. Recommendation For P4.C

Proceed to First Controlled Runtime Action Certification.

P4.C should certify this specification against existing code, define test cases, confirm no execution authority, and decide whether the existing `admin_core/operator_execution.py` path is sufficient for a later implementation block.

P4.C must not execute the action unless a later prompt explicitly authorizes implementation and execution.

## Required Verdicts

`reality_audit_complete=true`

`implementation_conflict_audit_complete=true`

`truth_source_audit_complete=true`

`runtime_audit_complete=true`

`action_packet_spec_complete=true`

`approval_spec_complete=true`

`preaction_recheck_complete=true`

`abort_spec_complete=true`

`rollback_preview_complete=true`

`observation_spec_complete=true`

`replay_protection_complete=true`

`fail_closed_certified=true`

`safe_to_continue_to_first_controlled_runtime_action_certification=true`

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

P4.B specification complete.

Action implementation was not started.

