# Отчёт: устранение M5a/M5c circular predecessor dependency

Дата: `2026-07-26`

Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

## Обнаруженный дефект

Fresh production reconciliation после `fd79e356` доказал одновременно:

```text
no valid Action Class contract
-> no selected execution move / no Packet
-> restore_barrier_required_for_emergency_failover
-> contract issue preflight blocked by restore barrier
-> no valid contract
```

Это был existing-owner producer/consumer ordering defect. Он не являлся
`ENGINEERING_AUTHORITY`, `OPERATIONAL_AUTHORITY`, `REAL_WORLD_LIMIT` или
Program terminal: M5a должен завершаться до M5c Packet/barrier boundary.

## Исправленная canonical ordering

```text
M5a  fresh read-only Action Class request
  -> independent exact one-use contract decision
M5b  fresh planner revalidation under valid contract
  -> PACKET_MATERIALIZATION_ELIGIBLE or exact STOP_SAFE
M5c  fresh Candidate -> Packet -> lease
  -> packet-bound Operational Authority package
  -> independent decision on restore barrier / bounded execution
```

`restore_barrier_required_for_emergency_failover` теперь сохраняется как
`post_contract_operational_blocker`, но не входит в M5a issue preflight.

## Machine-readable boundaries

1. Нет valid contract и Packet, но Situation/Decision/L3/preflight свежие:
   `ENGINEERING_AUTHORITY_ACTION_CLASS_CONTRACT_REQUEST_READY`.
   Создаётся только fresh actionable request template; policy, Candidate,
   Packet, lease, barrier, apply и movement запрещены.

2. Есть valid one-use contract, но Packet отсутствует:
   `SAFE_PACKET_MATERIALIZATION_PREDECESSOR_REQUIRED`.
   Existing planner re-enters M5b; contract не создаёт и не расходуется при
   Candidate/Packet/lease preparation. Расходование остаётся атомарным
   непосредственно перед единственной forward Runtime mutation.

3. Exact fresh Packet прошёл canonical recheck:
   `OPERATIONAL_AUTHORITY_RESTORE_BARRIER_READY`.
   `admin_core/operator_execution.py` публикует только read-only package для
   отдельного operational decision. Package сам не пишет barrier и не даёт
   apply permission.

Во всех состояниях сохраняются exact subject/scope, max users `1`, max
concurrent transactions `1`, Situation/Decision/source/snapshot identities,
expiry, verification, verifier-triggered rollback/containment, cooldown,
anti-flap и one-use law.

## Проверка

```text
PYTHONPYCACHEPREFIX=/tmp/v7-pycache python3 -m unittest \
  tests.unit.test_v7_users_autoswitch_policy \
  tests.unit.test_service_failure_automation_evolution \
  tests.unit.test_operator_execution_packet

Ran 230 tests ... OK
```

Регрессии подтверждают: no contract/no Packet produces M5a request; barrier
не блокирует M5a; valid contract re-enters packet materialization without
consumption; exact rechecked Packet produces only read-only operational
package; Packet/lease preparation, policy, barrier write, apply, routing,
movement, rollback, Authority expansion и Production Maturity change не
происходят во время repair.

## Следующий безопасный результат

После deploy existing production reconciliation должен сформировать новый
fresh M5a `ENGINEERING_AUTHORITY_ACTION_CLASS_CONTRACT_REQUEST_READY` package.
Этот отчёт не выдаёт и не утверждает contract; он не создаёт Candidate, Packet,
lease или restore barrier. Legal terminal после verification — только fresh
independent M5a Authority request с current id/hash/expiry.
