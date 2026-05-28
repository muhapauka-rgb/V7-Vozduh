# E22.1 Post-Run Safety Verification

Collected: 2026-05-28T07:12:01Z

## Registry Hashes

```text
users.registry  = bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c
egress.registry = a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8
```

These match the pre-run hashes.

## Selected Moves

```text
missing /opt/v7/egress/state/selected-moves.json
missing /opt/v7/egress/state/selected_moves.json
missing /opt/v7/egress/state/current-selected-moves.json
```

Selected moves remained zero by E22 packet semantics.

## Hidden Movers

```text
hidden_scan_exit=1
```

No `v7-user-switch`, `v7-routing-sync`, or `v7-users-autoswitch --apply` process was observed after the run.

## Audit Store

```text
path=/opt/v7/audit/operator-execution-audit.jsonl
mode=-rw-------
line_count=9
approval_record_persisted=1
denial_record=8
approval_records=['appr_e22_1_vps_zero_movement_20260528T071118Z']
runtime_mutation_any=False
user_movement_any=False
routing_mutation_any=False
runtime_action_performed_any=False
```

## Runtime Checkers

```text
v7-reconcile-check: OK
v7-user-route-check: OK
v7-killswitch-check: OK
v7-provisioning-reconcile-check: OK
```

## Safety Verdict

No user movement, routing mutation, autoswitch apply, kill-switch mutation, or runtime action occurred. The only live mutation was append-only approval/audit record persistence.
