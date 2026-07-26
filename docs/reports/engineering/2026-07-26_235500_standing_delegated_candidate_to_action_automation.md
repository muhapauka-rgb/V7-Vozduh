# Standing delegated Candidate-to-action automation

Дата: 2026-07-26
Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

## Цель

Устранить бесконечный цикл короткоживущих M5a approvals. Один независимый
Authority decision должен активировать узкий standing contract; после него
каждый новый qualifying Candidate проходит существующую цепочку автоматически,
без ручного подтверждения Candidate, Packet или hash.

## Discover -> Reuse -> Extend -> Implement

Discovery подтвердил, что новый Runtime, Planner, watcher, queue или Packet
owner не нужен. Уже существовали:

- Service Matrix production producer и его timer lifecycle;
- passive/advisory consumer и OMP consumer;
- `tools/v7-users-autoswitch` как единственный planner/autoswitch owner;
- `tools/v7-governed-canary-dry-run-cycle
  --execute-bounded-delegated-transaction`;
- `admin_core/operator_execution.py` как policy, Packet, lease и
  restore-barrier Authority owner;
- verification, rollback/no-rollback, Outcome, Learning и final-`OPEN`.

Найденный дефект: bounded executor читал статическую read-only policy preview,
а Service Matrix lifecycle не вызывал этот consumer. Поэтому заявленное
`candidate_approval_required=false` не могло стать реальным автоматическим
действием.

## Реализация

Существующие owners расширены минимально:

1. `admin_core/operator_execution.py`
   - формирует и регистрирует один exact standing-policy Authority request;
   - связывает request с полной policy template и текущим policy-file hash;
   - append-only сохраняет request и решение с actor provenance;
   - выдаёт 30-дневный live contract только из exact зарегистрированного
     request;
   - не допускает повторную выдачу, scope drift или expired request/contract.
2. `tools/v7-governed-canary-dry-run-cycle`
   - читает live contract из `/etc/v7/policy.json`;
   - проверяет exact Authority audit record;
   - допускает только свежий matching production service-failure event;
   - сохраняет `max_users=1`, concurrency=1, fresh Candidate/Packet/lease,
     anti-flap, cooldown, verification, rollback/containment и final `OPEN`.
3. `tools/v7-service-matrix-refresh-all`
   - после существующих passive/advisory/OMP consumers вызывает существующий
     bounded executor только при ACTIVE standing contract;
   - отсутствие contract или Candidate является нормальным fail-closed
     terminal;
   - после реального completed action повторно вызывает существующий OMP
     consumer.
4. Legacy M5a request/contract TTL увеличен с 300 до 900 секунд как
   fallback. Standing activation request действует 24 часа и всё равно
   инвалидируется при любом изменении policy generation.

Новый timer, daemon, watcher, queue, registry, Planner, Runtime или Authority
owner не создан и не включён.

## Safety

Standing scope:

- action class: `single-user governed candidate failover`;
- один user, одна concurrent transaction;
- только fresh matching service-failure event;
- существующий planner only;
- fresh Candidate, Packet и lease; reuse запрещён;
- live capacity/service/route/freshness/confidence gates;
- restore barrier, immediate verification, temporal outcome,
  rollback/containment и final `OPEN`;
- Authority self-expansion и Production Maturity change запрещены.

До отдельного exact Authority решения standing contract не активирован.
Текущая реализация сама по себе не пишет production policy, не создаёт
Candidate/Packet/lease, не пишет restore barrier, не выполняет apply и не
перемещает пользователей.

## Проверки

- Python compile: `PASS`.
- Focused affected campaign: `136 tests PASS`.
- Standing request/registration/issuance/expiry/duplicate tests: `PASS`.
- Missing contract/audit/event, scope expansion and packet reuse fail closed:
  `PASS`.
- Existing bounded delegated transaction without Candidate/Packet approval:
  `PASS`.
- Full unit discovery был запущен, но не является пригодным terminal gate:
  существующие `test_admin_core_events` имеют шесть unrelated
  `FileNotFoundError` из-за отсутствующей
  `tests/unit/fixtures/events/`, а длинный Polygon CLI test не завершился в
  разумное bounded окно. Затронутые owners проверены отдельной полной focused
  кампанией.

## Deployment and production verification

`PENDING` до commit, push, canonical safe deploy, production non-test
fail-closed caller, truth/convergence и формирования exact standing Authority
request.

## Текущий legal terminal

`ENGINEERING_IMPLEMENTATION_COMPLETE_DEPLOY_AND_STANDING_POLICY_AUTHORITY_REQUEST_REQUIRED`
