# Autoswitch Canary Interference Review

## Current Authority

Autoswitch is live-authoritative in the sampled state:

```text
v7-users-autoswitch.timer: active/enabled
v7-users-autoswitch.service: static/inactive at sample time
timer cadence: OnUnitActiveSec=20s
service command: /usr/local/bin/v7-users-autoswitch --apply
```

Telegram sentinel is also active in the sampled system:

```text
v7-telegram-sentinel.timer: active/enabled
service command: /usr/local/bin/v7-telegram-sentinel --threshold-seconds 14 --timeout 1
```

The sentinel state reported `started=false` with reason `no_blocked_egress_or_no_healthy_target`, but the timer/service authority remains present.

## Interference Risks

- Autoswitch can move users through `v7-user-switch` while a canary is being observed.
- Autoswitch state shows most enabled users recently moved twice in one hour and ten times in 24 hours.
- Current penalty windows extend into 2026-05-25T02:02-02:05Z.
- Load summary is produced by `v7-users-autoswitch`, so autoswitch is already an active decision source.
- A concurrent autoswitch move would invalidate canary attribution: a route change could be caused by autoswitch, manual canary, or both.

## Required Future Hold

Before any live canary, there must be a separately approved autoswitch hold plan. At minimum:

- confirm `v7-users-autoswitch.timer` cannot run during the canary window;
- confirm Telegram sentinel cannot trigger autoswitch movement during the canary window;
- capture autoswitch safety state before and after;
- restore the previous autoswitch authority only after post-checks.

This document does not apply that hold. Applying a hold would itself be a runtime operation requiring explicit approval.

## Verdict

Autoswitch interference is currently a **NO-GO** blocker.
