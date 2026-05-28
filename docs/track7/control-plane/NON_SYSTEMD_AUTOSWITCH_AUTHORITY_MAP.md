# Non-Systemd Autoswitch Authority Map

Block: E8.1.

Mode: strictly read-only.

Runtime mutation performed: NO.

## Scope

This document maps the autoswitch authority that invalidated Block E8 quiet-window rehearsal.

Block E8 observed this process:

```text
/bin/bash -c while true; do v7-egress-history; v7-egress-stability; v7-egress-load; v7-egress-diagnose; v7-state-merge; v7-user-desired-state-save; v7-state-json-save; v7-users-autoswitch; sleep 30; done
```

Block E8.1 inspected it without stopping it.

Evidence:

```text
docs/track7/control-plane/e8_1-evidence/process-truth.txt
docs/track7/control-plane/e8_1-evidence/proc-details.txt
docs/track7/control-plane/e8_1-evidence/systemd-login-authority.txt
docs/track7/control-plane/e8_1-evidence/health-benchmark-origin.txt
docs/track7/control-plane/e8_1-evidence/cron-shell-history-authority.txt
docs/track7/control-plane/e8_1-evidence/file-origin-search.txt
docs/track7/control-plane/e8_1-evidence/mutation-verification-readonly.txt
```

## Executive Truth

The E8 process is not a random shell left behind from logout.

It is the main process of the enabled systemd unit:

```text
v7-health.service
```

The earlier label "non-systemd autoswitch authority" was directionally correct because the process is not owned by `v7-users-autoswitch.timer` or `v7-users-autoswitch.service`. The more exact truth is:

```text
autoswitch authority also exists inside v7-health.service
```

That means stopping only `v7-users-autoswitch.timer` and `v7-users-autoswitch.service` cannot create a quiet window.

## Process Truth

Observed process:

```text
PID=2938206
PPID=1
SID=2938206
PGID=2938206
TTY=?
USER=root
STARTED=Sat May 9 00:56:10 2026
ELAPSED=16+ days at collection time
STAT=Ss
COMMAND=/bin/bash -c while true; do v7-egress-history; v7-egress-stability; v7-egress-load; v7-egress-diagnose; v7-state-merge; v7-user-desired-state-save; v7-state-json-save; v7-users-autoswitch; sleep 30; done
```

`/proc` evidence:

```text
Name=bash
State=S sleeping
PPid=1
Uid=0
Gid=0
cgroup=0::/system.slice/v7-health.service
cwd=/
exe=/usr/bin/bash
root=/
```

Parent:

```text
PID=1
COMMAND=/usr/lib/systemd/systemd --switched-root --system --deserialize=51
```

Verdict:

```text
process is supervised by systemd through v7-health.service
process has no TTY
process survives SSH logout
process survives command shell exit
process is expected to survive reboot because v7-health.service is enabled and Restart=always
```

## Exact Launch Chain

Observed `systemctl show v7-health.service` facts:

```text
Id=v7-health.service
Description=V7 Health Loop
ActiveState=active
SubState=running
FragmentPath=/etc/systemd/system/v7-health.service
DropInPaths=/etc/systemd/system/v7-health.service.d/10-routing-order.conf
UnitFileState=enabled
Type=simple
Restart=always
RestartUSec=5s
MainPID=2938206
ExecMainPID=2938206
ControlGroup=/system.slice/v7-health.service
```

Unit file:

```text
[Service]
Type=simple
ExecStart=/bin/bash -c 'while true; do v7-egress-history; v7-egress-stability; v7-egress-load; v7-egress-diagnose; v7-state-merge; v7-user-desired-state-save; v7-state-json-save; v7-users-autoswitch; sleep 30; done'
Restart=always
RestartSec=5
```

Launch chain:

```text
systemd PID 1
  -> v7-health.service
    -> /bin/bash -c 'while true; ... v7-users-autoswitch; sleep 30; done'
      -> every loop iteration:
         - v7-egress-history
         - v7-egress-stability
         - v7-egress-load
         - v7-egress-diagnose
         - v7-state-merge
         - v7-user-desired-state-save
         - v7-state-json-save
         - v7-users-autoswitch
         - sleep 30
```

## Direct Autoswitch Authorities

### Authority 1: `v7-users-autoswitch.timer`

Observed:

```text
v7-users-autoswitch.timer ActiveState=active
v7-users-autoswitch.timer UnitFileState=enabled
OnBootSec=2min
OnUnitActiveSec=20s
Unit=v7-users-autoswitch.service
```

Triggered service:

```text
v7-users-autoswitch.service
Type=oneshot
ExecStart=/usr/local/bin/v7-users-autoswitch --apply
```

Mutation level:

```text
runtime-user-movement-apply
```

Blast radius:

```text
bounded by autoswitch selected_moves and policy limits, but can still affect multiple users
```

Quiet-window impact:

```text
must be held for quiet-window rehearsal
```

### Authority 2: `v7-health.service`

Observed:

```text
v7-health.service ActiveState=active
v7-health.service UnitFileState=enabled
v7-health.service MainPID=2938206
```

Command:

```text
v7-users-autoswitch
```

without `--apply`.

Important behavior from current repo-side source:

```text
v7-users-autoswitch is read-only for user movement without --apply
but it is not fully no-write:
  - plan() calls _persist_dynamic_load_summary()
  - reconnect observation can write client-reconnect-state.json
```

Mutation level:

```text
state-write / planner-write / autoswitch-decision-influence
```

Direct user movement:

```text
not directly, because --apply is absent
```

Indirect authority:

```text
yes, because it writes load/reconnect/planner state that can influence later apply decisions and invalidates quiet-window attribution
```

Quiet-window impact:

```text
must be held or isolated for meaningful quiet-window observation
```

### Authority 3: Admin API autoswitch endpoints

Repo-side static evidence:

```text
/api/autoswitch-plan
/api/actions/autoswitch-dry-run
/api/actions/autoswitch-apply-guarded
```

Relevant commands:

```text
autoswitch plan/dry-run -> v7-users-autoswitch --pretty
autoswitch apply guarded -> v7-users-autoswitch --mode guarded --apply --pretty
```

Mutation level:

```text
plan/dry-run: planner/state-write risk
apply-guarded: runtime-user-movement-apply
```

Quiet-window impact:

```text
operator/admin action freeze is required during quiet-window and canary windows
```

### Authority 4: Telegram sentinel code path

Current repo-side unit:

```text
ExecStart=/usr/local/bin/v7-telegram-sentinel --threshold-seconds 14 --timeout 1 --no-autoswitch
```

Current unit verdict:

```text
current systemd service explicitly disables autoswitch launch
```

Tool code still contains a capable path:

```text
v7-users-autoswitch --mode guarded --apply --service telegram --route-class GLOBAL_STABLE --pretty
```

Historical event evidence shows previous sentinel events with autoswitch started.

Current authority level:

```text
not active through current unit because --no-autoswitch is present
```

Residual risk:

```text
manual or alternate invocation without --no-autoswitch can run autoswitch apply
```

## Indirect User Movement Authorities

### `v7-users-autoswitch --apply`

Repo-side source shows:

```text
apply() calls _run_switch()
_run_switch() runs ["v7-user-switch", ip, egress]
```

Therefore:

```text
v7-users-autoswitch --apply -> v7-user-switch -> users.registry / routing behavior
```

### Admin manual user switch

Repo-side static evidence:

```text
admin/v7-admin-api calls ["v7-user-switch", ip, target]
```

Mutation level:

```text
one-user live movement
```

### Routing sync authorities

Observed/repo-side authorities include:

```text
v7-routing-sync.service
hardening/v7-path-guard-repair
tools/runtime-support/v7-user-rotate-key
admin/API repair or reconcile action paths
```

`v7-health.service` has:

```text
Wants=v7-routing-sync.service
After=v7-routing-sync.service
```

This matters because stopping/starting `v7-health.service` may have service-order implications and may pull routing-sync into a future restore sequence unless separately controlled.

## Cron / Tmux / Screen / At Evidence

Collected evidence:

```text
root crontab: no crontab for root
cron files grep: no matching v7 autoswitch launch found
atq: command not found
tmux: no socket
screen: no sockets
rc/profile grep: no matching launch hook found
```

Verdict:

```text
no cron/tmux/screen/at/profile authority was found for the active loop
```

## File / Script Origin Evidence

Command locations:

```text
v7-users-autoswitch=/usr/local/bin/v7-users-autoswitch
v7-user-switch=/usr/local/bin/v7-user-switch
v7-routing-sync=/usr/local/bin/v7-routing-sync
v7-egress-history=/usr/local/bin/v7-egress-history
v7-egress-stability=/usr/local/bin/v7-egress-stability
v7-egress-load=/usr/local/bin/v7-egress-load
v7-egress-diagnose=/usr/local/bin/v7-egress-diagnose
v7-state-merge=/usr/local/bin/v7-state-merge
v7-user-desired-state-save=/usr/local/bin/v7-user-desired-state-save
v7-state-json-save=/usr/local/bin/v7-state-json-save
```

Historical backups contain earlier `v7-health.service` definitions with similar loops:

```text
/opt/v7/backups/*/v7-health.service
/opt/v7/legacy/bin/v7-health-loop
```

Verdict:

```text
the health loop is intentional runtime structure, not a transient shell alias
the autoswitch-in-health-loop design appears legacy-derived and currently installed in live systemd
```

## Authority Summary Table

| Authority | Launches autoswitch? | Uses `--apply`? | Writes state? | Can move users? | Must hold for quiet window? |
|---|---:|---:|---:|---:|---:|
| `v7-users-autoswitch.timer` -> service | yes | yes | yes | yes | yes |
| `v7-health.service` loop | yes | no | yes | no direct movement | yes |
| Admin `/api/actions/autoswitch-apply-guarded` | yes | yes | yes | yes | yes by operator freeze |
| Admin `/api/actions/autoswitch-dry-run` | yes | no | possible planner writes | no direct movement | yes by operator freeze |
| `v7-telegram-sentinel.service` current unit | no, because `--no-autoswitch` | no | sentinel writes only | no | monitor only |
| Manual shell invocation | possible | possible | possible | possible | yes by operator freeze |

## Phase Tests And Verdicts

### Phase 1 - Process Truth

Test:

```text
pgrep/ps/pstree/proc/cgroup inspection
```

Verdict:

```text
PASS
exact active loop PID and systemd cgroup identified
```

### Phase 2 - File / Script Origin

Test:

```text
command -v/stat/grep over runtime roots, history, cron, rc/profile hooks
```

Verdict:

```text
PASS
origin traced to v7-health.service, no cron/tmux/screen/profile origin found
```

### Phase 3 - Autoswitch Authority Model

Test:

```text
systemd unit inspection + repo static search for autoswitch/user-switch/routing-sync call sites
```

Verdict:

```text
PASS
direct and indirect authorities mapped
```

### Phase 4 - Hold / Restore Feasibility

Test:

```text
static feasibility analysis only
```

Verdict:

```text
CONDITIONAL
full hold is theoretically possible only if v7-health.service authority is included or split; not approved/executed in E8.1
```

### Phase 5 - Quiet Window Readiness

Test:

```text
current authority map compared against E8 quiet-window requirements
```

Verdict:

```text
NO-GO
quiet-window cannot be retried with timer/service-only hold
```

## Runtime Mutation Verification

Commands executed in E8.1 were read-only inspection/status/check commands.

```text
Runtime mutation performed: NO
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed: NO
Canary performed: NO
```
