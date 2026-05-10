# V7 Phase 117 — Compact Channels Table + Drawer Details

Date: 2026-05-10

## Goal

Make the `Каналы` workspace easier for an operator to scan:

- keep the table compact;
- show only high-signal operational state in the row;
- move heavy details into the channel drawer.

## Implemented

- Reduced the main channel table from many technical columns to compact columns:
  - Канал
  - Состояние
  - Роль / сервисы
  - Скорость
  - Пользователи / нагрузка
  - Готовность
  - Действие
- Updated the overview channel mini-table to use the same compact model.
- Added related draft lifecycle data to `/api/egress-detail`.
- Added a `Lifecycle` section inside the live channel drawer:
  - draft id / label
  - validation
  - pool action
  - runtime readiness
  - next action

## Safety Notes

- UI and read-only detail endpoint only.
- No routing changes.
- No user movement.
- No egress state changes.
- No service restarts.
- No secret exposure.

## Validation

```bash
PYTHONPYCACHEPREFIX=/private/tmp/v7-pyc python3 -m py_compile admin/v7-admin-api
awk 'BEGIN{n=0} /<script>/{n++; flag=(n==1); next} /<\/script>/{if(flag){exit}; flag=0} flag' admin/v7-admin-api > /private/tmp/v7-admin-v2-phase117.js
node --check /private/tmp/v7-admin-v2-phase117.js
git diff --check
tests/run-local-checks.sh
```

Result:

```text
V7_LOCAL_CHECKS=OK
```

## Manual UI Check

1. Open Admin V2.
2. Go to `Каналы`.
3. Confirm the channel table is compact and readable.
4. Click a channel row.
5. Confirm the drawer includes:
   - Enable readiness
   - Channel actions
   - Lifecycle
   - Speed comparison
   - Assigned users
   - Client speed samples
   - Service matrix
   - Configuration
   - Recent channel events

