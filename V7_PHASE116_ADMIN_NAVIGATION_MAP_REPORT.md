# V7 Phase 116 — Admin Navigation Map

Date: 2026-05-10

## Goal

Improve the redesigned admin navigation without making the UI visually heavier.

The operator should understand:

- where each major function lives;
- which workspace is safe/read-only;
- where deeper lifecycle actions are located;
- why the Gosuslugi/RU path is currently client-side RU_LOCAL, not a noisy server-side control on every screen.

## Implemented

- Added top-level `Карта` button in Admin V2.
- Added `Карта раздела` button to:
  - `Каналы`
  - `Маршруты`
- Added drawer-first navigation help:
  - Admin map: Главная, Пользователи, Каналы, Маршруты, Проверки, Безопасность, Настройки, Логи.
  - Channels map: Обзор, Добавить канал, Сервисная матрица, Готовность и скорость.
  - Routing map: Обзор, Группы доменов, Проверка, Режимы клиентов, Готовность RU, Факт маршрутов.
- Kept the main pages compact:
  - no new heavy table on the root screens;
  - no raw JSON on primary navigation pages;
  - safety explanations live in drawer.

## Safety Notes

- This is UI/navigation only.
- No routing changes.
- No user movement.
- No egress enable/disable.
- No kill switch changes.
- No secrets displayed.

## Validation

```bash
PYTHONPYCACHEPREFIX=/private/tmp/v7-pyc python3 -m py_compile admin/v7-admin-api
awk 'BEGIN{n=0} /<script>/{n++; flag=(n==1); next} /<\/script>/{if(flag){exit}; flag=0} flag' admin/v7-admin-api > /private/tmp/v7-admin-v2-phase116.js
node --check /private/tmp/v7-admin-v2-phase116.js
git diff --check
tests/run-local-checks.sh
```

Result:

```text
V7_LOCAL_CHECKS=OK
```

## Manual UI Check

1. Open Admin V2.
2. Click `Карта` in the top bar.
3. Confirm a drawer opens with all major sections and short explanations.
4. Open `Каналы` and click `Карта раздела`.
5. Open `Маршруты` and click `Карта раздела`.
6. Confirm guide buttons navigate to the expected workspace and do not apply any changes.

