# P6.A Reality Audit

Project: V7 Vozduh

Program: P6

Block: P6.A

Mode: Architecture / Discovery / User Movement Design

## Scope

P6.A is design only.

No user movement, routing change, autoswitch apply, policy apply, rollback execution, deploy, systemd change, Git push, or Git merge was performed.

## Repository Search

Searched for:

- user movement
- autoswitch
- rebalance
- candidate movement
- routing decisions
- execution contracts
- operator execution
- rollback preview
- verification
- runtime action
- selected moves

## Existing Implementations

| Area | Existing source | Behavior | P6.A decision |
| --- | --- | --- | --- |
| Movement preview | `tools/v7-route-movement-preview` | Read-only user-switch and routing-sync preview. Emits files/routes/rollback expectations. | Reuse |
| Autoswitch planner | `tools/v7-users-autoswitch` | Read-only by default, optional `--apply` uses `v7-user-switch`. Includes selection, capacity, safety, selected moves, rebalance. | Reuse concepts only; do not run apply |
| Candidate readiness | `tools/v7-second-canary-target-readiness` | Read-only candidate and execution target readiness review. | Reuse |
| Operator execution | `admin_core/operator_execution.py` | Packet validation, runtime recheck, replay denial, append-only audit/governance for zero-move action. | Extend packet concepts, do not add movement engine in P6.A |
| Verification | `v7-user-route-check`, `v7-killswitch-check`, `v7-provisioning-reconcile-check` | Runtime checkers for route/user/provisioning safety. | Reuse as required pre/post checks |
| Historical movement packets | `docs/track7/productization/e24-evidence`, `e27_2-evidence`, `e28_2-evidence` | Bounded user movement packet and execution evidence. | Reuse schema concepts |
| Rollback evidence | `docs/track7/productization/e27_2-evidence`, `e28_2-evidence` | Forward and rollback verification for approved bounded users. | Reuse rollback pattern |

## Repository Reality

User movement already exists historically as a governed operational path around:

- `v7-user-switch`
- `v7-route-movement-preview`
- approval packets
- execution-time recheck
- route/user verification
- explicit rollback

P6.A must not create a parallel movement mechanism.

## Verdict

- reality_audit_complete=true
- existing_movement_logic_found=true
- movement_design_only=true
- user_movement_performed=false
- routing_changed=false
- autoswitch_apply_run=false
