# P1.C Implementation Backlog

implementation_backlog_defined=true

## P0 — Required

| Item | Outcome |
| --- | --- |
| Runtime Convergence Store | Store trust snapshots, fingerprint summaries, drift records and verification history. |
| Runtime Convergence API | Admin can read trust summary, fingerprint summary and drift list. |
| Runtime Trust Status Component | `Главная`, `Проверки`, `Безопасность` show runtime trust consistently. |
| Runtime Convergence Drawer | Operator can inspect status, drift, verification history and recommended action. |
| Evidence Bundle Link | Convergence checks link to evidence. |
| Drift Status Contract | Runtime drift types and severities are consistent across UI/API. |
| No-Mutation API Contract | Trust APIs are read-only. |

## P1 — Production

| Item | Outcome |
| --- | --- |
| Release Surface Integration | Runtime trust can compare against release/provenance expectations. |
| Backup/Restore Integration | Restore verification and backup scope can use convergence evidence. |
| Governance Gate Integration | Proposals/batches show runtime trust blocker. |
| Drift Closure Workflow | Known/closed drift can be recorded with evidence and role gating. |
| Verification Refresh Flow | Operator can safely refresh convergence checks through guarded workflow. |
| Historical Drift Search | Operators can inspect drift timeline and recurrence. |

## P2 — Future

| Item | Outcome |
| --- | --- |
| Multi-Node Convergence | Production pool shows trust across multiple V7 nodes. |
| Drift Diff Viewer | Expert role can inspect structured diff safely. |
| Convergence Trend Alerts | Degradation/staleness alerts across time. |
| Automated Release Match Suggestions | Non-authoritative suggestions for release reconciliation. |

## Backlog Verdict

P0 makes runtime trust visible. P1 makes it part of release, recovery and governance flows. P2 scales it to production pool operations.
