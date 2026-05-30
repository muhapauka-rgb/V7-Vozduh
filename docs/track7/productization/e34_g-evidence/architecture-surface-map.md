# E34.G Architecture Surface Map

architecture_surface_map_defined=true

## Surface Rule

Architecture components are not top-level products. They appear as status, blockers, proposals, evidence, and guided actions inside existing V7 Admin sections.

## E32-E34 Surface Map

| Architecture component | Primary admin surface | Secondary surface | Operator sees | Hidden by default |
| --- | --- | --- | --- | --- |
| Capacity Program | `Каналы` readiness/load, `Проверки` readiness, `Настройки` impact | `Главная` metrics and alerts | Capacity status, available headroom, batch allowed/blocked, reason. | Class lifecycle internals, confidence formula, raw validation samples. |
| Execution Batches | `Главная` alerts, `Проверки`, `Логи` | `Настройки` autoswitch impact | Proposed movement, affected users, target, rollback, status. | Batch state machine, packet internals, replay ledger detail. |
| Policy Engine | `Настройки` policy/impact, `Маршруты` checks | `Логи` evaluation trace | Allow/deny/review required, blocker reason, next safe action. | Policy priority resolution, internal rule graph. |
| Concurrency Controls | `Проверки`, `Логи`, action result drawers | `Главная` blockers | Action blocked because user/target/batch is reserved or locked. | Lock ordering, reservation ledger internals, owner heartbeat fields. |
| Scheduler | `Главная` alerts, `Настройки` autoswitch, `Логи` | `Проверки` | Planned actions, blocked queue, next safe window. | Scheduling algorithm internals and queue data structures. |
| Routing Intelligence | `Маршруты`, `Пользователи` priority services, `Каналы` service matrix | `Главная` topology | Best route/channel proposal, required services, affected user, confidence. | Raw scoring model unless expert drawer is opened. |
| Backup | `Безопасность` backups | `Главная` alerts, `Логи` | Backup freshness, verification, create/verify/download actions. | Storage backend internals and raw archive manifests. |
| Release | `Безопасность` / future deployment drawer | `Логи`, `Проверки` | Release identity, certification, runtime drift, rollback candidate. | Release manifest internals unless expert detail is opened. |
| Installer | Future guided flow reached from `Безопасность` or setup mode | `Проверки` preflight | NEXT/CHECK/READY flow, blockers, health checks. | Package implementation and shell commands. |
| Recovery | `Безопасность` actions, `Главная` alerts, drawers | `Логи` | Problem, evidence, recovery option, rollback option, verification. | Low-level commands and raw logs. |
| Operator Independence | `Что дальше`, `Сценарии`, drawers, info panels | All sections | Guided workflow and next safe action. | Internal runbook schema. |

## Integration Outcome

No new top-level architecture section is required.

Architecture appears as:

- status;
- explanation;
- proposal;
- blocker;
- preview;
- guided action;
- verification result;
- audit evidence.
