# M5a: атомарная CPS-проекция свежего Authority Request

Дата: `2026-07-26T15:04:53Z`

## Цель

Закрыть только обнаруженный producer -> consumer разрыв: production owner уже формировал свежий read-only M5a Action Class Authority request, но CPS не хранил его точные `request_id`, `request_hash` и expiry. Поэтому CPS мог показывать общий `ENGINEERING_AUTHORITY`, не давая независимому Authority owner проверяемой ссылки на текущий запрос.

## Discovery и reuse

Переиспользованы существующие owners:

- `tools/v7-users-autoswitch` формирует M5a reconciliation и request;
- `admin_core/operator_execution.py` валидирует one-use request и остаётся единственным owner выдачи контракта;
- `tools/v7_sync_lib.py` остаётся единственным atomic CPS writer;
- `tools/v7-truth-check` остаётся существующим CLI consumer CPS reconciliation.

Новый registry, Authority owner, policy writer, Candidate/Packet/lease owner или Runtime не созданы.

## Реализованное соединение

Добавлен безопасный режим:

`tools/v7-truth-check --reconcile-action-class-contract-request PATH --json`

Он принимает только полный fresh result существующего M5a owner и fail-closed проверяет:

1. schema, pending status, hash, request ID и short expiry через существующий Authority validator;
2. exact `ENGINEERING_AUTHORITY_ACTION_CLASS_CONTRACT_REQUEST_READY` и exact legal next action;
3. package binding request ID/hash/expiry и отсутствие Packet;
4. scope `max_users=1`, `max_concurrent_transactions=1`, source/incident generations, verification, rollback, cooldown, anti-flap и stop conditions через Authority validator;
5. отсутствие contract issuance, policy write, Candidate, Packet, lease, apply, routing mutation, user movement, rollback apply, Authority expansion и Production Maturity change.

После проверки existing atomic CPS writer одновременно обновляет Section 0, registry, protected CAP-U07 row и deterministic sequence. Он добавляет только текущие references:

- `CURRENT_AUTHORITY_REQUEST_ID/HASH/EXPIRY/FINGERPRINT/STATUS/SCOPE`;
- `CURRENT_PACKET=NONE`;
- `CURRENT_LEASE=NONE`.

## Проверка

- `python3 -m unittest tests.unit.test_service_failure_automation_evolution` — `15/15 PASS`.
- Тесты подтверждают успешную atomic CPS projection валидного M5a request и fail-closed rejection изменённой identity.
- Static compilation — PASS.
- `tools/v7-truth-check --local --json` до коммита ожидаемо возвращает `LOCAL_NO_GO` только из-за незакоммиченных runtime-critical файлов данной реализации и уже существующих чужих report changes; semantic failure не обнаружен.

## Запрещённые эффекты

`NONE`: контракт не выдан, `/etc/v7/policy.json` не изменён, Packet/lease не созданы, restore barrier не записан, apply/routing/user movement/rollback не выполнены, Authority и Production Maturity не изменены.

## Точный следующий legal terminal

После deploy и fresh production caller CPS будет содержать один актуальный M5a request. Дальше допускается только независимое решение существующего Authority owner `APPROVE_ONCE_AS_SCOPED` либо `DECLINE` для его exact request ID/hash до expiry. При отсутствии такого решения программа остаётся `ENGINEERING_AUTHORITY`; M5b, Candidate, Packet, lease, restore barrier и execution не запускаются.
