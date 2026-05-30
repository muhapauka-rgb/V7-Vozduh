# E34.G Navigation Integration

navigation_integration_defined=true

## Decision

No new top-level sections are required.

Current navigation is sufficient:

```text
Главная
Пользователи
Каналы
Маршруты
Проверки
Безопасность
Настройки
Логи
```

## Integration Map

| Architecture topic | Integrated into |
| --- | --- |
| Capacity | `Каналы`, `Проверки`, `Настройки`, `Главная` |
| Execution Batches | `Главная`, `Проверки`, `Логи`, action drawers |
| Policy | `Настройки`, `Маршруты`, `Логи` |
| Concurrency | Action drawers, `Проверки`, `Логи` |
| Scheduler | `Главная`, `Настройки -> Автосвитч`, `Логи` |
| Routing Intelligence | `Маршруты`, `Пользователи`, `Каналы` |
| Backup / Restore | `Безопасность` |
| Release / Provenance | `Безопасность`, `Проверки`, `Логи` |
| Installer | setup mode, `Безопасность`, `Проверки`, `Логи` |
| Operator Independence | `Что дальше`, `Сценарии`, info panels, drawers |

## Why No New Top-Level Sections

Adding top-level `Capacity`, `Policy`, `Scheduler`, `Concurrency`, or `Release` would force operators to think in backend architecture terms.

The product rule is operator-task orientation:

```text
What happened?
Who is affected?
What should I do?
```

Therefore architecture is embedded in existing sections as explanations, blockers, proposals, and guided actions.
