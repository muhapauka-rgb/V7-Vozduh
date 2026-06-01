# Block D Autoswitch Shadow And Operator Program Report

Project: V7 Vozduh

Block: D

Title: Autoswitch Shadow And Operator Program

Date: 2026-06-01

## Summary

Block D introduced autoswitch safely only as read-only shadow.

Final certification:

```text
NOT_READY
```

No autonomous execution was enabled. No autoswitch apply was run. No users were moved.

## 1. Reality Audit

Existing autoswitch and governance functionality exists and was reused:

- `v7-users-autoswitch`
- `v7-autoswitch-safety-review`
- `v7-route-movement-preview`
- `v7-operator-execution-packet`
- `v7-second-canary-target-readiness`
- `admin_core/operator_execution.py`
- `admin_core/operator_observability.py`

Runtime state:

- Execution target count: `10`
- Execution target hard limit: `10`
- Headroom: `0`
- Selected moves: `0`
- Autoswitch timer: `inactive`

## 2. Conflict Audit

No parallel autoswitch, candidate queue, approval model, or movement system was created.

Existing implementation was reused in read-only mode.

## 3. Truth Source Audit

Canonical sources:

- Candidate recommendation: `v7-users-autoswitch` shadow JSON
- Movement truth: `/opt/v7/egress/state/users.registry`
- Egress truth: `/opt/v7/egress/state/egress.registry`
- Approval: `v7-operator-execution-packet`
- Verification: runtime checker outputs

## 4. Runtime Audit

Runtime checkers:

- `V7_USER_ROUTE_CHECK=OK`
- `V7_KILLSWITCH_CHECK=OK`
- `V7_PROVISIONING_RECONCILE_CHECK=OK`

Safety review:

- `status=critical`
- Critical finding: no enabled egress detected by safety review

Admin health:

- `127.0.0.1:8017` unavailable

## 5. Shadow Mode

Command:

```text
v7-users-autoswitch --mode guarded --service telegram --route-class GLOBAL_STABLE --pretty
```

Shadow result:

- `apply_requested=false`
- `candidate_moves=12`
- `selected_moves=0`
- `action_counts={"keep":6,"switch":12}`
- `move_type_counts={"failover":12,"none":6}`

## 6. Shadow Accuracy

Accuracy is not acceptable for operator execution.

Reasons:

- Raw planner recommends `12` failovers.
- Recommendations include the certified execution cohort.
- D0 decision says new execution target is needed before further growth.
- Safety review is critical.
- Selected moves remain `0`.

## 7. Approval Model

Certified approval model requirements:

- Proposal ID
- Planner generation ID
- Runtime hashes
- Exact allowed users
- Exact allowed targets
- TTL
- Dual approval
- Replay protection
- Runtime recheck
- Rollback manifest
- Observation window

## 8. Operator Execution

No operator execution was performed.

Operator execution is not certified because the shadow proposal failed safety and scope gates.

## 9. Observation

Observation completed for shadow mode only.

No before/after movement window was needed because no movement occurred.

## 10. Rollback

Rollback readiness is defined and technically available per user, but bulk rollback of the ten-user cohort to egress `1` remains capacity-risky under D0.

## 11. Fail Closed

Fail-closed behavior was verified:

- Safety critical blocked execution.
- Wide raw recommendation was not promoted.
- No packet was executed.
- No hidden movers were observed.

## 12. Certification

Certification result:

```text
NOT_READY
```

## 13. Remaining Risks

- Admin API health unavailable.
- Execution target full at `10/10`.
- Safety review has a critical registry interpretation issue.
- Shadow recommendations are too broad for bounded autonomy.
- Trusted RU state remains `NEEDS_ATTENTION`.

## 14. Recommendation For BLOCK E

Before Block E, do not enable autonomous execution. Recommended next work:

1. Resolve safety-review registry interpretation.
2. Create or certify a new execution target as D0 recommended.
3. Add an operator-scoped autoswitch proposal cap.
4. Require shadow recommendation to match a bounded packet before any execution.
5. Restore admin API health or explicitly remove UI dependency from approval.

## Required Verdicts

- `shadow_mode_certified=true`
- `shadow_accuracy_acceptable=false`
- `operator_approval_model_certified=true`
- `operator_execution_certified=false`
- `rollback_ready=true`
- `fail_closed_verified=true`
- `safe_to_continue_to_block_e=false`

## Safety Verdict

- `autonomous_execution_enabled=false`
- `scope_expanded_only_as_approved=true`
- `autoswitch_apply_without_approval=false`
- `deploy_performed=false`
- `users_moved=false`
- `routing_changed=false`

