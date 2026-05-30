# E34.G Current Admin Intake

current_admin_loaded=true

## Current Admin Philosophy

Current V7 Admin is an operator-first control panel, not a product dashboard.

The preserved design principles are:

- calm;
- premium;
- low noise;
- operator-first;
- evidence-first;
- progressive disclosure;
- fail-closed for risky actions.

## Current Navigation

The current top navigation remains:

| Section | Operator purpose |
| --- | --- |
| `Главная` | System status, topology, alerts, active users, channels. |
| `Пользователи` | Users, organizations, profile issuance, phones/devices, access lifecycle. |
| `Каналы` | Egress channels, onboarding, service matrix, readiness and speed. |
| `Маршруты` | Route classes, checks, client modes, RU readiness, route reality. |
| `Проверки` | Diagnostics, readiness maps, check results. |
| `Безопасность` | Safe mode, backups, rollback, maintenance, logs/disk. |
| `Настройки` | Policy, impact, autoswitch, route modes, guardrails. |
| `Логи` | Event stream, filters, audit/evidence summaries. |

## Current Interaction Surfaces

Current admin already provides:

- top-level navigation;
- workspace tabs inside sections;
- table title tabs inside dense tables;
- right-side/centered drawer for details;
- info panel for contextual explanations;
- topology and metrics on overview;
- `Что дальше`, `Сценарии`, and `Карта админки` guidance;
- theme, language, refresh, helper text, and density controls.

## Integration Constraint

E32-E34 architecture must be surfaced through existing operator tasks.

Operators should think:

```text
What happened?
Who is affected?
What should I do?
```

Operators should not need to think:

```text
Where is Capacity?
Where is Scheduler?
Where is Policy?
```
