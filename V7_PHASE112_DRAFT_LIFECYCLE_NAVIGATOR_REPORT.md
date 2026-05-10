# V7 Phase 112 — Draft Lifecycle Navigator

Дата: 2026-05-10

## Что сделано

- Добавлен lifecycle-навигатор для egress drafts.
- Backend теперь вычисляет для каждого draft:
  - текущий этап;
  - следующий безопасный шаг;
  - понятную подпись действия;
  - блокеры;
  - список этапов `Detect → Save Draft → Preflight → Runtime → Quarantine → Add Disabled → Provision → Enable`.
- `admin-v2` показывает lifecycle в карточке результата.
- В списке drafts колонка `Validation` теперь дополнительно показывает следующий шаг.
- После Clash `Create Draft` карточка результата явно говорит, что создан отдельный неактивный V7 draft и следующий шаг — `Preflight`.

## Зачем это нужно

После добавления Clash YAML у оператора появляется два разных объекта:

1. Исходный Clash bundle.
2. Отдельный child draft из выбранного proxy.

Lifecycle-навигатор не дает перепутать их:

- для Clash bundle следующий шаг = `Convert Clash proxy`;
- для child draft следующий шаг = `Run Preflight`;
- после успешных проверок следующий шаг меняется на `Runtime`, `Quarantine`, `Add Disabled`, `Provision`, затем `Ready for guarded Enable`.

## Безопасность

- Сетевое поведение не менялось.
- Runtime не запускается автоматически.
- Pool не меняется автоматически.
- Kill switch не меняется.
- Пользователи не перемещаются.
- Lifecycle — это только состояние и подсказки для оператора.

## Проверки

Локально:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/v7-pyc python3 -m py_compile admin/v7-admin-api
node --check /private/tmp/v7-admin-v2-phase112.js
git diff --check
tests/run-local-checks.sh
```

Unit-smoke:

- Создан временный Clash YAML draft.
- Из него создан child draft.
- Проверено:
  - source draft показывает `Convert Clash proxy`;
  - child draft показывает `Run Preflight`;
  - child protocol = `shadowsocks_or_outline`.

Сквозная dry-run проверка:

- Создан proxy draft с sing-box JSON.
- В песочнице вручную проставлены PASS-статусы preflight/runtime/quarantine.
- Проверено:
  - `Pool Preview` готов;
  - `Add Disabled` добавляет registry line;
  - `Runtime Provision` создает managed config;
  - lifecycle переходит в `Ready for guarded Enable`.

## Следующий шаг

Phase 113:

- сделать отдельный guarded `Enable` flow для disabled/provisioned каналов;
- перед enable показывать:
  - runtime readiness;
  - что изменится в registry;
  - что не будет меняться;
  - kill-switch readiness;
  - rollback hint;
- включение должно оставаться отдельным действием и не переносить пользователей автоматически.
