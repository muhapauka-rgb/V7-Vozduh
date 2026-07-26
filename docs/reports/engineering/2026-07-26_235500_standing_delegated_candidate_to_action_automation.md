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

- Commit и GitHub: `941187a143a2da008f80c8ce8203e4cd8423c21c`.
- Canonical deploy:
  `deploy-z8-14-Updatesystem-941187a-20260727T001302`, `PASS`.
- Manifest изменил только:
  `tools/v7-users-autoswitch`,
  `tools/v7-governed-canary-dry-run-cycle`,
  `tools/v7-service-matrix-refresh-all`,
  `admin_core/operator_execution.py`.
- Production non-test bounded caller завершился
  `GOVERNED_TRANSACTION_STOPPED / STOP_SAFE` с причиной
  `delegated_policy_admission_denied`: `apply=false`,
  `routing mutation=false`, `restore barrier=false`, `users_moved=0`.
- Production Authority owner зарегистрировал request
  `sdpauth_r1_906f2d2515016198d4c47727`, hash
  `906f2d2515016198d4c47727cc1c5fafcff391408b1627174645ea3c1d450b54`,
  expiry `2026-07-27T17:14:29.219060+00:00`.
- Request registration: append-only record
  `9f9bbab045d5f125103e37cd929904a5b19173b0df063323c650452fc73dcf2`;
  `authority_granted=false`, `policy_write=false`, `runtime_apply=false`,
  `routing_mutation=false`, `users_moved=0`.

Exact scope: existing planner only; action class
`single-user governed candidate failover`; fresh Candidate/Packet/lease;
`max_users=1`; `max_concurrent_transactions=1`; confidence, prediction and
trust floors `70`; cooldown `1800s`; anti-flap `PASS`; immediate user,
channel, service and truth verification; rollback or certified no-rollback;
final `OPEN`; self-expansion, new action classes, blast-radius increase,
identity reuse and Production Maturity change are forbidden.

## Текущий legal terminal

`STANDING_DELEGATED_POLICY_AUTHORITY_REQUEST_READY`

До exact независимого решения контракт отсутствует. После однократного
`APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY` будущие qualifying Candidates
не требуют ручного Candidate/Packet/hash approval; каждый из них всё равно
должен заново пройти fresh event, planner, Packet, lease, live gates,
verification, rollback/no-rollback, Outcome и Learning.
