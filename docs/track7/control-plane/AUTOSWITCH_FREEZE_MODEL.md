# Autoswitch Freeze Model

This document describes a future hold/freeze model only. No timer or service was stopped, disabled, masked, restarted, or edited.

## Safest Hold Sequence

1. Announce a one-user canary maintenance window.
2. Capture current `v7-users-autoswitch.timer` and `v7-users-autoswitch.service` state.
3. Capture Telegram sentinel timer/service state.
4. Capture autoswitch safety, reconnect, load, and switch-history state.
5. Apply a separately approved hold that prevents `v7-users-autoswitch --apply` from firing.
6. Confirm no autoswitch process is active.
7. Observe at least 2 timer periods plus 10 seconds.
8. Confirm registry, rule, route, and switch-history stability.
9. Open the one-user canary window.
10. Close the window after post-checks or rollback.
11. Restore the exact prior autoswitch timer/service state.
12. Verify autoswitch did not immediately move the canary user after restore.

## Pre-Hold Checks

- current timer enabled/active state;
- service static/running state;
- current policy switch mode and limits;
- current candidate assignment;
- current autoswitch safety state;
- current switch-history tail;
- current route/rule snapshots.

## Hold Confirmation

The hold is confirmed only when:

- the timer cannot start an apply run during the window;
- no service process is active;
- no admin autoswitch apply is in progress;
- no user-switch operation is in progress;
- quiet observation interval completes without movement.

## Canary Window Rules

During the window:

- only the approved one-user switch may run;
- no routing-sync fallback;
- no autoswitch dry-run with production state paths;
- no policy/Direct/RU/proxy/kill-switch mutation;
- rollback is allowed only for the approved canary user.

## Restore Verification

After restore:

- timer state equals pre-hold state;
- service is not stuck active;
- no immediate switch loop occurs;
- candidate user's final assignment is expected;
- switch-history explains all moves in the window.

## Partial Hold Risk

A partial hold is worse than no hold if one authority path remains active. The hold plan must account for systemd timer, admin apply endpoint, direct CLI use, and channel-scoped apply UI actions.

## What Must Remain Running

- datapath;
- kill switch;
- existing egress interfaces;
- read-only checks;
- admin visibility.

## What Must Not Be Touched

- routing tables;
- ip rules;
- nftables;
- WireGuard configs;
- runtime registries except through the future approved one-user action;
- policy apply state.
