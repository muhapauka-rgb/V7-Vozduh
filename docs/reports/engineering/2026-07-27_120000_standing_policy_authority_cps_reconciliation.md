# Reconciliation действующей standing policy с CPS

Дата: 2026-07-27

## Итог

`PASS` — устранён разрыв между фактическим owner-backed standing contract в production и устаревшей CPS-проекцией, которая ошибочно ожидала ещё одного Engineering Authority решения.

## Причина

Production `/etc/v7/policy.json` и append-only audit существующего владельца `admin_core/operator_execution.py` уже содержали действующий контракт:

- contract: `sdpc_f200a060c720a12669248105`;
- source request: `sdpauth_r1_906f2d2515016198d4c47727`;
- решение: `APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY`;
- expiry: `2026-08-25T17:21:00.971884+00:00`;
- audit provenance: ровно одна соответствующая запись.

Однако CPS продолжал показывать этот же request как `AWAITING_INDEPENDENT_AUTHORITY_DECISION`. Это создавало ложный `ENGINEERING_AUTHORITY` terminal и блокировало законный путь re-entry на новом событии.

## Исправление

В существующих владельцах добавлено только следующее:

1. `tools/v7-users-autoswitch --standing-delegated-policy-status` — redacted read-only проверка policy + append-only audit. Она не создаёт Candidate, Packet или lease и не входит в planner/apply path.
2. `tools/v7-truth-check --reconcile-active-standing-delegated-policy` — production read-only caller этого статуса и атомарный CPS consumer.
3. `tools/v7_sync_lib.py` — fail-closed валидация schema, active program, exact contract/request identity, scope hash, expiry и audit provenance до единственной CPS-записи.

В CPS зафиксировано:

- `CURRENT_AUTHORITY_REQUEST_STATUS = ACTIVE_OWNER_BACKED_STANDING_POLICY`;
- terminal: `REAL_WORLD_LIMIT_WAIT_FOR_FRESH_MATCHING_SERVICE_FAILURE_EVENT`;
- exact next action: `V7_SERVICE_FAILURE_AUTOMATION_FRESH_EVENT_REVALIDATION`.

Это не является выдачей нового Authority: действующий contract лишь допускает автоматическую revalidation **после нового matching owner-backed service-failure event**. Каждый Candidate, Packet и lease всё равно обязан быть новым; исторические identity не переиспользуются.

## Проверки

- focused unit tests: PASS, включая позитивную CPS-reconciliation проверку и Authority-precedence regression;
- production deploy: `deploy-z8-14-Updatesystem-4b08e75-20260727T115816`;
- production policy/audit caller: PASS;
- source CPS atomic write + reread + consistency: PASS;
- Continue OMP после reconciliation: `REAL_WORLD_LIMIT_EXTERNAL_BOUNDARY_PRESERVED`, без внутренней работы и без мутаций.
- final truth/convergence: `PASS`, `FULLY_ALIGNED`; local, GitHub и production runtime указывают на `4b08e751e4f206db1a80dd0bae20d6475f1066ff`.

## Запрещённые эффекты

Все равны `false` / `0`: policy write, contract issuance, Candidate/Packet/lease creation, restore-barrier write, Runtime apply, routing mutation, user movement, rollback apply, Authority expansion и изменение Production Maturity.

## Точный следующий frontier

`V7_SERVICE_FAILURE_AUTOMATION_FRESH_EVENT_REVALIDATION` — только при свежем owner-backed matching service-failure event. Существующий Service Matrix затем выполняет planner revalidation и допускает лишь fresh identities через уже активный standing policy contract.
