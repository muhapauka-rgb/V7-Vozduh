# E22.1 VPS Runtime Availability Snapshot

Collected: 2026-05-28T07:08:16Z

## Identity

```text
pwd=/root
hostname=v3119922.hosted-by-vdsina.ru
date_utc=Thu May 28 07:08:16 UTC 2026
```

## Runtime Registries

```text
-rw-r--r-- 1 root root 1811 May 26 21:46 /opt/v7/egress/state/egress.registry
-rw-r--r-- 1 root root  774 May 27 13:18 /opt/v7/egress/state/users.registry

users.registry  = bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c
egress.registry = a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8
```

## Selected Moves

No selected-move state files were present:

```text
missing /opt/v7/egress/state/selected-moves.json
missing /opt/v7/egress/state/selected_moves.json
missing /opt/v7/egress/state/current-selected-moves.json
```

E22 packet semantics therefore classify selected moves as:

```text
selected_move_count=0
selected_move_source=missing_treated_as_empty
selected_move_hash=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
```

## Restore Barrier / Generation State

```json
{
  "block": "E11.17",
  "created_at": "2026-05-27T10:51:51.650380+00:00",
  "enabled": true,
  "expires_at": "2000-01-01T00:00:00+00:00",
  "owner": "control_plane_governance",
  "reason": "E11.17 generation-clearance rehearsal with zero movement budget",
  "ttl_reason": "E11.14 containment TTL; apply timer remains held and future apply restore requires explicit clearance or refresh",
  "rehearsal": "expired_cleared_budget_zero",
  "allow_post_ttl_apply": true,
  "generation_clearance": true,
  "clearance_max_selected_moves": 0,
  "clearance_issued_at": "2026-05-27T13:13:16.749351+00:00"
}
```

## Planner / Apply Timers

```text
v7-users-autoswitch-planner.timer: inactive
v7-users-autoswitch-apply.timer: inactive
v7-users-autoswitch.timer last fired Wed 2026-05-27 20:13:14 MSK, 13h before snapshot
```

## Runtime Checkers

```text
v7-reconcile-check: OK
v7-user-route-check: OK
v7-killswitch-check: OK
v7-provisioning-reconcile-check: OK
```

## Hidden Movers

```text
hidden_scan_exit=1
```

No `v7-user-switch`, `v7-routing-sync`, or `v7-users-autoswitch --apply` process was observed.

## Tool Availability Gap

The VPS runtime does not currently expose these repo governance helpers in `PATH`:

```text
v7-second-canary-target-readiness: tool_missing
v7-restore-settle-gate: tool_missing
```

This did not block E22.1 because the selected action is record-only with zero movement and zero routing mutation. It remains a productization/runtime convergence gap for future live runtime actions.
