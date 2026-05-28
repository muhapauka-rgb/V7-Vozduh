# E25.2 Pre-Execution Live Runtime Recheck

## Result

`ABORT_BEFORE_MUTATION`

Fresh VPS runtime recheck failed the target readiness gate. No user movement command was executed.

## Runtime Identity

- hostname: `v3119922.hosted-by-vdsina.ru`
- timestamp: `2026-05-28T11:01:21Z`
- repo branch: `Updatesystem`
- repo HEAD: `5de30074356771beef8d5b750415a38c78dbb28a`
- packet hash: `589aca11bdfa1c69db86e9d16d9a90f0588787d8ea5594f17486902f0ebf9829`
- packet id: `pkt_e25_1_first_bounded_user_move_10_7_0_11_20260528T103331Z`
- packet expiry: `2026-05-28T12:33:31.168538+00:00`

## Registry State

- `users.registry=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- `egress.registry=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`

Candidate row:

```text
ip=10.7.0.11 current=1 table=1009 enabled=1
```

Route table before execution:

```text
default dev v7e356a192b79 scope link
```

`route_get` direct command returned:

```text
RTNETLINK answers: Network is unreachable
```

Runtime checkers still reported OK for managed routes, so this was not treated as a standalone movement blocker after the target readiness gate had already failed.

## Target Readiness

`v7-second-canary-target-readiness --json` returned:

- `approval_status=NO-GO`
- `second_canary_readiness=NO-GO`
- `selected_target=NONE`
- candidate still valid: true
- WireGuard target users: `0`
- WireGuard diagnose: `OK`
- WireGuard load: `OK`
- WireGuard `min_mbps=4.61`, below floor `10.0`
- WireGuard `stability=0.297919`, below floor `0.45`

Blocker:

`target_readiness_not_go`

## Restore-Settle Gate

E25.1 fresh sample gate remained GO when rechecked locally:

- `gate_status=GO`
- `sample_count=3`
- `apply_timer_intervals_covered=5.1`
- `selected_moves_by_sample=[0,0,0]`
- `registry_stable=true`
- `checkers_ok=true`
- `hidden_movers_observed=false`

Restore-settle did not override the target readiness NO-GO.

## Selected Moves

No selected-move files were present under `/opt/v7/egress/state`; interpreted as `selected_moves=0`.

## Barrier / Generation State

`/opt/v7/egress/state/autoswitch-restore-barrier.json` present:

- `enabled=true`
- `allow_post_ttl_apply=true`
- `generation_clearance=true`
- `clearance_max_selected_moves=0`
- `expires_at=2000-01-01T00:00:00+00:00`

No separate generation state file was present.

## Planner / Apply Timers

- planner timer: inactive
- apply timer: inactive
- planner service: inactive
- apply service: inactive

## Hidden Movers

No active process matched:

- `v7-user-switch`
- `v7-routing-sync`
- `v7-users-autoswitch --apply`

## Runtime Checkers

- `V7_RECONCILE_RESULT=OK`
- `V7_USER_ROUTE_CHECK=OK`
- `V7_KILLSWITCH_CHECK=OK`
- `V7_PROVISIONING_RECONCILE_CHECK=OK`

## Abort Decision

E25.2 aborts before movement because the approved target is not GO at execution time.

No `v7-user-switch` command was executed.
