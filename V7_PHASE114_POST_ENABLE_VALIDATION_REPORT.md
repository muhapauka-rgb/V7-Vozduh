# V7 Phase 114 — Post-Enable Validation

Дата: 2026-05-10

## Что сделано

- Добавлена read-only проверка после включения draft-канала.
- Новый endpoint:
  - `POST /api/actions/egress-draft-post-enable-validation`
- `Enable Apply` теперь сразу возвращает `post_enable_validation`.
- В `admin-v2` добавлен блок `Post-Enable Validation`.
- В списке drafts после enable появляется кнопка `Validate`.

## Что проверяет Post-Enable Validation

- egress есть в `egress.registry`;
- egress действительно `enabled=1`;
- runtime profile path существует;
- runtime readiness не сломан;
- enable не перенес пользователей;
- enable не менял маршруты;
- enable не менял kill switch;
- показывает безопасные следующие действия:
  - service matrix;
  - manual switch одного пользователя;
  - rebalance dry-run.

## Важно

Post-enable validation ничего не меняет.

Это контрольный лист после включения канала, чтобы оператор видел:

```text
Канал включен в pool.
Пользователи не переехали.
Маршруты не менялись.
Следующий шаг безопасный и ручной.
```

## Проверки

Локально:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/v7-pyc python3 -m py_compile admin/v7-admin-api
node --check /private/tmp/v7-admin-v2-phase114.js
git diff --check
tests/run-local-checks.sh
```

Unit-smoke:

- Создан proxy draft.
- Выполнены:
  - `Add Disabled`;
  - `Runtime Provision`;
  - `Enable Apply`;
  - `Post-Enable Validation`.
- Проверено:
  - post-enable status = `OK`;
  - `registry_enabled` = `OK`;
  - `assigned_users=0`;
  - `users_moved_by_enable=false`;
  - `routes_changed_by_enable=false`;
  - секрет не попал в JSON response.

## Следующий шаг

Phase 115:

- сделать безопасный “next action panel” после enable:
  - кнопка service matrix;
  - кнопка manual switch для одного тестового пользователя;
  - кнопка rebalance dry-run;
  - без автоматического переноса пользователей.
