# Runtime Nervous System Evidence 00 - Runtime Discovery

Program: `PROGRAM_V7_RUNTIME_NERVOUS_SYSTEM_AND_OPERATING_POLICY_CERTIFICATION`

Workspace: `/Users/ponch/Documents/New project`

Branch: `Updatesystem`

Initial local truth:

```text
git status -sb
## Updatesystem...origin/Updatesystem

git branch --show-current
Updatesystem

git log --oneline -8
4905000 PROGRAM OUTCOME.1 snapshot refresh cadence finding
3dbfc70 PROGRAM OUTCOME.1 production materialization report
a7eb3aa PROGRAM OUTCOME.1 stable snapshot source refresh gate
9e0f243 PROGRAM OUTCOME.1 production switch history mapper closure
aedaaf7 PROGRAM OUTCOME.1 existing outcome mapper integration
61ceab4 PROGRAM data lineage reality audit and outcome map
8d10ba5 PROGRAM production shadow recommendations certification
3437026 PROGRAM CONV.3 convergence owner UX fix
```

## Primary Runtime Components

| Area | Existing owner | Existing truth source | Trigger | Consumer | Failure mode |
| --- | --- | --- | --- | --- | --- |
| Planner / selected moves | `tools/v7-users-autoswitch` | registry, service matrix, route state, intelligence snapshots | CLI, admin dry-run, `v7-autoswitch-planner.timer` in production | admin API, operator, selected-move views | fail-closed selected moves, dry-run, snapshot stop |
| Apply execution authority | `tools/v7-users-autoswitch --apply` via apply service/timer and governed blocks | selected moves, restore barriers, live route state | `v7-users-autoswitch.timer/service` when restored | runtime routes, audit, rollback packet | movement blocked by barrier, eligibility, policy, dry-run, timer held |
| Governance | admin API and operator-governance modules | approval packets, runtime governance audit, operator execution audit | operator action, approval packet flow | execution/rollback handlers | no approval, stale barrier, missing audit path |
| Rollback | `tools/v7-users-autoswitch` rollback packet generation plus operator execution path | rollback packet, restore barrier, pre-move state | live canary/full lifecycle blocks | operator and runtime recovery | packet missing, stale, incomplete, or not approved |
| Restore barrier lifecycle | `tools/v7-users-autoswitch`, governed apply restore reports, operator lifecycle | restore barrier files/state | planner/apply lifecycle | planner/apply/rollback | stale barrier, missing generation, bypass risk |
| Intelligence snapshots | `tools/v7-intelligence-snapshot-refresh` | `/opt/v7/egress/state/intelligence/` | manual CLI / dry-run; no production systemd unit found | planner, admin views, advisory scores | stale/missing/volatile snapshots, source hash mismatch |
| Recommendations | `tools/v7-users-autoswitch` plus `admin_core` read views | intelligence snapshot families and planner inputs | planner cycle, admin/operator view | operator decision support | recommendation quality not certified, no execution authority |
| Prediction | `admin_core/intelligence_workers.py`, snapshot builders, RI6 workers | snapshot families and outcome actuals | snapshot refresh / worker path | trust, recommendations, operator view | missing/low-confidence prediction; must not execute |
| Trust | RI6 trust/prediction modules and snapshot outputs | live outcomes, trust summaries | snapshot refresh / calibration | recommendation ranking and confidence | low trust de-escalates authority |
| Outcome collection | existing outcome mapper and audit/event readers | switch history, operator execution audit, governance audit, runtime audit | mapper/read-only integration, snapshot refresh | calibration/trust/prediction | missing actuals, mapper disabled, source volatility |
| Audit | `v7-audit-log`, audit JSONL files, admin read views | audit files | runtime/governance/execution events | reports, closure, operator evidence | audit path unavailable or incomplete |
| Closure | admin/operator observability and certification reports | audit completion and closure artifacts | operator/reporter | next gate | no closure means no promotion |
| Workers/timers | systemd timers and services | production systemd state | systemd | runtime and signal refresh | duplicate/stale/unknown scheduler ownership |
| Convergence truth | `tools/v7-convergence-status`, `tools/v7-truth-check`, `tools/v7-safe-deploy` | local, GitHub, production fingerprint | explicit read-only truth check | operator/Codex process | STOP on unknown or mismatch |

## Reuse / Extend / Refactor / Replace / Do Not Touch

| Component | Classification | Reason |
| --- | --- | --- |
| `tools/v7-users-autoswitch` | REUSE + EXTEND by policy only | Existing closest runtime orchestrator and planner/apply/rollback owner. Do not duplicate. |
| `v7-autoswitch-planner.timer/service` | REUSE + RECONCILE | Production currently uses it as non-apply planner scheduler. This supersedes older dormant-only evidence. |
| `v7-users-autoswitch.timer/service` | REUSE + GOVERN | Movement-capable apply scheduler exists but is currently held/inactive in latest production truth. |
| `tools/v7-intelligence-snapshot-refresh` | REUSE + EXTEND | Existing snapshot writer. Missing sustained production cadence is blocker. |
| Intelligence snapshot root | REUSE | Existing single snapshot root. No new root allowed. |
| RI6 trust/prediction workers | REUSE | Existing intelligence owner. Runtime must consume bounded outputs only. |
| Admin API read/operator views | REUSE + EXTEND | Existing operator visibility surface. Do not mix with execution changes in this program. |
| Governance/execution/rollback handlers | DO NOT TOUCH | Prompt forbids ownership changes. Certification only. |
| New planner/governance/execution/orchestrator | REPLACE = forbidden | Parallel authority would create duplicate truth and duplicate execution path. |

