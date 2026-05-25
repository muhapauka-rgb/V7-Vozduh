# Control Plane Risk Matrix

This matrix is governance only. It does not approve execution of mutation tools.

| Layer | Risk | Blast Radius | Rollback Clarity | Canary Allowed? |
|---|---|---|---|---|
| autoswitch | automated user movement through `v7-user-switch --apply` path | potentially many users over repeated timer runs | partial; depends on switch history and previous assignments | no, must be held first |
| routing-sync | registry-wide route/rule mutation | all enabled users in `users.registry` | weak without full route/rule snapshot | no first mutation |
| user-switch | one user registry/assignment/route mutation | one user if autoswitch held and no routing-sync fallback | clear for switch-back to previous egress | conditional future canary only |
| Trusted RU | Gosuslugi-sensitive diagnostic/decision influence | route-class and downstream policy influence | unclear; state refresh/decision can be stale | no live refresh/decision in canary |
| policy apply | route/policy state and possible systemd/apply effects | route classes or broader runtime | partial, depends on policy backup/rollback | no |
| Direct/RU | route-class/domain mutation | route classes, possibly many users | partial; depends on domain/state backups | no |
| proxy runtime | proxy/public/runtime guard mutation | public ingress/proxy paths, possibly users | partial; rollback tools exist but are not fully proven | no |
| kill switch | leak guard rebuild/removal | whole datapath | high impact; rollback depends on prior ruleset | no during canary except emergency approval |
| rollback tools | restore configs/state from backups | target-dependent, can be broad | tool-specific; not universally proven | only as pre-approved rollback for named action |

## Current Canary Status

```text
NO-GO
```

The only plausible future canary layer is `user-switch` for one named user, after autoswitch hold, reconcile explanation, target readiness, and rollback readiness.
