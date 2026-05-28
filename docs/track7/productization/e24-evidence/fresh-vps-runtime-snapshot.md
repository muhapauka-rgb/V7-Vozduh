# E24 Fresh VPS Runtime Snapshot

Collected: 2026-05-28T08:22:47Z on `v3119922.hosted-by-vdsina.ru`.

## Boundary

This snapshot used read-only registry parsing, route inspection, checker execution, tool visibility, timer status, and hidden process scans.

`v7-users-autoswitch` dry-run was not executed. The sandbox escalation reviewer flagged that it may write runtime load-summary state, which exceeds E24's no-mutation authorization.

## Registry Hashes

```text
users_registry_hash=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c
egress_registry_hash=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8
restore_barrier_hash=f5f37e9595f87233939ed067ef25e58c500adae687de4090a8c1832140571079
autoswitch_safety_hash=e13fcf81c723247ac0781c95206fc8fdc55bc5791ca696b39fb5aa5768d50083
```

## Users Per Egress

```text
1=4
awg0=3
awg3=9
wireguard-1779454504-c43409=0
openvpn-1779388847-d2ad7c=0
vless=0 enabled users
```

Enabled users:

```text
10.0.0.2 current=awg3 table=100
10.0.0.3 current=awg3 table=101
10.0.0.6 current=awg3 table=104
10.7.0.2 current=awg3 table=1000
10.7.0.3 current=awg3 table=1001
10.7.0.4 current=awg3 table=1002
10.7.0.5 current=awg3 table=1003
10.7.0.6 current=awg3 table=1004
10.7.0.8 current=awg3 table=1006
10.7.0.9 current=awg0 table=1007
10.7.0.10 current=awg0 table=1008
10.7.0.11 current=1 table=1009
10.7.0.12 current=1 table=1010
10.7.0.13 current=awg0 table=1011
10.7.0.14 current=1 table=1012
10.7.0.15 current=1 table=1013
```

## Selected Moves

```text
selected-moves.json=missing
selected_moves.json=missing
current-selected-moves.json=missing
selected_moves=0 by packet semantics
```

## Restore Barrier / Generation State

```json
{
  "block": "E11.17",
  "enabled": true,
  "expires_at": "2000-01-01T00:00:00+00:00",
  "allow_post_ttl_apply": true,
  "generation_clearance": true,
  "clearance_max_selected_moves": 0,
  "clearance_issued_at": "2026-05-27T13:13:16.749351+00:00"
}
```

## Timers And Hidden Movers

```text
v7-users-autoswitch-planner.timer=inactive
v7-users-autoswitch-apply.timer=inactive
v7-users-autoswitch.timer=inactive
hidden_movers=[]
```

No `v7-user-switch`, `v7-routing-sync`, or `v7-users-autoswitch --apply` process was observed.

## Switch History

```text
switch-history.log=missing
switch-history.jsonl=missing
switch_history.jsonl=missing
```

No switch-history file was present in `/opt/v7/egress/state`.

## Runtime Checkers

```text
v7-reconcile-check=OK
v7-user-route-check=OK
v7-killswitch-check=OK
v7-provisioning-reconcile-check=OK
```

## Route Sanity

All enabled user route tables have a default route matching their registry egress, and `v7-user-route-check` passed.

Selected candidate route sanity:

```text
10.7.0.11 table=1009 current=1
table_route=default dev v7e356a192b79 scope link
route_get=8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009
```

## Target State Snapshot

```text
target=wireguard-1779454504-c43409
interface=v7e06a394c478
protocol=wireguard
users=0
soft_limit=1
hard_limit=2
canary_reserved=true
ip_link=<POINTOPOINT,NOARP,UP,LOWER_UP>
ip_addr=10.8.0.17/24
latest_handshake=27 seconds ago at collection time
```

## Abort Conditions

```text
runtime_registries_missing=false
selected_moves_gt_zero=false
hidden_movers_active=false
runtime_checkers_fail=false
target_readiness_cannot_be_trusted=true for execution due missing VPS readiness helper
restore_settle_cannot_be_trusted=true for execution due missing VPS restore-settle helper
```

E24 continues as a conditional approval-packet design only. It does not approve E25 execution until runtime/repo convergence is fixed.
