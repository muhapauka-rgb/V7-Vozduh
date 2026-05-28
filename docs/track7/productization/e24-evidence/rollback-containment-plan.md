# E24 Rollback And Containment Plan

## Forward Command For E25 Only

```text
v7-user-switch 10.7.0.11 wireguard-1779454504-c43409
```

## Rollback Command For E25 Only

```text
v7-user-switch 10.7.0.11 1
```

## Rollback Verification

After rollback:

```text
users.registry: 10.7.0.11 current=1
table 1009: default dev v7e356a192b79
route_get: 8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009
WireGuard users=0
v7-reconcile-check=OK
v7-user-route-check=OK
v7-killswitch-check=OK
v7-provisioning-reconcile-check=OK
hidden_movers=absent
```

## Required Holds Before E25 Movement

```text
hold planner timer/service
hold apply timer/service
do not run autoswitch apply
do not run routing-sync
```

## Emergency Containment Triggers

- selected_moves becomes nonzero before or after movement;
- hidden mover appears;
- runtime checker fails;
- candidate user not on expected source;
- target readiness not GO;
- restore-settle not GO;
- route_get mismatch;
- switch-history contains unexpected user;
- users.registry hash changes outside approved user;
- WireGuard users exceeds 1 after forward movement;
- rollback verification fails.

## Delayed Monitoring Window

Collect at least five samples after movement and after rollback:

- users.registry hash;
- candidate route table and route_get;
- selected_moves;
- switch-history count/tail;
- hidden mover scan;
- runtime checkers;
- WireGuard users;
- target readiness;
- restore-settle.

rollback_plan_complete=true
containment_plan_complete=true
