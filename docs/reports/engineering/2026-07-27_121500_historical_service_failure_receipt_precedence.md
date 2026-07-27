# Защита active standing-policy frontier от исторической Service Failure квитанции

Дата: 2026-07-27

## Итог

`PASS` — историческая безопасная квитанция OMP теперь потребляется в CPS без
замены действующего frontier `V7_SERVICE_FAILURE_AUTOMATION_FRESH_EVENT_REVALIDATION`.

## Обнаруженный разрыв

Production owner уже один раз законно потребил историческую Service Failure
квитанцию:

- receipt: `sfomp_9de75be9b0e39374d2c916e3`;
- source incident: `sxe_85d1171940a4ea9bc6c3097ee79e3861`;
- Situation: `situation_53539f91b52567f1095df086`;
- Decision Trace: `decision_356fe5f1626216ac1974b138`;
- classification: `CORRECT_SAFE_TERMINAL`.

До исправления общий CPS consumer мог проецировать такой исторический terminal
как текущий, хотя отдельный Authority owner уже подтвердил действующий standing
contract `sdpc_f200a060c720a12669248105`. Это создавало риск потери живого
fresh-event re-entry frontier. Это producer-consumer precedence defect, а не
новая Authority, production incident или основание для apply.

## Исправление и результат

В существующей функции `reconcile_service_failure_automation_receipt_to_cps`
добавлено узкое fail-closed правило: при активной audit-verified standing policy
и `CORRECT_SAFE_TERMINAL` historical receipt CPS записывает только audit pointer
к receipt, сохраняя active-policy state, stop condition и fresh-event successor.

Атомарная source-CPS проекция содержит:

- `LAST_SERVICE_FAILURE_RECEIPT_ID = sfomp_9de75be9b0e39374d2c916e3`;
- `LAST_SERVICE_FAILURE_RECEIPT_CONSUMPTION = HISTORICAL_CONSUMED_ACTIVE_STANDING_POLICY_FRONTIER_PRESERVED`;
- transition: `SERVICE_FAILURE_AUTOMATION_HISTORICAL_RECEIPT_CONSUMED_NO_TERMINAL_OVERRIDE_V1`;
- current next action: `V7_SERVICE_FAILURE_AUTOMATION_FRESH_EVENT_REVALIDATION`.

## Проверки

- focused tests: PASS — исторический receipt не вытесняет standing-policy
  frontier, обычная reconciliation сохраняется, stale one-use Authority
  projection заменяется active policy;
- production deploy: `deploy-z8-14-Updatesystem-39fcccc-20260727T120545`;
- deploy manifest: только `tools/v7_sync_lib.py`;
- production receipt прочитан из существующего append-only closure owner и
  атомарно reconciled в source CPS;
- Continue OMP: `PASS`,
  `REAL_WORLD_LIMIT_EXTERNAL_BOUNDARY_PRESERVED`;
- effects: `0` users moved; Runtime/routing/apply/rollback/restore-barrier,
  Authority expansion и Production Maturity change — отсутствуют.

## Точный terminal и re-entry

Текущий terminal остаётся реальным внешним boundary, а не зависанием:
`REAL_WORLD_LIMIT_WAIT_FOR_FRESH_MATCHING_SERVICE_FAILURE_EVENT`.

Только новый matching owner-backed service-failure event может снова запустить
существующий Matrix -> Planner path. Он обязан создать новые Candidate, Packet и
lease identities; ни receipt, ни исторические execution identities повторно не
используются.
