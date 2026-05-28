# Rehearsal Restore Guarantees

Restore is as critical as the hold. This document defines restore requirements for a future quiet-window rehearsal. It was not executed in Block E7 or E8.2.

Block E8.1 proved that a complete restore must include `v7-health.service` if Option A full-authority hold is approved.

## Required Restore Order

1. Stop observation.
2. Capture final quiet evidence.
3. Start `v7-health.service`.
4. Verify `v7-health.service` state.
5. Start autoswitch timer.
6. Verify timer state.
7. Verify autoswitch service state.
8. Verify no orphan mutation process.
9. Capture route/rule/registry snapshots.
10. Preserve evidence directory.

## Exact Restore Command

```bash
systemctl start v7-health.service
systemctl start v7-users-autoswitch.timer
```

Do not manually start `v7-users-autoswitch.service` unless pre-hold evidence proves it was active and operator approval explicitly includes service restore.

Restore caveat:

```text
v7-health.service has Wants/After relationship with v7-routing-sync.service.
The approved packet must treat any restore-time routing-sync process as an attribution event and block canary promotion.
```

## Post-Restore Checks

```bash
systemctl is-active v7-users-autoswitch.timer v7-users-autoswitch.service > "$V7_QW_DIR/systemctl-active.after.txt" 2>&1 || true
systemctl is-enabled v7-users-autoswitch.timer v7-users-autoswitch.service > "$V7_QW_DIR/systemctl-enabled.after.txt" 2>&1 || true
systemctl is-active v7-health.service > "$V7_QW_DIR/v7-health-active.after.txt" 2>&1 || true
systemctl is-enabled v7-health.service > "$V7_QW_DIR/v7-health-enabled.after.txt" 2>&1 || true
systemctl show v7-health.service --property=ActiveState,SubState,MainPID,ExecMainPID,ControlGroup,Wants,After > "$V7_QW_DIR/v7-health-show.after.txt" 2>&1 || true
systemctl list-timers --all 'v7-users-autoswitch*' > "$V7_QW_DIR/timers.after.txt" 2>&1 || true
pgrep -a -f 'v7-users-autoswitch|v7-user-switch|v7-routing-sync|v7-health' > "$V7_QW_DIR/processes.after.txt" 2>&1 || true
sha256sum /opt/v7/egress/state/users.registry > "$V7_QW_DIR/users-registry.after.sha256"
ip -4 rule show > "$V7_QW_DIR/ip-rules.after.txt"
ip -4 route show table all > "$V7_QW_DIR/routes-all.after.txt"
```

## Restore Success

Restore succeeds only if:

- `v7-health.service` state matches intended restored authority;
- timer state matches intended restored authority;
- service is not unexpectedly active;
- no orphan `v7-user-switch` or `v7-routing-sync` process exists;
- no unapproved restore-time `v7-routing-sync` process appears;
- registry hash did not change from approved evidence expectations;
- route/rule snapshots show no rehearsal-caused mutation;
- evidence directory contains before/hold/quiet/after captures.

## Partial Restore

Partial restore means:

- timer cannot be started;
- timer starts but does not appear in `list-timers`;
- `v7-health.service` cannot be started;
- `v7-health.service` starts but immediately fails or restarts repeatedly;
- service enters failed state;
- orphan mutation process remains;
- restore appears to start or depend on unapproved routing-sync;
- operator cannot verify restored authority.

Partial restore blocks canary discussion. The operator must preserve evidence and escalate before any other control-plane action.

## Failure Handling

```bash
systemctl status v7-users-autoswitch.timer v7-users-autoswitch.service v7-health.service --no-pager > "$V7_QW_DIR/systemctl-status.restore-failure.txt" 2>&1 || true
systemctl show v7-health.service --property=ActiveState,SubState,Result,MainPID,NRestarts,Wants,After > "$V7_QW_DIR/v7-health-show.restore-failure.txt" 2>&1 || true
systemctl list-timers --all 'v7-users-autoswitch*' > "$V7_QW_DIR/timers.restore-failure.txt" 2>&1 || true
pgrep -a -f 'v7-users-autoswitch|v7-user-switch|v7-routing-sync|v7-health' > "$V7_QW_DIR/processes.restore-failure.txt" 2>&1 || true
```

Do not compensate with routing, user-switch, policy, proxy, kill-switch, or rollback commands unless a separate emergency approval is issued.
