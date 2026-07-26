# Отчёт: устранение deadlock между L3 wake и Action Class contract

Дата: 2026-07-26
Статус: PRODUCTION_DEPLOYED_AND_CONSUMER_VERIFIED

## Причина

В существующем `tools/v7-users-autoswitch` одноразовый Action Class contract
проверялся до L3 evidence gate. При отсутствующем или истёкшем contract
`_authority_budget_gate` корректно удалял выбранное перемещение. Затем
`_emergency_failover_authority_gate` строил L3 wake только из оставшегося
`selected`; в результате не возникало ни evidence, ни допустимого fresh request.
После fail-closed запрета на выпуск contract без L3 wake образовывался цикл:

`contract missing -> selected empty -> no L3 wake -> contract request denied`.

Это дефект порядка producer -> consumer, а не основание для ослабления
Authority или создания искусственного production event.

## Исправление существующего owner

`AutoswitchPlanner.plan()` сохраняет ограниченный request-cap pre-contract
shadow selection и передаёт его исключительно в L3 evidence gate.

- `tools/v7-users-autoswitch` помечает источник как
  `pre_contract_shadow_selection_read_only`, только когда contract gate уже
  обнулил execution selection;
- evidence-only rows никогда не попадают в `eligible`: для этого требуется,
  чтобы та же строка пережила Action Class contract gate;
- следовательно, L3 wake может открыть только выпуск fresh owner-issued
  contract, но не Candidate, Packet, lease, routing mutation или user movement;
- после contract issuance обычный planner обязан заново пройти freshness,
  policy, authority, target, rollback и execution gates.

## Проверка

Добавлен регрессионный тест отсутствующего Action Class contract при свежем
service failure. Он подтверждает одновременно:

1. `selected_moves == []`;
2. `ACCEPT_WAKE` с `confirmed_service_failure` сохраняется;
3. execution boundary остаётся
   `STOP_SAFE_CURRENT_ACTION_CLASS_CONTRACT_REQUIRED`;
4. Candidate, Packet и lease не созданы.

Выполнено:

```text
PYTHONPYCACHEPREFIX=/tmp/v7-pycache python3 -m unittest \
  tests.unit.test_v7_users_autoswitch_policy \
  tests.unit.test_service_failure_automation_evolution \
  tests.unit.test_operator_execution_packet

Ran 225 tests ... OK
```

После первого deploy production planner подтвердил сам L3 producer:
`ACCEPT_WAKE` для `10.0.0.2`, VLESS и bounded shadow target, при
`selected_moves == []`. Это доказало отсутствие Candidate/Packet/lease/apply,
но выявило последний consumer gap: dedicated
`--action-class-contract-reconciliation-only` намеренно не включал emergency
evidence policy и поэтому видел пустой `l3_wake`.

Follow-up включает policy только во внутреннем observe-mode planner
reconciliation entrypoint. Внешний флаг по-прежнему запрещён, а entrypoint не
вызывает `apply()`. Добавлен end-to-end unit test: fresh pre-contract L3 wake
доходит до reconciliation request; неполный fixture честно удерживается
snapshot/source gate, не получая contract автоматически.

Повторно выполнено:

```text
PYTHONPYCACHEPREFIX=/tmp/v7-pycache python3 -m unittest \
  tests.unit.test_v7_users_autoswitch_policy \
  tests.unit.test_service_failure_automation_evolution \
  tests.unit.test_operator_execution_packet

Ran 226 tests ... OK
```

Следующая production revalidation корректно не создала Candidate, Packet, lease
или apply, поскольку действующий scope-bound contract встретил независимый
`restore_barrier_required_for_emergency_failover`. Это выявило второй ordering
defect: reconciliation проверял L3 wake, но не передавал в contract issue
preflight independent blockers того же existing emergency gate. В результате
контракт мог быть выдан раньше, чем становится юридически consumable.

Исправление добавляет все независимые pre-contract execution blockers в request
preflight. Исключены только два contract-artifact значения:
`confirmed_l3_wake_required` (уже проверяется L3 owner) и
`no_selected_moves_for_emergency_failover` (ожидаемый эффект отсутствующего
contract). В частности, отсутствие owner-issued restore barrier теперь не
позволяет выпустить one-use contract. Новый тест подтверждает именно эту
границу.

Повторно выполнено:

```text
PYTHONPYCACHEPREFIX=/tmp/v7-pycache python3 -m unittest \
  tests.unit.test_v7_users_autoswitch_policy \
  tests.unit.test_service_failure_automation_evolution \
  tests.unit.test_operator_execution_packet

Ran 227 tests ... OK
```

## Legal terminal до final preflight deploy

`PRODUCTION_DEPLOY_AND_NON_TEST_RECONCILIATION_CALL_REQUIRED`.

Следующий допустимый шаг: safe deploy только `tools/v7-users-autoswitch`, затем
production read-only reconciliation. Если живое fresh L3 evidence действительно
подтверждено, существующий Authority owner сможет сформировать новый scope-bound
request только после owner-issued restore barrier; если нет, terminal остаётся
`RESTORE_BARRIER_REQUIRED_FOR_EMERGENCY_FAILOVER`.
Ни L8, ни Production Maturity, ни routing/user scope этим исправлением не
изменяются.

## Final production verification

Три узких safe deploy выпускали только `tools/v7-users-autoswitch`:

1. `8188109d` — pre-contract L3 shadow evidence;
2. `82eb0c3f` — reconciliation consumer этого evidence;
3. `a93353cb` — restore-barrier preflight.

Финальный runtime release:
`deploy-z8-14-Updatesystem-a93353c-20260726T181144`; restart service не
требовался. `tools/v7-truth-check --all --json` вернул `PASS/FULLY_ALIGNED`,
а `tools/v7-convergence-status --json` — `PASS/ALIGNED` для local, GitHub и
production commit `a93353cb0e2f24f039ef93665ef139af6d1e1a1c`.

Production non-test reconciliation подтвердил:

- coherent existing snapshot owner выполнен и source stable;
- L3 pre-contract shadow evidence включён;
- fresh L3 wake принят;
- expired `acc_d18b14f16f7c11393b3a68c6` не был потреблён;
- новый contract не выдан;
- policy write, Authority grant, Candidate, Packet, lease, runtime apply,
  routing mutation, rollback и user movement отсутствуют;
- единственный exact blocker:
  `restore_barrier_required_for_emergency_failover`.

Итоговый legal terminal:
`RESTORE_BARRIER_REQUIRED_FOR_EMERGENCY_FAILOVER`.

Следующий OMP frontier — существующий restore-barrier Authority owner: сначала
его отдельный scope-bound request и independent decision, затем fresh
reconciliation, fresh one-use Action Class contract и полная revalidation.
Ни barrier, ни routing action данным ремонтом автоматически не создаются.
