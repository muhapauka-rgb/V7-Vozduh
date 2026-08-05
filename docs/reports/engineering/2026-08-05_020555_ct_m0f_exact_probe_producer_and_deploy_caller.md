# Engineering Report: CT-M0F exact client probe producer и production caller

Дата: `2026-08-05T02:05:55Z`

Mission: `V7_CONSTANT_TIME_COHORT_FAILOVER_REUSABLE_FAST_PRIMITIVES_CLOSURE_V1`

## Итог

CT-M0F-E доведена до честного production terminal: существующий owner
`tools/v7-client-speed-api` расширен native exact-context probe режимом,
связан с уже существующим Time consumer
`admin_core.operator_execution_pipeline`, задеплоен штатным
`tools/v7-safe-deploy` и вызван production deploy owner в fail-closed режиме.

Это не является измеренным recovery sample и не закрывает CT-M0F-V. Текущий
остаток — один точный owner-backed context/access для выделенной certification
identity и затем отдельные допустимые cold/warm generations.

## Discover -> Reuse -> Extend -> Implement

- Найден и переиспользован существующий client telemetry owner; новый сервис,
  store, queue, watcher, Planner, Runtime или Authority owner не создавался.
- Старый браузерный speed-test признан семантически недостаточным: он не
  доказывает fresh socket и exact namespace/source/fwmark/table context.
- Существующий binary получил CLI режим
  `--exact-client-probe-context`, который до сетевого вызова проверяет schema,
  hash, expiry, incident/generation, certification identity, clock domain,
  namespace inode, source, interface, fwmark, table, target fingerprint,
  timeout/retry/cadence и cold/warm generation.
- Probe создаёт новый TLS socket, выполняет fresh DNS, source/interface/SO_MARK
  binding, сверяет `ip route get`, запрещает private destination, проверяет
  application payload и ожидаемый public egress IP.
- Receipt сразу потребляется существующими
  `exact_client_network_context_traffic_probe_contract` и
  `client_recovery_clock_contract`. Management/default route, browser-only,
  Matrix, route lookup без payload и kernel counters не получают PASS.
- `receipt_id` детерминирован по contract/validation generation, поэтому один
  generation не может создать разные идентичности повторной выборки.

## Проверка

- Focused unit/service-failure/sync tests: `PASS`.
- Subprocess fail-closed test: missing/expired context -> `rc=2`,
  `PROBE_INVALID`, zero effects.
- Deploy allowlist: `PASS`.
- Deployment manifest changed runtime owners only:
  `tools/v7-client-speed-api`, `tools/v7_sync_lib.py`.
- Первый post-deploy attempt обнаружил реальный producer-consumer дефект:
  Python `main()` не передавал fail-closed return code. Deploy owner остановил
  установку с `NO-GO`; дефект исправлен и покрыт subprocess тестом.
- Финальный deploy: `PASS`.
- Deploy ID: `deploy-z8-14-Updatesystem-20ca164-20260805T090442`.
- Deployed commit: `20ca164a1d5e0c8d0df0cb221549bde899516126`.
- Production non-test caller: встроенный deploy-owner check потребил новый
  entrypoint и принял только `rc=2 + PROBE_INVALID + zero effects`.
- Truth: `PASS`, `FULLY_ALIGNED`.
- Convergence: `PASS`, `ALIGNED`; local/GitHub/production commit совпадает.

## Effects

- routing mutation: `NONE`;
- user movement: `0`;
- Packet/lease/apply/rollback: `NONE`;
- policy/Authority/Production Maturity: `NO CHANGE`;
- service restart: `NONE`;
- Natural L8 credit: `NONE`.

## Legal terminal и следующий consumer

Текущий terminal:

`CT_M0F_E_EXACT_CLIENT_PROBE_PRODUCER_DEPLOYED_AND_FAIL_CLOSED_PRODUCTION_CALLER_CONSUMED`

CT-M0F-V остаётся `FORMED_DEPENDENCY_BLOCKED`, поскольку fail-closed caller
доказывает entrypoint и запреты, но не route-bound client recovery.

Точный следующий action:

```text
existing Controlled Production owner
-> one hashed short-lived CT-M0F-V context
-> dedicated certification identity in exact namespace/source/interface/fwmark/table
-> one independently admitted cold validation generation
-> fresh Candidate/Packet/lease only under existing gates
-> deployed exact probe producer
-> Time consumer
-> performance ledger and residual recomputation
```

Обычный пользователь, host/Matrix/counter evidence и повтор уже доказанного
generation запрещены. После первого consumed cold sample OMP автоматически
пересчитывает состав оставшихся четырёх samples и следующий safe successor.
