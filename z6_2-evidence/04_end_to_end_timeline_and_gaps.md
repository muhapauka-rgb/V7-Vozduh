# End-to-End Runtime Timeline and Gaps

## Timeline

| Step | Owner | Input | Output | Authority |
|---:|---|---|---|---|
| 1. Signal sampling | Service matrix refresh, Telegram sentinel, quality compact, health/speed/client observers | Network/service/runtime observations | Signal JSON files and event JSONL | Distributed signal authority. |
| 2. Runtime cycle start | `systemd/v7-users-autoswitch.timer/service` | Timer tick | `v7-users-autoswitch --apply` process | Primary autonomous scheduler authority. |
| 3. Planner state load | `v7-users-autoswitch` | Policy, state, health, quality, safety, service matrix, sentinel, reconnect, load, restore barrier | Planner context | Partial orchestrator authority. |
| 4. Candidate generation | `v7-users-autoswitch` | Active users, egress health, policy, route classes | Candidate failover/rebalance decisions | Planner authority. |
| 5. Selected move generation | `v7-users-autoswitch.plan()` | Candidates, safety, policy, barrier | In-process selected moves | Ephemeral selected-move authority. |
| 6. Restore barrier gate | `v7-users-autoswitch` | Barrier file, generation token, selected-move hash/count/budget | Selected moves allowed or suppressed | Enforcement authority; lifecycle owner fragmented. |
| 7. Apply admission | `v7-users-autoswitch.apply(plan)` | `--apply`, enabled mode, non-observe, selected moves | Execute or no-op result | Runtime apply authority. |
| 8. Movement execution | `v7-user-switch` called by autoswitch or Admin | User IP and target egress | Route mutation | Movement authority. |
| 9. Verification | `v7-users-autoswitch` route verification or Admin runtime checks | Post-switch route state | Success/failure | Path-local verification authority. |
| 10. Rollback | Autoswitch local rollback, Admin rollback, generic latest-change rollback | Failure or operator command | Revert movement/config or restore backup | Fragmented rollback authority. |
| 11. State update | Autoswitch, signal tools, Admin actions | Outcome and observations | Safety, reconnect, load, events, audits | Fragmented state writer authority. |
| 12. Audit/closure | Admin audit, runtime audit, operator execution audit, stdout/journal, historical reports | Command/action outcome | Event records and report evidence | No unified cycle-end owner. |

## Critical Questions

Q1. What currently starts the runtime cycle?

Primary autonomous start owner: `systemd/v7-users-autoswitch.timer` triggering `systemd/v7-users-autoswitch.service`, which runs `/usr/local/bin/v7-users-autoswitch --apply`.

Q2. What currently ends the runtime cycle?

No unified end owner. Cycle end is fragmented across command exit/stdout, autoswitch state writes, Admin response/audit where applicable, runtime-support audit, and historical/operator reports.

Q3. Who owns planner execution?

`tools/v7-users-autoswitch`.

Q4. Who owns selected moves?

Autonomous runtime selected moves are owned in memory by `v7-users-autoswitch.plan()` and consumed by `v7-users-autoswitch.apply(plan)`. Persistent selected-move files are reader/evidence conventions, not the live planner queue.

Q5. Who owns restore barrier generation?

No singular active owner found. Historical/manual/governance operations created and updated barrier metadata; `v7-users-autoswitch` owns enforcement, not full lifecycle creation/closure.

Q6. Who owns runtime recheck?

Fragmented. `v7-users-autoswitch` performs path-local runtime checks for its own apply. `admin_core/operator_execution.py` performs runtime recheck only for zero-move governance records. Admin validation gates are preview/read-only.

Q7. Who owns execution?

`v7-users-autoswitch` owns autonomous execution; Admin endpoints own manual autoswitch/direct user-switch/rollback execution; `v7-user-switch` is the low-level movement tool.

Q8. Who owns rollback?

Fragmented. Autoswitch owns local verification rollback for its own moves; Admin owns manual rollback calls; `v7-rollback-last-change --apply` owns generic latest-backup rollback when invoked.

Q9. Who owns audit completion?

No single owner. Admin audit, runtime-support audit, operator execution audit, service event logs, autoswitch stdout/journal, and historical reports each cover part of the lifecycle.

Q10. Can any component bypass the intended governance path?

Yes. Autonomous autoswitch, Admin direct user-switch, manual CLI `v7-user-switch`, Admin rollback, generic rollback, and latent sentinel autoswitch invocation can bypass the preview-only execution-contract path.

## Orchestration Gaps

| Gap | Reality |
|---|---|
| Start owner | Exists for autonomous cycle: autoswitch timer/service. |
| End owner | Missing unified cycle closure. |
| Selected-move persistence | No canonical live selected-move queue; selected moves are ephemeral in autoswitch. |
| Restore barrier lifecycle | Enforcement exists; generation/clearance/closure owner is fragmented. |
| Runtime recheck | Exists by path, not globally. |
| Execution contract | Admin/P2 surfaces are preview/read-only and explicitly not executable. |
| Manual movement | Admin/CLI can move users outside planner-selected moves. |
| Rollback | Multiple rollback scopes and authorities; no single contract-scoped rollback owner. |
| Audit | Multiple audit writers; no single final lifecycle audit owner. |
| Scheduler | Active autoswitch timer plus draft planner timer path create latent duplicate scheduler risk. |

## Minimum Consolidation Required Before Any Future Implementation

This is not a design proposal; it is the gap boundary discovered by Z6.2.

Any future work must reuse the existing autoswitch planner/apply authority and must not create a parallel planner, selected-move source, execution path, scheduler, rollback authority, or audit truth source.

The unresolved ownership boundaries are:

- canonical runtime-cycle closure;
- canonical selected-move read/write model;
- canonical restore-barrier generation, clearance, and closure ownership;
- global runtime admission/recheck across autonomous, Admin, and manual paths;
- contract-scoped rollback ownership;
- single audit-completion truth for movement lifecycle.

