# E11.9 Multi-Theory Postmortem Matrix

| theory | result | evidence |
|---|---|---|
| existing users can drain cleanly | YES | all 10 approved WireGuard users switched to target `1` with `switch_rc=0` |
| autoswitch will not immediately reassign users back | YES | three post-restore samples kept WireGuard users at `0` |
| reservation enforcement truly works | YES | planner continued blocking WireGuard with `canary_reserved_production_assignment_blocked` |
| drain targets are healthy | YES | target `1` diagnose OK, route_get OK, runtime checks OK |
| no hidden rebalance path exists | YES | selected moves stayed `0`; no hidden movement observed |
| no stale planner cache | YES | post-drain dry-runs reflected WireGuard users `0` |
| no routing-sync interference | YES | no `v7-routing-sync` process observed |
| no delayed restore side effects | YES | observation A/B/C showed no new WireGuard assignment and no selected moves |
| no kill-switch/routing regressions | YES | `v7-killswitch-check` and `v7-user-route-check` remained OK |
| no settle-window violations | YES | apply restored only after selected moves `0`; post-restore samples stayed clean |
| no hidden apply path | YES | apply timer restored after gate; no manual `--apply`; selected moves remained `0` |
| no capacity overload after drain | YES | target `1` reached 10 users, within dynamic hard/failover limits |
| no policy conflict | YES | reservation block and manual drain semantics coexisted; no new WG candidates selected |
| no target readiness regression | YES | post-drain target readiness selected WireGuard as GO target |
| no restore governance regression | YES | apply timer active after restore and runtime checks remained OK |

Conclusion: E11.9 recovered the reserved WireGuard clean target without rollback, reassignment loop, or routing regression.
