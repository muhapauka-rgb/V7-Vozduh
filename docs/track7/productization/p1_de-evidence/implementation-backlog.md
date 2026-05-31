# P1.D/E Implementation Backlog

implementation_backlog_defined=true

## P0 — Required

| Item | Outcome |
| --- | --- |
| Release Trust Store | Store current release summary, certification, lineage, rollback and verification history. |
| Release Trust API | Admin can read current release, release history and release details. |
| Release Trust Status Component | `Главная`, `Проверки`, `Безопасность` show release trust consistently. |
| Release Drawer | Operator can inspect status, certification, rollback and verification history. |
| Runtime Convergence Link | Release trust shows whether runtime matches release. |
| Evidence Bundle Link | Release verification references evidence. |
| No-Mutation API Contract | Release trust APIs are read-only. |

## P1 — Production

| Item | Outcome |
| --- | --- |
| Backup/Restore Integration | Release rollback and restore lineage visible from Security. |
| Release Verification Refresh | Guarded refresh flow updates trust evidence without deployment side effects. |
| Rollback Readiness Display | Operator can see rollback readiness before risky actions. |
| Release History Search | Operators can inspect previous releases and verification. |
| Drift/Release Correlation | Runtime drift points to release mismatch when relevant. |
| Role-Gated Provenance Details | Expert users can inspect hashes/manifests/signatures safely. |

## P2 — Future

| Item | Outcome |
| --- | --- |
| Multi-Node Release Trust | Production pool release trust across nodes. |
| Release Comparison Drawer | Compare current, previous and rollback target releases. |
| Release Risk Scoring | Non-authoritative risk summary for operators. |
| Installer Integration | Deployment/install flow writes release trust records. |

## Backlog Verdict

P0 makes release trust visible. P1 connects it to recovery and verification. P2 scales it to production pool and installer workflows.
