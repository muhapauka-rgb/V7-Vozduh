# E11.8 Full Reservation Enforcement Investigation

## Scope

This investigation checked the reservation path across registry parsing, planner eligibility, failover, rebalance, projected load selection, apply, target readiness, routing-sync/reconcile, cached state, and existing-user drain semantics.

## Findings By Theory

| Theory | Result | Evidence |
|---|---:|---|
| autoswitch eligibility ignores `canary_reserved` | proven | `Egress` had no `canary_reserved` field and `_gate_basic` did not inspect it. |
| planner ignores reservation metadata | proven | `_candidate()` used basic/org/quality/service/load/safety gates only. None read reservation metadata. |
| apply ignores reservation metadata | partially true | apply consumes `selected_moves`; it does not independently revalidate reservation. If planner selects a reserved target, apply will execute it. |
| load balancer path ignores reservation | proven | `_healthy_for_load()` only excluded disabled, maintenance, manual_only, unhealthy, Telegram hard-blocked, and low-quality targets. |
| stale planner cache | not primary | Runtime source lacked reservation handling. The bypass was code-level, not only cached state. |
| reservation metadata parse bug | proven as missing parser | registry row had `canary_reserved=true`, but `_load_egress()` did not parse it. |
| metadata not loaded into runtime state | proven | runtime grep showed no `canary_reserved` in `/usr/local/bin/v7-users-autoswitch` before fix. |
| autoswitch fallback bypasses reservation | proven | failover candidates were built from the same reservation-unaware candidate gate. |
| rebalance path bypasses reservation | proven risk | rebalance uses eligible candidates; eligibility ignored reservation before fix. |
| target readiness uses reservation but autoswitch does not | true as governance gap | target readiness could observe reserved metadata, but autoswitch did not enforce it. |
| reservation only advisory | true before fix | no runtime production assignment block existed. |
| policy precedence issue | secondary | `manual_only/reserve_only` would have blocked some paths, but `canary_reserved` had no precedence at all. |
| routing-sync/reconcile reintroduces users | not supported | switch-history reasons were `autoswitch_failover`; no hidden routing-sync/user-switch process was observed. |
| multiple autoswitch code paths inconsistent | proven | target readiness/reservation docs recognized the metadata; autoswitch planner/apply did not. |
| reservation semantics missing in planner/apply logic | proven | no parser, no gate, no apply validation. |
| production assignment occurred before reservation and never drained | mixed | Some production assignments occurred after reservation and after diagnose fix; existing users also require explicit drain semantics now. |
| existing users not drained | true but separate | E11.8 fix deliberately prevents new assignment and holds existing users until a separate drain approval. |
| restore-settle interaction | not primary | restore governance was proven; this was autoswitch target eligibility. |
| planner state persistence issue | not primary | no evidence that stale state alone caused selection. |
| hidden production egress priority override | not needed | WireGuard priority/quality made it attractive, but missing reservation enforcement was sufficient cause. |

## Exact Assignment Path

The observed movement path was:

1. E11.3 added `canary_reserved=true` metadata.
2. E11.6 made WireGuard diagnose OK and therefore production-eligible under old autoswitch logic.
3. `v7-users-autoswitch` loaded WireGuard as a normal `GLOBAL_FAST` egress because it ignored `canary_reserved`.
4. Failover/rebalance candidate selection scored WireGuard highly.
5. `v7-users-autoswitch --apply` timer selected bounded batches.
6. apply called `v7-user-switch` with `V7_SWITCH_REASON=autoswitch_failover`.
7. production users landed on WireGuard.

## Bounded Fix Chosen

The safe fix path was:

- parse `canary_reserved`;
- remove reserved targets from dynamic production load pool;
- block reserved targets as production destinations for planned/failover/reconnect/rebalance candidate paths;
- keep existing users on a reserved target in place if healthy, with explicit `canary_reserved_current_hold_requires_separate_drain_approval`;
- do not drain users in this block.

This closes new production assignment without broad user movement.
