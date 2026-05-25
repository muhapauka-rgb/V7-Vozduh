# Quiet-Window Rehearsal Sequence

This document defines the ordered live rehearsal sequence for a future quiet-window observation. It is governance only. The sequence was not executed in Block E7.

## Objective

Temporarily hold autoswitch authority, observe whether the control plane becomes quiet, evaluate reconcile behavior under that quiet window, and restore autoswitch authority. The rehearsal does not move users and does not change routing.

## Absolute Non-Goals

Do not run:

```text
v7-user-switch
v7-routing-sync
v7-users-autoswitch --apply
v7-policy-apply
v7-trusted-ru-refresh-missing
v7-proxy-runtime-guard-apply
```

Do not modify:

```text
ip route
ip rule
nftables
WireGuard configs
/opt/v7 state except bounded evidence files
/etc/v7
kill switch rules
```

## Ordered Sequence

### 1. Pre-Rehearsal Validation

Run only after explicit human approval for rehearsal.

```bash
export V7_QW_TS="$(date -u +%Y%m%dT%H%M%SZ)"
export V7_QW_DIR="/root/v7-quiet-window-$V7_QW_TS"
mkdir -p "$V7_QW_DIR"
systemctl is-active v7-users-autoswitch.timer v7-users-autoswitch.service > "$V7_QW_DIR/systemctl-active.before.txt" 2>&1 || true
systemctl is-enabled v7-users-autoswitch.timer v7-users-autoswitch.service > "$V7_QW_DIR/systemctl-enabled.before.txt" 2>&1 || true
systemctl list-timers --all 'v7-users-autoswitch*' > "$V7_QW_DIR/timers.before.txt" 2>&1 || true
pgrep -a -f 'v7-users-autoswitch|v7-user-switch|v7-routing-sync' > "$V7_QW_DIR/processes.before.txt" 2>&1 || true
sha256sum /opt/v7/egress/state/users.registry > "$V7_QW_DIR/users-registry.before.sha256"
ip -4 rule show > "$V7_QW_DIR/ip-rules.before.txt"
ip -4 route show table all > "$V7_QW_DIR/routes-all.before.txt"
tail -n 40 /opt/v7/events/switch-history.jsonl > "$V7_QW_DIR/switch-history.before.txt" 2>/dev/null || true
```

Validation points:

- evidence directory exists;
- autoswitch pre-state captured;
- no `v7-user-switch` or `v7-routing-sync` process is already active;
- registry, routes, rules, and switch history are captured.

Abort before hold if `v7-user-switch` or `v7-routing-sync` is active.

### 2. Autoswitch Hold Sequence

```bash
systemctl stop v7-users-autoswitch.timer
systemctl stop v7-users-autoswitch.service
```

Validation immediately after hold:

```bash
systemctl is-active v7-users-autoswitch.timer v7-users-autoswitch.service > "$V7_QW_DIR/systemctl-active.hold.txt" 2>&1 || true
systemctl list-timers --all 'v7-users-autoswitch*' > "$V7_QW_DIR/timer.hold.txt" 2>&1 || true
pgrep -a -f 'v7-users-autoswitch|v7-user-switch|v7-routing-sync' > "$V7_QW_DIR/processes.hold.txt" 2>&1 || true
```

Abort if autoswitch remains active or any user/routing mutation process appears.

### 3. Quiet-Window Observation

```bash
sleep 90
sha256sum /opt/v7/egress/state/users.registry > "$V7_QW_DIR/users-registry.quiet.sha256"
ip -4 rule show > "$V7_QW_DIR/ip-rules.quiet.txt"
ip -4 route show table all > "$V7_QW_DIR/routes-all.quiet.txt"
tail -n 40 /opt/v7/events/switch-history.jsonl > "$V7_QW_DIR/switch-history.quiet.txt" 2>/dev/null || true
pgrep -a -f 'v7-users-autoswitch|v7-user-switch|v7-routing-sync' > "$V7_QW_DIR/processes.quiet.txt" 2>&1 || true
```

Stable means:

- registry hash unchanged;
- no new switch-history movement;
- route and rule snapshots show no unexplained drift;
- no autoswitch/user-switch/routing-sync process appears.

### 4. Reconcile Verification

```bash
v7-reconcile-check > "$V7_QW_DIR/reconcile.1.txt" 2>&1; echo "rc=$?" >> "$V7_QW_DIR/reconcile.1.txt"
ip -4 rule show > "$V7_QW_DIR/ip-rules.after-reconcile-1.txt"
sleep 10
v7-reconcile-check > "$V7_QW_DIR/reconcile.2.txt" 2>&1; echo "rc=$?" >> "$V7_QW_DIR/reconcile.2.txt"
ip -4 rule show > "$V7_QW_DIR/ip-rules.after-reconcile-2.txt"
```

Stable means repeated reconcile output is consistent and rule snapshots do not drift during the checks.

### 5. Route / Rule Verification

```bash
cmp -s "$V7_QW_DIR/users-registry.before.sha256" "$V7_QW_DIR/users-registry.quiet.sha256"; echo "registry_hash_cmp_rc=$?" > "$V7_QW_DIR/registry-hash-compare.txt"
diff -u "$V7_QW_DIR/ip-rules.before.txt" "$V7_QW_DIR/ip-rules.quiet.txt" > "$V7_QW_DIR/ip-rules.before-vs-quiet.diff" 2>&1 || true
diff -u "$V7_QW_DIR/routes-all.before.txt" "$V7_QW_DIR/routes-all.quiet.txt" > "$V7_QW_DIR/routes.before-vs-quiet.diff" 2>&1 || true
```

Diffs are evidence. They are not automatically repair instructions.

### 6. Datapath Verification

```bash
v7-user-route-check > "$V7_QW_DIR/user-route-check.txt" 2>&1; echo "rc=$?" >> "$V7_QW_DIR/user-route-check.txt"
v7-killswitch-check > "$V7_QW_DIR/killswitch-check.txt" 2>&1; echo "rc=$?" >> "$V7_QW_DIR/killswitch-check.txt"
v7-provisioning-reconcile-check > "$V7_QW_DIR/provisioning-reconcile-check.txt" 2>&1; echo "rc=$?" >> "$V7_QW_DIR/provisioning-reconcile-check.txt"
```

These are read-only checks for the rehearsal. Any warning is evidence for review, not permission to repair.

### 7. Abort Conditions

Abort immediately and restore autoswitch if any occur:

- autoswitch process reappears;
- user-switch or routing-sync process appears;
- registry hash changes unexpectedly;
- switch-history shows user movement;
- route/rule snapshot drift cannot be explained;
- kill switch check warns or fails;
- restore uncertainty appears;
- operator cannot complete the sequence inside the approved window.

### 8. Restore Sequence

```bash
systemctl start v7-users-autoswitch.timer
```

Do not manually start the service unless pre-hold evidence proves it was active and the operator separately approves.

### 9. Post-Restore Verification

```bash
systemctl is-active v7-users-autoswitch.timer v7-users-autoswitch.service > "$V7_QW_DIR/systemctl-active.after.txt" 2>&1 || true
systemctl is-enabled v7-users-autoswitch.timer v7-users-autoswitch.service > "$V7_QW_DIR/systemctl-enabled.after.txt" 2>&1 || true
systemctl list-timers --all 'v7-users-autoswitch*' > "$V7_QW_DIR/timers.after.txt" 2>&1 || true
pgrep -a -f 'v7-users-autoswitch|v7-user-switch|v7-routing-sync' > "$V7_QW_DIR/processes.after.txt" 2>&1 || true
sha256sum /opt/v7/egress/state/users.registry > "$V7_QW_DIR/users-registry.after.sha256"
ip -4 rule show > "$V7_QW_DIR/ip-rules.after.txt"
ip -4 route show table all > "$V7_QW_DIR/routes-all.after.txt"
tail -n 40 /opt/v7/events/switch-history.jsonl > "$V7_QW_DIR/switch-history.after.txt" 2>/dev/null || true
```

The rehearsal is not complete until restore state is verified and the evidence packet is preserved.
