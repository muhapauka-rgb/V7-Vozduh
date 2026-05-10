# V7 Phase 118 — Compact Users Table + User Events Drawer

Date: 2026-05-10

## Goal

Make the `Пользователи` workspace easier to scan while keeping all detailed operator tools close to the user.

## Implemented

- Reduced the main users table to compact operational columns:
  - Пользователь
  - Готовность
  - Канал / маршрут
  - Подключение
  - Был онлайн
  - Скорость
  - Действие
- Updated the overview users mini-table to use the same compact model.
- Added user-specific events to `/api/user-detail`.
- Added `Recent user events` section to the live user drawer.

## Existing Drawer Sections Preserved

- Onboarding flow.
- Next action.
- Operator actions.
- Route reality.
- Client speed.
- Profiles and delivery.
- Warnings.
- Recent user commands.
- Switch history.
- Raw user detail.

## Safety Notes

- UI and read-only detail endpoint only.
- No user movement.
- No routing changes.
- No profile regeneration.
- No egress changes.
- No secret exposure.

## Validation

```bash
PYTHONPYCACHEPREFIX=/private/tmp/v7-pyc python3 -m py_compile admin/v7-admin-api
awk 'BEGIN{n=0} /<script>/{n++; flag=(n==1); next} /<\/script>/{if(flag){exit}; flag=0} flag' admin/v7-admin-api > /private/tmp/v7-admin-v2-phase118.js
node --check /private/tmp/v7-admin-v2-phase118.js
git diff --check
tests/run-local-checks.sh
```

Result:

```text
V7_LOCAL_CHECKS=OK
```

## Manual UI Check

1. Open Admin V2.
2. Go to `Пользователи`.
3. Confirm the table is compact and readable.
4. Click a user row.
5. Confirm the drawer includes route, speed, profiles, warnings, commands, events, and switch history.

