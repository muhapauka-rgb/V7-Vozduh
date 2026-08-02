# Инженерный отчёт: second-by-second latency forensics одной governed transaction

Дата: `2026-08-03T00:45:00+00:00`

Mission: `ONE_GOVERNED_TRANSACTION_SECOND_BY_SECOND_LATENCY_FORENSICS_AND_REPAIR_V1`

Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

Итог: `TIME_OPTIMIZATION_LOOP_PARTIAL_PRODUCTION_CONSUMED`; доминирующая устранимая задержка исправлена и повторно измерена в production, полный governed lifecycle ожидает законную fresh source/target identity от существующего controlled-topology owner.

## Что было переиспользовано

Новые Program, Planner, Runtime, Time owner, ledger, watcher и registry не создавались. Использованы существующие владельцы: `v7-users-autoswitch`, `v7-service-matrix-test`, `v7-governed-canary-dry-run-cycle`, `v7-user-switch`, Matrix durable write, performance foundation, CPS и OMP.

Stage-25 receipt `afstage_2595c3494c52f5fa6ba96592` остаётся immutable и не перезапускался. Из него выбраны репрезентативные forward terminal gaps:

| Класс | Gap | Operation fingerprint | Terminal time |
| --- | ---: | --- | --- |
| быстрый | `88.770 s` | `4891e0a550af2e6f` | `2026-08-02T11:59:56.501848+00:00` |
| median | `127.464 s` | `3f98d465825fc60a` | `2026-08-02T11:52:23.435374+00:00` |
| медленный | `145.322 s` | `3973391eec6a3d28` | `2026-08-02T12:22:10.812678+00:00` |

Это wall-order gaps между соседними governed terminal records. Канонический coarse baseline receipt: `92.882--147.411 s`. Он доказывает внешний latency window, но не подменяется монотонными внутренними span.

## Root cause и critical path

`v7-users-autoswitch` последовательно запускал отдельный процесс `v7-service-matrix-test` для каждого из 14 обязательных сервисов. Каждый процесс выполнял сетевую пробу, отдельно захватывал Matrix lock и отдельно делал durable write. Сам существующий Matrix test уже умел параллельные probes, но этот consumer не использовал capability.

Старый critical path:

`governed verification -> 14 x (Python startup -> one network probe -> Matrix lock -> durable write) -> terminal`

Новый critical path:

`governed verification -> one Python startup -> exact 14-service parallel probe set -> one Matrix lock/write -> terminal`

Это existing-owner producer-consumer defect, а не нехватка Authority, Runtime policy или реального события.

## Реализация

Production commit: `347cacbfb6e44679e626579ab662a5af9f391a4a`.

Deploy: `deploy-z8-14-Updatesystem-347cacb-20260803T003958`.

Safe-deploy manifest заменил только:

- `/usr/local/bin/v7-users-autoswitch`;
- `/usr/local/bin/v7-user-switch`;
- `/usr/local/bin/v7-governed-canary-dry-run-cycle`;
- `/usr/local/bin/v7-service-matrix-test`.

`v7-service-matrix-test` получил exact bounded `--services` subset и публикует compact monotonic/system timeline через существующий result. `v7-users-autoswitch` вызывает один subset process и публикует nested spans существующего governed output. `v7-user-switch` измеряет реальный `ip route replace` через Linux monotonic uptime. Поведение gates, service set, fail semantics, Authority и rollback не ослаблены.

## Production before/after benchmark одного и того же verifier path

Clock source: `time.monotonic_ns`; exact service set: 14; оба запуска: `14/14 PASS`.

| Измерение | До | После | Изменение |
| --- | ---: | ---: | ---: |
| service verification | `91.965611 s` | `8.786229 s` | `-83.179382 s`, `10.47x` быстрее |

Nested after-repair timeline:

| Span owner | Elapsed |
| --- | ---: |
| Python module initialization | `0.000374 s` |
| parallel network/service probe attempts | `7.521070 s` |
| Matrix lock + durable write | `1.265159 s` |
| process user CPU | `0.040909 s` |
| process system CPU | `0.009182 s` |

Все измеренные интервалы больше секунды теперь атрибутированы: network/service waits и одна Matrix durable write. CPU составляет около 50 ms; прежняя задержка была I/O/process/lock amplification, а не низкоуровневой route mutation.

## Проверки

- syntax: PASS;
- focused affected tests: `156/156 PASS`;
- broader affected suite: `325/326 PASS`; единственный failure существовал вне изменённой цепочки и проверяет, что последний mock-call остаётся `observe`, хотя текущий product owner после него законно вызывает controlled-topology diagnostic; assertion не ослаблялся и в эту bounded Mission не включался;
- safe-deploy manifest: PASS, blockers absent;
- production non-test service-verifier caller: PASS;
- forbidden effects during benchmark: routing mutation `0`, users moved `0`, rollback apply `0`, Authority expansion `0`, Production Maturity change `0`.

## Честная remaining boundary

Fresh read-only controlled topology diagnostic вернул:

- status: `CONTROLLED_TOPOLOGY_FULL_PATH_EXTERNAL_RESOURCE_REQUIRED`;
- admission: `AUTO_ADMITTED_BY_STANDING_DELEGATED_CONTROLLED_TOPOLOGY_POLICY`;
- manifest present: `true`;
- manifest hash: `741e196abb21a5d2c018ca7087f7ec049864342d248a156a3b4772d0b9ab7106`;
- `source_target_identity_complete=false`.

Поэтому полный post-repair governed single-user transaction не был создан искусственно. Не доказаны и не фиксируются как terminal: полный nested lifecycle, каждый full-path interval >1 s, post-repair low-level mutation sample, full same-path lifecycle p50/p95 и `ONE_GOVERNED_TRANSACTION_FASTEST_SAFE_PATH_PROVEN`.

Exact blocker: `FRESH_LAWFUL_CONTROLLED_SINGLE_TRANSACTION_BENCHMARK_SOURCE_TARGET_IDENTITY_REQUIRED`.

Durable automatic re-entry:

`next existing controlled-topology generation with source_target_identity_complete=true -> existing Matrix/governed single-user transaction -> fresh Candidate/Packet/lease -> existing-policy apply/verification/rollback or no-rollback -> nested monotonic timeline -> performance foundation -> CPS/OMP residual recomputation`.

Stage 48 остаётся заблокирован Time gate. Stage 25 не повторяется, обычные пользователи не используются для benchmark, L8 не фабрикуется.

## Legal terminals

Доказаны:

- `REPRESENTATIVE_SLOW_GOVERNED_TRANSACTIONS_SELECTED`;
- `EXISTING_SINGLE_TRANSACTION_TIMING_GAP_MAP_PROVEN`;
- `DOMINANT_SINGLE_TRANSACTION_LATENCY_CAUSES_PROVEN`;
- `DOMINANT_AVOIDABLE_SINGLE_TRANSACTION_LATENCY_REPAIRED`;
- `SERVICE_VERIFICATION_SAME_PATH_BEFORE_AFTER_REBENCHMARK_CONSUMED`;
- `TIME_OPTIMIZATION_LOOP_PARTIAL_PRODUCTION_CONSUMED`.

Не заявляются до fresh lawful full-path transaction:

- `ONE_GOVERNED_TRANSACTION_NESTED_MONOTONIC_TIMELINE_PROVEN`;
- `EVERY_GT_1_SECOND_INTERVAL_OWNER_ATTRIBUTED` для всего lifecycle;
- `SAME_PATH_BEFORE_AFTER_REBENCHMARK_CONSUMED` для всего lifecycle;
- `ONE_GOVERNED_TRANSACTION_FASTEST_SAFE_PATH_PROVEN`;
- `STAGE_48_OPTIMIZED_RUNTIME_READY`.
