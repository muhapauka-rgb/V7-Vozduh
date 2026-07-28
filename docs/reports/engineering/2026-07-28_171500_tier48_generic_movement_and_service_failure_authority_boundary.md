# Tier-48: generic movement, Service Failure adapter и независимая Authority boundary

Дата: `2026-07-28` (`Asia/Bangkok`)

Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

Исполнимая ревизия: `V2.0`
Статус: `T48_ENGINEERING_AND_ADAPTER_CONSUMED; EXACT_TIER48_SERVICE_FAILURE_AUTHORITY_DECISION_REQUIRED`

## Итог

`T48-M0`–`T48-M6` выполнены через существующих владельцев. Generic movement
primitive, adaptive exact-cohort contract и Service Failure adapter инженерно
квалифицированы до `48` пользователей при строго последовательных транзакциях
(`max_concurrent_transactions=1`). Existing production evidence и Polygon /
implementation-contract evidence разделены; инженерная проверка не выдала
Authority и не была записана как новый production Outcome.

Новая Program, Mission, Authority owner, Planner, Runtime, queue, watcher,
registry или truth source не создавались.

## Discover → Reuse → Extend → Implement

Повторно прочитаны owners generic movement, governed transaction,
operation-scoped binding, historical blast-radius evidence, Service Failure
Matrix/autoswitch, Polygon scenario corpus, standing policy/audit, CPS и OMP.

Переиспользованы:

- production evidence scopes `1,2,4,5,10,25,48` только для уже доказанных
  assignment/route/outcome dimensions;
- существующие Candidate/Packet/lease, cooldown, anti-flap, capacity,
  verification, rollback/no-rollback и circuit-breaker contracts;
- существующий Polygon design-time owner и сценарий partial apply;
- существующий Authority policy/audit owner и CPS atomic reconciliation.

Минимально расширены существующие owners:

- adaptive cohort selection теперь ограничена одновременно Authority,
  incident scope, live capacity и текущей load envelope;
- exact cohort identity, per-member subreceipts, durable checkpoint,
  duplicate-forward-apply denial, partial-apply containment и cohort circuit
  breaker доказаны для `1,2,4,5,10,25,48`;
- Service Failure adapter явно наследует generic primitive до `48`, но не
  наследует Authority или production evidence автоматически;
- CPS хранит независимые оси engineering certification, production evidence,
  Authority approval и Runtime enablement.

## Реализация, тесты и deploy

Runtime commit: `7fbc91fab17b3b91de04411a07d460dbe077eb03`

Deploy: `deploy-z8-14-Updatesystem-7fbc91f-20260728T165531`

Deploy manifest содержал только:

- `tools/v7_sync_lib.py`;
- `tests/scenarios/future_scale/foundation.json`;
- `tools/v7-users-autoswitch`;
- `admin_core/autonomy_trust_acceleration.py`;
- `admin_core/operator_execution.py`.

Affected campaign: `529 passed` за `106s`. Проверены Authority contracts,
Packet/lease, autoswitch, Service Failure, Polygon, governed canary и
operation-scoped binding.

Первый production direct caller честно обнаружил deployed caller → scenario
corpus binding gap: `/usr/local/tests/scenarios/future_scale/foundation.json`
не являлся production layout owner. Assertions и semantic gate не ослаблялись.
Existing `polygon_production_certification_layout` был подключён к прямому
deployed entrypoint.

Repair commit: `cb2f50d1e48dbfe1c68390d906356fec7220c51f`

Deploy: `deploy-z8-14-Updatesystem-cb2f50d-20260728T170109`

После repair production non-test caller
`/usr/local/bin/v7-truth-check --omp-scenario-execution
PHASE6V4_PARTIAL_APPLY_CIRCUIT_BREAKER --json` завершился `PASS`:

- evidence class: `ENGINEERING_SCENARIO_EVIDENCE`;
- scenario fingerprint:
  `f5ec55d8ca79f1670e8d9215b411965a876120d869112abee5583e641461f521`;
- dependency fingerprint:
  `439b9dede94733f2a72925a4300a06b96bcf1089a5ca5058cdfc076f3b0b27ba`;
- replay: `fsreplay_522bb28af7b03ab9d44331b7`;
- consumer: `OMP_PROGRAM_EXECUTION_RECONCILIATION`, `consumed=true`;
- next scenario: `NONE`, corpus frontier exhausted;
- Authority, Packet, Production Maturity, restore barrier, rollback apply,
  routing/runtime mutation и user movement: `NONE`.

## Четыре независимые оси

| Ось | Owner-backed current truth |
| --- | --- |
| Generic production evidence | scopes до `48`, только exact historical dimensions |
| Engineering certification | exact cohort contracts и containment до `48` |
| Service Failure adapter | engineering compatible до `48` |
| Authority / Runtime | действующий Tier-4 contract; `max_users=4`, concurrency `1` |

Controlled Service Failure adapter Outcomes для `5 → 10 → 25 → 48` остаются
отдельным residual после независимого Authority решения. Они не были
сфабрикованы Polygon и не засчитаны из engineering evidence.

## T48-M7 — свежий независимый запрос

Существующий production Authority owner зарегистрировал ровно один свежий
request; contract не выдавался:

- request: `sdpauth_r1_e3aecc34f26ffbff4fdc169c`;
- request hash:
  `e3aecc34f26ffbff4fdc169c10b9e4f13c693e374e24d71c6f00ed03e88fd600`;
- policy scope hash:
  `1c716df6801e28c004613e23d27ef66702cfc7e8c489a274f210435b723271e0`;
- expires at: `2026-07-29T10:05:20.106430+00:00`;
- decision set: `APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY` или `DECLINE`;
- exact scope: `channel hard-fail failover`, `max_users=48`,
  `max_concurrent_transactions=1`, existing Planner safe targets only, fresh
  Candidate/Packet/lease, live capacity/health/freshness/cooldown/anti-flap,
  per-user + aggregate verification, rollback or certified no-rollback,
  cohort circuit breaker, final safe mode `OPEN`, self-expansion forbidden.

Registration write затронула только existing append-only Authority audit.
`authority_granted=false`, `policy_write=false`, `runtime_apply=false`,
`routing_mutation=false`, `users_moved=0`.

Штатный CPS bridge подтвердил request как единственный `PENDING`, сохранил
действующий Tier-4 contract `sdpc_a3cd9882bf0850010a6e37b5` и атомарно
записал текущие оси без forbidden effects.

## Exact legal terminal и residual

Текущий терминал:

`EXACT_TIER48_SERVICE_FAILURE_AUTHORITY_DECISION_REQUIRED`.

Это независимая Authority boundary, а не engineering blocker и не завершение
всей V2.0 программы. До решения запрещены Tier-48 Runtime activation,
Candidate/Packet/lease для такого выполнения, user movement и production
cohort Outcome.

После owner-backed `APPROVE` допустимы только утверждённые `T48-M8`–`T48-M9`:
Polygon готовит controlled condition, а существующий Runtime последовательно
получает настоящие Service Failure Outcomes `5 → 10 → 25 → 48` через каждый
fresh live gate. `DECLINE` сохраняет Tier-4 и формирует соответствующий
owner-backed terminal. Полная Program closure возможна только после
consumption controlled Outcomes, Replay/Learning, CPS/OMP reconciliation и
финальной `T48-M10` verification.
