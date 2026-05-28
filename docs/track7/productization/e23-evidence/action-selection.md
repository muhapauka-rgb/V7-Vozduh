# E23 Zero-Move Action Selection

## Candidate Review

| Candidate | Verdict | Reason |
|---|---|---|
| A) generation-clearance transition | Not selected | Existing restore barrier already has `generation_clearance=true` and `clearance_max_selected_moves=0`; changing it would touch autoswitch-consumed state. |
| B) restore-barrier state transition | Not selected | Restore barrier is read by autoswitch; mutating it would be runtime-affecting even with zero user movement. |
| C) bounded apply-timer no-op lifecycle | Not selected | Timer/apply lifecycle can create delayed movement risk; VPS lacks restore-settle helper in PATH. |
| D) runtime governance-only state mutation | Selected | Append-only state transition under `/opt/v7/audit`, not read by routing/autoswitch, zero blast radius, naturally rollback-safe by revocation record. |
| E) equivalent zero-move orchestration mutation | Covered by D | The selected action is the minimal orchestration/governance state transition. |

## Selected Runtime Action

```text
selected_runtime_action=ZERO_MOVE_GOVERNANCE_STATE_TRANSITION
runtime_mutation_scope=append_only_runtime_governance_state
runtime_governance_store=/opt/v7/audit/operator-runtime-governance-actions.jsonl
audit_store=/opt/v7/audit/operator-execution-audit.jsonl
```

## Exact Mutation Scope

Allowed writes:

```text
/opt/v7/audit/operator-runtime-governance-actions.jsonl
/opt/v7/audit/operator-execution-audit.jsonl
```

Forbidden and not performed:

```text
users.registry mutation
egress.registry mutation
autoswitch-restore-barrier.json mutation
autoswitch-safety.json mutation
route/ip/nft mutation
v7-user-switch
v7-routing-sync
v7-users-autoswitch --apply
systemctl start/stop/restart
UI execution
```

## Rollback

Rollback is not a runtime repair. The action is append-only and non-consumed by routing/autoswitch, so rollback is:

```text
append revocation/containment record only
do not delete audit records
do not mutate users.registry
do not mutate routes
```

## Blast Radius Proof

The selected action cannot move traffic because:

- it writes only `/opt/v7/audit` append-only JSONL records;
- it does not touch `/opt/v7/egress/state/users.registry`;
- it does not touch `/opt/v7/egress/state/egress.registry`;
- it does not touch route tables, nftables, WireGuard/AWG state, or systemd services;
- it does not run autoswitch apply;
- it has `selected_move_budget=0`, `allowed_users=[]`, `allowed_targets=[]`.

blast_radius_zero=true
