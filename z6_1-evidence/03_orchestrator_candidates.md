# Z6.1 Existing Orchestrator Candidates

Scores: 10 is highest. Reuse Score measures how strongly a candidate should be reused/extended. Risk Score measures risk if left uncoordinated or duplicated.

| Candidate | Location | Purpose | Inputs | Outputs | Authority Level | Reuse Score | Risk Score | Classification |
|---|---|---|---|---|---|---:|---:|---|
| Autoswitch Mini-Orchestrator | `tools/v7-users-autoswitch`, `systemd/v7-users-autoswitch.*` | Plan and optionally apply bounded user egress moves | Users/egress registries, policy, org policy, service matrix, Telegram sentinel, quality summary, safety, reconnect state, load summary, restore barrier | JSON plan, selected moves, dynamic load summary, safety/reconnect state, `v7-user-switch` calls, verify/rollback results | HIGH for autoswitch runtime movement | 9 | 8 | REUSE + EXTEND |
| Admin Action Runner | `admin/v7-admin-api` | Authenticated operator/admin/owner action surface | HTTP action requests, session/CSRF, runtime state files, policy files | Mutating runtime command calls, audit records, overview responses | HIGH for manual/admin runtime mutation | 8 | 9 | REUSE + EXTEND |
| Admin Execution Contract Foundation | `admin/v7-admin-api` execution APIs | Read-only execution contracts, events, timeline, rollback summaries, explanation | Execution contract/event stores and proposal/readiness state | Read-only API responses | LOW/NONE for runtime execution | 7 | 2 | EXTEND |
| Zero-Move Operator Execution | `admin_core/operator_execution.py` | Validate zero-move packet, recheck runtime hashes, append approval/denial/governance records | Operator packet, users/egress registry hashes, selected moves source, audit store | Audit JSONL, optional zero-move governance action record | MEDIUM for governance record, NONE for runtime movement | 8 | 3 | EXTEND |
| Operator Observability Workflow | `admin_core/operator_observability.py` | Read-only governance/approval/rehearsal/operator summaries | Runtime state, selected moves, restore barrier, reports/evidence | Preview/readiness models | LOW advisory | 8 | 2 | REUSE |
| Telegram Sentinel Signal Owner | `tools/v7-telegram-sentinel`, `systemd/v7-telegram-sentinel.*` | Fast Telegram reachability signal; production no-autoswitch mode | Egress registry, Telegram TCP samples, prior sentinel state | `telegram-sentinel.json`, service matrix updates, event JSONL, latent autoswitch process launch | MEDIUM signal authority; latent HIGH if no `--no-autoswitch` | 7 | 6 | REUSE |
| Generic Rollback Owner | `tools/runtime-support/v7-rollback-last-change`, Admin rollback endpoints | Restore latest backup from broad roots | Latest `.bak.*` / `.backup.*` file under broad roots | File restore, optional chmod/systemctl, audit log | HIGH rollback authority | 5 | 8 | REFACTOR LATER |
| Signal Scheduler Set | service matrix and quality timers | Keep runtime signals fresh | Timers, state snapshots, probe output | Service matrix, quality summary | MEDIUM supporting authority | 7 | 4 | REUSE |
| Restore/Canary Readiness Tools | `tools/v7-restore-settle-gate`, `tools/v7-second-canary-target-readiness` | Read-only readiness and restore settle classification | Saved evidence and state snapshots | Gate/readiness verdicts | LOW read-only | 7 | 1 | REUSE |

## Closest Existing Ownership Chain

`systemd/v7-users-autoswitch.timer` -> `systemd/v7-users-autoswitch.service` -> `tools/v7-users-autoswitch.plan()` -> selected moves -> `tools/v7-users-autoswitch.apply()` -> `v7-user-switch` -> verification -> rollback-on-verify-fail -> safety/reconnect state writes.

This is not a full Runtime Orchestrator because it does not own proposal approval, P2 execution contracts, global lock/scheduling across all mutation paths, final audit closure, or full rollback manifest closure. It is a partial Runtime Orchestrator for autoswitch runtime movement.
