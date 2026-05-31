# E35.1 Admin Integration Plan

Runtime mutation: NO
User movement: NO
Routing/apply/autoswitch apply: NO

admin_integration_defined=true

E35.1 must integrate into existing `/admin-v2`. No new top-level navigation section is required.

Use existing sections:

- Главная
- Пользователи
- Каналы
- Маршруты
- Проверки
- Настройки
- Логи

## UX Principle

The operator should see a calm answer to:

```text
Why is this user on this channel?
Can this channel serve the user's required services?
What blocks this candidate?
What is only a preference?
What would happen next?
```

Raw policy JSON and matrix internals must stay behind progressive disclosure.

## 1. Пользователи -> User Drawer

Add a read-only "Routing Control" area first.

Show:

- Group.
- Routing Mode: `AUTO` or `OPERATOR_PINNED`; `MANUAL` displayed only as future/reserved if encountered.
- Preferred Channel when pinned.
- Current Channel.
- Effective Required Services.
- Group baseline services.
- User-added services.
- Explicit exemptions if any.
- Group allowed channels summary.
- Suitability status for current channel.
- "Why this user is here" explanation.
- Evidence and Proposal links when unsuitable, degraded or unknown.

Suggested labels:

- `Режим маршрутизации`;
- `Группа`;
- `Предпочитаемый канал`;
- `Обязательные сервисы`;
- `Эффективные требования`;
- `Текущий канал подходит`;
- `Почему пользователь здесь`;
- `Жёсткие запреты`;
- `Мягкие предпочтения`.

Status model:

| Status | Operator text |
|---|---|
| SUITABLE | Текущий канал подходит |
| DEGRADED | Канал работает с ограничениями |
| HARD_BLOCKED | Канал не подходит |
| UNKNOWN | Недостаточно данных |
| PINNED_OK | Закреплённый канал подходит |
| PINNED_DEGRADED | Закреплённый канал требует внимания |

Avoid:

- implying that selecting a required service immediately moves the user;
- showing raw service matrix by default;
- calling `current` a pinned channel.

## 2. Каналы -> Channel Drawer

Add read-only "Group and Service Suitability" area.

Show:

- Which groups allow this channel.
- Which groups exclude this channel.
- Whether channel is exclusive to a group.
- Service matrix status by important service groups.
- Capacity class/status.
- Current users on channel.
- Users blocked from this channel and why.
- Users for whom this channel is suitable.
- Evidence/Proposal links.

Suggested labels:

- `Разрешён для групп`;
- `Ограничен для групп`;
- `Сервисная пригодность`;
- `Пользователи, которым канал не подходит`;
- `Причины запрета`;
- `Ёмкость`.

Do not turn the channel drawer into a giant table. Show top blockers and let details open in drawer sections.

## 3. Настройки -> Groups

Use existing Settings area and existing Users -> Organizations surface. Do not add a new top-level Groups section.

Recommended placement:

- Primary edit/read surface: `Настройки` -> `Организации и ёмкость` evolves into `Группы и маршрутизация`.
- Identity management remains under `Пользователи` -> `Организации`.

Show:

- Group list.
- Display name.
- Linked organizations count.
- Allowed channels.
- Excluded channels.
- Preferred channels.
- Required services.
- Default routing mode.
- Isolation.
- Audit history link.
- Future policies placeholder.

Write controls are future/P2 unless explicitly implemented later. E35.1 should define read shape and UX, not live mutation.

Suggested copy:

```text
Группа задаёт правила выбора каналов для пользователей. Изменение правил не двигает пользователей само по себе. Движение возможно только через proposal/governance/execution.
```

## 4. Маршруты

Show service-aware preview and hard-block reasons.

Add:

- route-class suitability summary;
- required services affected;
- hard-block vs soft-preference explanation;
- candidate channels with reasons;
- Evidence/Proposal links.

The route section should answer:

- which route class is affected;
- which services require this route class;
- which channels pass;
- which channels are blocked;
- why speed did or did not matter.

## 5. Главная

Only summary-level indicators:

- Users on unsuitable current channel.
- Users with required service degraded.
- Groups with restrictive channel policy.
- Pinned users needing attention.
- Required services with no suitable channel.

Do not show raw matrix internals on main page.

Suggested cards:

- `Обязательные сервисы`;
- `Группы с ограничениями`;
- `Пользователи требуют внимания`;
- `Закреплённые каналы`.

Each card opens a drawer/list with Evidence/Proposal links.

## 6. Проверки

Add/extend check cards:

- Required services matrix freshness.
- Group policy validity.
- Suitability model consistency.
- Pinned user validity.
- Unknown service IDs.

These are diagnostics only.

## 7. Логи

Existing Logs should continue to show:

- service preference updates;
- org/group policy updates;
- proposal/evidence/trust history;
- future routing-control changes.

Add filtering vocabulary later:

- `routing_control`;
- `required_services`;
- `group_policy`;
- `routing_mode`;
- `suitability`.

## 8. Admin Reality-First Contract

Product Capability:

- Required services and routing control.

Admin Surface:

- Users drawer, Channel drawer, Settings Groups, Routing, Main indicators, Checks and Logs.

Runtime Service:

- service matrix, autoswitch planner, route dry-run, future governance.

Storage:

- service preferences, identity groups, org-egress policy, future user routing controls.

API:

- read endpoints for effective routing controls and suitability; future guarded mutation endpoints.

UI Component:

- chips, status badges, drawers, suitability reason list, group policy editor.

Tests:

- admin integration scan, localization scan, no new top-level section scan.
