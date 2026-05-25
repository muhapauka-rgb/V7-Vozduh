# Autoswitch Hold Safety Model

This model defines the safest known live hold approach for a future quiet-window rehearsal. It was not executed in Block E7.

## Safety Principle

Hold only autoswitch authority. Do not touch routing, user assignment, policy, Direct/RU, proxy runtime, kill switch, or datapath state.

## Hold Components

| Component | Hold Action | Reason |
|---|---|---|
| `v7-users-autoswitch.timer` | stop during rehearsal | Prevent scheduled `--apply` launches. |
| `v7-users-autoswitch.service` | stop during rehearsal | End an active autoswitch run if one exists. |
| `v7-telegram-sentinel` | leave running unless separately approved | Sentinel is advisory unless evidence proves direct user movement. |
| routing/user tools | do not run | They are mutation tools, not part of rehearsal. |

## If Autoswitch Is Currently Running

The operator must capture active process evidence before hold:

```bash
pgrep -a -f 'v7-users-autoswitch|v7-user-switch|v7-routing-sync' > "$V7_QW_DIR/processes.before.txt" 2>&1 || true
systemctl status v7-users-autoswitch.service --no-pager > "$V7_QW_DIR/autoswitch-service.before.txt" 2>&1 || true
```

If `v7-user-switch` or `v7-routing-sync` is active, abort before hold. A concurrent mutation makes attribution impossible.

If only `v7-users-autoswitch` is active, the approved hold may stop the service, then must verify that no child user movement process remains:

```bash
systemctl stop v7-users-autoswitch.service
pgrep -a -f 'v7-users-autoswitch|v7-user-switch|v7-routing-sync' > "$V7_QW_DIR/processes.after-service-stop.txt" 2>&1 || true
```

## Timer Hold

```bash
systemctl stop v7-users-autoswitch.timer
```

Expected result:

```text
v7-users-autoswitch.timer inactive
no pending timer launch for v7-users-autoswitch
```

## Race Avoidance

Use this order:

1. capture active process state;
2. stop timer;
3. stop service;
4. verify timer inactive;
5. verify service inactive;
6. verify no autoswitch/user-switch/routing-sync process;
7. begin quiet observation only after verification.

This order prevents a new timer launch while service state is being checked.

## Planner Write Suppression

Autoswitch without apply may still write planner/load/reconnect state. During rehearsal, the autoswitch service and timer must be held so planner writes should stop. Normal non-autoswitch observability writes are not proof of failure unless they change canary attribution.

Evidence files to compare:

```text
/opt/v7/egress/state/autoswitch-safety.json
/opt/v7/egress/state/client-reconnect-state.json
/opt/v7/egress/state/egress-load-summary.json
/opt/v7/events/switch-history.jsonl
```

## Half-Held State

Half-held means one of these is true:

- timer remains active after stop;
- service remains active after stop;
- autoswitch process remains;
- timer stopped but restore evidence is missing;
- service stopped but an orphan child process remains.

Half-held state is a rehearsal failure. Restore timer authority and escalate; do not proceed to canary.

## Restore Guarantee

The rehearsal must restore the captured pre-hold timer authority:

```bash
systemctl start v7-users-autoswitch.timer
systemctl is-active v7-users-autoswitch.timer v7-users-autoswitch.service
systemctl list-timers --all 'v7-users-autoswitch*'
```

Do not start `v7-users-autoswitch.service` manually unless pre-hold evidence showed it active and the operator explicitly approves.
