# Block E8.1 - Non-Systemd Autoswitch Authority Mapping Report

Mode: strictly read-only.

Live mutation: forbidden and not performed.

## 1. Current Authority Truth

Block E8 found an autoswitch loop that survived `v7-users-autoswitch.timer` and `v7-users-autoswitch.service` hold:

```text
/bin/bash -c while true; do v7-egress-history; v7-egress-stability; v7-egress-load; v7-egress-diagnose; v7-state-merge; v7-user-desired-state-save; v7-state-json-save; v7-users-autoswitch; sleep 30; done
```

Block E8.1 identified the exact authority:

```text
v7-health.service
```

The process is:

```text
PID=2938206
PPID=1
SID=2938206
TTY=?
USER=root
STARTED=Sat May 9 00:56:10 2026
cgroup=/system.slice/v7-health.service
MainPID of v7-health.service=2938206
```

Therefore the earlier "non-systemd autoswitch loop" should now be understood as:

```text
not controlled by v7-users-autoswitch.timer/service,
but systemd-supervised through v7-health.service
```

## 2. Exact Autoswitch Authorities

### Direct apply authority

```text
v7-users-autoswitch.timer
  -> v7-users-autoswitch.service
    -> /usr/local/bin/v7-users-autoswitch --apply
```

Properties:

```text
timer active/enabled
OnUnitActiveSec=20s
service Type=oneshot
service ExecStart=/usr/local/bin/v7-users-autoswitch --apply
```

### Health-loop planner authority

```text
v7-health.service
  -> /bin/bash -c 'while true; do ... v7-users-autoswitch; sleep 30; done'
```

Properties:

```text
service active/enabled
Type=simple
Restart=always
RestartSec=5
MainPID=2938206
loop interval=30 seconds
```

This invocation does not use `--apply`, but the current source can still write planner/load/reconnect state.

### Admin authority

Repo static evidence:

```text
/api/autoswitch-plan -> v7-users-autoswitch --pretty
/api/actions/autoswitch-dry-run -> v7-users-autoswitch --pretty
/api/actions/autoswitch-apply-guarded -> v7-users-autoswitch --mode guarded --apply --pretty
manual user-switch endpoints -> v7-user-switch
```

### Telegram sentinel authority

Current systemd unit:

```text
ExecStart=/usr/local/bin/v7-telegram-sentinel --threshold-seconds 14 --timeout 1 --no-autoswitch
```

Current verdict:

```text
not an active autoswitch launcher through current unit
```

Residual risk:

```text
tool code can run v7-users-autoswitch --apply if invoked without --no-autoswitch
```

## 3. Exact Launch Chain

```text
PID 1 systemd
  -> v7-health.service
    -> PID 2938206 /bin/bash -c 'while true; do ... v7-users-autoswitch; sleep 30; done'
```

No cron/tmux/screen/at/profile startup origin was found:

```text
root crontab: no crontab
cron grep: no matching authority
tmux: no socket
screen: no sockets
rc/profile grep: no matching launch hook
```

The launch is persistent because:

```text
v7-health.service UnitFileState=enabled
v7-health.service Restart=always
```

## 4. Whether Loop Is Intentional / Runtime-Critical

Verdict:

```text
intentional runtime service, not temporary shell debris
```

Evidence:

- installed live systemd unit explicitly contains the loop;
- unit is enabled;
- unit has `Restart=always`;
- process is the unit `MainPID`;
- cgroup is `system.slice/v7-health.service`;
- historical backups contain similar `v7-health.service` / `v7-health-loop` patterns.

Nuance:

```text
the health service is runtime-critical for current health/state updates,
but embedding autoswitch planner/state writes inside it is a quiet-window blocker
```

## 5. Whether Quiet Window Is Realistically Achievable

Yes, theoretically.

But not with the old E8 hold packet.

A realistic quiet window requires control of:

```text
v7-users-autoswitch.timer
v7-users-autoswitch.service
v7-health.service autoswitch planner loop
admin/operator autoswitch/user-switch paths
manual shell invocation paths
sentinel invocation without --no-autoswitch
```

The main new complication:

```text
holding v7-health.service is broader than autoswitch hold
```

It can pause:

```text
v7-egress-history
v7-egress-stability
v7-egress-load
v7-egress-diagnose
v7-state-merge
v7-user-desired-state-save
v7-state-json-save
```

It also has:

```text
Wants=v7-routing-sync.service
After=v7-routing-sync.service
```

So a future hold/restore packet must explicitly prevent unexpected routing-sync attribution confusion.

## 6. Whether Reconcile-Under-Quiet Can Now Be Attempted

Current answer:

```text
NO
```

Reason:

```text
authority is now mapped,
but full authority hold has not been approved or executed
```

It can be attempted only after:

1. a new explicit approval covers `v7-health.service` authority handling;
2. pre-hold evidence captures health/timer/admin/sentinel state;
3. hold model ensures no `v7-users-autoswitch`, `v7-user-switch`, or `v7-routing-sync` process exists;
4. restore model is explicit and separately verified.

## 7. Updated Canary Status

```text
current_canary_status=NO-GO
```

Reason:

```text
quiet_window_verified=false
reconcile_under_quiet=not sampled
autoswitch authority requires broader hold model
```

## 8. Updated Execution Allowed Now

```text
execution_allowed_now=False
```

Allowed now:

```text
read-only inspection
repo-side docs
static analysis
local tests
governance checks
```

Still forbidden:

```text
canary
user-switch
routing-sync
autoswitch apply
policy apply
Trusted RU refresh
Direct/RU mutation
proxy apply
kill switch mutation
systemctl stop/start/restart without separate approval
```

## 9. Exact Next Recommended Step

Prepare Block E8.2:

```text
FULL-AUTHORITY QUIET-WINDOW REHEARSAL APPROVAL PACKET
```

It must explicitly decide one of two paths:

1. approve a bounded `v7-health.service` hold in addition to autoswitch timer/service hold; or
2. first perform a separate runtime design/refactor to split autoswitch planning out of `v7-health.service`.

No canary should be discussed as executable until E8.2 succeeds.

## 10. Phase Tests And Verdicts

### Phase 1 - Process Truth

Test:

```text
pgrep, ps, pstree, /proc status/cmdline/cgroup, systemd-cgls
```

Result:

```text
PID 2938206 identified as v7-health.service MainPID
```

Verdict:

```text
PASS
```

### Phase 2 - File / Script Origin

Test:

```text
systemctl show/cat v7-health.service
command -v/stat target commands
grep runtime/repo/history/cron/profile origins
```

Result:

```text
origin is /etc/systemd/system/v7-health.service
```

Verdict:

```text
PASS
```

### Phase 3 - Autoswitch Authority Model

Test:

```text
systemd timer/service inspection + admin/sentinel/static call-site search
```

Result:

```text
autoswitch authorities mapped:
timer apply, health planner, admin API, sentinel-capable code path, manual shell
```

Verdict:

```text
PASS
```

### Phase 4 - Hold / Restore Feasibility

Test:

```text
static hold-model analysis
```

Result:

```text
full hold requires v7-health.service handling or unit split
```

Verdict:

```text
CONDITIONAL
```

### Phase 5 - Quiet Window Readiness

Test:

```text
authority map compared against quiet-window requirements
```

Result:

```text
old timer/service-only rehearsal cannot work
full rehearsal needs broader approval
```

Verdict:

```text
NO-GO for execution now
```

## 11. Runtime Mutation Verification

Read-only checks executed:

```text
systemctl show/cat/list/status-style inspection
pgrep/ps/pstree/proc/cgroup inspection
loginctl/systemctl --user inspection
crontab/cron/atq/tmux/screen inspection
grep/stat/command -v inspection
ip rule/route show
v7-user-route-check
v7-killswitch-check
v7-provisioning-reconcile-check
v7-reconcile-check
```

Mutation statement:

```text
Runtime mutation performed: NO
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed: NO
Canary performed: NO
```

## 12. Artifacts

```text
docs/track7/control-plane/NON_SYSTEMD_AUTOSWITCH_AUTHORITY_MAP.md
docs/track7/control-plane/FULL_AUTOSWITCH_HOLD_MODEL.md
docs/track7/control-plane/QUIET_WINDOW_BLOCKERS_REASSESSMENT.md
docs/track7/control-plane/e8_1-evidence/process-truth.txt
docs/track7/control-plane/e8_1-evidence/proc-details.txt
docs/track7/control-plane/e8_1-evidence/systemd-login-authority.txt
docs/track7/control-plane/e8_1-evidence/health-benchmark-origin.txt
docs/track7/control-plane/e8_1-evidence/cron-shell-history-authority.txt
docs/track7/control-plane/e8_1-evidence/file-origin-search.txt
docs/track7/control-plane/e8_1-evidence/mutation-verification-readonly.txt
```
