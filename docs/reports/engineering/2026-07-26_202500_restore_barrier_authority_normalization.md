# Отчёт: нормализация Authority на границе restore barrier

Дата: `2026-07-26`

Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

## Цель

Снять неоднозначность между Action Class contract, Packet и
`CREATE_RESTORE_BARRIER_CLEARANCE`, не выдавая contract, не записывая barrier
и не выполняя production action.

## Свежая owner-backed сверка

Read-only production вызов существующего owner
`/usr/local/bin/v7-users-autoswitch --action-class-contract-reconciliation-only`
прошёл со статусом `PASS`.

- coherent snapshot owner выполнил refresh под shared service-matrix lock;
- source stable, L3 pre-contract shadow evidence accepted;
- текущий Action Class contract отсутствует или истёк;
- `issue_preflight.ready=false`;
- единственный pre-contract blocker:
  `restore_barrier_required_for_emergency_failover`;
- shadow scope существует только как read-only evidence:
  `10.0.0.2`, `vless -> wireguard-1779454504-c43409`, максимум один user и
  одна транзакция;
- Candidate, Packet, lease, policy write, Authority grant, runtime apply,
  routing mutation, user movement, rollback и Production Maturity change:
  `NONE`.

## Точная классификация

Это **не** готовый запрос на `ENGINEERING_AUTHORITY` для выпуска Action Class
contract и **не** готовый запрос на `OPERATIONAL_AUTHORITY` для записи barrier:
оба варианта требовали бы exact fresh Packet, а штатная read-only сверка Packet
не создаёт.

Следовательно, канонический ответ должен быть:

```text
SAFE_PREDECESSOR_REQUIRED
-> RECONCILE_PACKET_BOUND_RESTORE_BARRIER_PREDECESSOR_ORDERING
-> STOP_SAFE_NOT_ACTIONABLE_EXACT_PACKET_ABSENT
```

Это обнаруженный producer/consumer semantic gap: production reconciliation
честно сообщал raw blocker, но не публиковал машинно-однозначную Authority
classification, packet identity и безопасный approval package. Поэтому старый
`authority_decision_request` был шаблоном с `issue_preflight.ready=false`, а
не допустимой просьбой утвердить или исполнить действие.

## Исправление существующего owner

Расширен только
`tools/v7-users-autoswitch.action_class_contract_reconciliation_request`.
При packet-bound restore-barrier blocker он теперь публикует:

- `authority_classification=SAFE_PREDECESSOR_REQUIRED`;
- exact legal action `RECONCILE_PACKET_BOUND_RESTORE_BARRIER_PREDECESSOR_ORDERING`;
- `approval_package.status=STOP_SAFE_NOT_ACTIONABLE_EXACT_PACKET_ABSENT`;
- явный empty packet identity вместо устаревшего historical Packet;
- свежие Situation/Decision/source identities, scope `1/1`, expiry,
  verification, verifier-triggered rollback/containment, cooldown, anti-flap,
  forbidden effects и re-entry condition.

Package остаётся `actionable=false`: он не является approval и не меняет
existing Authority ownership.

## Проверка

```text
PYTHONPYCACHEPREFIX=/tmp/v7-pycache python3 -m unittest \
  tests.unit.test_v7_users_autoswitch_policy \
  tests.unit.test_service_failure_automation_evolution \
  tests.unit.test_operator_execution_packet

Ran 229 tests ... OK
```

Тест фиксирует exact packet absence, `SAFE_PREDECESSOR_REQUIRED`, статус
`STOP_SAFE_NOT_ACTIONABLE_EXACT_PACKET_ABSENT`, scope `max_users=1`,
`max_concurrent_transactions=1` и запрет restore-barrier write.

## Legal terminal и re-entry

Текущий terminal: `SAFE_PREDECESSOR_REQUIRED`.

Точное re-entry condition: существующий owner должен либо доказать identity
fresh non-executing Packet для отдельной packet-bound restore-barrier
reconciliation, либо устранить противоречивую packet-bound precondition. После
этого выполняется новая fresh reconciliation; только если её
`issue_preflight.ready=true`, existing Authority owner может принять
`APPROVE_ONCE_AS_SCOPED` или `DECLINE` для нового one-use contract.

Ни старые request/Packet/lease, ни этот отчёт не могут быть переиспользованы
как Authority или execution input.

## Production deploy и consumer verification

Изменение выпущено только штатным `tools/v7-safe-deploy`:

```text
commit:     d1e29c6f73a03cf3551a6a5b691e112eda7d7894
release:    deploy-z8-14-Updatesystem-d1e29c6-20260726T202653
runtime:    only /usr/local/bin/v7-users-autoswitch
restart:    not required
```

Fresh non-test production caller `/usr/local/bin/v7-users-autoswitch
--action-class-contract-reconciliation-only` получил новый package от
deployed owner:

```text
authority_classification = SAFE_PREDECESSOR_REQUIRED
exact_legal_next_action = RECONCILE_PACKET_BOUND_RESTORE_BARRIER_PREDECESSOR_ORDERING
approval_package.status = STOP_SAFE_NOT_ACTIONABLE_EXACT_PACKET_ABSENT
approval_package.actionable = false
packet_identity.present = false
```

Проверены и сохранены live identity для этой единственной read-only
reconciliation: subject `10.0.0.2`, `vless ->
wireguard-1779454504-c43409`, scope `1 user / 1 transaction`, current
incident/source/snapshot/selected-move generations, 300-second request expiry,
owner verification, verifier-triggered rollback/containment, 180-second
cooldown и anti-flap. Пакет не является executable approval: exact request и
hash действуют только как fresh owner evidence и истекают без последствий.

Production caller вновь подтвердил `false` для contract/policy/barrier write,
Candidate, Packet, lease, runtime apply, routing mutation, user movement,
rollback apply, Authority and Production Maturity effects.
