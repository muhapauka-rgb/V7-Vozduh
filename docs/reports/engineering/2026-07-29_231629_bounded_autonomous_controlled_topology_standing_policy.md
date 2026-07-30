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

## Production deploy и caller/consumer verification

Commit:

`5ac5e2d767aadf274957535022af796ef35e3090`.

`tools/v7-safe-deploy` manifest: `PASS`. Изменены только:

- `tools/v7_sync_lib.py`;
- `tools/v7-users-autoswitch`;
- `admin_core/autonomy_trust_acceleration.py`;
- `admin_core/operator_execution.py`.

Systemd, daemon и timer changes: `NONE`.

Post-deploy manifest: zero delta. Production non-test
`v7-users-autoswitch --standing-delegated-policy-status` подтвердил:

- действующий legacy service-failure contract остаётся валидным и не
  переинтерпретирован;
- production caller видит новый combined-policy request path;
- policy/audit owner зарегистрировал один fresh exact request;
- Authority grant, policy write, Candidate, Packet, lease, restore barrier,
  apply, routing mutation, user movement и rollback: `NONE`.

Fresh request:

- request id:
  `sdpauth_r1_c8e5e66dc47c5289a1acc97f`;
- request hash:
  `c8e5e66dc47c5289a1acc97ffd19021607f7428b1dc26d75e5bd0b8b4e7edb67`;
- policy scope hash:
  `8d9c4500e81e9520b90dd3a79f7f7df141d0d3fb98913fb958d661a1738fe72b`;
- expires:
  `2026-07-30T16:29:48.978955+00:00`;
- status:
  `AWAITING_INDEPENDENT_AUTHORITY_DECISION`.

CPS и OMP атомарно reconciled в:

`ENGINEERING_AUTHORITY_STANDING_DELEGATED_CONTROLLED_TOPOLOGY_POLICY_DECISION_REQUIRED`.

Старый one-off topology request не является текущим execution permission.

Final verification:

- affected campaign: `130 tests PASS`;
- `tools/v7-truth-check --all --json`:
  `PASS`, `FULLY_ALIGNED`;
- `tools/v7-convergence-status --json`:
  `PASS`, `ALIGNED`;
- local/GitHub/production commit:
  `5ac5e2d767aadf274957535022af796ef35e3090`;
- deploy delta mismatch: `NONE`.

## Текущий legal terminal

Fresh exact request сформирован и потреблён CPS/OMP как независимая
`ENGINEERING_AUTHORITY` граница.

До его независимого решения production trial не разрешён. Допустимое решение:

`APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY`

или:

`DECLINE`.

`ONE_IDENTITY_AUTONOMOUS_CONTROLLED_TOPOLOGY_TRIAL_PROVEN` пока не заявлен.

## Продолжение после независимого Authority решения

Получено и потреблено существующим Authority owner точное решение:

- request:
  `sdpauth_r1_c8e5e66dc47c5289a1acc97f`;
- request hash:
  `c8e5e66dc47c5289a1acc97ffd19021607f7428b1dc26d75e5bd0b8b4e7edb67`;
- policy scope hash:
  `8d9c4500e81e9520b90dd3a79f7f7df141d0d3fb98913fb958d661a1738fe72b`;
- decision:
  `APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY`;
- decision id:
  `sdpdec_5c64e7680fc1d8f87e77b2a2`;
- issued contract:
  `sdpc_4cb7657fcbafdf18dbc26e59`;
- contract hash:
  `4cb7657fcbafdf18dbc26e59abd2510b23a4d6bcaf3dee43d435d1b3c082744e`;
- issued at:
  `2026-07-29T16:40:39.708816+00:00`;
- expires at:
  `2026-08-28T16:40:39.708816+00:00`.

Решение прошло только через
`admin_core/operator_execution.py` и существующий append-only audit. Прямого
редактирования `/etc/v7/policy.json`, скрытого Authority grant, нового policy
store или нового execution owner не было.

Effective policy profile:

`SERVICE_FAILURE_WITH_CONTROLLED_CERTIFICATION_TOPOLOGY_V1`.

Policy сохраняет независимые оси:

- Authority-approved tier: `48`;
- controlled-certification Runtime tier: `48`;
- ordinary-production Runtime tier: `4`;
- max concurrent transactions: `1`;
- topology transaction: только `1` certification identity;
- ordinary identity/assignment/route deltas: `0`;
- self-expansion: `FORBIDDEN`.

## Existing-owner execution и production proof

После активации использованы только уже существующие Matrix, topology,
reservation, Candidate, Packet, lease, bounded executor, feedback и Learning
owners. До каждой доработки выполнялась смысловая проверка существующей
реализации; новый Planner, registry, queue, watcher, Runtime или Authority
system не создавался.

Обычный production Matrix caller выполнил одну policy-bound topology
транзакцию:

- certification identity: `10.7.0.100`;
- source: `1`;
- target: `vless`;
- Packet:
  `pkt_preview_f50b2b469cf6c6035414fd8f`;
- Decision:
  `decision_commit_bed8fc3d3e01b4917e892629`;
- governed operation:
  `govdry_22d599a2e20213deba269142`;
- Runtime operation:
  `runtime_autoswitch_524bdf3518988062f91f1485`;
- feedback:
  `execfb_a38309fd1dd7d34d083836c4`;
- Learning:
  `learn_d94b3ad5007e120fb9e028ce`;
- outcome: `SUCCESS`;
- verification: `COMPLETE`;
- rollback: `NOT_REQUIRED`;
- circuit breaker final state: `OPEN`.

Packet reuse, lease reuse, Authority expansion, ordinary-customer movement и
Production Maturity change отсутствуют.

## Найденные и устранённые producer-consumer gaps

В ходе caller/consumer verification были обнаружены и закрыты три общих, а не
channel-specific, дефекта.

1. Outcome projection считала `rollback_used=true` по одному наличию объекта
   `rollback_result`, даже когда terminal был `NOT_REQUIRED`. Одновременно
   compact Matrix receipt терял reservation facts. Исправлено commit
   `36a7000d` (`Correct topology outcome projections`). Production affected
   replay вернул `rollback_used=false`, `outcome_quality=SUCCESS`,
   `verification_complete=true`; append-only исторический Outcome не
   переписывался.

2. Planner валидировал форму standing policy, но не проверял, входит ли
   выбранное topology action в `allowed_actions`. В результате
   `PROVISION_DEDICATED_CONTROLLED_CERTIFICATION_SOURCE` мог дойти до
   executor, хотя policy допускала только
   `REBIND_CONTROLLED_CERTIFICATION_SOURCE`. Исправлено commit `02cf4f62`
   (`Enforce topology action scope before execution`). Теперь unsupported
   action останавливается на точном Authority frontier до Candidate, Packet,
   lease или production effect.

3. Закрытый `INTENT_CLOSED` incident повторно пересчитывался по более позднему
   `users.registry`. Возврат пользователя на тот же канал в новом жизненном
   цикле мог ложным образом открыть старый terminal scope и выдавать
   `INCIDENT_SCOPE_ACCOUNTING_BROKEN` /
   `SUCCESSFUL_ATTEMPT_WITHOUT_SCOPE_UPDATE`. Исправлено commit `353a3198`
   (`Freeze closed incident scope projections`) внутри существующего
   scope-accounting owner. Терминальный denominator теперь заморожен правилом
   `INTENT_CLOSED_TERMINAL_SCOPE_FROZEN`; новый live route относится только к
   новой incident generation.

## Финальная проверка реализации

Затронутая кампания после последнего исправления:

- `245 tests PASS`;
- новые regression cases:
  closed zero-scope не открывается от будущего route generation;
  partial terminal scope сохраняет protected count и относит остаток к
  explicitly excluded/recovered;
- существующая active-incident live-route accounting остаётся без изменений;
- единственные предупреждения — ранее существовавшие Python
  `DeprecationWarning: invalid escape sequence \d`.

Production deploy:

- commit: `353a3198e9c2432faa3dbb81c7ec15d805d1b52b`;
- `tools/v7-safe-deploy` preflight: `PASS`;
- единственный runtime delta:
  `tools/v7-users-autoswitch`;
- deploy id:
  `deploy-z8-14-Updatesystem-353a319-20260730T081201`;
- zero-delta provenance/snapshot refresh deploy id:
  `deploy-z8-14-Updatesystem-353a319-20260730T081644`;
- daemon/timer enablement: `NONE`;
- routing mutation/user movement/rollback apply/Authority expansion:
  `NONE`.

Production non-test read-only consumer:

`/usr/local/bin/v7-users-autoswitch --consume-service-failure-automation-only`.

Результат:

- `PASS`;
- consumed records: `61`;
- changed compact records: `1`;
- rejected records: `0`;
- Candidate/Packet/lease: `NONE`;
- Runtime apply/routing mutation/user movement/rollback apply: `NONE`;
- Authority/Production Maturity change: `NONE`.

Повторный
`/usr/local/bin/v7-users-autoswitch --standing-delegated-policy-status`
подтвердил:

- policy/audit: `PASS`;
- service-failure causal integrity: `PASS`;
- invalid states: `[]`;
- один корректно открытый incident:
  `sfinc_79c7265b16283934089d5119f65455dd`;
- source: `1`;
- affected/protected/unresolved/excluded:
  `46/0/46/0`;
- durable successor:
  `tools/v7_sync_lib.consume_service_failure_automation_frontier`;
- re-entry:
  существующий OMP consumer под `closure-records.lock`.

`tools/v7-truth-check --reconcile-active-standing-delegated-policy --json`
после production proof: `PASS`. CPS и OMP обновлены атомарно; policy,
contract, Candidate, Packet, lease, restore barrier и routing не изменялись
этим reconciliation.

Финальный convergence:

- `tools/v7-truth-check --all --json`:
  `PASS`, `FULLY_ALIGNED`;
- `tools/v7-convergence-status --json`:
  `PASS`, `ALIGNED`;
- local/GitHub/production commit:
  `353a3198e9c2432faa3dbb81c7ec15d805d1b52b`;
- production binary hashes:
  `MATCH`;
- deploy delta mismatches:
  `[]`.

## Финальный legal terminal после approval

Standing delegated policy активна и production caller/consumer доказаны.
Повторное подтверждение этой policy не требуется до expiry, revoke или
точного invalidation trigger.

Следующая selected topology option требует другое действие:

`PROVISION_DEDICATED_CONTROLLED_CERTIFICATION_SOURCE`

для существующего valid draft:

`1-1779291887-55965c`.

Это действие не входит в текущий `allowed_actions`; поэтому exact current
frontier законно равен:

`ENGINEERING_AUTHORITY_PROVISION_DEDICATED_CONTROLLED_CERTIFICATION_SOURCE_REQUIRED`.

До отдельного независимого решения:

- reservation/assignment change: `FORBIDDEN`;
- Candidate/Packet/lease: `FORBIDDEN`;
- restore barrier: `FORBIDDEN`;
- deliberate failure/apply/routing/user movement/rollback: `FORBIDDEN`.

Одновременно текущий approved source `1` остаётся
`STOP_SAFE_BASELINE_UNHEALTHY` (`0/14`) с owner-backed внешней причиной:

`EXTERNAL_AMNEZIAWG_PEER_OR_CREDENTIAL_PROVIDER`.

Это не отменяет активную standing policy и не требует повторной ladder
certification. Оно определяет два законных пути re-entry: восстановление
точного external peer/profile с fresh healthy Matrix baseline либо отдельное
Authority решение для provisioning уже выбранного dedicated draft.
