# M5a: approved contract, safe expiry and fresh re-entry

Дата: 2026-07-26
Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`
Этап: `M5a -> M5b`, production owner-backed reconciliation

## Результат

Пользовательское решение `APPROVE_ONCE_AS_SCOPED` было принято только для
точной пары:

- request: `accauth_r1_fbd403e97422f1684420e5d3`;
- hash: `fbd403e97422f1684420e5d3f167fdbe9dd58d13490c76e6b0dc7ada73c636d7`.

Существующий Authority owner выдал одноразовый контракт
`acc_510e6fbeba91a9edb442c5c3` (`510e6fbeba91a9edb442c5c378870bbf10d9fe523d7e10f591adfd618436f937`).
Его scope: пользователь `10.0.0.2`, `vless -> wireguard-1779454504-c43409`,
`max_users=1`, `max_concurrent_transactions=1`; expiry:
`2026-07-26T16:18:09.882190+00:00`.

## M5b: фактический terminal

Свежий production `--mode observe` сформировал Shadow recommendation
`switch` для того же пользователя и здоровой цели, но завершился:

`STOP_SAFE_CURRENT_ACTION_CLASS_CONTRACT_REQUIRED`

Причина подтверждена существующим owner: к моменту повторной сверки
контракт истёк; planner generation был
`5030f32a1189c03760f94fdfc5e6381f409b830bd1666d8f4ce71519fe289fdb`,
а terminal был `dry_run_restore_barrier_clearance_generation_expired`.

Это штатный fail-closed terminal. Не были созданы Candidate, Packet или lease;
`runtime_apply=false`, `routing_mutation=false`, `users_moved=0`,
`rollback_apply=false`, Authority expansion отсутствует, Production Maturity
не изменялась. Истёкший contract и его approval не переиспользованы.

## Новый owner-backed M5a handoff

Существующий autoswitch producer сформировал, а существующий append-only
`operator-execution` audit owner зарегистрировал новый request без policy
write:

- request: `accauth_r1_c956e2cc486f8364e80035c3`;
- hash: `c956e2cc486f8364e80035c3727e125352f2165942f766fbc0161546db3dc0c3`;
- registration record:
  `878a4d531895d5768b37d9c1bd4b5384aafdd3e554110aeb0f5b2abc6a93a47d`;
- expiry: `2026-07-26T16:25:43.918931+00:00`;
- scope: `10.0.0.2`, `vless -> wireguard-1779454504-c43409`, one user and
  one concurrent transaction.

`tools/v7-truth-check --reconcile-action-class-contract-request` atomically
projected only this fresh request into CPS: `PASS`,
`ACTION_CLASS_CONTRACT_REQUEST_CPS_RECONCILED`, post-write reread `PASS`.

## Exact next legal action

`ENGINEERING_AUTHORITY_ACTION_CLASS_CONTRACT_REQUEST_READY` for the new exact
request above. An independent exact `APPROVE_ONCE_AS_SCOPED` or `DECLINE` is
still required. Until then policy write, Packet/lease creation, restore-barrier
write, apply, routing mutation, user movement and rollback apply remain
forbidden.
