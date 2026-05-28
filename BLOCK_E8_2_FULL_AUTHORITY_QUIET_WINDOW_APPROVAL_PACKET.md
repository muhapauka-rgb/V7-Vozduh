# Block E8.2 - Full-Authority Quiet-Window Approval Packet

Mode: read-only / planning only.

Live mutation: forbidden and not performed.

## 1. Purpose

Block E8.1 proved that autoswitch authority is larger than the original
`v7-users-autoswitch.timer/service` pair. A future quiet-window rehearsal must
also account for `v7-health.service`, admin/manual launch paths, and
sentinel-capable invocation paths.

E8.2 does not execute a quiet-window. It prepares the approval packet needed to
decide whether E8.3 should run a bounded full-authority quiet-window rehearsal.

## 2. Current Authority Truth

Known autoswitch authorities:

```text
1. v7-users-autoswitch.timer/service
   -> /usr/local/bin/v7-users-autoswitch --apply

2. v7-health.service
   -> every 30 seconds:
      v7-egress-history
      v7-egress-stability
      v7-egress-load
      v7-egress-diagnose
      v7-state-merge
      v7-user-desired-state-save
      v7-state-json-save
      v7-users-autoswitch

3. Admin/API endpoints
   -> autoswitch plan/dry-run/apply guarded
   -> user-switch action paths

4. Manual shell invocation
   -> v7-users-autoswitch
   -> v7-users-autoswitch --apply
   -> v7-user-switch
   -> v7-routing-sync

5. Sentinel-capable code path
   -> current unit uses --no-autoswitch
   -> alternate invocation without --no-autoswitch remains capable
```

The E8.1 loop is intentional runtime service behavior:

```text
v7-health.service enabled
Restart=always
PPID=1
cgroup=/system.slice/v7-health.service
```

## 3. Full Hold Model

A full quiet-window hold must suppress all autoswitch/user-movement authorities
for a short observation window.

Authorities to hold or freeze:

```text
v7-users-autoswitch.timer
v7-users-autoswitch.service
v7-health.service autoswitch planner loop
admin autoswitch/user-switch actions
manual shell autoswitch/user-switch/routing-sync actions
sentinel invocation without --no-autoswitch
```

Authorities that remain forbidden:

```text
v7-user-switch
v7-routing-sync
v7-users-autoswitch --apply
v7-policy-apply
v7-policy-resolve
v7-direct-add-domain
v7-direct-remove-domain
v7-direct-auto-sync
v7-trusted-ru-diagnostic
v7-trusted-ru-refresh-missing
v7-proxy-runtime-guard-apply
v7-proxy-public-enable
v7-proxy-public-disable
v7-killswitch-enable
v7-killswitch-disable-temporary
```

## 4. Option A - Bounded Temporary Hold

Option A is a future approved live rehearsal that temporarily holds the systemd
apply authority and `v7-health.service`.

Future hold commands, not executed in E8.2:

```bash
systemctl stop v7-users-autoswitch.timer
systemctl stop v7-users-autoswitch.service
systemctl stop v7-health.service
```

Future restore commands, not executed in E8.2:

```bash
systemctl start v7-health.service
systemctl start v7-users-autoswitch.timer
```

Expected duration:

```text
2 to 5 minutes maximum
```

### What Stops During Option A

```text
v7-egress-history
v7-egress-stability
v7-egress-load
v7-egress-diagnose
v7-state-merge
v7-user-desired-state-save
v7-state-json-save
v7-users-autoswitch planner invocation
v7-users-autoswitch --apply timer path
```

### What Must Continue To Be True

```text
datapath remains on already-applied routes/rules
no users are moved
users.registry hash remains stable
switch-history remains stable
ip rules remain stable
route tables remain stable
kill switch remains OK
user-route-check remains OK
provisioning reconcile does not worsen
```

### Option A Risks

| Risk | Why It Matters | Mitigation |
|---|---|---|
| health summaries pause | operator UI and planner inputs can become stale | keep hold to 2-5 minutes |
| load/reconnect state pauses | autoswitch may lack fresh context after restore | collect pre/post snapshots |
| `v7-health.service` restore has `Wants/After` relationship with `v7-routing-sync.service` | restore may create attribution confusion if routing-sync appears | treat any routing-sync process as abort/no-canary evidence |
| admin/manual actions remain possible | human action can invalidate quiet-window evidence | explicit operator freeze |
| apply timer may fire after restore | expected restored authority, but not part of quiet-window evidence | restore only after final quiet evidence |

### Option A GO Conditions

All must be true:

```text
operator explicitly approves holding v7-health.service
operator explicitly approves restoring v7-health.service
admin/manual freeze is active
no v7-user-switch process before hold
no v7-routing-sync process before hold
pre-hold route/rule/registry/switch-history evidence captured
kill switch check is OK or known unchanged from E8 evidence
restore-time routing-sync attribution risk is accepted or ruled out
abort conditions are accepted
maximum duration is approved
```

### Option A NO-GO Conditions

Any one blocks Option A:

```text
operator does not approve v7-health.service hold
v7-routing-sync is active before hold
v7-user-switch is active before hold
admin/manual freeze cannot be guaranteed
restore-time v7-routing-sync risk is unacceptable
kill switch/user route/provisioning checks fail before hold
operator cannot complete restore inside approved duration
```

### Option A Verdict

```text
operationally possible
governance risk: medium-high
best use: immediate truth finding when refactor cannot wait
not approved by E8.2
```

## 5. Option B - Split/Refactor First

Option B is a design path before any new live quiet-window rehearsal.

Target design:

```text
v7-health.service
  -> health/history/stability/load/state merge only

v7-autoswitch-planner.service/timer
  -> v7-users-autoswitch without --apply

v7-users-autoswitch.timer/service
  -> v7-users-autoswitch --apply
```

### Option B Benefits

```text
health updates can continue during future quiet-window
autoswitch planner can be held independently
apply authority remains independently holdable
restore no longer requires stopping broad health service
quiet-window evidence is easier to attribute
```

### Option B Risks

```text
requires runtime design and deployment
requires unit rollback plan
requires post-deploy authority mapping
can introduce service-ordering bugs if rushed
does not produce immediate reconcile-under-quiet evidence
```

### Option B GO Conditions

```text
repo design reviewed
unit split reviewed
rollback for unit split documented
deploy approval granted separately
post-deploy tests include authority mapping and quiet-window dry evidence
```

### Option B Verdict

```text
preferred durable path
requires separate design/deploy approval
not a live action in E8.2
```

## 6. Abort Conditions For Future E8.3

Abort immediately and restore if any occur:

```text
v7-users-autoswitch process appears during quiet observation
v7-health.service remains active after hold
v7-health loop process reappears during quiet observation
v7-user-switch appears
v7-routing-sync appears
users.registry hash changes unexpectedly
switch-history receives new user movement
ip rule snapshot drifts unexpectedly
route table snapshot drifts unexpectedly
v7-killswitch-check fails or worsens
v7-user-route-check fails or worsens
v7-provisioning-reconcile-check worsens
restore uncertainty appears
operator cannot finish inside approved duration
```

## 7. Evidence Required For Future E8.3

Before hold:

```text
date -u
systemctl show/cat/is-active/is-enabled for v7-health.service
systemctl show/cat/is-active/is-enabled/list-timers for v7-users-autoswitch.*
pgrep for autoswitch/user-switch/routing-sync/health
users.registry sha256
switch-history snapshot
ip -4 rule show
ip -4 route show table all
v7-reconcile-check
v7-user-route-check
v7-killswitch-check
v7-provisioning-reconcile-check
```

During quiet-window:

```text
2 to 3 repeated samples
no autoswitch/user-switch/routing-sync/health loop process
stable registry hash
stable switch-history
stable ip rules
stable route tables
reconcile repeated samples
datapath checks
```

After restore:

```text
v7-health.service active
v7-users-autoswitch.timer active
no unexpected v7-user-switch or v7-routing-sync process
registry/rules/routes/switch-history captured
restore status preserved
```

## 8. E8.2 Governance Updates

Updated:

```text
docs/track7/control-plane/FULL_AUTOSWITCH_HOLD_MODEL.md
docs/track7/control-plane/QUIET_WINDOW_REHEARSAL_SEQUENCE.md
docs/track7/control-plane/REHEARSAL_ABORT_CONDITIONS.md
docs/track7/control-plane/REHEARSAL_RESTORE_GUARANTEES.md
docs/track7/control-plane/CANARY_GO_NO_GO.md
docs/track7/control-plane/CONTROL_PLANE_RISK_MATRIX.md
```

Created:

```text
docs/track7/control-plane/e8_2-evidence/README.md
```

## 9. Current Status

```text
current_canary_status=NO-GO
quiet_window_verified=false
execution_allowed_now=False
reconcile_under_quiet=NOT_SAMPLED_WITH_FULL_AUTHORITY_HOLD
```

## 10. Can E8.3 Full Quiet-Window Rehearsal Be Done Safely?

Answer:

```text
CONDITIONAL
```

E8.3 can be considered only if the operator explicitly approves Option A and
accepts the `v7-health.service` hold/restore scope. Without that approval, E8.3
is NO-GO.

## 11. Which Variant Is Better?

Best durable path:

```text
Option B: split/refactor health loop and autoswitch planner first
```

Best immediate truth-finding path:

```text
Option A: bounded temporary hold, only with explicit approval
```

Recommendation:

```text
Choose Option B if schedule allows.
Choose Option A only if reconcile-under-quiet evidence is needed before design/refactor work.
```

## 12. Exact Next Recommended Step

Recommended:

```text
Prepare a repo-side design proposal for splitting v7-health.service from autoswitch planner authority.
```

Conditional alternative:

```text
Request explicit E8.3 approval for Option A:
bounded temporary hold of v7-health.service plus v7-users-autoswitch.timer/service,
2 to 5 minutes maximum,
no canary,
no routing-sync,
no user-switch,
restore immediately after evidence collection.
```

## 13. Mutation Statement

```text
Runtime mutation performed: NO
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed: NO
```
