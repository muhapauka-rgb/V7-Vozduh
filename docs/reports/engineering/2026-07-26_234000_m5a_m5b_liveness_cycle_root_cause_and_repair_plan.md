# M5a/M5b liveness cycle: root cause and repair plan

Дата: 2026-07-26
Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

## Диагноз

Текущий цикл не является корректным Authority terminal. Это existing-owner
liveness/predecessor defect:

1. `CURRENT_ACTION_CLASS_CONTRACT_REQUEST_TTL_SECONDS = 300` оставляет человеку
   только пять минут на exact решение.
2. `tools/v7-users-autoswitch` также запрашивает `max_ttl_seconds = 300` для
   уже выданного contract, хотя существующий Authority owner допускает максимум
   900 секунд.
3. После contract issuance нет одного owner-managed вызова, который немедленно
   выполняет M5b read-only revalidation. Ручная доставка между issuance и M5b
   стала частью critical path.
4. M5a Action Class decision избыточно связан с быстро меняющейся planner/source
   generation, хотя точная operational generation должна окончательно
   фиксироваться M5c Packet/Operational Authority boundary.

Следствие: request или contract истекает, система формирует новый request,
человек снова подтверждает, а capability не приближается к M5b/M5c.

## Безопасное исправление

Выполнить bounded Mission
`V7_SERVICE_FAILURE_M5A_M5B_ATOMIC_HANDOFF_LIVENESS_REPAIR_V1` через
существующие `tools/v7-users-autoswitch`, `admin_core/operator_execution.py`,
policy/audit owner и CPS/OMP consumers.

1. Разделить два класса freshness:
   - M5a approval/Action Class scope: program, incident generation, user,
     source, target, action class, ceiling, `max_users=1`, concurrency=1,
     verification, rollback, cooldown, anti-flap;
   - M5c operational freshness: exact current planner/source/snapshot/
     selected-move generation и Packet identity.
2. Использовать существующий 900-second ceiling для M5a request и issued
   contract; не увеличивать scope, blast radius, Authority или число uses.
3. Добавить в существующий owner единый exact-decision consumer:
   `approve -> locked issue -> immediate observe-only M5b revalidation`.
   Между этими шагами не должно быть operator/Codex handoff.
4. M5b может принять контракт только если неизменны incident, subject,
   source/target, action class, policy generation and scope. Изменение любого
   semantic field даёт `STOP_SAFE` и новый independent request. Обновление
   observation generation само по себе не должно превращать M5a в новый
   Authority decision; текущую generation фиксирует следующий Packet owner.
5. Единый consumer возвращает только
   `NO_ACTION_NO_SHADOW_CANDIDATE`, `STOP_SAFE_OTHER_EXECUTION_GATE_REQUIRED`
   или `PACKET_MATERIALIZATION_ELIGIBLE`. Он не создаёт Candidate, Packet,
   lease, restore barrier и не выполняет apply.
6. M5c остаётся отдельной границей: fresh Candidate/Packet/lease и отдельная
   packet-bound `OPERATIONAL_AUTHORITY`.

## Обязательные тесты

- решение, принятое после 5 минут, но внутри 15 минут, проходит только при
  неизменном semantic scope;
- issuance автоматически запускает M5b в том же owner invocation;
- changed incident/user/source/target/policy/scope -> `STOP_SAFE`;
- concurrent duplicate approval -> ровно один decision/contract;
- M5b после expiry -> `STOP_SAFE`, без повторного использования approval;
- zero Candidate/Packet/lease/restore barrier/apply/routing/user/rollback
  effects;
- focused/full affected tests, safe deploy, production non-test consumer,
  affected replay, truth, convergence and CPS residual recomputation.

## Текущий terminal

Не продолжать цикл подтверждений на текущей реализации. Истёкшие requests и
contracts не переиспользовать. Exact next engineering frontier:
`V7_SERVICE_FAILURE_M5A_M5B_ATOMIC_HANDOFF_LIVENESS_REPAIR_V1`.
