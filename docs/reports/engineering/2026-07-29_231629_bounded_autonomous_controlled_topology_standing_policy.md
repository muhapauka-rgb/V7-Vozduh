# Engineering Report: bounded autonomous controlled topology

Дата: 2026-07-29

Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

Mission: `BOUNDED_AUTONOMOUS_CONTROLLED_CERTIFICATION_TOPOLOGY_AUTHORITY_V1`

## Результат discovery

Новый Authority owner, policy store, Planner, Runtime, registry, queue, watcher,
scheduler или execution path не требуются.

Существующие владельцы уже обеспечивают:

- независимый standing-policy request/decision/issuance и append-only audit:
  `admin_core/operator_execution.py`;
- policy truth: `/etc/v7/policy.json`;
- live capability map и deterministic selection:
  `tools/v7-users-autoswitch`;
- controlled-source reserve/release:
  `tools/v7-egress-set-state`;
- Candidate, Packet, lease, restore barrier и bounded apply:
  `tools/v7-governed-canary-dry-run-cycle`;
- event-driven caller: `tools/v7-service-matrix-refresh-all`;
- Outcome, Replay, Learning, CPS и OMP consumers.

Точный разрыв: активный standing contract семантически допускает только
`channel hard-fail failover`. Он не содержит topology action class, нулевые
ordinary-user deltas, reservation bounds и перечень допустимых topology
production effects. Поэтому V2.5 законно формировал one-off
`REBIND_CONTROLLED_CERTIFICATION_SOURCE` request.

## Реализация

Существующий standing-policy owner расширен profile-aware контрактом
`SERVICE_FAILURE_WITH_CONTROLLED_CERTIFICATION_TOPOLOGY_V1`.

Добавлен action class:

`bounded autonomous controlled certification topology`.

Начальный scope допускает только:

`REBIND_CONTROLLED_CERTIFICATION_SOURCE`.

Границы:

- certification identities only;
- max users per transaction = 1;
- max concurrent transactions = 1;
- ordinary identity/assignment/route delta = 0;
- target ordinary users = 0;
- fresh health, stability, capacity, manifest, Candidate, Packet и lease;
- restore barrier before apply;
- verification и bounded idempotent rollback;
- external resource, credential, hard-limit mutation и self-expansion
  запрещены.

Profile-specific поля входят в normalized scope только при их наличии.
Исторические service-failure-only contracts сохраняют прежние payload/hash и
не переинтерпретируются после engineering deploy.

Существующий topology diagnostic теперь:

- валидирует combined contract и точный action-class scope;
- выдаёт
  `AUTO_ADMITTED_BY_STANDING_DELEGATED_CONTROLLED_TOPOLOGY_POLICY`
  только при exact active audited contract;
- не считает старый one-off request разрешением;
- делает one-off package non-actionable после standing activation;
- сохраняет нулевые production effects в read-only admission.

При независимой активации combined policy существующий Authority audit owner
append-only помечает все undecided one-off topology requests как
`SUPERSEDED_BY_STANDING_DELEGATED_CONTROLLED_TOPOLOGY_POLICY`.

CPS/OMP reconciliation различает pending combined standing-policy request и
старый one-off topology request. Pending combined request является текущим
`ENGINEERING_AUTHORITY` frontier и имеет приоритет над one-off решением.

## Проверка

Affected test campaign:

- `tests.unit.test_operator_execution_packet`;
- `tests.unit.test_service_failure_automation_evolution`.

Результат до финального deploy: `130 tests PASS`.

Дополнительно доказано:

- без независимого решения policy не записывается;
- legacy scope/hash остаётся прежним;
- malformed ordinary-assignment scope fail-closed;
- exact approved combined contract проходит audit-backed validation;
- one-off request superseded exactly once при standing activation;
- active combined contract подавляет one-off admission;
- pending combined request атомарно становится CPS/OMP Authority frontier;
- до Authority решения: Candidate/Packet/lease/restore barrier/apply/routing/
  movement/rollback/Authority expansion/Production Maturity change = `NONE`.

## Текущий legal terminal

Engineering implementation готовится к safe deploy и production non-test
caller verification.

После deploy должен быть сформирован один fresh:

`STANDING_DELEGATED_CONTROLLED_TOPOLOGY_POLICY_AUTHORITY_REQUEST_READY`.

До его независимого решения production trial не разрешён. Требуемое решение:

`APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY`

или:

`DECLINE`.

`ONE_IDENTITY_AUTONOMOUS_CONTROLLED_TOPOLOGY_TRIAL_PROVEN` пока не заявлен.
