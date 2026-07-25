# Аудит существующей автоматизации Service Failure

Дата: `2026-07-25`

Commit snapshot: `711b6a77ca034911d6d12743866390d0ae18c7b2`

Ветка: `Updatesystem`

## Вердикт

Предложение строить новый `Automation Gap Closure Engine` отклонено как
дублирование. В V7 уже существуют OMP Automation Gap Closure, полноценный
autoswitch Decision Matrix, bounded emergency failover, Shadow Autonomy,
Outcome/Learning и Authority Evolution.

Фактическая недоработка — не отсутствие механизмов, а незамкнутый production
producer -> consumer:

```text
Service Failure capture
-> passive STOP_SAFE chain
-> transient OMP frontier
-> missing durable OMP consumption
```

Следовательно, дальнейшая программа должна соединить существующих owners, а не
создавать новые подсистемы.

## Что подтверждено

| Область | Доказанный статус |
| --- | --- |
| OMP Automation Gap Closure V4.7-V4.10 | полный canonical contract; реальный Service Failure caller не найден |
| Service Failure producer | production Matrix timer активен |
| Passive consumer | production-called, records Situation/Decision/Outcome/replay/Learning |
| OMP product frontier | создаётся только в результате нового consumption и затем теряется из latest-run projection |
| OMP runtime consumer этого frontier | не найден |
| Decision Matrix | capacity, service suitability, policy, confidence, cooldown, anti-flap, rollback и safety gates уже существуют |
| Emergency failover | реализован, тесты проходят, ограничен одним пользователем; current capability inactive |
| Autoswitch timer | installed/enabled, но production `inactive`; manual-mode boundary подтверждён |
| Shadow Autonomy | модель и JSONL owner существуют; production history пуст; автоматического producer нет |
| Shadow model current read-only projection | формирует MOVE/KEEP без apply; outcome comparisons отсутствуют |
| Outcome/Learning | существующие execution, feedback, trust, replay и calibration owners присутствуют |
| Authority | CPS `GOVERNED_ONLY`; автоматическое расширение запрещено |

## Production observations

- `v7-service-matrix-refresh.timer`: `enabled`, `active`.
- `v7-users-autoswitch.timer`: `enabled`, `inactive` с 2026-07-02.
- `l3-runtime-state.json`: capability реализована и ранее production-proven,
  однако `active_capability=false`.
- passive consumption records: `103`.
- текущий shadow JSONL: `0` records.
- Matrix latest-run summary после idempotent replay содержит `0`
  `omp_product_frontiers`, хотя durable incident consumption ранее состоялось.
- production runtime binaries совпадают с local snapshot commit `711b6a77`.

## Последний ответственный link

Producer:

`tools/v7-users-autoswitch._consume_passive_production_events`

Transient projection:

`tools/v7-service-matrix-refresh-all -> service-matrix-refresh-summary.json:
omp_product_frontiers`

Missing consumer:

`continue_omp_engineering_control_loop` или его минимальный existing-owner
adapter, читающий durable unconsumed incident obligation.

Exact defect:

`OMP_PRODUCT_FRONTIER_PRODUCED_TRANSIENTLY_NOT_DURABLY_CONSUMED`

## Дополнительные gaps

1. `STOP_SAFE` не запускает существующий OMP V4.7-V4.10 responsibility
   classifier в production.
2. Passive consumer намеренно не вызывает planner и поэтому не различает
   `нет target`, `нет данных`, `нет caller`, `нет кода`, `нет Authority`.
3. Shadow model записывается только через admin API вызов; incident-driven
   producer отсутствует.
4. Human shadow comparisons существуют, но автоматическая сверка с реальным
   owner-backed outcome не доказана.
5. Текущая production policy содержит старую широкую batch-authority проекцию,
   тогда как CPS разрешает только `GOVERNED_ONLY`. До любого MOVE нужен
   fail-closed reconciliation через current Authority owner.
6. Массовая shadow impact-проекция не отделена достаточно жёстко от текущего
   executable budget `1 user / 1 transaction`.

## Проверки

Прошли:

- `tests.unit.test_service_failure_episode`: 11 tests;
- `tests.unit.test_shadow_autonomy`: 9 tests;
- focused emergency failover authorization/off/stale/no-target: 4 tests.

Итого: `24 tests PASS`.

Эти тесты доказывают механизмы, но не закрывают missing production
producer-consumer link.

Fresh canonical verification:

- `tools/v7-truth-check --all --json`: `PASS`, `FULLY_ALIGNED`;
- `tools/v7-convergence-status --json`: `PASS`, local/GitHub/production commit
  `711b6a77ca034911d6d12743866390d0ae18c7b2`.

Новые plan/report files ещё не являются committed implementation и не
активируют CPS.

## Новый план

Canonical proposed plan:

`docs/programs/V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM.md`

Exact first frontier:

`V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_M1_DURABLE_INCIDENT_FRONTIER_AND_OMP_CONSUMER_V1`

## Safety result

- Runtime apply: `NONE`;
- routing mutation: `NONE`;
- user movement: `0`;
- Packet/lease: `NONE`;
- rollback apply: `NONE`;
- Authority change: `NONE`;
- Production Maturity change: `NONE`;
- production writes during audit: `NONE`.
