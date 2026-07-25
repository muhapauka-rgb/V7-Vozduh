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

Ожидает штатного safe deploy и реального Matrix caller. Этот раздел будет
заполнен только owner-backed результатами после deploy.

## Запрещённые effects на этапе реализации

- Runtime apply: `NONE`;
- routing mutation: `NONE`;
- user movement: `0`;
- Packet/lease/rollback apply: `NONE`;
- Authority: `NO_CHANGE`;
- Production Maturity: `NO_CHANGE`.
