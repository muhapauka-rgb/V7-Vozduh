# V7 Phase 113 — Guarded Draft Enable

Дата: 2026-05-10

## Что сделано

- Добавлен отдельный guarded flow включения draft-канала после `Add Disabled` и `Runtime Provision`.
- Новые endpoints:
  - `POST /api/actions/egress-draft-enable-preview`
  - `POST /api/actions/egress-draft-enable-apply`
- В `admin-v2` у draft появляется кнопка `Enable`, когда:
  - draft уже добавлен в pool как disabled;
  - runtime profile готов;
  - readiness показывает `enable_ready=true`.
- Apply требует typed confirmation:
  - `ENABLE_DRAFT_EGRESS`

## Логика

Новый канал идет так:

```text
Draft
→ Preflight
→ Runtime
→ Quarantine
→ Add Disabled
→ Provision Runtime
→ Enable Preview
→ Enable Apply
```

Enable делает только одно:

- меняет egress в registry на `enabled=1` через существующий `v7-egress-set-state`.

Enable НЕ делает:

- не переносит пользователей;
- не меняет per-user route tables;
- не запускает rebalance;
- не меняет kill switch;
- не перезапускает V7 services.

## Guard checks

Перед apply проверяется:

- draft существует;
- draft имеет `pool_egress_id`;
- egress есть в `egress.registry`;
- registry сейчас `enabled=0`;
- runtime profile status = `READY`;
- runtime readiness = `enable_ready`;
- `v7-egress-set-state <egress> enabled` preview проходит.

## Lifecycle

Lifecycle теперь понимает финальное состояние:

- до enable: `Ready for guarded Enable`;
- после enable: `Enabled`.

## Проверки

Локально:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/v7-pyc python3 -m py_compile admin/v7-admin-api
node --check /private/tmp/v7-admin-v2-phase113.js
git diff --check
tests/run-local-checks.sh
```

Unit-smoke:

- В песочнице создан proxy draft.
- Проставлены PASS-статусы preflight/runtime/quarantine.
- Выполнены:
  - `Add Disabled`;
  - `Runtime Provision`;
  - `Enable Preview`;
  - `Enable Apply`.
- Проверено:
  - registry получил `enabled=1`;
  - metadata получила `pool_action=enabled`;
  - lifecycle перешел в `Enabled`;
  - секрет не попал в JSON response.

## Следующий шаг

Phase 114:

- сделать “post-enable validation”:
  - проверить registry;
  - проверить runtime profile path;
  - проверить egress readiness;
  - показать, что users не перемещены;
  - показать оператору безопасные следующие действия: manual switch одного пользователя или rebalance dry-run.
