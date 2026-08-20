# V5.3 T0–T11: Polygon lane без ожидания естественного failure

Дата: 2026-08-21 01:52 MSK  
Track: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`  
Решение: инженерную проверку продолжать через существующий synthetic/Polygon
контур, не ожидая бесконечно естественного отказа.

## DECISION

Естественный production failure больше не является обязательным условием для
инженерного измерения T0–T11.

Разделение теперь такое:

```text
Polygon/synthetic lane
  → измеряет causal chain, gates, timing и cleanup
  → users_moved=0, route mutation=0

Production ordinary lane
  → требует свежий реальный scope и все существующие safety gates
  → не получает synthetic credit автоматически
```

Это не новая архитектура, owner или источник истины. Используется уже
существующий `v7-governed-canary-dry-run-cycle`, controlled-topology owner,
Matrix owner и существующие Planner/OMP/CPS gates.

## WHY THIS IS SAFE

- Synthetic T0 не выдаётся за natural production incident.
- Ordinary users не используются.
- Маршруты и production Runtime не изменяются.
- Candidate/Packet/Lease могут быть проверены только во временной Polygon
  fixture-цепочке; production state не потребляется.
- Existing cleanup/reset и no-trust/no-learning rules сохраняются.
- Phase G decision `NO_CROSS_EGRESS_PARALLELISM_ADMITTED` сохраняется; Polygon
  не переоткрывает cross-egress parallelism.

## EXECUTED POLYGON EVIDENCE

### Governed canary / controlled topology

Команда: `python3 -m unittest -v tests.unit.test_governed_canary_cli`.

- `127/127 PASS`;
- время: `0.689 s`;
- проверены controlled identity, source isolation, target readiness,
  reservation, Candidate/Packet/Lease binding, bounded execution timing,
  verification, cleanup/reset и запрет trust/learning fabrication.

### Matrix comparison и T0–T11 lifecycle binding

Команда: `python3 -m unittest -v
tests.unit.test_v5_3_matrix_controlled_comparison
tests.unit.test_v5_3_matrix_decision_lifecycle_binding`.

- `14/14 PASS`;
- время: `29.545 s`;
- full/subset service failure equivalence: PASS;
- Matrix writer и decision lifecycle binding: PASS;
- T0–T11 mission admission и FAST hold: PASS;
- Polygon probe timing для уже проверенных caps: 0.833 s (cap 1), 0.610 s
  (cap 2), 0.727 s (cap 4). Эти числа остаются Polygon evidence и не меняют
  production decision о parallelism.

### Service-failure episode coverage

Из 92 тестов service-failure episode 90 прошли. Два существующих теста требуют
старой CPS projection и возвращают `CURRENT_STATE_CONSISTENCY_FAIL` либо
`STOP_SAFE_FRESH_EVENT_REVALIDATION_REQUIRED`; они не являются основанием для
ослабления gates и не исправлялись в этом блоке.

## WHAT THIS CHANGES

Изменено только инженерное правило продолжения:

`NATURAL_FAILURE_REQUIRED_FOR_ENGINEERING_PROGRESS = FALSE`

Остаётся неизменным:

`NATURAL_FAILURE_REQUIRED_FOR_PRODUCTION_USER_MOVEMENT = TRUE`

То есть больше не ждём реального инцидента, чтобы измерить цепочку, но synthetic
прогон не получает права двигать обычного клиента или менять production route.

## CURRENT T0–T11 FRONTIER

```text
Polygon synthetic T0
  → fresh Matrix evidence
  → source/target gates
  → governed dry-run timing
  → cleanup/verification
  → compare with existing full Matrix baseline
```

Локальные unit/Polygon проверки уже закрывают большую часть этой цепочки. Новой
production execution authority не создавалось.

## NEXT STEP

Следующий bounded шаг — запустить один существующий controlled synthetic-client
dry-run в изолированной Polygon fixture-среде, собрать T0–T11 timing breakdown и
сравнить его с full Matrix baseline. После этого отдельно решить, есть ли
доказанный gap для изменения Matrix selection/cadence; FAST и cross-egress
parallelism остаются закрытыми до отдельного доказательства.

## EFFECTS

- Production users moved: `0`.
- Production route mutations: `0`.
- Timer/cadence/timeout: unchanged.
- Runtime deploy: none.
- New owner/registry/queue/watcher: none.
- Local truth: PASS.

