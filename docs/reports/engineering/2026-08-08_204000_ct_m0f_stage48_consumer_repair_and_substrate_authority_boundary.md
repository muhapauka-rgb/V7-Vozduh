# CT-M0F / Stage-48: consumer repair и точная Authority boundary

Дата: 2026-08-08

## Результат

Два существующих producer → consumer дефекта устранены и развёрнуты в production.

1. После `perfclose_6e6c4fa62f834a8d4b88da24` Matrix ошибочно публиковал
   `STAGE_48_EXISTING_OWNER_ADMISSION_REQUIRED`, хотя active standing contract
   `sdpc_285af5fc6f4de20415c3e5b1` уже разрешает этот certification-only action
   class до 48 при serial execution. Теперь receipt является prerequisite, а не
   второй неявной Authority границей.
2. Producer запроса substrate неверно связывал выбранный shared Planner target
   с несуществующим `EXECUTION_ONLY` contract и завершался исключением. Теперь
   shared target остаётся предметом свежей revalidation, а запрос отражает
   точный incremental delta: 40 → 48, то есть максимум 8, а не 48 identities.

## Production доказательства

- Commit `3c022b9057815285c39b6a56c431db34f46cad88` развернут штатным
  `tools/v7-safe-deploy`. Следующий обычный Matrix timer автоматически вызвал
  `v7-governed-canary-dry-run-cycle --execute-availability-first-standing-stage
  --availability-first-stage 48`.
- Matrix дошёл до live gates без ручного запуска и без movement:
  `stage_48_optimized_runtime_ready=true`,
  `stage_48_execution_permitted=true`, `users_moved=0`.
- Законный terminal: `GOVERNED_TRANSACTION_STOPPED` /
  `availability_first_standing_stage_not_admitted` с exact blockers
  `availability_first_controlled_source_missing` и
  `availability_first_source_cohort_too_small`.
- Commit `2474717707e65ac8c8d1032a48cf9f023204fbe6` развернут как
  `deploy-z8-14-Updatesystem-2474717-20260808T203725`. Post-deploy existing
  Authority producer выпустил один append-only request:
  `cpsauth_r1_ef268a075d65194d0fae03a1` /
  `ef268a075d65194d0fae03a15339a43e3b692e0a24362a4e588ae5c4844ab624`.

## Точная граница

Request действует до `2026-08-09T13:38:18.834910+00:00` и просит только
явно перечисленные subscopes: `IDENTITY_PROVISIONING`,
`CERTIFICATION_CLASSIFICATION_AND_ASSIGNMENT`, `CONTROLLED_SOURCE_CONDITION`,
`PROGRESSIVE_CAMPAIGN_EXECUTION`. Он не содержит policy write, Packet/lease,
restore barrier, Runtime apply, routing mutation, ordinary customer effect,
Authority expansion, Production Maturity change или Natural L8 credit.

До независимого решения по этому exact request законный следующий terminal:
`ENGINEERING_AUTHORITY_CONTROLLED_CERTIFICATION_SUBSTRATE_REQUEST_READY`.
После APPROVE/DECLINE existing owners обязаны заново проверить registry,
source/target, capacity, health, Packet/lease и all live gates; исторические
artifacts не переиспользуются.

## Проверки

- `python3 -m unittest tests.unit.test_service_failure_episode` — PASS (62).
- Focused producer tests — PASS.
- `tools/v7-safe-deploy` manifest перед каждым deploy — PASS, only declared
  allowlisted runtime paths.
- После предыдущего deploy `tools/v7-truth-check --all --json` —
  `FULLY_ALIGNED`; `tools/v7-convergence-status --json` — `ALIGNED`.

