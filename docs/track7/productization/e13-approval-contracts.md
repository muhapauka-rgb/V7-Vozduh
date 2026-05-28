# E13 Approval Contract Design

## Purpose

Approvals must bind a human decision to a specific runtime truth. They are not
buttons. They are expiring contracts over a preview, generation, selected-move
fingerprint, rollback plan, and evidence bundle.

## Contract Principles

1. Freshness is mandatory.
2. A preview without rollback is not approvable.
3. A generation token without selected-move fingerprint is not approvable.
4. A target readiness GO does not imply execution allowed.
5. Nonzero selected-move budget requires explicit approval.
6. Approval scope is exact: users, from targets, to targets, budget, expiry.
7. Replay, mismatch, stale hash, expired token, or budget overflow fails closed.
8. Every approved movement must have a visible delayed-monitor closeout.

## Movement Preview Contract

Required fields:

```text
contract_type=movement_preview
operation_id
generated_at
expires_at
state_source=live|copied|simulation
users_registry_hash
egress_registry_hash
planner_generation_id
selected_moves_count
selected_moves_fingerprint
candidate_moves_total
movement_budget
approved_users
from_targets
to_targets
route_delta_summary
target_capacity_delta
rollback_manifest_id
required_gates
blocked_candidates_summary
evidence_bundle_id
```

Approval status:

- draft: preview generated, no approval.
- approvable: all gates fresh and rollback exists.
- stale: source hash or expiry invalid.
- blocked: gate fails or budget exceeded.
- approved: operator bound the preview to an approval.
- consumed: movement lifecycle used the approval.
- expired: no longer valid.

## Selected-Move Fingerprint Contract

Fingerprint input:

- user id;
- source target;
- destination target;
- movement type;
- planner generation id;
- rollback target;
- route delta class.

The fingerprint must not include mutable display-only fields. It must be stable
for the same approved movement and must change if any user, target, direction,
or generation changes.

## Generation Token Contract

Required fields:

```text
contract_type=generation_token
token_id
issued_at
expires_at
issued_by
planner_generation_id
apply_generation_id_expected
restore_generation_id
selected_moves_fingerprint
max_selected_moves
allowed_users
allowed_from_targets
allowed_to_targets
restore_barrier_id
approval_id
replay_nonce
status=active|consumed|expired|revoked
```

Validation rules:

- token generation must match current planner generation;
- selected-move fingerprint must match current selected moves;
- selected move count must be `<= max_selected_moves`;
- token must be active and unconsumed;
- token must be scoped to exact users and targets;
- token must be rejected after expiry or state-hash drift;
- token consumption must be recorded before mutation is allowed.

## Rollback Contract

Required fields:

```text
contract_type=rollback
rollback_manifest_id
approved_operation_id
users
rollback_target_per_user
expected_route_after_rollback
target_health_required
verification_checks
rollback_order
partial_failure_policy
emergency_containment_policy
```

Rules:

- rollback must be generated before forward approval;
- rollback target must be healthy at approval time;
- partial rollback must be visible and cannot be silently auto-repaired;
- rollback closeout requires route verification and delayed movement monitoring.

## Blast Radius Contract

Required fields:

- exact affected users;
- maximum movement count;
- target capacity before/after;
- route classes affected;
- production targets touched;
- reserved targets touched;
- rollback users;
- delayed-monitor scope;
- what is explicitly out of scope.

The UI must show blast radius before any confirmation text.

## Restore Barrier Contract

Required fields:

- barrier id;
- created by operation;
- created at;
- TTL;
- status active/expired/cleared;
- clearance required yes/no;
- fail-closed behavior;
- associated generation token;
- selected-move budget;
- delayed-monitor requirement.

Rules:

- expired uncleared barrier fails closed;
- clearance without matching generation token fails closed for nonzero budget;
- barrier clearance is never one-click.

## Delayed Monitoring Contract

Required fields:

- monitored operation;
- required sample count;
- sample interval policy;
- registry hash sequence;
- switch-history count sequence;
- selected_moves sequence;
- hidden mover scan sequence;
- checker sequence;
- closeout verdict.

Rules:

- operation is not promotion-clean until delayed monitoring closes cleanly;
- unexpected movement opens emergency containment flow;
- clean samples must be linked to the operation history.

## Approval Expiration

Approvals expire when:

- time window expires;
- users registry hash changes;
- egress registry hash changes;
- planner generation changes;
- selected-move fingerprint changes;
- target readiness changes from GO;
- rollback target becomes unhealthy;
- selected moves exceed budget;
- hidden mover is detected.

## What Can Be Automatic

- read-only snapshot refresh;
- checker execution;
- dry-run preview generation;
- evidence bundle generation;
- stale approval expiration;
- warning creation;
- operation history archive;
- non-mutating comparison.

## What Requires Explicit Approval

- nonzero selected-move budget;
- bounded user movement;
- rollback execution;
- apply timer restore;
- restore barrier clearance;
- generation token issuance;
- reservation mutation;
- target lifecycle mutation;
- emergency containment.

## What Requires Second Confirmation

- movement affecting more than one user;
- any nonzero clearance budget;
- apply timer restore after restore lifecycle;
- barrier clearance after TTL;
- target hard-limit boundary;
- reserved target use;
- rollback with partial-failure risk;
- emergency containment that changes timer state.

## What Should Never Become One-Click

- broad autoswitch apply;
- unbounded rebalance;
- Direct/RU mutation;
- Trusted RU refresh;
- proxy apply;
- kill switch mutation;
- production target drain;
- target reservation removal;
- repairing unexpected movement without a report.

