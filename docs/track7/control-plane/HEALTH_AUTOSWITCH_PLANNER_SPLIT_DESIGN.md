# Health / Autoswitch Planner Split Design

Block: E8.3.

Mode: repo-side design only.

No live runtime mutation was performed.

## Problem

Current runtime `v7-health.service` contains both health/state summary work and
autoswitch planner invocation:

```text
v7-health.service
  -> while true:
     v7-egress-history
     v7-egress-stability
     v7-egress-load
     v7-egress-diagnose
     v7-state-merge
     v7-user-desired-state-save
     v7-state-json-save
     v7-users-autoswitch
     sleep 30
```

This creates an authority boundary problem:

```text
stopping v7-users-autoswitch.timer/service does not stop autoswitch planner/state writes
stopping v7-health.service pauses unrelated health/state updates
quiet-window attribution is impossible while the combined loop is active
```

## Design Goal

Split health observation from autoswitch planning:

```text
v7-health.service
  -> health/history/stability/load/state merge/json save only
  -> no v7-users-autoswitch

v7-autoswitch-planner.service/timer
  -> v7-users-autoswitch without --apply
  -> planner/state authority only

v7-users-autoswitch.timer/service
  -> v7-users-autoswitch --apply
  -> apply authority only
```

## Proposed Unit Files

Draft files:

```text
systemd/drafts/v7-health.service
systemd/drafts/v7-autoswitch-planner.service
systemd/drafts/v7-autoswitch-planner.timer
```

These are not deployed by E8.3.

## Proposed Authority Boundaries

| Authority | Unit | Command | Can Move Users? | Can Write State? | Hold Boundary |
|---|---|---|---|---|---|
| health/state summary | `v7-health.service` | health/history/load/state commands only | no | yes, health/state summaries | keep running during quiet-window |
| autoswitch planner | `v7-autoswitch-planner.timer/service` | `v7-users-autoswitch` | no direct apply | yes, planner/load/reconnect state | hold for quiet-window |
| autoswitch apply | `v7-users-autoswitch.timer/service` | `v7-users-autoswitch --apply` | yes | yes, user movement and logs | hold for quiet-window |
| admin/manual | API or shell | autoswitch/user-switch/routing-sync | depends on command | depends on command | operator freeze |
| sentinel-capable | sentinel invocation without `--no-autoswitch` | autoswitch apply capable | possible | possible | verify inactive or `--no-autoswitch` |

## Health Service Draft

The health service keeps the 30-second loop but removes `v7-users-autoswitch`.

Health-only loop:

```text
v7-egress-history
v7-egress-stability
v7-egress-load
v7-egress-diagnose
v7-state-merge
v7-user-desired-state-save
v7-state-json-save
sleep 30
```

Expected behavior:

```text
health summaries continue during quiet-window
autoswitch planner state does not churn from health service
datapath remains unaffected
```

Ordering:

```text
After=network-online.target v7-routing-sync.service
```

The draft intentionally does not include `Wants=v7-routing-sync.service`.
Ordering without `Wants` avoids starting `v7-routing-sync.service` as a side
effect of starting `v7-health.service`.

## Autoswitch Planner Draft

Planner service:

```text
ExecStart=/usr/local/bin/v7-users-autoswitch
```

Timer:

```text
OnBootSec=2min
OnUnitActiveSec=30s
AccuracySec=5s
```

Expected behavior:

```text
planner keeps existing non-apply cadence
planner can be stopped independently for quiet-window
apply authority remains separate in v7-users-autoswitch.timer/service
```

## Apply Authority Remains Separate

Existing apply unit remains conceptually unchanged:

```text
v7-users-autoswitch.timer
  -> v7-users-autoswitch.service
    -> /usr/local/bin/v7-users-autoswitch --apply
```

This remains the user movement authority. It must still be held for rehearsal or
canary.

## Quiet-Window After Split

After successful deploy and post-deploy authority mapping, a quiet-window can
hold only:

```text
v7-autoswitch-planner.timer
v7-autoswitch-planner.service
v7-users-autoswitch.timer
v7-users-autoswitch.service
```

`v7-health.service` should remain active.

Quiet-window success criteria after split:

```text
v7-health.service active
v7-autoswitch-planner.timer inactive during hold
v7-autoswitch-planner.service inactive during hold
v7-users-autoswitch.timer inactive during hold
v7-users-autoswitch.service inactive during hold
no v7-users-autoswitch process
no v7-user-switch process
no v7-routing-sync process
registry hash stable
route/rule snapshots stable
reconcile sampled under quiet
```

## Design Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Unit split deployed incorrectly | health or planner cadence changes | deploy from exact draft files, capture before/after evidence |
| Planner timer forgotten | planner state no longer refreshes | verify timer enabled/active after deploy |
| Health unit still has old drop-in | restore/start may keep routing-sync coupling | audit `/etc/systemd/system/v7-health.service.d/*` before deploy |
| Apply and planner authority confused | quiet-window still noisy | post-deploy authority mapping required |
| Planner writes remain non-quiet | expected, but now holdable | hold planner timer/service during quiet-window |

## Deployment Status

```text
design_ready_for_review=true
deploy_performed=false
runtime_mutation_performed=NO
canary_status=NO-GO
execution_allowed_now=False
```
