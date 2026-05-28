# Health / Autoswitch Planner Split Migration Plan

Block: E8.3.

Mode: repo-side plan only.

No deploy was performed.

## Purpose

This plan describes a future approved deployment that splits the combined
`v7-health.service` loop into:

```text
v7-health.service = health/state summary only
v7-autoswitch-planner.service/timer = planner/state refresh only
v7-users-autoswitch.service/timer = apply authority only
```

## Files Affected By Future Deploy

Future runtime files:

```text
/etc/systemd/system/v7-health.service
/etc/systemd/system/v7-autoswitch-planner.service
/etc/systemd/system/v7-autoswitch-planner.timer
/etc/systemd/system/v7-health.service.d/10-routing-order.conf
```

Repo draft sources:

```text
systemd/drafts/v7-health.service
systemd/drafts/v7-autoswitch-planner.service
systemd/drafts/v7-autoswitch-planner.timer
```

Important:

```text
the existing v7-health.service drop-in must be audited before deploy
the future split should avoid Wants=v7-routing-sync.service on v7-health.service
```

## Pre-Deploy Evidence

Future approved commands:

```bash
export V7_SPLIT_TS="$(date -u +%Y%m%dT%H%M%SZ)"
export V7_SPLIT_DIR="/root/v7-health-autoswitch-split-$V7_SPLIT_TS"
mkdir -p "$V7_SPLIT_DIR"

date -u > "$V7_SPLIT_DIR/date.txt"
hostname > "$V7_SPLIT_DIR/hostname.txt"
systemctl cat v7-health.service > "$V7_SPLIT_DIR/v7-health.cat.before.txt" 2>&1 || true
systemctl show v7-health.service --property=Id,ActiveState,SubState,UnitFileState,MainPID,ExecMainPID,ControlGroup,Restart,Wants,After,ExecStart > "$V7_SPLIT_DIR/v7-health.show.before.txt" 2>&1 || true
systemctl cat v7-users-autoswitch.service v7-users-autoswitch.timer > "$V7_SPLIT_DIR/v7-users-autoswitch.cat.before.txt" 2>&1 || true
systemctl list-timers --all 'v7*autoswitch*' > "$V7_SPLIT_DIR/autoswitch-timers.before.txt" 2>&1 || true
pgrep -a -f 'v7-users-autoswitch|v7-user-switch|v7-routing-sync|v7-health' > "$V7_SPLIT_DIR/processes.before.txt" 2>&1 || true
sha256sum /opt/v7/egress/state/users.registry > "$V7_SPLIT_DIR/users-registry.before.sha256" 2>&1 || true
ip -4 rule show > "$V7_SPLIT_DIR/ip-rules.before.txt"
ip -4 route show table all > "$V7_SPLIT_DIR/routes-all.before.txt"
```

## Backup Commands

Future approved commands:

```bash
mkdir -p "$V7_SPLIT_DIR/backups"
cp -a /etc/systemd/system/v7-health.service "$V7_SPLIT_DIR/backups/v7-health.service.before" 2>/dev/null || true
cp -a /etc/systemd/system/v7-health.service.d "$V7_SPLIT_DIR/backups/v7-health.service.d.before" 2>/dev/null || true
cp -a /etc/systemd/system/v7-autoswitch-planner.service "$V7_SPLIT_DIR/backups/v7-autoswitch-planner.service.before" 2>/dev/null || true
cp -a /etc/systemd/system/v7-autoswitch-planner.timer "$V7_SPLIT_DIR/backups/v7-autoswitch-planner.timer.before" 2>/dev/null || true
cp -a /etc/systemd/system/v7-users-autoswitch.service "$V7_SPLIT_DIR/backups/v7-users-autoswitch.service.before" 2>/dev/null || true
cp -a /etc/systemd/system/v7-users-autoswitch.timer "$V7_SPLIT_DIR/backups/v7-users-autoswitch.timer.before" 2>/dev/null || true
```

## Deploy Commands

Future approved commands only:

```bash
install -m 0644 systemd/drafts/v7-health.service /etc/systemd/system/v7-health.service
install -m 0644 systemd/drafts/v7-autoswitch-planner.service /etc/systemd/system/v7-autoswitch-planner.service
install -m 0644 systemd/drafts/v7-autoswitch-planner.timer /etc/systemd/system/v7-autoswitch-planner.timer

systemctl daemon-reload
systemctl enable v7-health.service
systemctl enable v7-autoswitch-planner.timer
systemctl restart v7-health.service
systemctl start v7-autoswitch-planner.timer
```

Drop-in handling:

```text
If /etc/systemd/system/v7-health.service.d/10-routing-order.conf contains Wants=v7-routing-sync.service,
future deployment must either remove that coupling with explicit approval or replace it with a reviewed no-Wants ordering model.
Do not silently leave a drop-in that reintroduces routing-sync start coupling.
```

## Verification Commands

Future approved read-only verification:

```bash
systemctl is-active v7-health.service v7-autoswitch-planner.timer v7-users-autoswitch.timer > "$V7_SPLIT_DIR/systemctl-active.after.txt" 2>&1 || true
systemctl is-enabled v7-health.service v7-autoswitch-planner.timer v7-users-autoswitch.timer > "$V7_SPLIT_DIR/systemctl-enabled.after.txt" 2>&1 || true
systemctl cat v7-health.service > "$V7_SPLIT_DIR/v7-health.cat.after.txt" 2>&1 || true
systemctl cat v7-autoswitch-planner.service v7-autoswitch-planner.timer > "$V7_SPLIT_DIR/v7-autoswitch-planner.cat.after.txt" 2>&1 || true
systemctl list-timers --all 'v7*autoswitch*' > "$V7_SPLIT_DIR/autoswitch-timers.after.txt" 2>&1 || true
pgrep -a -f 'v7-users-autoswitch|v7-user-switch|v7-routing-sync|v7-health' > "$V7_SPLIT_DIR/processes.after.txt" 2>&1 || true
sha256sum /opt/v7/egress/state/users.registry > "$V7_SPLIT_DIR/users-registry.after.sha256" 2>&1 || true
ip -4 rule show > "$V7_SPLIT_DIR/ip-rules.after.txt"
ip -4 route show table all > "$V7_SPLIT_DIR/routes-all.after.txt"
v7-user-route-check > "$V7_SPLIT_DIR/user-route-check.after.txt" 2>&1; echo "rc=$?" >> "$V7_SPLIT_DIR/user-route-check.after.txt"
v7-killswitch-check > "$V7_SPLIT_DIR/killswitch-check.after.txt" 2>&1; echo "rc=$?" >> "$V7_SPLIT_DIR/killswitch-check.after.txt"
v7-provisioning-reconcile-check > "$V7_SPLIT_DIR/provisioning-reconcile-check.after.txt" 2>&1; echo "rc=$?" >> "$V7_SPLIT_DIR/provisioning-reconcile-check.after.txt"
```

Expected after deploy:

```text
v7-health.service active and no longer contains v7-users-autoswitch
v7-autoswitch-planner.timer active/enabled
v7-autoswitch-planner.service inactive except brief oneshot runs
v7-users-autoswitch.timer remains separate apply authority
no v7-user-switch process
no unexpected v7-routing-sync process
users.registry hash stable unless separately explained
route/rule snapshots stable unless separately explained
```

## Rollback Commands

Future approved rollback:

```bash
systemctl stop v7-autoswitch-planner.timer
systemctl stop v7-autoswitch-planner.service

cp -a "$V7_SPLIT_DIR/backups/v7-health.service.before" /etc/systemd/system/v7-health.service
if [ -d "$V7_SPLIT_DIR/backups/v7-health.service.d.before" ]; then
  rm -rf /etc/systemd/system/v7-health.service.d
  cp -a "$V7_SPLIT_DIR/backups/v7-health.service.d.before" /etc/systemd/system/v7-health.service.d
fi

systemctl daemon-reload
systemctl restart v7-health.service
systemctl start v7-users-autoswitch.timer
```

Rollback verification:

```bash
systemctl is-active v7-health.service v7-users-autoswitch.timer > "$V7_SPLIT_DIR/systemctl-active.rollback.txt" 2>&1 || true
systemctl cat v7-health.service > "$V7_SPLIT_DIR/v7-health.cat.rollback.txt" 2>&1 || true
pgrep -a -f 'v7-users-autoswitch|v7-user-switch|v7-routing-sync|v7-health' > "$V7_SPLIT_DIR/processes.rollback.txt" 2>&1 || true
sha256sum /opt/v7/egress/state/users.registry > "$V7_SPLIT_DIR/users-registry.rollback.sha256" 2>&1 || true
ip -4 rule show > "$V7_SPLIT_DIR/ip-rules.rollback.txt"
ip -4 route show table all > "$V7_SPLIT_DIR/routes-all.rollback.txt"
```

## Abort Conditions

Abort deployment and restore from backup if any occur:

```text
v7-health.service fails to start
v7-health.service still contains v7-users-autoswitch after deploy
v7-autoswitch-planner.timer cannot be enabled/started
v7-users-autoswitch --apply runs unexpectedly
v7-user-switch appears
v7-routing-sync appears unexpectedly
users.registry changes unexpectedly
ip rules or route tables drift unexpectedly
kill switch check fails or worsens
operator cannot verify unit contents
```

## Expected Runtime Behavior After Successful Split

```text
health summaries continue from v7-health.service
autoswitch planner runs from v7-autoswitch-planner.timer/service
autoswitch apply remains in v7-users-autoswitch.timer/service
future quiet-window can hold planner+apply timers without stopping health
canary remains NO-GO until post-split authority mapping and quiet-window rehearsal succeed
```

## E8.3 Status

```text
design_ready_for_deploy_approval=true
deploy_performed=false
runtime_mutation_performed=NO
execution_allowed_now=False
current_canary_status=NO-GO
```

## E8.4 Deployment Result

E8.4 executed the bounded systemd split deploy.

Evidence:

```text
docs/track7/control-plane/e8_4-evidence/pre-deploy.txt
docs/track7/control-plane/e8_4-evidence/backup-manifest.txt
docs/track7/control-plane/e8_4-evidence/deploy-output.txt
docs/track7/control-plane/e8_4-evidence/post-deploy-authority.txt
docs/track7/control-plane/e8_4-evidence/post-deploy-process-guard-clean.txt
docs/track7/control-plane/e8_4-evidence/post-deploy-safety.txt
```

Result:

```text
deploy_success=true
rollback_performed=false
v7-health.service_health_only=true
planner_authority_separated=true
apply_authority_unchanged=true
users_registry_changed=false
egress_registry_changed=false
user_movement_observed=false
routing_drift_observed=false
kill_switch_ok=true
user_route_check_ok=true
provisioning_reconcile_ok=true
reconcile_result_after_deploy=FAIL
```

Runtime files changed by E8.4:

```text
/etc/systemd/system/v7-health.service
/etc/systemd/system/v7-autoswitch-planner.service
/etc/systemd/system/v7-autoswitch-planner.timer
/etc/systemd/system/v7-health.service.d/10-routing-order.conf
```

Runtime backups:

```text
/root/v7-e84-systemd-split-20260525T123450Z/backups/
```

Canary remains blocked:

```text
current_canary_status=NO-GO
quiet_window_verified=false
execution_allowed_now=False
```
