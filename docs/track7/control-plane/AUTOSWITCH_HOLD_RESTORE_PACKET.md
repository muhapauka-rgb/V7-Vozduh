# Autoswitch Hold / Restore Packet

These are exact future operational commands for a quiet-window rehearsal. They were not executed in Block E6.

## Preconditions

- Operator approval for rehearsal only.
- No canary approval implied.
- No user movement approval implied.
- Operator has console access if restore commands fail.

## 0. Set Evidence Directory

```bash
export V7_QW_TS="$(date -u +%Y%m%dT%H%M%SZ)"
export V7_QW_DIR="/root/v7-quiet-window-$V7_QW_TS"
mkdir -p "$V7_QW_DIR"
```

This writes evidence files under `/root`. It is acceptable only inside the approved rehearsal.

## 1. Pre-Hold Capture

```bash
systemctl is-active v7-users-autoswitch.timer v7-users-autoswitch.service v7-telegram-sentinel.timer v7-telegram-sentinel.service > "$V7_QW_DIR/systemctl-active.before.txt" 2>&1 || true
systemctl is-enabled v7-users-autoswitch.timer v7-users-autoswitch.service v7-telegram-sentinel.timer v7-telegram-sentinel.service > "$V7_QW_DIR/systemctl-enabled.before.txt" 2>&1 || true
systemctl list-timers --all 'v7-*' > "$V7_QW_DIR/timers.before.txt" 2>&1 || true
pgrep -a -f 'v7-users-autoswitch|v7-user-switch|v7-routing-sync' > "$V7_QW_DIR/processes.before.txt" 2>&1 || true
sha256sum /opt/v7/egress/state/users.registry > "$V7_QW_DIR/users-registry.before.sha256"
ip -4 rule show > "$V7_QW_DIR/ip-rules.before.txt"
ip -4 route show table all > "$V7_QW_DIR/routes-all.before.txt"
tail -n 40 /opt/v7/events/switch-history.jsonl > "$V7_QW_DIR/switch-history.before.txt" 2>/dev/null || true
cp -a /opt/v7/egress/state/autoswitch-safety.json "$V7_QW_DIR/autoswitch-safety.before.json" 2>/dev/null || true
cp -a /opt/v7/egress/state/client-reconnect-state.json "$V7_QW_DIR/client-reconnect-state.before.json" 2>/dev/null || true
cp -a /opt/v7/egress/state/egress-load-summary.json "$V7_QW_DIR/egress-load-summary.before.json" 2>/dev/null || true
```

## 2. Hold Autoswitch Apply Authority

```bash
systemctl stop v7-users-autoswitch.timer
systemctl stop v7-users-autoswitch.service
```

Do not disable or mask in the rehearsal unless a stop fails and the operator explicitly approves escalation.

## 3. Hold Verification

```bash
systemctl is-active v7-users-autoswitch.timer v7-users-autoswitch.service > "$V7_QW_DIR/systemctl-active.hold.txt" 2>&1 || true
systemctl list-timers --all 'v7-users-autoswitch*' > "$V7_QW_DIR/timer.hold.txt" 2>&1 || true
pgrep -a -f 'v7-users-autoswitch|v7-user-switch|v7-routing-sync' > "$V7_QW_DIR/processes.hold.txt" 2>&1 || true
```

Expected:

```text
v7-users-autoswitch.timer inactive
v7-users-autoswitch.service inactive
no v7-users-autoswitch process
no v7-user-switch process
no v7-routing-sync process
```

## 4. Quiet Observation

```bash
sleep 90
sha256sum /opt/v7/egress/state/users.registry > "$V7_QW_DIR/users-registry.quiet.sha256"
ip -4 rule show > "$V7_QW_DIR/ip-rules.quiet.txt"
ip -4 route show table all > "$V7_QW_DIR/routes-all.quiet.txt"
tail -n 40 /opt/v7/events/switch-history.jsonl > "$V7_QW_DIR/switch-history.quiet.txt" 2>/dev/null || true
pgrep -a -f 'v7-users-autoswitch|v7-user-switch|v7-routing-sync' > "$V7_QW_DIR/processes.quiet.txt" 2>&1 || true
```

## 5. Reconcile Experiment

```bash
v7-reconcile-check > "$V7_QW_DIR/reconcile.1.txt" 2>&1; echo "rc=$?" >> "$V7_QW_DIR/reconcile.1.txt"
ip -4 rule show > "$V7_QW_DIR/ip-rules.after-reconcile-1.txt"
v7-reconcile-check > "$V7_QW_DIR/reconcile.2.txt" 2>&1; echo "rc=$?" >> "$V7_QW_DIR/reconcile.2.txt"
ip -4 rule show > "$V7_QW_DIR/ip-rules.after-reconcile-2.txt"
v7-user-route-check > "$V7_QW_DIR/user-route-check.txt" 2>&1; echo "rc=$?" >> "$V7_QW_DIR/user-route-check.txt"
v7-killswitch-check > "$V7_QW_DIR/killswitch-check.txt" 2>&1; echo "rc=$?" >> "$V7_QW_DIR/killswitch-check.txt"
v7-provisioning-reconcile-check > "$V7_QW_DIR/provisioning-reconcile-check.txt" 2>&1; echo "rc=$?" >> "$V7_QW_DIR/provisioning-reconcile-check.txt"
```

## 6. Restore Autoswitch Authority

```bash
systemctl start v7-users-autoswitch.timer
```

Do not manually start `v7-users-autoswitch.service` unless the pre-hold state showed it was active and the operator explicitly approves.

## 7. Restore Verification

```bash
systemctl is-active v7-users-autoswitch.timer v7-users-autoswitch.service v7-telegram-sentinel.timer v7-telegram-sentinel.service > "$V7_QW_DIR/systemctl-active.after.txt" 2>&1 || true
systemctl is-enabled v7-users-autoswitch.timer v7-users-autoswitch.service v7-telegram-sentinel.timer v7-telegram-sentinel.service > "$V7_QW_DIR/systemctl-enabled.after.txt" 2>&1 || true
systemctl list-timers --all 'v7-*' > "$V7_QW_DIR/timers.after.txt" 2>&1 || true
pgrep -a -f 'v7-users-autoswitch|v7-user-switch|v7-routing-sync' > "$V7_QW_DIR/processes.after.txt" 2>&1 || true
sha256sum /opt/v7/egress/state/users.registry > "$V7_QW_DIR/users-registry.after.sha256"
ip -4 rule show > "$V7_QW_DIR/ip-rules.after.txt"
ip -4 route show table all > "$V7_QW_DIR/routes-all.after.txt"
tail -n 40 /opt/v7/events/switch-history.jsonl > "$V7_QW_DIR/switch-history.after.txt" 2>/dev/null || true
```

## 8. Failure Handling

If restore fails:

```bash
systemctl status v7-users-autoswitch.timer v7-users-autoswitch.service --no-pager
systemctl start v7-users-autoswitch.timer
systemctl list-timers --all 'v7-users-autoswitch*'
```

If a user moves during rehearsal:

```bash
do not run routing-sync
do not run user-switch
capture users.registry, switch-history, ip rules, and route tables
escalate to operator
```

## Explicit Non-Goals

Do not run:

```text
v7-user-switch
v7-routing-sync
v7-users-autoswitch --apply
v7-policy-apply
v7-trusted-ru-refresh-missing
v7-proxy-runtime-guard-apply
```
