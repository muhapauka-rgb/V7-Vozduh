# Rehearsal Restore Guarantees

Restore is as critical as the hold. This document defines restore requirements for a future quiet-window rehearsal. It was not executed in Block E7.

## Required Restore Order

1. Stop observation.
2. Capture final quiet evidence.
3. Start autoswitch timer.
4. Verify timer state.
5. Verify service state.
6. Verify no orphan mutation process.
7. Capture route/rule/registry snapshots.
8. Preserve evidence directory.

## Exact Restore Command

```bash
systemctl start v7-users-autoswitch.timer
```

Do not manually start `v7-users-autoswitch.service` unless pre-hold evidence proves it was active and operator approval explicitly includes service restore.

## Post-Restore Checks

```bash
systemctl is-active v7-users-autoswitch.timer v7-users-autoswitch.service > "$V7_QW_DIR/systemctl-active.after.txt" 2>&1 || true
systemctl is-enabled v7-users-autoswitch.timer v7-users-autoswitch.service > "$V7_QW_DIR/systemctl-enabled.after.txt" 2>&1 || true
systemctl list-timers --all 'v7-users-autoswitch*' > "$V7_QW_DIR/timers.after.txt" 2>&1 || true
pgrep -a -f 'v7-users-autoswitch|v7-user-switch|v7-routing-sync' > "$V7_QW_DIR/processes.after.txt" 2>&1 || true
sha256sum /opt/v7/egress/state/users.registry > "$V7_QW_DIR/users-registry.after.sha256"
ip -4 rule show > "$V7_QW_DIR/ip-rules.after.txt"
ip -4 route show table all > "$V7_QW_DIR/routes-all.after.txt"
```

## Restore Success

Restore succeeds only if:

- timer state matches intended restored authority;
- service is not unexpectedly active;
- no orphan `v7-user-switch` or `v7-routing-sync` process exists;
- registry hash did not change from approved evidence expectations;
- route/rule snapshots show no rehearsal-caused mutation;
- evidence directory contains before/hold/quiet/after captures.

## Partial Restore

Partial restore means:

- timer cannot be started;
- timer starts but does not appear in `list-timers`;
- service enters failed state;
- orphan mutation process remains;
- operator cannot verify restored authority.

Partial restore blocks canary discussion. The operator must preserve evidence and escalate before any other control-plane action.

## Failure Handling

```bash
systemctl status v7-users-autoswitch.timer v7-users-autoswitch.service --no-pager > "$V7_QW_DIR/systemctl-status.restore-failure.txt" 2>&1 || true
systemctl list-timers --all 'v7-users-autoswitch*' > "$V7_QW_DIR/timers.restore-failure.txt" 2>&1 || true
pgrep -a -f 'v7-users-autoswitch|v7-user-switch|v7-routing-sync' > "$V7_QW_DIR/processes.restore-failure.txt" 2>&1 || true
```

Do not compensate with routing, user-switch, policy, proxy, kill-switch, or rollback commands unless a separate emergency approval is issued.
