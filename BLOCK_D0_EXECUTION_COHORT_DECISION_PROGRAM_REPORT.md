# Block D0 Execution Cohort Decision Program Report

Project: V7 Vozduh

Block: D0

Title: Execution Cohort Decision Program

Date: 2026-06-01

## Summary

Decision only. No runtime decision was executed.

Recommended path:

```text
CREATE_NEW_EXECUTION_TARGET
```

The current execution target is full at `10/10`, rollback would return all ten users to egress `1` and exceed its current hard-limit policy, and hold is only useful as a temporary observation state.

## 1. Reality Audit

Current execution target:

- `amneziawg-exec-20260528-10-8-1-14`
- Interface: `v7execwg0`
- Current count: `10`
- Hard limit: `10`
- Headroom: `0`

Runtime state:

- `selected_count=0`
- `autoswitch.timer=inactive`
- `audit_count=16`
- `switch_history_count=2750`

## 2. Conflict Audit

Existing logic was reused:

- `admin_core/operator_observability.py`
- `admin_core/operator_execution.py`
- `tools/v7-second-canary-target-readiness`
- `tools/v7-route-movement-preview`
- `tools/v7-operator-execution-packet`

No parallel capacity or readiness system was created.

## 3. Truth Source Audit

Canonical sources:

- Capacity: `/opt/v7/egress/state/egress.registry`
- Cohort: `/opt/v7/egress/state/users.registry`
- Trust: `/opt/v7/egress/state/trusted-ru-decision.state`
- Verification: runtime checker outputs

No truth source conflict was found.

## 4. Runtime Audit

Runtime hashes:

- `users_hash=600ca744661e76ddb4d77098b7faedb333b4cd3f6daa2027de104939a88e165b`
- `egress_hash=4e6cce7183353bf5eeb211858112b6ef8a02ba5d6b39a7ef3df6f70c4dc5b805`
- `selected_hash=7023312b1b17c2e59cc4b596f9715c68a364be3d837a8bfdf816b63006c2216d`
- `routes_all_hash=1f42974ceb4aee43ce1c05a88f50bb5101cbd155aea0c2a7a2b0098acd13cd68`
- `rules_hash=200fc826c0f26d7e05ff11ef7600d3c9141f9ebe3b084c68946ceb825b1d9ac4`

Runtime checkers:

- `V7_USER_ROUTE_CHECK=OK`
- `V7_KILLSWITCH_CHECK=OK`
- `V7_PROVISIONING_RECONCILE_CHECK=OK`

Admin API health remained unavailable at `127.0.0.1:8017`.

## 5. Cohort Observation

Execution cohort:

- `10.7.0.2`
- `10.7.0.3`
- `10.7.0.4`
- `10.7.0.5`
- `10.7.0.6`
- `10.7.0.8`
- `10.7.0.11`
- `10.7.0.12`
- `10.7.0.14`
- `10.7.0.15`

All route tables point to `v7execwg0`.

## 6. Capacity Review

The current execution target has no headroom:

- Current count: `10`
- Hard limit: `10`
- Headroom: `0`

It is not suitable for future autoswitch testing or additional cohort expansion.

## 7. Rollback Impact

Rollback all ten users to egress `1` would produce:

- Execution target count: `0`
- Egress `1` count: `10`

Egress `1` current policy:

- Soft limit: `1`
- Hard limit: `2`

Rollback is available but not recommended as the default decision.

## 8. New Target Review

No second execution-only or reserve execution target was found.

Current target can be held for observation but cannot support further growth.

## 9. Decision Matrix

HOLD:

- Safe short-term, but blocks growth.

ROLLBACK:

- Frees target, but overloads egress `1` under current policy and loses cohort continuity.

CREATE_NEW_EXECUTION_TARGET:

- Preserves current cohort and creates a future capacity path.

## 10. Final Decision

Recommended path:

```text
CREATE_NEW_EXECUTION_TARGET
```

No execution was performed.

## 11. Recommendation For BLOCK D

Block D should create or certify a second execution target before any further cohort expansion. It should also explicitly address admin API health and capacity policy before authorizing movement.

## Required Verdicts

- `capacity_review_complete=true`
- `cohort_observation_complete=true`
- `rollback_impact_review_complete=true`
- `new_target_review_complete=true`
- `decision_made=true`
- `recommended_path=CREATE_NEW_EXECUTION_TARGET`
- `safe_to_continue_to_block_d=true`

## Safety Verdict

- `users_moved=false`
- `rollback_executed=false`
- `autoswitch_apply_run=false`
- `routing_changed=false`
- `deploy_performed=false`

