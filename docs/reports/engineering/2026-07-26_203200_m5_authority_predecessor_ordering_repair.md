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

## Production deploy и current legal terminal

Штатный `tools/v7-safe-deploy` выпустил только существующие owner-файлы:

```text
commit:     0cc651087327929deef6c5030670b6c858f54363
release:    deploy-z8-14-Updatesystem-0cc6510-20260726T212015
runtime:    /usr/local/bin/v7-users-autoswitch
            /usr/local/bin/admin_core/operator_execution.py
restart:    not required
```

Fresh non-test production reconciliation вернул:

```text
status                    = ACTION_CLASS_CONTRACT_ISSUE_REVIEW_READY
authority_classification  = ENGINEERING_AUTHORITY_ACTION_CLASS_CONTRACT_REQUEST_READY
exact_legal_next_action   = INDEPENDENT_DECISION_ON_FRESH_ONE_USE_ACTION_CLASS_CONTRACT_REQUEST
issue_preflight.ready     = true
pre-contract blockers     = []
post-contract blocker     = restore_barrier_required_for_emergency_failover
```

Current independently decidable M5a request (не approval и не policy write):

```text
request_id:   accauth_r1_c0465cdcec15778e52f02064
request_hash: c0465cdcec15778e52f02064e51074f6eba91ba070deed6b8bb23df9452b9cc1
expires_at:   2026-07-26T14:25:49.831683+00:00
```

Binding: Situation incident `91a9a78afb8a8ab4673d8d30`, user `10.0.0.2`,
`vless -> wireguard-1779454504-c43409`, one user, one transaction, fresh
source/snapshot/selected-move identities, owner verification,
verifier-triggered rollback/containment, cooldown `180s` и anti-flap.

Contract не выдан, policy не записана; Packet identity остаётся empty, Candidate,
Packet, lease, restore barrier, runtime apply, routing/user movement, rollback,
Authority expansion и Production Maturity change — `NONE`. Если request истечёт
или будет declined, следующий шаг всегда новая fresh reconciliation, без reuse.

## Final truth и convergence

После production caller: `tools/v7-truth-check --all --json` вернул
`PASS / FULLY_ALIGNED`, а `tools/v7-convergence-status --json` —
`PASS / ALIGNED`. Local, GitHub и production Runtime связаны с commit
`1db9d4b44d65b7eec752531b45fc9baea9b6e749`. Независимые, ранее существовавшие
незакоммиченные engineering reports не включались в этот change set.
