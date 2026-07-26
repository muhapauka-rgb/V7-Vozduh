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

Дальнейшая production-проверка установила источник race: существующий
`v7-telegram-sentinel` обновляет `service-matrix.json` каждые 4 секунды. Он
уже использует общий `service-matrix.lock`, но отдельный refresh и последующий
unlocked reconciliation могли разойтись между двумя запусками sentinel.
Поэтому reconciliation переведён на уже существующий `observe` lifecycle:
он удерживает этот lock, вызывает существующий snapshot owner и строит
request template до освобождения lock. Это write только intelligence snapshots;
policy, Authority, Packet, routing и users по-прежнему не меняются.

## Проверка до deploy

Запущены 308 unit tests, включая новый сценарий source-binding stop:

`python3 -m unittest tests.unit.test_service_failure_automation_evolution tests.unit.test_v7_users_autoswitch_policy tests.unit.test_v7_truth_check tests.unit.test_autonomy_trust_acceleration`

Результат: `OK`.

## Границы

Изменение является read-only reconciliation semantics. Оно не выполняет
routing mutation, user move, packet execution, lease, rollback, runtime apply,
Authority grant или Production Maturity change.

## Production caller verification

Коммит `03a1def27e2c2decb7793a9a4e16c9445ea12e00` доставлен штатным
`v7-safe-deploy` как единственный runtime-файл `tools/v7-users-autoswitch`
(`deploy-z8-14-Updatesystem-03a1def-20260726T101205`).

Production entrypoint вернул:

- `POLICY_READ_ONLY_HANDOFF_WITH_EXISTING_SNAPSHOT_REFRESH`;
- `coherent_snapshot_preflight.performed=true`;
- `source_stable=true`;
- `shared_service_matrix_lock_held=true`;
- `snapshot_stop_required=false`;
- `ACTION_CLASS_CONTRACT_ISSUE_REVIEW_READY`.

Проверены запрещённые эффекты: `policy_write=false`,
`authority_granted=false`, `runtime_apply=false`, `routing_mutation=false`,
`user_movement=0`, `candidate_created=false`, `packet_created=false`,
`lease_created=false`, `rollback_apply=false`, `production_maturity_change=false`.

## Точный legal terminal и следующий закрытый цикл

Engineering residual закрыт. Единственный следующий consumer — независимый
existing owner `/etc/v7/policy.json`; он может либо отклонить request (возврат
в fresh `STOP_SAFE`), либо выдать короткий one-use contract для ровно одного
пользователя `vless -> wireguard-1779454504-c43409` с freshness,
verification, rollback, cooldown, anti-flap и expiry. После этого existing
autoswitch boundary обязан заново прочитать и проверить contract до любого
Candidate/Packet/lease/apply.

Это `ENGINEERING_AUTHORITY` terminal, а не поломка snapshot, не разрешение на
runtime apply и не причина повышать Authority или Production Maturity.

## Итоговая валидация

- Focused и полный набор: `309` unit tests, `OK`.
- `tools/v7-truth-check --all --json`: `PASS`, `FULLY_ALIGNED`.
- `tools/v7-convergence-status --json`: `PASS`, `ALIGNED`.
- Local, GitHub и production runtime snapshot: commit
  `8c4e193db121f4667b4f3e36d022119fe0e722d9`.

Ни старый `APPROVE_ONCE_AS_SCOPED`, ни общее согласие не являются заменой
актуального exact policy-owner contract.
