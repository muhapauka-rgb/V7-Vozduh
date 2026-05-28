# Quiet-Window Rehearsal Sequence

This document defines the ordered live rehearsal sequence for a future quiet-window observation. It is governance only. The sequence was not executed in Block E7, E8.2, or E8.3.

## Objective

Temporarily hold full autoswitch authority, observe whether the control plane becomes quiet, evaluate reconcile behavior under that quiet window, and restore authority. The rehearsal does not move users and does not change routing.

Block E8.1 updated the authority map: `v7-health.service` also invokes `v7-users-autoswitch` every 30 seconds. A future rehearsal that holds only `v7-users-autoswitch.timer` and `v7-users-autoswitch.service` is incomplete.

Block E8.3 proposes a split design. If that split is deployed and verified, the
preferred rehearsal sequence changes from stopping `v7-health.service` to holding
the new planner timer/service while leaving health active.

Block E8.4 deployed and verified the split. Future rehearsal should use the
post-split sequence unless a later authority map shows regression.

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
systemctl is-active v7-health.service > "$V7_QW_DIR/v7-health-active.before.txt" 2>&1 || true
systemctl is-enabled v7-health.service > "$V7_QW_DIR/v7-health-enabled.before.txt" 2>&1 || true
systemctl show v7-health.service --property=Id,ActiveState,SubState,UnitFileState,MainPID,ExecMainPID,ControlGroup,Restart,RestartUSec,Wants,After,ExecStart > "$V7_QW_DIR/v7-health-show.before.txt" 2>&1 || true
systemctl cat v7-health.service > "$V7_QW_DIR/v7-health-cat.before.txt" 2>&1 || true
pgrep -a -f 'v7-users-autoswitch|v7-user-switch|v7-routing-sync' > "$V7_QW_DIR/processes.before.txt" 2>&1 || true
sha256sum /opt/v7/egress/state/users.registry > "$V7_QW_DIR/users-registry.before.sha256"
ip -4 rule show > "$V7_QW_DIR/ip-rules.before.txt"
ip -4 route show table all > "$V7_QW_DIR/routes-all.before.txt"
tail -n 40 /opt/v7/events/switch-history.jsonl > "$V7_QW_DIR/switch-history.before.txt" 2>/dev/null || true
```

Validation points:

- evidence directory exists;
- autoswitch pre-state captured;
- `v7-health.service` pre-state captured;
- no `v7-user-switch` or `v7-routing-sync` process is already active;
- registry, routes, rules, and switch history are captured.

Abort before hold if `v7-user-switch` or `v7-routing-sync` is active.

### 2A. Pre-Split Autoswitch Hold Sequence

This is a future command packet only. It applies only before the E8.3 split is
deployed. It requires explicit approval that names `v7-health.service`.

```bash
systemctl stop v7-users-autoswitch.timer
systemctl stop v7-users-autoswitch.service
systemctl stop v7-health.service
```

Validation immediately after hold:

```bash
systemctl is-active v7-users-autoswitch.timer v7-users-autoswitch.service > "$V7_QW_DIR/systemctl-active.hold.txt" 2>&1 || true
systemctl is-active v7-health.service > "$V7_QW_DIR/v7-health-active.hold.txt" 2>&1 || true
systemctl list-timers --all 'v7-users-autoswitch*' > "$V7_QW_DIR/timer.hold.txt" 2>&1 || true
pgrep -a -f 'v7-users-autoswitch|v7-user-switch|v7-routing-sync|v7-health' > "$V7_QW_DIR/processes.hold.txt" 2>&1 || true
```

Abort if autoswitch remains active, `v7-health.service` remains active, or any user/routing mutation process appears.

### 2B. Post-Split Autoswitch Hold Sequence

This is the preferred sequence after the E8.4 split deployment and post-deploy
authority mapping.

```bash
systemctl stop v7-autoswitch-planner.timer
systemctl stop v7-autoswitch-planner.service
systemctl stop v7-users-autoswitch.timer
systemctl stop v7-users-autoswitch.service
```

Validation immediately after hold:

```bash
systemctl is-active v7-health.service > "$V7_QW_DIR/v7-health-active.hold.txt" 2>&1 || true
systemctl is-active v7-autoswitch-planner.timer v7-autoswitch-planner.service > "$V7_QW_DIR/planner-active.hold.txt" 2>&1 || true
systemctl is-active v7-users-autoswitch.timer v7-users-autoswitch.service > "$V7_QW_DIR/apply-active.hold.txt" 2>&1 || true
pgrep -a -f 'v7-users-autoswitch|v7-user-switch|v7-routing-sync' > "$V7_QW_DIR/processes.hold.txt" 2>&1 || true
```

Abort if planner/apply authority remains active, if `v7-health.service` is not
active, or if any user/routing mutation process appears.

Block E8.5 executed this post-split sequence successfully. The corrected hold
evidence is `docs/track7/control-plane/e8_5-evidence/hold-confirmation-2.txt`.

Authoritative E8.5 result:

```text
planner/apply authority held=true
v7-health.service active=true
autoswitch_fully_quiet=true
quiet_window_verified=true
```

### 3. Quiet-Window Observation

```bash
sleep 90
sha256sum /opt/v7/egress/state/users.registry > "$V7_QW_DIR/users-registry.quiet.sha256"
ip -4 rule show > "$V7_QW_DIR/ip-rules.quiet.txt"
ip -4 route show table all > "$V7_QW_DIR/routes-all.quiet.txt"
tail -n 40 /opt/v7/events/switch-history.jsonl > "$V7_QW_DIR/switch-history.quiet.txt" 2>/dev/null || true
pgrep -a -f 'v7-users-autoswitch|v7-user-switch|v7-routing-sync|v7-health' > "$V7_QW_DIR/processes.quiet.txt" 2>&1 || true
```

Stable means:

- registry hash unchanged;
- no new switch-history movement;
- route and rule snapshots show no unexplained drift;
- no autoswitch/user-switch/routing-sync process appears.
- no `v7-health.service` loop process appears.

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

### 8A. Pre-Split Restore Sequence

This is a future command packet only. Restore must include the service that was
held before split.

```bash
systemctl start v7-health.service
systemctl start v7-users-autoswitch.timer
```

Do not manually start `v7-users-autoswitch.service` unless pre-hold evidence proves it was active and the operator separately approves.

Important restore caveat:

```text
v7-health.service has Wants/After relationship with v7-routing-sync.service.
The future approval must explicitly accept or rule out restore-time routing-sync activity before Option A is executed.
```

### 8B. Post-Split Restore Sequence

After the verified E8.4 split, restore should not need to restart
`v7-health.service`.

```bash
systemctl start v7-autoswitch-planner.timer
systemctl start v7-users-autoswitch.timer
```

Do not manually start either oneshot service unless pre-hold evidence proves it
was active and operator approval explicitly includes service restore.

Block E8.5 restored only timers:

```bash
systemctl start v7-autoswitch-planner.timer
systemctl start v7-users-autoswitch.timer
```

The timers fired normally after restore. No manual `v7-users-autoswitch --apply`
was executed, and settled evidence showed no registry hash change or new
switch-history movement.

### E8.5 Quiet-Window Evidence Result

```text
quiet_samples=A,B,C
users.registry stable=true
egress.registry stable=true
switch-history stable=true
ip rules stable=true
route tables stable=true
reconcile_under_quiet=STABLE_FAIL
user-route-check=OK
killswitch-check=OK
provisioning-reconcile-check=OK
```

This upgrades the sequence from planned to operationally proven for quiet
observation. It does not approve canary.

### E8.6 Reconcile Classification

E8.6 classified the E8.5 reconcile `STABLE_FAIL`:

```text
classification=CONFIRMED_FALSE_POSITIVE
failure_class=pipefail_grep_q_sigpipe
affected_check=missing ip rule lookup table
```

Future quiet-window/canary rehearsal packets should treat
`v7-reconcile-check` as advisory until the checker is fixed, or should include
an explicit one-user waiver for this confirmed false-positive class.

### E8.7 Reconcile Checker Fix

E8.7 fixed and deployed the checker semantics.

Post-fix result:

```text
V7_RECONCILE_RESULT=OK
```

Future quiet-window/canary packets should restore `v7-reconcile-check` as a hard
pre-check, but only after rerunning it inside the fresh approved window.

### 9. Post-Restore Verification

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
tail -n 40 /opt/v7/events/switch-history.jsonl > "$V7_QW_DIR/switch-history.after.txt" 2>/dev/null || true
```

The rehearsal is not complete until restore state is verified and the evidence packet is preserved.
