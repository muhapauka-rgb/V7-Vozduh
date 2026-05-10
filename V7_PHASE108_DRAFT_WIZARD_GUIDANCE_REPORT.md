# V7 Phase 108 — Draft Wizard Guidance

Дата: 2026-05-10

## Что добавлено

- В `admin-v2` добавлены понятные операторские подсказки для egress draft wizard.
- Для `draft_unknown` показывается:
  - формат не распознан;
  - можно сохранить как безопасный черновик;
  - runtime/pool/routing/kill switch не будут затронуты.
- Для `draft_incomplete` / `needs_operator_fix` показывается:
  - каких полей не хватает;
  - почему preflight/runtime/pool заблокированы.
- Для OpenVPN:
  - показывается, что формат распознан;
  - runtime заблокирован до безопасного adapter.
- Для Clash YAML:
  - показывается, что нужен converter в V7-managed sing-box profile.

## UI safety

- В таблице draft-каналов опасные кнопки стали disabled, когда шаг ещё недоступен.
- Runtime/Quarantine/Pool/Add Disabled недоступны для:
  - unknown draft;
  - incomplete draft;
  - OpenVPN без adapter;
  - Clash YAML без converter.
- Preflight остаётся доступен для распознанных OpenVPN/Clash, чтобы получить понятный отчет/blockers.

## Проверки

- `python3 -m py_compile admin/v7-admin-api`
- extract `admin-v2` JavaScript из HTML
- `node --check /private/tmp/v7-admin-v2-phase108.js`
- `git diff --check`
- `tests/run-local-checks.sh`
- VPS deploy:
  - backup `/root/v7-admin-api.bak.<timestamp>.phase108`
  - `v7-admin-api.service` active

## Следующий шаг

- OpenVPN normalizer:
  - dry-run нормализация;
  - запрет dangerous scripts/hooks;
  - route/script/credentials блокеры;
  - только после этого runtime adapter.
