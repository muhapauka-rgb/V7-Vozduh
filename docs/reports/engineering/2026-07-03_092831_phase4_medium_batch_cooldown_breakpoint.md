# Phase 4 MEDIUM_BATCH Cooldown Breakpoint

## Summary

Controlled Production Certification Program Phase 4 remains active. The certification marker materialization owner extension was safely deployed and production convergence passed at commit `b8a634c987c6ab6239040ccd066d4760541203de`.

The controlled certification source `wireguard-1779454504-c43409` was marked through the existing `v7-egress-set-state certification-scope` owner for certification users `10.7.0.16` through `10.7.0.26`. Controlled degradation was then created through `v7-egress-set-state maintenance --controlled-certification --apply`.

## Evidence

| Item | Evidence |
| --- | --- |
| Safe deploy | `tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED --update-local-snapshot --json` returned `final_verdict=PASS` |
| Deployed commit | `b8a634c987c6ab6239040ccd066d4760541203de` |
| Deploy id | `deploy-z8-14-Updatesystem-b8a634c-20260703T092235` |
| Convergence | `tools/v7-convergence-status --json` returned `final_verdict=PASS`, `runtime_action_status=READY_FOR_RUNTIME_ACTION` |
| Marker owner | `v7-egress-set-state certification-scope --apply` returned `ACTION=certification_scope_marked` |
| Controlled degradation owner | `v7-egress-set-state maintenance --controlled-certification --apply` returned `V7_EGRESS_SET_STATE=OK` |
| Recovery owner | `v7-egress-set-state enabled --apply` returned `V7_EGRESS_SET_STATE=OK` |
| Route repair owner | `v7-user-reconcile-apply --repair routing --apply --confirm REPAIR_USER` returned `V7_USER_RECONCILE_APPLY=OK` for all certification users |
| Route reality after recovery | `v7-user-route-check` returned `V7_USER_ROUTE_CHECK=OK` |

## Breakpoint

The first governed MEDIUM_BATCH execution did not select the controlled source. It selected the still-open real production incident:

| Field | Value |
| --- | --- |
| Incident source selected | `openvpn-1779388847-d2ad7c` |
| Selected users | `10.7.0.12`, `10.7.0.13`, `10.7.0.15` |
| Selected move count | `3` |
| Authorized budget | `25` |
| Requested max users | `10` |
| Runtime result | rollback completed for the selected users |
| Verification failure | global route check saw controlled source users on the intentionally down certification source |

After restoring the controlled source and repairing route tables, a continuation governed execution still selected the real incident, but did not execute because the same users are under retry/rollback cooldown:

| Field | Value |
| --- | --- |
| apply_executed | `false` |
| users_moved | `0` |
| verification_result | `NOT_RUN` |
| blocker | `cooldown_active_713s`; `no_eligible_failover_target` |
| blocking owner | Runtime/Planner cooldown policy in the existing governed L3 path |
| terminal classification | `POLICY_PROHIBITION` |

## Owner Resolution

The blocker is not a permanent program stop. The cooldown is an existing safety policy after rollback. The required resolution is to wait for cooldown expiry and resume the same governed L3 execution path for `openvpn-1779388847-d2ad7c`.

The controlled Phase 4 source must not be degraded again until the real incident is either completed, held by a fresh owner-resolution terminal state, or canonically impossible. This prevents global verification for one incident from being polluted by an intentionally degraded controlled source.

## Production Impact

| Field | Value |
| --- | --- |
| Production mutation | Controlled certification source was temporarily degraded, then restored |
| Users moved in first governed attempt | `3` attempted, rollback completed |
| Users moved in continuation attempt | `0` |
| Certification users final route check | `OK` |
| Broad automation enabled | `NO` |
| New owner created | `NO` |
| Authority bypass | `NO` |
| Runtime bypass | `NO` |

## Next Execution Step

Continue the same certification program after cooldown expiry:

1. Run the existing governed L3 production validation path for `openvpn-1779388847-d2ad7c`.
2. If it passes, verify remaining users on that incident.
3. Resume Phase 4 MEDIUM_BATCH controlled source certification.
4. Degrade the controlled source only after global route reality is clean and no higher-priority real incident blocks certification.
