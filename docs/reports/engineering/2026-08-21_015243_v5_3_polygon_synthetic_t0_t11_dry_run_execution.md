# V5.3 T0–T11: выполненный Polygon synthetic dry-run

Дата: 2026-08-21 01:52 MSK  
Track: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`  
Lane: existing Polygon / governed synthetic fixture  

## RESULT

Изолированный synthetic-прогон выполнен через существующий
`tools/v7-governed-canary-dry-run-cycle` и его текущих owners. Ordinary users,
production Runtime и маршруты не использовались.

Targeted lifecycle suite: **4/4 PASS**, `0.069 s`.

Проверенные сценарии:

1. один governed transaction проходит до terminal lease и cleanup;
2. bounded delegated transaction работает без packet identity/operator prompt,
   сохраняя существующие guards;
3. switch lineage не выдаёт clearance без route commit;
4. service verification failure классифицируется как verification failure.

Основной one-user fixture подтвердил полный контролируемый порядок:

```text
synthetic failure input
  → fresh packet preview
  → Candidate/Packet binding
  → serial lease
  → restore barrier
  → apply stub (только в temp fixture)
  → route/service verification
  → Outcome/Learning/Closure
  → final Safe Mode OPEN
```

В fixture-результате существующий тест подтвердил `users_moved=1` внутри
изолированной временной модели и terminal `GOVERNED_TRANSACTION_COMPLETED`.
Это не означает перемещение production-клиента.

## BROADER POLYGON EVIDENCE

- governed canary/controlled topology suite: `127/127 PASS`, `0.689 s`;
- Matrix comparison + lifecycle binding suite: `14/14 PASS`, `29.545 s`;
- Matrix probe cap timing в Polygon: `0.833 s / 0.610 s / 0.727 s` для уже
  проверенных caps 1/2/4;
- Phase G rule сохраняется: `NO_CROSS_EGRESS_PARALLELISM_ADMITTED`.

## WHAT THIS PROVES

- Можно не ждать естественного production failure, чтобы проверять причинную
  последовательность T0–T11.
- Existing owners способны провести один synthetic governed transaction с
  serial safety gates, verification и cleanup.
- Ошибка service verification не маскируется под успешное восстановление.
- Отсутствие clearance без подтверждённого route commit сохраняется.

## WHAT THIS DOES NOT PROVE

- фактическую production latency T0–T11;
- реальное движение ordinary client;
- естественную корреляцию Matrix failure с живым пользовательским scope;
- production route visibility.

Для этих утверждений нужна отдельная live evidence; synthetic credit туда не
переносится.

## PRODUCTION SAFETY

- production users moved: `0`;
- production route mutation: `0`;
- production Matrix/Runtime/timer: unchanged;
- FAST: unchanged/held;
- new owner/queue/watcher/registry: none;
- deploy/push: none;

## NEXT STEP IN THE PLAN

Теперь можно продолжать инженерную часть T0–T11 без ожидания естественного
failure:

1. собрать timing breakdown существующего synthetic lifecycle по T0–T11;
2. сопоставить его с live Matrix cycle (`~65 s`) и full baseline;
3. определить, какой этап действительно является bottleneck;
4. только затем предложить минимальное изменение системы.

Production ordinary failover остаётся отдельной веткой и не запускается этим
Polygon прогоном.

