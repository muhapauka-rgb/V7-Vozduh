# Autoswitch Hold Governance

This is a dry operational model only. No autoswitch timer/service was stopped, disabled, masked, restarted, or edited during this block.

## Current Binding

Sampled authority from Block E2:

```text
v7-users-autoswitch.timer: active/enabled
v7-users-autoswitch.service: static/inactive at sample time
timer cadence: OnUnitActiveSec=20s
service command: /usr/local/bin/v7-users-autoswitch --apply
```

Telegram sentinel is also part of the influence surface:

```text
v7-telegram-sentinel.timer: active/enabled
service command: /usr/local/bin/v7-telegram-sentinel --threshold-seconds 14 --timeout 1
```

Sentinel state reported `started=false` for the sampled instant, but authority exists and can change with later signals.

## Autoswitch Write Behavior

Autoswitch is not harmless even when no user move happens:

- it can write load/reconnect/safety summaries;
- it maintains anti-flap and penalty state;
- with `--apply`, it can call `v7-user-switch`;
- it can move more than one user per run within policy limits;
- timer cadence is short enough to interfere with manual observation.

## Safest Future Hold Model

The safest future hold is a separately approved, bounded maintenance hold around autoswitch authority:

1. Capture current timer/service status.
2. Capture autoswitch safety state and candidate user penalty state.
3. Hold the autoswitch apply timer for the canary window.
4. Confirm no autoswitch service instance is currently running.
5. Keep read-only observability checks available.
6. Run the one-user canary only if all GO criteria pass.
7. Run post-checks and rollback if needed.
8. Restore the previous autoswitch timer state after the window.
9. Capture final timer/service status and autoswitch safety state.

This document does not prescribe a live command. The hold command itself is runtime mutation and needs explicit approval at execution time.

## Hold Blast Radius

Holding autoswitch affects all users because automatic failover/rebalance would be paused. This is safer for a one-user canary than allowing concurrent automated user movement, but it is still a platform-wide operational change.

## What Must Remain Running

- kill switch protections;
- existing routing/datapath;
- current egress interfaces;
- read-only health and route checks;
- admin visibility.

## What Must Not Run During Canary Window

- `v7-users-autoswitch --apply`;
- `v7-user-switch` for any user except the approved canary user;
- `v7-routing-sync`;
- policy apply;
- Direct/RU mutation;
- proxy runtime apply;
- Trusted RU refresh/decision execution.

## Confirm Autoswitch Inactive

Future pre-checks must confirm:

- autoswitch timer cannot fire during the canary window;
- no autoswitch service process is active;
- no recent autoswitch switch event occurred after the hold began;
- candidate user anti-flap state is stable and understood.

## Restore Model

Restoration must be explicit and verified:

- restore previous timer state only after post-checks;
- verify timer state matches the captured pre-hold state;
- confirm autoswitch does not immediately move the canary user back;
- retain rollback evidence and canary outcome.

## Verdict

Autoswitch hold is required before live canary, but applying the hold is not approved by this block.
