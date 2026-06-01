# BLOCK P6.A - First User Movement Design Report

Project: V7 Vozduh

Program: P6

Block: P6.A

Mode: Architecture / Discovery / User Movement Design

## 1. Reality Audit

P6.A found existing movement, preview, readiness, verification, rollback, and packet concepts.

Core reusable sources:

- `tools/v7-route-movement-preview`
- `tools/v7-users-autoswitch`
- `tools/v7-second-canary-target-readiness`
- `admin_core/operator_execution.py`
- historical bounded movement packets in `docs/track7/productization/e24-evidence`, `e27_2-evidence`, and `e28_2-evidence`

No parallel movement system was created.

## 2. Conflict Audit

Equivalent movement logic exists and must be reused or extended later.

P6.A did not implement an execution engine, runtime hook, autoswitch apply path, routing apply path, or new packet system.

## 3. Truth Source Audit

Canonical runtime truth:

`/opt/v7/egress/state`

Canonical movement design facts:

- user truth: `users.registry`
- channel truth: `egress.registry`
- selected moves truth: selected-move files or empty canonical hash
- capacity truth: `egress-load-summary.json`
- trust truth: trusted RU state files
- preview truth: `v7-route-movement-preview`
- readiness truth: `v7-second-canary-target-readiness`

No truth-source conflict was found.

## 4. Runtime Audit

Fresh runtime facts:

- users registry hash: `07362c9aa6f959be2ab06f26928692c6844f37a3bd266be8de4e56193f6d9a9f`
- egress registry hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- selected moves count: `0`
- selected moves hash: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
- runtime snapshot hash: `ec11fffc70bf63d04dd76b723e415692b4be371ec007ec0df638fc5ecb216c84`
- capacity status: `ok`
- admin health: `OK`
- autoswitch timer: `inactive`

## 5. User Candidate Review

Selected user:

`10.7.0.11`

Current state:

- current egress: `1`
- route table: `1009`
- enabled: true

Reason:

This is the lowest-risk single-user candidate because it is the existing canary default, currently on the rollback target, has a dedicated table, and has historical governed movement/rollback evidence.

## 6. Channel Candidate Review

Selected destination:

`amneziawg-exec-20260528-10-8-1-14`

Destination state:

- interface: `v7execwg0`
- current users: `0`
- role: `EXECUTION_ONLY`
- manual_only: `1`
- reserve_only: `1`
- autoswitch_allowed: false
- rebalance_allowed: false
- reservation_owner: `operator_execution_governance`

Readiness output:

- candidate_still_valid: true
- selected_target: `amneziawg-exec-20260528-10-8-1-14`
- approval_status: `GO`
- second_canary_readiness: `GO`
- runtime_commands_executed: false

## 7. Movement Domain

Designed movement:

`10.7.0.11: 1 -> amneziawg-exec-20260528-10-8-1-14`

Rollback:

`10.7.0.11 -> 1`

Scope:

- one user
- one target
- one route table
- fully observable
- fully reversible
- fully auditable

## 8. Movement Packet

Future packet should reuse existing bounded movement packet fields:

- movement_budget: `1`
- allowed_users: `["10.7.0.11"]`
- allowed_targets: `["amneziawg-exec-20260528-10-8-1-14"]`
- from_egress: `1`
- to_egress: `amneziawg-exec-20260528-10-8-1-14`
- rollback_target: `1`
- route_table: `1009`
- target_interface: `v7execwg0`
- fresh runtime hashes
- approval TTL
- rollback manifest
- observation plan

## 9. Approval Design

Approval must be fresh, dual, short-lived, and exact to:

- user `10.7.0.11`
- destination `amneziawg-exec-20260528-10-8-1-14`
- budget `1`
- rollback target `1`

Any mismatch, expiry, replay, or scope expansion aborts.

## 10. Recheck Design

Pre-movement recheck must verify:

- candidate row unchanged;
- destination still GO and zero-user;
- selected moves still zero;
- registry hashes still match;
- route table `1009` baseline is unchanged;
- capacity and trust gates remain acceptable;
- checkers pass.

Any mismatch aborts.

## 11. Rollback Design

Rollback trigger includes checker failure, route drift, hidden mover, selected moves nonzero, target instability, or operator abort.

Rollback action for future certification:

`v7-user-switch 10.7.0.11 1`

P6.A did not execute rollback.

## 12. Observation Plan

Observation must include before, authorization, after-forward, delayed, final, and rollback samples if rollback is triggered.

Each sample must record registry hashes, route table `1009`, selected moves, destination users, checker outputs, and audit/switch-history counts.

## 13. Fail Closed Certification

Unknown, missing, stale, expired, invalid, mismatched, replayed, and blocked states all abort by design.

Design fail-closed model is certified. Movement execution is not certified by P6.A.

## 14. Readiness Review

Readiness:

`READY_WITH_BLOCKERS`

First User Movement Certification can begin, but actual movement still requires fresh P6.B authorization, packet, recheck, and verification.

## 15. Remaining Risks

- P6.A is a design block only.
- Production auth-backed dual approval still needs a fresh P6.B packet.
- The selected destination is execution-only and suitable for certification, not normal production assignment.
- Trusted RU remains `NEEDS_ATTENTION`, so the candidate must stay outside trusted/direct-sensitive route classes.
- Any future movement execution must explicitly keep autoswitch apply disabled/out of scope.

## 16. Recommendation For P6.B

Start P6.B as First User Movement Certification, not execution-by-default.

P6.B should generate a fresh single-user movement packet for:

`10.7.0.11: 1 -> amneziawg-exec-20260528-10-8-1-14`

and require a fresh runtime recheck immediately before any separately authorized execution.

## Required Verdicts

- reality_audit_complete=true
- implementation_conflict_audit_complete=true
- truth_source_audit_complete=true
- runtime_audit_complete=true
- user_candidate_defined=true
- channel_candidate_defined=true
- movement_domain_defined=true
- movement_packet_defined=true
- approval_defined=true
- premovement_recheck_defined=true
- rollback_defined=true
- observation_plan_defined=true
- fail_closed_certified=true
- safe_to_continue_to_first_user_movement_certification=true

## Safety Verdict

- users_moved=false
- routing_changed=false
- autoswitch_apply_run=false
- rollback_executed=false
- execution_engine_implemented=false
- runtime_hooks_with_authority=false
- deploy_performed=false
- systemd_changed=false

Design only.
