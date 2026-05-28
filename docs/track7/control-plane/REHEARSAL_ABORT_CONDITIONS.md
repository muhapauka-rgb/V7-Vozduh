# Rehearsal Abort Conditions

This document defines when a future quiet-window rehearsal must stop immediately. It was not executed in Block E7 or E8.2.

Block E8.1 added `v7-health.service` to the autoswitch authority model. Future abort and restore handling must cover that service explicitly.

## Immediate Abort Conditions

Abort the rehearsal and restore autoswitch authority if any occur:

- `v7-users-autoswitch` process reappears during quiet observation;
- `v7-health.service` remains active after an approved full-authority hold;
- a `v7-health.service` loop process reappears during quiet observation;
- `v7-user-switch` appears at any point;
- `v7-routing-sync` appears at any point;
- `users.registry` hash changes unexpectedly;
- switch-history receives a new user movement entry;
- ip rule snapshot changes without an approved command;
- route table snapshot changes without an approved command;
- `v7-killswitch-check` warns or fails;
- `v7-user-route-check` warns or fails in a new way;
- `v7-provisioning-reconcile-check` worsens;
- reconcile output becomes less stable across samples;
- the timer cannot be restored confidently;
- `v7-health.service` cannot be restored confidently;
- restoring `v7-health.service` appears to start or require unapproved `v7-routing-sync`;
- the operator cannot finish within the approved duration.

## Abort Sequence

Do not run repair commands. Capture evidence and restore autoswitch authority:

```bash
date -u > "$V7_QW_DIR/abort.timestamp.txt"
pgrep -a -f 'v7-users-autoswitch|v7-user-switch|v7-routing-sync' > "$V7_QW_DIR/processes.abort.txt" 2>&1 || true
systemctl is-active v7-health.service > "$V7_QW_DIR/v7-health-active.abort.txt" 2>&1 || true
systemctl show v7-health.service --property=ActiveState,SubState,MainPID,ExecMainPID,ControlGroup,Wants,After > "$V7_QW_DIR/v7-health-show.abort.txt" 2>&1 || true
sha256sum /opt/v7/egress/state/users.registry > "$V7_QW_DIR/users-registry.abort.sha256"
ip -4 rule show > "$V7_QW_DIR/ip-rules.abort.txt"
ip -4 route show table all > "$V7_QW_DIR/routes-all.abort.txt"
tail -n 80 /opt/v7/events/switch-history.jsonl > "$V7_QW_DIR/switch-history.abort.txt" 2>/dev/null || true
systemctl start v7-health.service
systemctl start v7-users-autoswitch.timer
systemctl is-active v7-users-autoswitch.timer v7-users-autoswitch.service > "$V7_QW_DIR/systemctl-active.abort-restore.txt" 2>&1 || true
systemctl is-active v7-health.service > "$V7_QW_DIR/v7-health-active.abort-restore.txt" 2>&1 || true
systemctl list-timers --all 'v7-users-autoswitch*' > "$V7_QW_DIR/timers.abort-restore.txt" 2>&1 || true
```

The `systemctl start v7-health.service` line is part of a future approved
Option A rehearsal only. It was not executed in E8.2.

## Forbidden During Abort

Do not run:

```text
v7-routing-sync
v7-user-switch
v7-users-autoswitch --apply
v7-policy-apply
v7-killswitch-enable
v7-killswitch-disable-temporary
rollback tools
```

Abort is an evidence-and-restore action, not a repair window.

## Abort Classification

| Abort Cause | Classification | Next Step |
|---|---|---|
| autoswitch process reappears | hold failure | Review systemd/timer authority before retry. |
| health loop reappears | incomplete full-authority hold | No quiet-window attribution; review `v7-health.service` authority. |
| registry changes | hidden user movement | No canary; investigate switch source. |
| route/rule drift | hidden datapath mutation | No canary; investigate route authority. |
| kill switch warning | leak risk | No canary; separate safety review. |
| restore uncertainty | authority risk | Operator intervention before further testing. |
| restore starts routing-sync | restore attribution risk | No canary; split design or separate routing-sync approval required. |
