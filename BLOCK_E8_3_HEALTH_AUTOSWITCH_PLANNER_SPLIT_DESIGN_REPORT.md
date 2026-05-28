# Block E8.3 - Health / Autoswitch Planner Split Design Report

Mode: repo-side design only.

Live mutation: forbidden and not performed.

## 1. What Was Designed

E8.3 prepares the durable Option B path from E8.2: split `v7-health.service`
from autoswitch planner authority.

Current runtime shape:

```text
v7-health.service
  -> health/history/load/state work
  -> v7-users-autoswitch without --apply
```

Proposed runtime shape:

```text
v7-health.service
  -> health/history/load/state work only

v7-autoswitch-planner.timer/service
  -> v7-users-autoswitch without --apply

v7-users-autoswitch.timer/service
  -> v7-users-autoswitch --apply
```

## 2. Repo Artifacts Created

Design docs:

```text
docs/track7/control-plane/HEALTH_AUTOSWITCH_PLANNER_SPLIT_DESIGN.md
docs/track7/control-plane/HEALTH_AUTOSWITCH_SPLIT_MIGRATION_PLAN.md
```

Draft unit files:

```text
systemd/drafts/v7-health.service
systemd/drafts/v7-autoswitch-planner.service
systemd/drafts/v7-autoswitch-planner.timer
```

Evidence index:

```text
docs/track7/control-plane/e8_3-evidence/README.md
```

## 3. Future Runtime Files Affected By Deploy

Future deploy would touch:

```text
/etc/systemd/system/v7-health.service
/etc/systemd/system/v7-autoswitch-planner.service
/etc/systemd/system/v7-autoswitch-planner.timer
/etc/systemd/system/v7-health.service.d/10-routing-order.conf
```

Existing `v7-users-autoswitch.timer/service` remains the apply authority and is
not replaced by the split. It must still be held for any future quiet-window.

## 4. Future Behavior After Split

Expected after approved deploy:

```text
v7-health.service remains active for health/state summaries
v7-health.service no longer calls v7-users-autoswitch
v7-autoswitch-planner.timer runs v7-users-autoswitch without --apply
v7-users-autoswitch.timer continues to run v7-users-autoswitch --apply
quiet-window can hold planner+apply without stopping health
```

## 5. Rollback Model

Rollback is documented in:

```text
docs/track7/control-plane/HEALTH_AUTOSWITCH_SPLIT_MIGRATION_PLAN.md
```

Rollback requires:

```text
stop v7-autoswitch-planner.timer/service
restore backed-up /etc/systemd/system/v7-health.service
restore backed-up /etc/systemd/system/v7-health.service.d if present
systemctl daemon-reload
restart v7-health.service
start v7-users-autoswitch.timer
verify process/rule/route/registry evidence
```

Rollback is not live-proven yet because no deploy was performed.

## 6. Design Risks

| Risk | Status |
|---|---|
| health service still starts routing-sync through old drop-in | must be audited during deploy |
| planner timer forgotten or disabled | covered by verification commands |
| old health loop still contains autoswitch | explicit post-deploy check required |
| apply authority confused with planner authority | authority mapping required after deploy |
| deployment changes runtime systemd | requires separate approval |

## 7. Is Design Ready For Separate Deploy Approval?

```text
YES
```

It is ready for review as a deploy proposal because it includes:

```text
draft unit files
pre-deploy evidence
backup commands
deploy commands
verification commands
rollback commands
abort conditions
expected runtime behavior
```

It is not approved for deployment by E8.3.

## 8. Canary Status

```text
current_canary_status=NO-GO
quiet_window_verified=false
execution_allowed_now=False
```

Why unchanged:

```text
split design is not deployed
post-split authority mapping is not done
quiet-window rehearsal has not succeeded
reconcile-under-quiet has not been sampled
```

## 9. Can We Move To E8.4 After Deploy?

Yes, after a separately approved split deploy, the next logical block is:

```text
E8.4 post-split authority mapping
```

E8.4 should prove:

```text
v7-health.service is health-only
v7-autoswitch-planner.timer/service owns non-apply planner authority
v7-users-autoswitch.timer/service owns apply authority
no hidden autoswitch authority remains
quiet-window can be attempted by holding planner+apply only
```

## 10. Exact Next Recommended Step

Recommended:

```text
Review E8.3 split design and decide whether to approve a separate deploy block.
```

Next block should not be a canary. It should be either:

```text
E8.4 split deploy approval and execution
```

or:

```text
additional design review for v7-health.service drop-in and routing-sync ordering
```

## 11. Mutation Statement

```text
Runtime mutation performed: NO
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed: NO
Deploy performed: NO
```
