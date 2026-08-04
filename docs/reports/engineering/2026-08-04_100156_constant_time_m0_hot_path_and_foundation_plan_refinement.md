# Engineering Report: уточнение CT-M0 и условной Foundation Mission

Дата UTC: `2026-08-04T10:01:56Z`

## Результат

Существующий план `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM` обновлён
до V4.1, а его интеграция в OMP — до V4.64. Новая программа, новый owner,
registry, queue, watcher, Planner, Runtime, truth source или Authority system
не создавались. CPS и текущий Runtime frontier этим изменением не активированы.

## Что уточнено

- CT-M0 обязан доказать полный hot-path producer-consumer graph от failure
  signal до durable deferred closure, включая скрытые serialization, hashing,
  audit и membership costs.
- Prepared decision получил точный generation/fingerprint invalidation
  contract; hot validator не перестраивает World Model.
- Routing class identity определяется только результатом аудита, а не общим
  source channel.
- Deferred closure начинается с durable closure seed до CAS и однозначно
  восстанавливается после crash по canonical/kernel truth.
- Per-user legacy path ограничен явными исключениями; массовый совместимый
  incident обязан выбирать class path.
- Каждому существующему primitive назначается один semantic disposition:
  reuse, extend, owner-internal replace, legacy-only, deferred/outside fast path
  или exact constant-time blocker.
- Добавлена только условная CT-M0F Mission. Она существует лишь при доказанном
  `EXTEND`/`REPLACE` residual; иначе сразу READY становится CT-M1.
- CT-M0F и CT-M1 не могут быть READY одновременно.

## Замкнутая последовательность

```text
CT-M0 reality/cost/dependency audit
-> CT-M0F only for proven existing-owner gaps
-> legacy exception selection certification
-> CT-M1 Polygon kernel/class prototype
-> generation commit and crash recovery
-> 10 vs 10,000 N-independence
-> bounded migration
-> controlled production
-> independent Authority/Runtime recommendation
```

Каждый этап сохраняет producer, output, consumer, behavior, verification,
next output, CPS projection, residual и один durable successor/legal terminal.

## Текущий legal terminal

`APPROVED_CAPABILITY_PLAN_NOT_LIVE_FRONTIER`

Текущий CPS остаётся единственным владельцем активации. Следующий допустимый
этап после отдельного CPS admission — read-only CT-M0, а не реализация заранее
выбранного primitive.
