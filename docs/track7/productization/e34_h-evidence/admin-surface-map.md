# E34.H Admin Surface Map

admin_surface_map_defined=true

## Complete Current Admin Section Map

| Admin section | New capabilities appearing here | Hidden by default | Drawer / drill-down | Expert mode |
| --- | --- | --- | --- | --- |
| `Главная` | Overall architecture status, proposals, degraded capacity/channel alerts, scheduler blockers, drift/recovery alerts. | Raw batch state, lock IDs, policy graph, raw manifests. | Proposal detail, alert detail, topology object detail. | Raw evidence bundle, proposal JSON, checker output. |
| `Пользователи` | Required services, user-specific health, movement proposals for one user, access lifecycle evidence. | Scoring math, raw route table internals. | User readiness, required services, service satisfaction, route evidence. | Full user flow trace and raw route proof. |
| `Каналы` | Capacity, service matrix, target quality, channel readiness, evacuation/rebalance proposals. | Capacity lifecycle internals, raw quality samples. | Channel detail, users on channel, service matrix evidence, readiness history. | Full diagnose/benchmark history. |
| `Маршруты` | Routing Intelligence, route proposals, service-aware previews, route reality, RU readiness. | Raw policy graph and route scoring model. | Route class detail, proposal detail, service/category explanation. | Full route table, marks, policy trace. |
| `Проверки` | Readiness, runtime convergence, capacity validation, installer preflight, proposal verification. | Low-level command output and service internals. | Check result detail, evidence bundle, blocker explanation. | Raw checker logs and JSON. |
| `Безопасность` | Backup/restore, rollback, safe mode, release/provenance, recovery, installer deployability. | Archive internals, release manifest internals. | Backup detail, rollback preview, release/provenance drawer, recovery flow. | Raw manifests, backup verification logs. |
| `Настройки` | Policy, autoswitch, guardrails, capacity/policy impact, scheduler knobs. | Policy graph internals, scheduler queue internals. | Impact detail, policy diff, autoswitch dry-run. | Raw policy JSON and scheduler state. |
| `Логи` | Audit lineage, replay denial, proposal decisions, operator actions, recovery closure. | Verbose raw logs in main list. | Event detail and related evidence. | Raw event payloads and lineage links. |

## Admin Surface Verdict

Every E32-E34 architecture family has a current or planned admin surface without adding new top-level navigation.
