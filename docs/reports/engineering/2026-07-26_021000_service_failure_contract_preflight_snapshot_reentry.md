# Engineering Report — contract preflight snapshot re-entry

## Цель

Замкнуть безопасный переход после `STOP_SAFE_CURRENT_ACTION_CLASS_CONTRACT_REQUIRED`:
контракт action class не должен направляться владельцу policy до проверки, что
текущие intelligence snapshots свежи и привязаны к тем же источникам, что и
решение planner.

## Найденный дефект

Read-only production planner обнаружил одновременно два независимых остатка:

- `current_action_class_contract` отсутствует; и
- `intelligence_snapshots.stop_required=true` из-за
  `source_hash_mismatch:service_matrix` для `service-scores` и
  `channel-service-scores`.

Прежняя read-only проекция показывала готовность request template для policy
owner только по отсутствию contract. Это не давало опасного эффекта, но могло
передать преждевременную задачу следующему consumer.

## Исправление

Существующий `tools/v7-users-autoswitch` теперь публикует
`ACTION_CLASS_CONTRACT_REQUEST_TEMPLATE_WAITING_FRESH_PRECONDITIONS`, когда
snapshot gate остановлен. Его единственный следующий consumer в таком случае:

`existing v7-intelligence-snapshot-refresh/source owner -> planner -> action-class contract reconciliation`.

Только после свежего re-entry допускается
`ACTION_CLASS_CONTRACT_ISSUE_REVIEW_READY` для существующего owner
`/etc/v7/policy.json`. Новых owner, Authority, queue, runtime или registry не
создано.

## Проверка до deploy

Запущены 308 unit tests, включая новый сценарий source-binding stop:

`python3 -m unittest tests.unit.test_service_failure_automation_evolution tests.unit.test_v7_users_autoswitch_policy tests.unit.test_v7_truth_check tests.unit.test_autonomy_trust_acceleration`

Результат: `OK`.

## Границы

Изменение является read-only reconciliation semantics. Оно не выполняет
routing mutation, user move, packet execution, lease, rollback, runtime apply,
Authority grant или Production Maturity change.

## Следующий закрытый цикл

1. Безопасно задеплоить только `tools/v7-users-autoswitch`.
2. Вызвать production read-only reconciliation и подтвердить ожидание snapshot
   owner.
3. Вызвать существующий `v7-intelligence-snapshot-refresh`, который обновляет
   только snapshots.
4. Повторно вызвать reconciliation.
5. Если freshness закрыта, оставить выдачу точного one-use contract отдельному
   policy owner; если нет — потребить точный producer defect через BDP/OMP.

Ни старый `APPROVE_ONCE_AS_SCOPED`, ни общее согласие не являются заменой
актуального exact policy-owner contract.
