# Разделение fast service-failure path и CT-M0F certification fallback

**Дата:** 2026-08-12  
**Ремонтные commits:** `a488f35b`, `48628f26`  
**Последний deploy:** `deploy-z8-14-Updatesystem-48628f2-20260812T220913`

## Обнаруженная причина задержки

После восстановления fast event consumer штатный
`v7-autoswitch-planner.timer` действительно запускал существующий Matrix
consumer. Однако service unit всегда запускал после него второй legacy planner.
Этот planner повторял pre-planner snapshot refresh, inventory, policy и
durable closure; наблюдавшийся critical path был около 49--58 секунд до
любого apply gate.

После удаления этого повтора event-only Matrix consumer всё ещё мог при
обычном service-failure автоматически войти в controlled-topology / CT-M0F
certification fallback. Этот fallback вызывает полноценные diagnostic и Matrix
операции. Он принадлежит отдельной certification lane и не является условием
реального failover с текущего failed source на lawful healthy target.

## Исправление

1. `v7-autoswitch-planner.service` теперь вызывает только существующий
   `v7-service-matrix-refresh-all --consume-existing-service-failure-events-only`.
   Новый timer или scheduler не создан.
2. В event-only режиме controlled-topology, availability-first и CT-M0F
   certification fallbacks получают строгое
   `DEFERRED_TO_CT_M0F_CERTIFICATION_LANE` и не запускаются автоматически.
3. Существующий event consumer сохраняет текущую обычную цепочку:

   `canonical failure -> current source scope -> passive/OMP obligation ->
   existing governed bounded action -> existing verification/Outcome/Learning`.

   Следовательно, source не нужно восстанавливать до failover; при scope=0
   остаётся safe no-action, при scope>0 и здоровой lawful target допускается
   только уже существующий governed path.

## Проверка

- Focused tests: planner unit contract, event-only CT-M0F separation, current
  failure/current assignment scope, fast sentinel wake — PASS.
- Production: после deploy новый штатный planner process содержит только
  `v7-service-matrix-refresh-all --consume-existing-service-failure-events-only`
  и его обычный `--consume-service-failure-automation-only` consumer; ни
  `--pre-planner-refresh=write`, ни controlled-topology diagnostic как
  service-unit fallback не стартуют.
- `tools/v7-truth-check --all --json` и
  `tools/v7-convergence-status --json`: PASS / `FULLY_ALIGNED` для runtime,
  local и GitHub commit `48628f26`.
- Нет ручного Matrix run, synthetic event, policy write, Authority change,
  routing mutation, user movement или fabricated CT-M0F sample.

## Реальный остаток

CT-M0F не завершён и валидный latency sample не заявляется: текущий OMP /
governed reconciliation consumer сам остаётся долгим. Следующая работа
подчинена тому же CT-M0F parent: измерить его exact subspans на owner-backed
sample, убрать только повторяющиеся pre-cutover work внутри существующих
owners и повторно измерить. Это общая optimisation для всех channel identities,
а не VLESS-specific repair.
