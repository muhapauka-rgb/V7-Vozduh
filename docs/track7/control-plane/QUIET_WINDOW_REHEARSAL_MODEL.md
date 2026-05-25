# Quiet-Window Rehearsal Model

This model defines a future quiet-window rehearsal. It is not a canary and it was not executed.

## Objective

Prove that V7 can enter a short, observable control-plane quiet window where autoswitch cannot move users, route/rule/registry snapshots remain stable, and reconcile behavior can be evaluated without concurrent autoswitch interference.

## Scope

Allowed in the future rehearsal after explicit approval:

- bounded autoswitch authority hold;
- read-only state capture;
- read-only route/rule inspection;
- read-only reconcile/user-route/kill-switch/provisioning checks;
- restore autoswitch authority.

Not allowed:

- user switch;
- routing sync;
- canary;
- policy apply;
- Direct/RU mutation;
- Trusted RU refresh;
- proxy apply;
- kill-switch rebuild;
- route/rule/nft/WG mutation.

## Success

The rehearsal succeeds when all are true:

- autoswitch apply authority is held for the whole window;
- no autoswitch process remains active;
- registry hash is stable;
- route/rule snapshots are stable;
- no switch-history entries appear;
- no production autoswitch planner writes happen;
- read-only checks complete;
- autoswitch authority is restored to the captured pre-hold state;
- no users moved.

## Failure

The rehearsal fails if any occur:

- autoswitch service starts during the window;
- registry, route, or rule snapshots drift unexpectedly;
- switch-history records movement;
- restore does not return timer/service state;
- any user movement occurs;
- any route/rule/nft/WG mutation occurs;
- checks cannot run within the maximum duration.

## Must Stay Untouched

- user assignments;
- route tables;
- ip rules;
- nftables;
- WireGuard configs;
- kill switch rules;
- egress state except normal read-only inspection outputs;
- Trusted RU/Direct/RU/policy/proxy runtime.

## Must Be Restored

- `v7-users-autoswitch.timer` state;
- `v7-users-autoswitch.service` non-running state;
- Telegram sentinel timer/service state if captured;
- operator awareness of whether any hold command failed.

## Maximum Duration

Recommended rehearsal window:

```text
max_duration=10 minutes
quiet_observation=90 seconds
```

The hold should not be left active after the rehearsal.

## Blast Radius

Holding autoswitch authority affects all users by pausing automated movement. It should not affect existing datapath if no routing/user mutation is executed.

## Current Rehearsal Status

```text
CONDITIONAL
```

The plan is ready for approval review. It is not approved or executed by this document.
