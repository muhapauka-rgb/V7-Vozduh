# Tier-48 activation и точная граница controlled certification pool

Дата: `2026-07-28` (`Asia/Bangkok`)

Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

Статус: `T48_M7_COMPLETE_CONSUMED; T48_M8_EXACT_EXTERNAL_POOL_BOUNDARY`

## Итог

Независимое решение Authority по request
`sdpauth_r1_e3aecc34f26ffbff4fdc169c` принято существующим owner и
атомарно потреблено. Standing delegated operational policy для Service
Failure активна с пределом `48` пользователей на одну строго
последовательную транзакцию.

`T48-M7` завершена. `T48-M8` честно остановлена до создания controlled
condition: существующий production certification pool не содержит пяти
выделенных пользователей на одном активном controlled source. Обычные
клиенты не были переклассифицированы или использованы для получения
сертификационного evidence.

Новая Program, Mission, Authority owner, Planner, Runtime, queue, watcher,
registry или truth source не создавались.

## Authority decision и активный contract

Approval был потреблён через существующий
`admin_core/operator_execution.py`:

- request id: `sdpauth_r1_e3aecc34f26ffbff4fdc169c`;
- request hash:
  `e3aecc34f26ffbff4fdc169c10b9e4f13c693e374e24d71c6f00ed03e88fd600`;
- policy scope hash:
  `1c716df6801e28c004613e23d27ef66702cfc7e8c489a274f210435b723271e0`;
- decision id: `sdpdec_e3941436d9a0d45a483767e4`;
- contract id: `sdpc_36bb4d9cc58ceac13287b973`;
- contract hash:
  `36bb4d9cc58ceac13287b9735eb458bb49b8756146b4daf25258f27f1b6b7583`;
- issued at: `2026-07-28T10:15:20.023896+00:00`;
- expires at: `2026-08-27T10:15:20.023896+00:00`;
- action class: `channel hard-fail failover`;
- `max_users_per_action=48`;
- `max_concurrent_transactions=1`;
- self-expansion: `false`.

Authority expansion и policy write произошли ровно как эффект этого
независимого approval. Candidate, Packet, lease, restore barrier, runtime
apply, routing mutation, rollback apply, user movement и Production Maturity
change при выдаче contract не выполнялись.

## Discover → Reuse → Extend → Implement

Проверены существующие `users.registry`, `egress.registry`, standing policy,
Authority audit, Controlled Production Certification Program, CPS и OMP.
Отдельное хранилище pool, список пользователей или второй truth source не
создавались.

Обнаружен минимальный producer-consumer gap: production standing-policy
status не публиковал агрегированную готовность существующего certification
pool, поэтому CPS не мог автоматически отличить готовую `T48-M8` от
отсутствующего controlled substrate.

Расширены только существующие owners:

- `tools/v7-users-autoswitch` публикует read-only агрегат без IP-адресов;
- `tools/v7_sync_lib.py` потребляет агрегат и формирует точный M8 frontier;
- unit tests проверяют отсутствие identity leakage и корректный Tier-5
  blocker.

Runtime commit:
`7664e96191906e5dc833fb4d2b3435e1d1855713`.

Affected tests: `PASS`. Проверены Service Failure evolution,
operator-execution packet, governed canary, Polygon harness и
operation-scoped binding.

## Safe deploy и production consumer

Штатный dry-run manifest: `PASS`.

Exact deploy delta:

- `tools/v7_sync_lib.py`;
- `tools/v7-users-autoswitch`.

Forbidden effects manifest:

- planner modification: `false`;
- policy modification: `false`;
- restore-barrier modification: `false`;
- autoswitch apply: `false`;
- routing mutation: `false`;
- user movement: `false`.

Production deploy:
`deploy-z8-14-Updatesystem-7664e96-20260728T173456`.

Production non-test caller
`/usr/local/bin/v7-users-autoswitch --standing-delegated-policy-status`
подтвердил:

- active contract: `sdpc_36bb4d9cc58ceac13287b973`;
- Authority-approved tier: `48`;
- Runtime-enabled tier: `48`;
- concurrency: `1`;
- total enabled certification users: `4`;
- active controlled sources: `1`;
- maximum certification users on one active source: `3`;
- missing users for first Tier-5 cohort: `2`;
- pool fingerprint:
  `fabe218d853bc10fc6900654517bb88939e170f8f5b08fb61acb520d6d975431`;
- ordinary customer reclassification: forbidden;
- raw user list stored: `false`.

Caller выполнил только read-only consumption:
`policy_write=false`, `candidate_created=false`, `packet_created=false`,
`lease_created=false`, `restore_barrier_write=false`,
`runtime_apply=false`, `routing_mutation=false`, `user_movement=0`,
`rollback_apply=false`, `authority_expansion=false`,
`production_maturity_change=false`.

## Primary CPS/OMP frontier reconciliation

Первое production consumption обнаружило ещё один existing-owner semantic
gap: `PRODUCT_EVOLUTION_FRONTIER` уже показывал M8 pool boundary, но общий
Section 0 и deterministic sequence сохраняли старый terminal
`REAL_WORLD_LIMIT_WAIT_FOR_FRESH_MATCHING_SERVICE_FAILURE_EVENT`.

Это могло вернуть следующий OMP consumer к пассивному ожиданию outage вместо
существующей `T48-M8`. Исправлены только текущая проекция и её consistency
validation:

- incident frontier остаётся независимым и равен
  `CURRENT_SOURCE_SCOPE_EMPTY`;
- capability-local Natural L8 wait остаётся
  `REAL_WORLD_LIMIT_CAPABILITY_LOCAL`;
- primary product frontier теперь равен
  `V7_SERVICE_FAILURE_T48_M8_CONTROLLED_POOL_RECONCILIATION`;
- program stop классифицирован как точная `ENGINEERING_AUTHORITY` boundary;
- deterministic sequence называет существующих владельцев pool и точное
  условие re-entry.

Commits:

- `3a5718fc98b095f47026cb56c77dce556a80f1b9`;
- `0fa3b7b8c0427507175405df74a91c286078e3d4`.

Deploys:

- `deploy-z8-14-Updatesystem-3a5718f-20260728T174715`;
- `deploy-z8-14-Updatesystem-0fa3b7b-20260728T175349`.

Оба manifest содержали только `tools/v7_sync_lib.py`; forbidden effects
отсутствовали. Финальная affected campaign: `193 tests PASS`.

Source-CPS existing consumer завершил
`ATOMIC_CPS_UPDATE_APPLIED` и подтвердил:

- `CURRENT_STOP_CONDITION=ENGINEERING_AUTHORITY`;
- `CURRENT_NEXT_ACTION_ID=V7_SERVICE_FAILURE_T48_M8_CONTROLLED_POOL_RECONCILIATION`;
- `CURRENT_PROGRAM_EXECUTION_FRONTIER=WAITING_INPUT:CONTROLLED_PRODUCTION_CERTIFICATION_POOL_OR_EXACT_ENGINEERING_AUTHORITY`;
- `CAUSAL_M7_TIER_DECISION_CONSUMPTION=SERVICE_FAILURE_TIER48_RUNTIME_ACTIVATION_DECIDED`;
- `T48_M8_STATUS=ENGINEERING_COMPLETE_AWAITING_EXACT_CONTROLLED_PRODUCTION_POOL_OR_AUTHORITY`.

OMP current-state references в разделах 20.2 и 26 обновлены на те же exact
stop, next action, Tier-48 contract и pool boundary. Исторические snapshot
разделы не использованы как scheduling truth.

Прямой production `v7-truth-check --all` не является допустимым source-CPS
consumer: binary-only production layout не содержит source manifest
`docs/track7/runtime-convergence/V7_TRUTH_MANIFEST.json`. Это не runtime defect;
production state был прочитан штатным deployed
`v7-users-autoswitch --standing-delegated-policy-status`, а source CPS
потреблён локальным owner через production access.

## Exact M8 terminal

Текущий owner-backed status:

`CONTROLLED_CERTIFICATION_POOL_INSUFFICIENT_FOR_TIER_5`.

Текущий legal terminal:

`ENGINEERING_COMPLETE_AWAITING_EXACT_CONTROLLED_PRODUCTION_POOL_OR_AUTHORITY`.

Exact blocker:

`fewer_than_5_enabled_certification_users_on_one_active_controlled_source`.

Exact re-entry:

`five_or_more_existing_owner_authorized_enabled_certification_users_are_assigned_to_one_active_controlled_source`.

Это не `REAL_WORLD_LIMIT`, не ожидание нового outage и не недостаток
инженерной реализации Tier-48. Текущая standing policy разрешает действие
только при уже существующей fresh Service Failure situation и live gates; она
не разрешает создавать production identities, переклассифицировать обычных
клиентов, выполнять setup movement или намеренно деградировать канал.

Для законного запуска controlled ladder `5 → 10 → 25 → 48` требуется
owner-authorized pool минимум из пяти выделенных certification users на одном
active controlled source. Сейчас на таком source находятся три пользователя;
всего выделенных certification users — четыре. Следовательно, нужен как
минимум ещё один реальный dedicated certification identity, а также
owner-authorized assignment достаточного состава на один controlled source.

До выполнения re-entry condition `T48-M9` не начинается, evidence не
фабрикуется, обычные клиенты не перемещаются. CPS, OMP и Runtime сохраняют
активный Tier-48 contract и точный durable successor.
