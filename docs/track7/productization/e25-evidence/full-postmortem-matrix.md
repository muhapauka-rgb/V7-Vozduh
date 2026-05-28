# E25 Full Postmortem Matrix

E25 aborted before movement.

| Risk / Theory | Observed | Evidence | Verdict |
|---|---:|---|---|
| candidate drift | NO | `10.7.0.11 current=1 table=1009` throughout precheck | PASS |
| target drift | YES | target readiness changed from E24.2 GO to E25 NO-GO | BLOCKER |
| WireGuard occupied | NO | no users on `wireguard-1779454504-c43409` | PASS |
| target readiness stale | YES/RISK | `stability.state` below floor while `egress-quality-summary.json` was above floor | BLOCKER / SOURCE_DIVERGENCE |
| restore-settle stale | NO | E24.2 fresh sample dir returned `gate_status=GO` | PASS |
| selected_moves appeared | NO | no selected files, sample values zero | PASS |
| hidden movers active | NO | process scan clean | PASS |
| approval packet stale/expired | YES | packet expired at `2026-05-28T09:22:47.888963+00:00` | BLOCKER |
| registry hash drift | NO | users/egress hashes unchanged | PASS |
| selected_move_hash mismatch | NOT LIVE TESTED | consumer rejected packet before movement-capable recheck | BLOCKED |
| generation mismatch | NOT LIVE TESTED | consumer rejected movement packet shape | BLOCKED |
| rollback target unhealthy | NO evidence | candidate remains on `1`, route/checkers OK | PASS |
| route table mismatch | NO | table `1009` default dev `v7e356a192b79` | PASS |
| route_get mismatch | NO | route_get uses `v7e356a192b79` | PASS |
| kill switch regression | NO | `V7_KILLSWITCH_CHECK=OK` | PASS |
| provisioning/reconcile regression | NO | reconcile/provisioning checks OK | PASS |
| replay succeeds incorrectly | NOT TESTED | no movement execution packet reached valid state | BLOCKED |
| movement budget bypass | NO | no movement executed; current consumer rejects nonzero budget | PASS as fail-closed |
| unapproved user movement | NO | no movement executed, registry unchanged | PASS |
| delayed autoswitch movement after rollback | NOT APPLICABLE | no forward/rollback occurred | N/A |
| planner/apply timer race | NO | timers inactive | PASS |
| switch-history ambiguity | PRESENT | switch-history missing; no movement occurred | MITIGATED |
| helper false GO | NO | target helper returned NO-GO; restore helper GO cross-checked | PASS |
| helper false NO-GO | POSSIBLE SOURCE DIVERGENCE | target helper uses `stability.state`, quality summary more favorable | REVIEW REQUIRED |
| runtime/repo divergence | PARTIAL | movement-critical helpers present; movement packet consumer absent on VPS and not movement-capable locally | BLOCKER |
| audit chain valid | E23 ONLY | audit tail readable; no E25 record written | PASS / NO E25 RECORD |
| runtime checkers OK | YES | all runtime checkers OK | PASS |
| generation guard valid | PARTIAL | restore barrier present; movement packet consumer not connected | BLOCKER |

## Classification

`E25_NO_GO_PRE_EXECUTION`

Root blockers:

1. `TARGET_READINESS_NO_GO_STABILITY_BELOW_FLOOR`
2. `APPROVAL_PACKET_EXPIRED`
3. `MOVEMENT_PACKET_CONSUMER_NOT_CONNECTED`

No bounded in-scope fix was executed because changing readiness semantics or implementing/deploying a movement execution engine is outside E25's approved live mutation scope.
