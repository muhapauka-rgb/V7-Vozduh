Mission ID: `CONTROLLED_TOPOLOGY_SHARED_TARGET_CAPACITY_AND_ROLE_RECONCILIATION_V1`
Run Nonce: `V7_STCR_20260730T111500+0700`

# Shared production target capacity and safe re-entry

Дата: 2026-07-30

## Результат

Выполнена production-проверка существующих owners для residual
`SHARED_PRODUCTION_TARGETS_NON_DESTRUCTIVE_FAILOVER_AND_MULTI_TARGET_CAPACITY_V1`.
Новый owner не создан. Изменены только существующие `tools/v7-users-autoswitch`
и CPS/OMP projection owner `tools/v7_sync_lib.py`.

## Что доказано

- Shared destination отделён от controlled source: source допускает deliberate
  condition только при собственной изоляции; destination никогда не получает
  fault injection.
- Техническая shared-target projection не создаёт Candidate, Packet, lease,
  restore barrier и не изменяет policy, routing или users.
- Production inventory в момент проверки: `awg3` имеет capacity reserve, но не
  проходит текущий stability floor; `awg0` также не проходит stability floor.
- Единственная текущая allocation, которая удовлетворяла старому source `1`,
  была `vless`. После actual source rebind на `vless` это source=target
  collision, поэтому allocation удалена из всех stage 5/10/25/48 projections.

## Исправленные producer-consumer links

1. Target diagnostic теперь публикует read-only
   `shared_production_target_capacity_projection`, не смешивая destination
   capacity с exclusive source requirement.
2. Topology diagnostic запрещает target, совпадающий с actual controlled
   source, включая каждую stage projection.
3. CPS/OMP consumer классифицирует такой случай как
   `SAFE_REENTRY_REQUIRED`, а не как ложный `EXTERNAL_OWNER_REQUIRED`.

## Production verification

- Deploy commits: `ba448222`, `3a8b2135`, `d1ed3b37`, `3c4ce8ae`,
  `19225830`, `e84ee0b1`, `dc0d9bdd` through `tools/v7-safe-deploy`.
- Final local/GitHub/production identity:
  `dc0d9bddb704f9bdf18d0fc540549e87dbe83877`.
- Production caller: `/usr/local/bin/v7-users-autoswitch --controlled-source-topology-diagnostic`.
- Production consumer output:
  `CONTROLLED_TOPOLOGY_SHARED_TARGET_REVALIDATION_REQUIRED` and
  `SAFE_REENTRY_REQUIRED:ACTUAL_SOURCE_DISTINCT_SHARED_TARGET_REVALIDATION`.
- Final `tools/v7-truth-check --all --json`: `PASS`, `FULLY_ALIGNED`.
- Final `tools/v7-convergence-status --json`: `ALIGNED`.

## Финальная canonical reconciliation

Проверен и deployed существующий CPS/OMP projection owner. Он признаёт
`WAITING_OWNER_EVENT:*` как отдельный безопасный terminal, поэтому не требует
искусственно подменять WIP capability-local wait глобальным
`REAL_WORLD_LIMIT`. Existing atomic CPS -> OMP reconciler теперь обновляет и
`Current terminal report`, и `Latest consumed report`; тест фиксирует это
поведение. Изменение не создаёт Runtime, Planner, Authority или policy owner.

## Legal terminal

`WAITING_OWNER_EVENT:CONTINUE_CONTROLLED_TOPOLOGY_ACTUAL_SOURCE_DISTINCT_TARGET_REVALIDATION`.

Existing Matrix/quality observation is the only re-entry source. The next
owner-backed output must be either a fresh distinct healthy target set or an
exact stability/capacity blocker. No Authority request, policy write,
Candidate, Packet, lease, restore-barrier write, apply, routing mutation,
user movement, rollback apply or Production Maturity change occurred.
