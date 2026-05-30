# P1.A Implementation Backlog

implementation_backlog_defined=true

## P0 — Required

| Item | Outcome |
| --- | --- |
| Evidence Bundle Store | Durable bundle metadata, links, timeline, item summaries and closure records. |
| Evidence Bundle API | Admin can list bundles, open one bundle and query by current object. |
| Evidence Drawer Component | Shared drawer for checks, logs, users, channels and routes. |
| Evidence Link Chips | Tables can show proof availability and open the drawer. |
| Redaction Contract | Secrets and private configs are not exposed in admin evidence. |
| Source Reference Contract | Bundles can link to check results, logs, proposals and audit records. |
| Reality-First Admin Integration | Evidence appears in existing `Главная`, `Проверки`, `Логи`, `Пользователи`, `Каналы`, `Маршруты`. |

## P1 — Production

| Item | Outcome |
| --- | --- |
| Closure Workflow | Operators can mark evidence closed with reason and verification. |
| Evidence Search | Search by object, severity, status, source, tag and time range. |
| Proposal Integration | Proposal cards show supporting evidence bundle. |
| Recovery Integration | Rollback/restore flows write and read evidence bundles. |
| Release Verification Integration | Release and provenance surfaces use evidence bundles. |
| Evidence Retention Policy | Store, summarize, expire and archive evidence predictably. |
| Role-Gated Advanced Details | Expert users can inspect raw technical detail safely. |

## P2 — Future

| Item | Outcome |
| --- | --- |
| Evidence Correlation Engine | Multiple related events are grouped into one case automatically. |
| Evidence Export | Operators can export sanitized evidence packets for support or audit. |
| Evidence Diff | Compare before/after evidence during recovery or release validation. |
| Multi-Node Evidence Federation | Production pool can show evidence across V7 nodes. |
| AI-Assisted Diagnosis Drafts | Optional draft diagnosis from evidence, never authority. |

## Backlog Verdict

P0 is enough to make evidence usable in current admin workflows. P1 makes evidence production-grade. P2 improves correlation and support workflows.

