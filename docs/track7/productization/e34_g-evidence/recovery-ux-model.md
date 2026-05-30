# E34.G Recovery UX Model

recovery_surface_defined=true

## Recovery Principle

Recovery belongs inside the existing operator workflow. It should not become a separate product area.

Recovery is surfaced where the operator already looks for containment:

- `Главная` for alerts and next safe action;
- `Безопасность` for backups, rollback, safe mode and maintenance;
- `Проверки` for verification;
- `Логи` for audit/evidence;
- object drawers for scoped recovery.

## Recovery Surfaces

| Recovery topic | Admin surface | Operator sees |
| --- | --- | --- |
| Backup health | `Безопасность -> Бэкапы`, `Главная` warning | Freshness, verification status, backup count, backup action. |
| Restore preview | `Безопасность -> Действия` | Restore candidate, scope, blockers, preview result. |
| Rollback | `Безопасность -> Действия`, relevant object drawer | Last tracked change, rollback preview, apply boundary, verification. |
| Runtime drift recovery | `Главная` alert, `Проверки`, `Логи` | Drift type, affected area, safe next action, evidence. |
| Release recovery | Future release drawer under `Безопасность` | Current release, rollback release, provenance status. |
| Routing recovery | `Маршруты -> Проверка`, user/channel drawer | Affected route class, service impact, dry-run or guarded action. |

## Recovery Flow UX

```text
Problem shown
-> evidence bundle summary
-> recovery options
-> preview
-> confirmation if risky
-> apply only if authorized
-> verification
-> closure verdict
```

## What Remains Hidden

Hide raw shell commands, backend manifests, lineage internals, and low-level logs until expert diagnostics are requested.
