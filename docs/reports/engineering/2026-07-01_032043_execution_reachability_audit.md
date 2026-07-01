# Complete Execution Reachability Audit

Date: 2026-07-01 03:20 UTC

## Summary

Verdict: `EXECUTION_PATH_BLOCKED`.

The execution path is no longer blocked at the canonical transition or restore barrier materialization. The previous minimal patch restored:

OMP Production Validation -> `tools/v7-governed-canary-dry-run-cycle` -> `admin_core/operator_execution_pipeline.py` -> `admin_core/operator_execution.py` -> restore barrier clearance -> `tools/v7-users-autoswitch --apply --verify`.

The current first pre-movement blocker is inside the runtime apply consumer:

`tools/v7-users-autoswitch::plan()` consumes the approved plan lock, then re-enters `_emergency_failover_authority_gate()`. That gate rejects the current L3 context and clears the approved selected move before `apply()` can call `_run_switch()`.

Observed production status from the latest L3 production validation:

- Transaction: `STOP_SAFE`
- Candidate user: `10.0.0.2`
- Source: `openvpn-1779388847-d2ad7c`
- Target: `vless`
- Restore barrier written: YES
- Approved plan lock valid: YES
- Selected moves before restore barrier: 1
- Selected moves after gate: 0
- Runtime apply executed: NO
- Users moved: 0
- Runtime commit: `0f9502bde3ac51a0d4e4f7b50309f5d7cdf11246`
- Terminal reason: `approved_plan_lock_selected_moves_missing`
- Execution blocker: `emergency_failover_autonomy`

## Semantic Duplicate Audit

| Responsibility | Existing owner | Status |
| --- | --- | --- |
| Governed/L3 transaction entry | `tools/v7-governed-canary-dry-run-cycle` | `EXISTS_COMPLETE` |
| Production validation to runtime action transition | `admin_core/operator_execution_pipeline.py` | `EXISTS_COMPLETE` |
| Packet validation, lease, runtime recheck, restore barrier materialization | `admin_core/operator_execution.py` | `EXISTS_COMPLETE` |
| Runtime movement consumer | `tools/v7-users-autoswitch` | `EXISTS_COMPLETE` |
| Approved plan lock validation | `tools/v7-users-autoswitch::_approved_plan_lock_validation()` | `EXISTS_COMPLETE` |
| Emergency failover authority gate | `tools/v7-users-autoswitch::_emergency_failover_authority_gate()` | `EXISTS_COMPLETE` |
| L3 execution eligibility | `tools/v7-users-autoswitch::_l3_execution_eligibility()` | `EXISTS_COMPLETE` |
| User movement execution | `tools/v7-users-autoswitch::_run_switch()` | `EXISTS_COMPLETE` |
| Verification | `tools/v7-users-autoswitch::_verify_routes()` / `_verify_emergency_required_services()` | `EXISTS_COMPLETE` |
| Rollback | `tools/v7-users-autoswitch::_run_switch(..., "rollback")` | `EXISTS_COMPLETE` |
| Learning/evidence closure | Existing L3 closure/finalization owners in `tools/v7-users-autoswitch` and governed cycle | `EXISTS_PARTIAL` for production proof because no movement happened |

No duplicate owner, runtime, planner, authority, packet, restore barrier, or execution path is required to explain the current blocker.

## Execution Graph

Canonical path to first user movement:

1. OMP Production Validation approval
2. `tools/v7-governed-canary-dry-run-cycle::execute_l3_production_validation()`
3. `run_l3_production_validation_plan()`
4. `admin_core/operator_execution_pipeline.py::l3_production_validation_runtime_action_transition()`
5. Packet creation and validation
6. Execution lease creation
7. `admin_core/operator_execution.py::execute_packet(mode="runtime_action")`
8. Runtime recheck
9. Restore barrier clearance write
10. `tools/v7-users-autoswitch --apply --verify`
11. Approved plan lock consumption
12. Restore barrier budget/generation check
13. Intelligence snapshot gate
14. Emergency failover authority gate
15. Restore barrier execution gate
16. Atomic execution envelope validation
17. L3 execution eligibility
18. `_run_switch(user, target, reason)`
19. First user movement

Post-movement closure:

20. Route verification
21. Required service verification
22. Rollback or success classification
23. Learning/evidence
24. Capability state / production maturity / OMP

## Execution Reachability Ladder

| Order | Gate | Owner | Can Stop | Current Status | Next Blocker if Removed |
| ---: | --- | --- | --- | --- | --- |
| 1 | Operator L3 confirmation token | `tools/v7-governed-canary-dry-run-cycle` | YES | PASS in latest run | Max-user scope |
| 2 | One-user scope | `tools/v7-governed-canary-dry-run-cycle` | YES | PASS | Active lease |
| 3 | Active execution lease check | `admin_core/operator_execution.py::execution_lease_state()` | YES | PASS; current lease is terminal `OPERATOR_CANCELLED` | Plan availability |
| 4 | Production plan availability | `run_l3_production_validation_plan()` / `tools/v7-users-autoswitch` | YES | PASS | Candidate selection |
| 5 | Candidate selection and safe target | `AutoswitchPlanner.plan()` / `_decision_for_user()` / `_select_moves()` | YES | PASS; 1 candidate selected before restore barrier | Pipeline transition |
| 6 | Production validation transition | `admin_core/operator_execution_pipeline.py` | YES | PASS | Packet validity |
| 7 | Packet validity and scope | `admin_core/operator_execution.py::validate_packet()` | YES | PASS | Lease creation |
| 8 | Execution lease creation | `admin_core/operator_execution.py::write_execution_lease()` | YES | PASS in latest run | Runtime recheck |
| 9 | Replay guard | `admin_core/operator_execution.py::execute_packet()` | YES | PASS for fresh approval | Runtime recheck |
| 10 | Runtime recheck | `admin_core/operator_execution.py::runtime_recheck()` / `recheck_nonzero_packet()` | YES | PASS | Restore barrier write |
| 11 | Restore barrier conflict/write | `append_restore_barrier_clearance()` | YES | PASS; barrier written | Runtime apply consumer |
| 12 | Runtime apply plan reload | `tools/v7-users-autoswitch::plan()` | YES | PASS | Approved plan lock |
| 13 | Approved plan lock | `_approved_plan_lock_validation()` | YES | PASS; `approved_plan_lock_validation.ok=true` | Restore barrier generation |
| 14 | Restore barrier budget/generation | `_restore_clearance_generation_check()` | YES | PASS | Intelligence snapshot gate |
| 15 | Intelligence snapshot gate | `_intelligence_snapshot_gate()` | YES | PASS / no material stop observed | Emergency failover authority gate |
| 16 | Emergency failover authority gate | `_emergency_failover_authority_gate()` | YES | `STOP_SAFE`; selected move cleared | Restore barrier execution gate |
| 17 | Apply selected-move presence | `tools/v7-users-autoswitch::apply()` | YES | `STOP_SAFE`; `approved_plan_lock_selected_moves_missing` | Atomic envelope validation |
| 18 | Restore barrier execution gate | `restore_barrier_execution_gate` in `plan()` | YES | `NEVER_REACHED` after current selected move is cleared | Atomic envelope validation |
| 19 | Atomic execution envelope | `_validate_atomic_execution_envelope()` | YES | `NEVER_REACHED` | L3 execution eligibility |
| 20 | L3 execution eligibility | `_l3_execution_eligibility()` | YES | `NEVER_REACHED` | User switch command |
| 21 | User switch command | `_run_switch()` | YES | `NEVER_REACHED` | First user movement |
| 22 | First user movement | External switch command consumed by `_run_switch()` | N/A | `NEVER_REACHED` | Post-movement verification |
| 23 | Route/service verification | `_verify_routes()` / `_verify_emergency_required_services()` | YES, after movement only | `NEVER_REACHED` | Rollback |
| 24 | Rollback | `_run_switch(..., "rollback")` | YES, after movement only | `NEVER_REACHED` | Learning/evidence |
| 25 | Learning/evidence/capability state | Existing L3 closure owners | YES for certification, not for first movement | `NEVER_REACHED` | OMP next cycle |

## Current STOP Details

The current execution fails closed before `_run_switch()`:

- `approved_plan_lock_validation.ok = true`
- `selected_moves_before_restore_barrier = 1`
- `_emergency_failover_authority_gate()` returns `ok = false`
- `plan.selected_moves = []`
- `apply()` returns `approved_plan_lock_selected_moves_missing`
- No user movement occurs

This means the canonical chain reaches runtime action materialization, but the runtime apply consumer does not yet preserve the one-user production validation move through the L3 emergency autonomy gate.

## Virtual Blocker Removal

Assume blocker 16 is removed correctly through the existing owner.

Next possible blockers, in order:

1. Restore barrier execution gate can still stop if neither approved lock nor emergency gate authorizes the selected move.
2. Atomic execution envelope can stop if operation identity, selected move hash, source bundle, or envelope identity changes.
3. L3 execution eligibility can stop on authority not authorized, wake not accepted, incident not ready, selected move count not exactly one, missing operation id/hash, user/source/target live state changes, source recovery, target loss, target service failure, or stale source-failure evidence.
4. `_run_switch()` can fail before movement if the external switch command fails.

Post-movement blockers:

5. Verification can fail and trigger rollback.
6. Rollback can fail.
7. Learning/evidence/capability state can block production proof/certification, but cannot block the first user movement once `_run_switch()` succeeds.

## Root Cause Reduction

Grouped blocker set:

| Group | Blockers | Scope |
| --- | --- | --- |
| Current pre-movement blocker | Emergency failover authority gate clears the approved production validation selected move; apply sees zero selected moves. | `tools/v7-users-autoswitch` |
| Expected live safety blockers | Atomic envelope, L3 eligibility, live source/target/user/freshness/service checks. | Existing runtime apply owner |
| External execution blocker | `_run_switch()` command failure before mutation. | Existing switch command/runtime integration |
| Post-movement closure blockers | Verification, rollback, learning/evidence/capability state. | Existing verification/rollback/learning owners |

Smallest current blocker set to reach first user movement:

1. `tools/v7-users-autoswitch::_emergency_failover_authority_gate()` / adjacent apply planning flow does not consume the already approved L3 Production Validation transaction as the bounded one-user execution authority for this run.

Everything after that remains conditional and must be revalidated live; no downstream blocker is currently proven because execution never reaches it.

## Minimal Executable Path To First User Movement

1. Keep the canonical chain unchanged:
   OMP Production Validation -> governed cycle -> operator execution pipeline -> operator execution -> restore barrier -> autoswitch apply.
2. In the existing runtime apply owner, preserve the approved production-validation selected move through the L3 emergency failover gate only when it remains inside the existing approved one-user transaction envelope.
3. Re-run the same One User Production Validation.
4. If the next live gate stops, reduce from that exact gate.

No new Runtime, Planner, Authority, owner, execution path, restore barrier owner, packet model, or architecture is required by this audit.

## Final Verdict

`EXECUTION_PATH_BLOCKED`
