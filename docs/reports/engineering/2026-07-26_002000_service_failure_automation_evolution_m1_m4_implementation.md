# Service Failure Automation Evolution — реализация M1–M4

Дата: `2026-07-26`

## Цель

Замкнуть существующую цепочку Service Failure без создания нового engine,
очереди, Planner, Runtime или Authority owner:

```text
passive Situation/STOP_SAFE
-> durable closure obligation
-> existing OMP consumer
-> exact STOP_SAFE classification
-> bounded Shadow decision
-> exact future outcome comparison
-> existing BDP/OMP route or legal Authority boundary
```

## Реализация

- `tools/v7-users-autoswitch` материализует один idempotent obligation в
  существующем `closure-records.jsonl`; он сохраняет Situation, Decision Trace,
  provenance, aggregate impact, bounded scope, capacity snapshot и ladder gap.
- Каждый `STOP_SAFE` классифицируется до выбора successor: correct terminal,
  data/evidence, no safe target, Authority или external owner.
- `tools/v7-service-matrix-refresh-all` вызывает advisory-only owner, затем
  стандартный `v7-truth-check --continue-omp --continue-omp-persist-cps`.
- `tools/v7_sync_lib.py` потребляет obligation ровно один раз в том же
  append-only closure owner и атомарно фиксирует exact CPS boundary.
- `admin_core/shadow_autonomy.py` получает owner-backed observed-outcome
  comparison; отсутствие apply никогда не считается outcome.
- `tools/v7-truth-check` на production разрешает canonical corpus `/opt/v7`,
  а не каталог установленных бинарников `/usr/local`.

## Локальная проверка

Пройдены 54 focused tests: Service Failure episode, новая automation evolution,
Shadow Autonomy и OMP program reconciliation. Отдельная temporary-CPS проверка
доказала, что `STOP_SAFE_AUTHORITY_REQUIRED` проходит atomic CPS validation как
точная `ENGINEERING_AUTHORITY` граница.

## Production verification

Штатные deploy выполнены только через `tools/v7-safe-deploy`:

- `deploy-z8-14-Updatesystem-1b92100-20260726T002036` — первоначальная
  реализация пяти ожидаемых runtime-файлов;
- `deploy-z8-14-Updatesystem-0eeb2b7-20260726T002631` — repair binary-only
  production consumer;
- `deploy-z8-14-Updatesystem-0c51ff2-20260726T002738` — idempotent retry
  pending obligation через тот же Matrix caller.

Реальный production `tools/v7-service-matrix-refresh-all` сформировал и
потребил два immutable receipts через существующий `closure-records.jsonl`:

- `sfomp_d1a8697a6f185fcbed1687ff`: expiry/recovery `CORRECT_SAFE_TERMINAL`;
- `sfomp_cd3c9abaa10c4178c34827e0`: persistent VLESS
  `STOP_SAFE_AUTHORITY_REQUIRED`, Situation
  `situation_47f4c50b6a1c33f12d8fd137`, Decision Trace
  `decision_c410493f06b1a6f34432d7e2`.

Последний receipt атомарно reconciled в canonical source CPS. Это доказывает
production caller -> durable obligation -> consumer behavior change -> exact
next output. CPS и OMP согласованно фиксируют
`V7_SERVICE_FAILURE_AUTOMATION_AUTHORITY_RECONCILIATION`.

Ни один receipt не содержит Runtime apply, routing mutation, movement,
Packet/lease, rollback apply, Authority expansion или Production Maturity
change. Shadow outcome comparison подключён, но для этого инцидента реального
move outcome нет и он честно не fabricated.

## Выполнение программы

- `M0`: `COMPLETE` — existing-owner audit.
- `M1`: `COMPLETE_CONSUMED` — durable obligation и real OMP consumption.
- `M2`: `COMPLETE_CONSUMED` для incident-bound read-only matrix: safe target
  найден, но current action contract отсутствует.
- `M3`: `COMPLETE_CONSUMED` для automatic bounded shadow binding; outcome
  comparison remains waiting for an exact owner-backed executed outcome.
- `M4`: `COMPLETE_CONSUMED` для routing classification к exact Authority
  boundary; нет repair gap, который можно безопасно продолжить без Authority.
- `M5–M7`: не запускаются церемониально. `M5` законно остановлена на
  `ENGINEERING_AUTHORITY`; `M6/M7` требуют реального bounded action outcome
  либо независимого Authority decision.

## Final legal terminal

`BOUNDED_SERVICE_FAILURE_ACTION_EXACT_AUTHORITY_BOUNDARY_PROVEN`.

Это не означает разрешение на failover. Следующее действие — только exact
owner-issued one-use action-class contract или новое independent
owner-backed Service Failure/Product Evolution obligation.

## Запрещённые effects на этапе реализации

- Runtime apply: `NONE`;
- routing mutation: `NONE`;
- user movement: `0`;
- Packet/lease/rollback apply: `NONE`;
- Authority: `NO_CHANGE`;
- Production Maturity: `NO_CHANGE`.
