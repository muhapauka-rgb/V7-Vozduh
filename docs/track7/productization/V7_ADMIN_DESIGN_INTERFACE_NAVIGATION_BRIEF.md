# V7 Admin Design / Interface / Navigation Brief for Codex

## Purpose

Этот документ нужен как стартовый промпт и рабочая документация для всех будущих задач по доведению текущей V7 Admin до ума в Codex.

Главная мысль: V7 Admin — не лендинг и не декоративный dashboard. Это операторская консоль управления VPN/egress/routing/identity/security системой, где интерфейс должен помогать оператору понять состояние, найти причину, выполнить безопасный предпросмотр, применить только разрешённое действие и проверить результат.

Рабочая админка сейчас живёт на `/admin-v2`.

Не сохранять логин/пароль в коде, документах, скриншотах или промптах. Доступы используются только вручную оператором.

## Current Sources of Truth

Фактические источники:

- Runtime admin: [admin/v7-admin-api](/Users/ponch/Documents/New%20project/admin/v7-admin-api)
- Live route: `/admin-v2`
- Frontend scaffold: [web/README.md](/Users/ponch/Documents/New%20project/web/README.md)
- Frontend source contract: [web/src/README.md](/Users/ponch/Documents/New%20project/web/src/README.md)
- Information architecture scaffold: [web/src/app/information-architecture.json](/Users/ponch/Documents/New%20project/web/src/app/information-architecture.json)
- Status semantics CSS: [web/src/styles/status-semantics.css](/Users/ponch/Documents/New%20project/web/src/styles/status-semantics.css)
- Design snapshots: [design/v7-admin-working-current.html](/Users/ponch/Documents/New%20project/design/v7-admin-working-current.html), [design/v7-admin-live-7080-current.html](/Users/ponch/Documents/New%20project/design/v7-admin-live-7080-current.html)

Important: `web/` is currently a Phase 6 non-production scaffold. The running admin remains the embedded Python admin in `admin/v7-admin-api` and `/admin-v2`.

## Product Identity

V7 Admin is an operator console for:

- users and profiles;
- organizations, phones, devices, identity lifecycle;
- egress channels / tunnels;
- route classes and service-aware routing;
- checks, diagnostics, readiness and leak protection;
- security, backups, safe mode and rollback;
- policy settings, autoswitch and guardrails;
- audit/event logs.

The interface should feel:

- calm;
- dense but readable;
- operational;
- evidence-first;
- fail-closed;
- built for repeated daily use.

It should not feel like:

- a marketing dashboard;
- a generic SaaS template;
- a decorative card gallery;
- a wizard-only UI where operators cannot inspect evidence;
- a raw terminal dump.

## Core UX Principle

Use the E34.E operator workflow everywhere:

```text
Problem -> Evidence -> Diagnosis -> Action -> Verification -> Closure
```

The admin should never push the operator directly from problem to mutation.

For any risky action, the UI must show:

- what object is affected;
- which users/routes/channels are in scope;
- whether the action is preview/dry-run or apply;
- blockers and warnings;
- rollback path;
- confirmation requirement;
- audit/log result.

## Information Architecture

The current primary navigation is a top horizontal nav:

| Top nav | Purpose | Operator question |
| --- | --- | --- |
| `Главная` | Summary, status, topology, alerts, active users, channels. | Is V7 OK and what should I look at first? |
| `Пользователи` | Users, organizations, profiles, phones, access, lifecycle. | Who is affected and what can I do for one person/company? |
| `Каналы` | Egress channels, add-channel flow, service matrix, readiness/speed. | Which outbound channels are alive and suitable? |
| `Маршруты` | Route classes, client modes, RU readiness, route reality, route checks. | Where does traffic go and why? |
| `Проверки` | Diagnostics, readiness map, check results. | Can I verify safety without changing runtime? |
| `Безопасность` | Safe mode, backups, rollback, log/disk maintenance. | Can I protect, backup, restore, or contain safely? |
| `Настройки` | Policy, impact, autoswitch, route modes, guardrails. | What system policy is configured and what would it affect? |
| `Логи` | Event stream, filters, summaries. | What happened, who did it, and when? |

There is also an internal `identity` workspace that is reached mostly from `Пользователи`. Do not add it as a new top-level nav unless the information architecture is intentionally revised.

## Current Subnavigation

Use subnavigation inside a section instead of creating new top-level nav items.

### Users

Current workspaces:

- `Пользователи`
- `Организации`
- `Выдать профиль`
- `Люди и телефоны`
- `Доступ`
- `Жизненный цикл`

Main user table columns:

- user/person label;
- company;
- IP;
- current channel;
- priorities / mandatory services;
- status;
- issue / next operator action;
- traffic;
- action.

Hidden optional columns include day/week/month/total traffic, phone, device.

### Channels

Current workspaces:

- `Обзор`
- `Добавить канал`
- `Сервисная матрица`
- `Готовность и скорость`

Channel table columns:

- channel;
- status;
- users;
- traffic;
- services;
- speed;
- optional role/load;
- action.

The add-channel flow supports VLESS, WireGuard, AmneziaWG/AWG and auto-detect, with config text, file, QR import, organization scope and advanced metadata.

### Routing

Current workspaces:

- `Обзор`
- `Проверка`
- `Режимы клиентов`
- `Готовность RU`
- `Факт маршрутов`

Routing is an evidence and preview area. It must distinguish:

- route classes;
- route modes;
- service categories;
- actual route reality;
- dry-run / preview;
- guarded apply.

### Checks

Current workspaces:

- `Обзор`
- `Карта готовности`
- `Результат`

Checks should be treated as read-only or explicitly labelled if they mutate state. Default mental model: checks provide evidence.

### Security

Current workspaces:

- `Обзор`
- `Действия`
- `Бэкапы`
- `Логи и место`

Security includes safe mode, rollback, backups, cleanup preview/apply and maintenance settings. This area must be especially explicit about preview vs apply.

### Settings

Current workspaces:

- `Обзор`
- `Политика V7`
- `Влияние`
- `Автосвитч`
- `Режимы маршрутов`
- `Ограничители`

Settings are rare/advanced controls. They should be grouped by operator intent and always show impact before apply.

### Logs

Current workspaces:

- `Лента`
- `Фильтры`
- `Сводка`

Logs must be searchable by source, severity, action, user IP and context. Logs are not decoration; they are audit/evidence.

## Layout Model

Current layout patterns:

- sticky top bar with brand, nav, status and utility buttons;
- `.shell` max width around `1720px`;
- overview summary cards in a dense metric grid;
- topology panel on the main page;
- alert/event list;
- tables inside `.table-shell`;
- `workspace-tabs` for secondary navigation;
- right-side drawer for details;
- centered info panel for contextual guidance;
- toast stack for action feedback;
- optional compact density and light/dark theme.

Preferred page shape:

```text
top nav
section summary stats
workspace tabs / table title tabs
main panel or table
drawer for detail
action result panel / toast
logs/audit link
```

Avoid:

- cards inside cards;
- landing-page heroes;
- decorative illustrations;
- overly large headings inside tool panels;
- dense raw JSON on the first screen;
- one-off navigation patterns.

## Visual Style

Current design language:

- dark-first, light mode supported;
- restrained green accent;
- status colors only where meaningful;
- compact panels and tables;
- 8-16px radii depending on element importance;
- no huge hero blocks;
- no decorative gradients/orbs;
- no negative letter spacing;
- no viewport-scaled fonts.

Core tokens from runtime admin:

```text
bg: #0b0f14
panel: #111820
panel2: #0f151c
line: rgba(255,255,255,.10)
text: #f3f7fb
muted: #96a3b2
ok/green: #34d399
info/blue: #60a5fa
warn/yellow: #facc15
bad/red: #fb7185
```

Use existing semantic classes:

- `.pill.ok`
- `.pill.warn`
- `.pill.bad`
- `.pill.info`
- `.pill.muted`
- `.ghost`
- `.primary`
- `.mini-action`
- `.panel`
- `.table-shell`
- `.drawer-section`
- `.wizard-card`
- `.filterbar`
- `.searchbar`

## Status Semantics

Do not invent new colors casually.

Use:

- `ok` for operating as expected;
- `warn` for degraded, stale, waiting, needs attention;
- `bad` for blocked, failed, leak risk, down, unsafe;
- `info` for quarantine, maintenance, recovering, intentional non-default state;
- `muted` for disabled, unknown, not applicable, missing evidence.

If evidence is missing, the operator meaning is usually `unknown`, not `ok`.

## Action Design Rules

Every action must be one of:

- read-only view;
- dry-run / preview;
- guarded apply;
- rollback / containment;
- export/download;
- configuration save.

Risky actions must:

- be labelled clearly;
- show scope and blast radius;
- show preview first where possible;
- require confirmation when changing runtime, users, routes, security, release, backup or policy;
- write audit;
- show result and next step.

Good button hierarchy:

- `.ghost` for navigation, refresh, preview, info, filters;
- `.primary` for the main safe next action in a panel;
- danger styling only for destructive or high-risk actions;
- icon-only buttons only when the icon is obvious and has tooltip/label.

Do not hide dangerous actions in tiny ambiguous controls.

## Data and API Mental Model

Main read source:

- `GET /api/overview`

Important data groups in overview:

- `summary`;
- `services`;
- `registries.users`;
- `registries.egress`;
- `state.egress`;
- `state.route_classes`;
- `user_readiness`;
- `identity`;
- `events`;
- `access.roles`;
- `access.action_min_role`.

Mutation-like calls are generally under:

```text
/api/actions/...
```

Codex must inspect the backend handler before changing action behavior. Do not alter endpoint contracts casually.

## Required Services and Channel Selection

The current user table includes `Приоритеты`, meaning mandatory/preferred service groups for route/channel choice.

Current known groups in UI:

- YouTube;
- Instagram;
- Telegram;
- Google / Google Auth;
- ChatGPT / OpenAI Auth;
- Claude / Anthropic;
- WhatsApp.

Design implication:

The UI must make mandatory service requirements visible in the user row and user drawer. When choosing or recommending a channel, the operator should see whether the selected channel has live service support for the required services.

Do not present channel selection as only “fastest channel”. The choice must consider:

- required services;
- service matrix;
- channel health;
- capacity/load;
- route class;
- user/company policy;
- stickiness/current assignment;
- safety blockers.

## Drawer and Detail Rules

Use drawer for:

- user details;
- channel details;
- route details;
- check details;
- log/audit record details;
- navigation map;
- workflow playbook;
- operator scenario details.

Drawer should show:

- short summary;
- status pill;
- next safe action;
- grouped evidence;
- technical details only after summary;
- audit/log context when relevant.

Do not make operators leave the page for normal detail inspection.

## Operator Guidance

Current admin already has:

- `Что дальше`;
- `Сценарии`;
- `Карта админки`;
- contextual `Инф` panels.

Keep and strengthen this pattern.

Good guidance is not tutorial text everywhere. It should answer:

- where am I;
- what does this status mean;
- what should I do next;
- what is safe;
- what requires preview or confirmation.

## Responsive Behavior

Must work on desktop first, then tablet/mobile.

Desktop:

- dense tables;
- sticky top nav;
- drawers;
- grids.

Mobile/narrow:

- nav scrolls horizontally;
- grids collapse to one/two columns;
- tables remain horizontally scrollable;
- primary actions do not overflow;
- text must not overlap or disappear without a tooltip/alternative.

Do not scale font with viewport width.

## What Codex Should Do When Improving UI

Before editing:

1. Inspect `admin/v7-admin-api` for current runtime admin.
2. Inspect `/admin-v2` HTML structure or the latest design snapshot.
3. Identify the exact section/workspace affected.
4. Preserve existing endpoint behavior unless the task explicitly asks backend changes.
5. Preserve preview/apply separation.
6. Preserve audit and role requirements.

When designing:

1. Keep summary before details.
2. Keep operator next action visible.
3. Keep status semantics consistent.
4. Use tables for repeated operational entities.
5. Use cards only for compact summaries, checks, wizard steps and repeated status items.
6. Use drawers for details instead of new pages.
7. Keep raw JSON and technical logs behind detail/evidence surfaces.

After editing:

1. Verify `/admin-v2` renders.
2. Check desktop and mobile widths.
3. Check no text overlaps.
4. Check buttons fit.
5. Check unsafe actions still require preview/confirmation.
6. Check no credentials or secrets are exposed.

## Copy-Paste Prompt for Future Codex UI Tasks

```text
You are working on V7 Admin, the current operator admin console at /admin-v2.

This is not a landing page. It is an operational control panel for users, egress channels, routing intelligence, checks, security, backups, policy, autoswitch and logs.

Use the design/navigation contract in docs/track7/productization/V7_ADMIN_DESIGN_INTERFACE_NAVIGATION_BRIEF.md.

Respect the current information architecture:
- top nav: Главная, Пользователи, Каналы, Маршруты, Проверки, Безопасность, Настройки, Логи
- use workspace tabs inside sections instead of adding new top-level nav
- use drawer/details for drilldown
- preserve preview -> apply separation
- preserve role/audit/safety behavior
- preserve required-services/channel-selection semantics

Core UX rule:
Problem -> Evidence -> Diagnosis -> Action -> Verification -> Closure.

Do not make decorative dashboards. Build dense, calm, operator-first UI.
Use existing classes/tokens/patterns where possible: panel, table-shell, workspace-tabs, pill ok/warn/bad/info/muted, ghost, primary, drawer-section, wizard-card, filterbar, searchbar.

For any risky action, show scope, blast radius, preview/dry-run result, confirmation requirement, rollback/containment path and audit result.

Do not expose credentials or secrets. Do not bypass backend validation. Do not change endpoint contracts without migration notes.
```

## Open UI Cleanup Directions

These are likely next design improvements:

- Make required services and channel suitability more explicit in user drawer and channel matrix.
- Turn “what should operator do next” into a consistent component across Overview, Users, Channels and Routing.
- Normalize table column controls across users, channels and organizations.
- Separate read-only diagnostics from guarded apply visually in Routing and Settings.
- Improve Security copy so preview/apply/rollback boundaries are unmistakable.
- Add a consistent “evidence bundle” pattern for checks, logs and drawers.
- Keep `/admin-v2` as runtime fallback until the `web/` scaffold is explicitly migrated.
