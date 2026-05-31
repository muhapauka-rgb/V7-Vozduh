# E35.0 Admin Surface Audit

## Scope

Audit question: where should Routing Mode, Preferred Channel, Group Constraints, and Required Services appear in the existing admin.

## Existing Admin Sections

Current V7 Admin sections:

- Главная
- Пользователи
- Каналы
- Маршруты
- Проверки
- Безопасность
- Настройки
- Логи

No new top-level section is needed.

## Current Placement

Organizations/groups:

- `Пользователи` -> `Организации`

Required services:

- `Пользователи` table `Приоритеты`
- user priority drawer `Обязательные сервисы`

Channel suitability:

- `Каналы` -> `Сервисная матрица`
- channel drawer/proposals/evidence

Route modes:

- `Маршруты` -> route/client modes
- `Настройки` -> `Режимы маршрутов`

Org/channel policy:

- `Настройки` -> org/capacity policy editor
- channel onboarding organization scope

## Recommended Placement

Routing Mode / Preferred Channel:

- Primary: `Пользователи` row and user drawer.
- Secondary: `Маршруты` user route reality drawer.

Required Services:

- Keep in `Пользователи`, but wording should clarify it is a suitability/proposal signal until hard gates exist.
- Add suitability result near the current channel in the user drawer.

Group Constraints:

- Primary: `Пользователи` -> `Организации` group editor.
- Secondary: `Настройки` policy impact view.
- Channel scope visibility: `Каналы` drawer/onboarding.

Channel Suitability:

- Primary: `Каналы` matrix and channel drawer.
- Cross-link from user drawer to best/worst matching channels.

## Audit Verdict

admin_surface_audit_complete=true
new_top_level_section_needed=false
current_admin_can_host_e35=true

## E35 Implication

The next implementation should extend existing workflows, not create a new admin area. The most operator-useful path is:

Пользователь -> обязательные сервисы -> suitability -> proposal/governance path.
