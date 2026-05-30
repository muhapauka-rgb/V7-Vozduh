# E34.H Implementation Backlog

implementation_backlog_defined=true

## P0 — Required For Product

| Item | Outcome |
| --- | --- |
| Proposal Store and proposal API | Admin can show MOVEMENT/EVACUATION/REBALANCE/OBSERVATION as first-class objects. |
| Evidence Bundle component and API | Checks/drawers/logs can show evidence consistently. |
| Required Services editor and service satisfaction surface | User/company required services visibly affect channel recommendations. |
| Capacity API wrapper | Admin can show effective batch cap and blockers without parsing scattered state. |
| Proposal card/drawer component | Operator sees impact, confidence, reason, affected users, rollback and next action. |
| Policy admission trace summary | Operator can understand allow/deny/review without raw policy graph. |
| Runtime no-mutation checks for preview surfaces | UI clearly separates preview/dry-run from apply. |

## P1 — Required For Production

| Item | Outcome |
| --- | --- |
| Batch Store and Packet Store | Governed movement lifecycle becomes auditable and replay-safe in product. |
| Lock Store and Reservation Ledger | Concurrency blocks are durable and visible. |
| Release Store and Provenance Ledger | Release identity and rollback lineage become product features. |
| Backup/Restore manifest API hardening | Security section can prove restore scope and backup freshness. |
| Runtime Convergence Service | Admin can show runtime/repo/release drift. |
| Runbook Store and Closure Record Store | Operator independence becomes executable workflow. |
| Role-gated expert diagnostics | Expert evidence is available without overwhelming normal operators. |

## P2 — Future Enhancement

| Item | Outcome |
| --- | --- |
| Installer Service UI | Guided deployment flow inside setup/security surfaces. |
| Scheduler queue UI | Future planned actions visible with safe windows and blockers. |
| Production pool observability | Multi-target pool capacity and scheduling visibility. |
| Advanced evidence correlation | Link proposals, batches, logs, releases and recovery into one timeline. |
| Multi-server inventory | Commercial deployment across many V7 nodes. |

## Backlog Verdict

Implementation backlog is defined by product need and reality-first mapping.
