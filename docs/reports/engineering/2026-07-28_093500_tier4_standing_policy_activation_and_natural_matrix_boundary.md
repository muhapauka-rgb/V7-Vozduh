# V7 Service Failure — Tier 4 standing policy activation and natural Matrix boundary

Date: `2026-07-28 09:35 +07`

Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

Method: `Discover → Reuse → Extend → Implement`

## Итог

Точный Tier-4 standing delegated operational policy выдан существующим
Authority owner, production Runtime активирован, audit/CPS/OMP/Runtime
атомарно согласованы.

Точный текущий terminal:

`CURRENT_SOURCE_SCOPE_EMPTY`.

Tier-4 production cohort не сфабрикован: к моменту активации существующий
Tier-1 Matrix drain уже вывел всех пользователей из текущего VLESS source
scope. Следующий обычный Matrix cycle это независимо подтвердил.

## Authority contract

- request ID: `sdpauth_r1_ed99070cd98caa0f054ffb6e`;
- request hash:
  `ed99070cd98caa0f054ffb6e244cf901bde0034a84d0696cd33e5bb1385d820d`;
- policy scope hash:
  `cdd21744e65ad49b69d0a88c9c3df7ee3244766cbdc71bee913bbd2b3c9d4ccb`;
- decision ID: `sdpdec_566ce2976aca13ad0be14a0b`;
- contract ID: `sdpc_a3cd9882bf0850010a6e37b5`;
- contract hash:
  `a3cd9882bf0850010a6e37b5e1fbbadcf7e2865fa6002b2fe30a9a2e219a0e25`;
- issued: `2026-07-28T02:06:51.026478+00:00`;
- expires: `2026-08-27T02:06:51.026478+00:00`;
- issuing owner: `admin_core/operator_execution.py`;
- action class: `channel hard-fail failover`;
- maximum users per transaction: `4`;
- maximum concurrent transactions: `1`;
- self-expansion: `FORBIDDEN`.

Policy write произошёл только как результат точного Authority decision.
Contract issuance не создал Candidate/Packet/lease, не выполнил apply,
routing mutation, user movement, rollback apply, Authority expansion или
Production Maturity change.

## Найденный и закрытый producer-consumer gap

Runtime уже владел новым Tier-4 contract, но CPS ещё содержал предыдущий
Tier-1 active request и точный pending Tier-4 request. Старый consumer
сравнивал только active request и возвращал:

`cps_runtime_authority_request_mismatch`.

Исправлена только существующая связь:

```text
Authority audit decision
-> active Runtime contract
-> CPS-preserved pending request preimage
-> truth-check production caller
-> atomic CPS/OMP consumer
```

Переход разрешён только при полном совпадении request ID/hash, policy scope
hash, action class, max users и concurrency. Любое иное несовпадение
по-прежнему закрывается `STOP_SAFE`.

Дополнительно valid fresh Runtime scope теперь превосходит устаревший CPS
scope: нулевой Runtime unresolved scope не может сохранять старый active
drain. Точный incident terminal проецируется как
`CURRENT_SOURCE_SCOPE_EMPTY`.

## Production deploy и caller/consumer

Изменения:

- `f1d146a117d8f41a2feab4f734dc69eb713a8660` — exact pending-to-active
  transition и Tier-4 CPS projection;
- `32a81a365112f478d4319b791a268731cdcc90ff` — точный empty-source
  terminal.

Оба deploy выполнены только через `tools/v7-safe-deploy`. Каждый manifest
изменял только:

- `/usr/local/bin/v7_sync_lib.py`.

Финальный deploy:

`deploy-z8-14-Updatesystem-32a81a3-20260728T093359`.

Production non-test caller:

`tools/v7-truth-check --reconcile-active-standing-delegated-policy --json`.

Результат:

- final verdict: `PASS`;
- atomic CPS update: `ATOMIC_CPS_UPDATE_APPLIED`;
- post-write reread: `PASS`;
- current-state consistency: `PASS`;
- causal integrity: `PASS`;
- invalid states: `NONE`;
- Authority-approved tier: `Tier 4`;
- Runtime-enabled tier: `Tier 4`, concurrency `1`;
- Product Evolution frontier:
  `EXACT_TIER_RUNTIME_AUTHORITY_ACTIVATED`.

## Natural Matrix-owned verification

Matrix не запускался вручную. Штатный
`v7-service-matrix-refresh.timer` сам запустил service в
`2026-07-28T02:28:48+00:00`; service завершился с `Result=success`,
`ExecMainStatus=0`.

До цикла VLESS `last_observed_at`:

`2026-07-28T02:13:42.685967+00:00`.

После цикла:

`2026-07-28T02:28:49.259364+00:00`.

Owner-backed VLESS projection:

- incident: `sfinc_be20296fba3d8a6a33e58a583f1b58db`;
- generation: `egid_be6367407f70e591005185a2`;
- affected: `0`;
- protected: `0`;
- unresolved: `0`;
- excluded/recovered: `0`;
- cumulative packet-bound success lineage: `63`;
- last feedback: `execfb_f5770df829554ffabe72278c`;
- last Learning: `learn_e16e4c543fa49dede6477238`;
- invalid causal states: `NONE`.

Поскольку eligible source scope равен нулю:

| Запрошенное доказательство | Текущий owner-backed результат |
| --- | --- |
| selected cohort size | `0; NO_ELIGIBLE_SOURCE_USERS` |
| fresh target / capacity reserve | `NOT_SELECTED; no Candidate` |
| Event/Candidate/Packet/lease | `NONE_NEW` |
| per-user / aggregate verification | `NOT_ENTERED` |
| circuit breaker | `NOT_ENTERED` |
| rollback / no-rollback | `NOT_ENTERED` |
| Outcome / Replay / Learning | `NONE_NEW` |
| updated unresolved scope | `0` |
| durable successor | ordinary Matrix re-observation on a genuine matching event |

Это корректная безопасная граница, а не неполная инженерная работа. Для
production cohort evidence нужен новый genuine matching service-failure scope;
возвращать пользователя на VLESS, создавать outage или повторно использовать
старые execution identities запрещено.

## Проверки

- focused transition/empty-scope tests: `PASS`;
- Service Failure evolution suite: `39/39 PASS`;
- extended affected suite: `553 PASS`;
- два существующих несвязанных test-helper errors:
  `tests.unit.test_omp_external_reentry` передаёт `continue_runner` дважды;
  изменённые файлы этот helper не затрагивают;
- `git diff --check`: `PASS`;
- deploy allowlist: `PASS`;
- production caller/consumer: `PASS`;
- natural Matrix timer caller: `PASS`;
- Runtime causal integrity: `PASS`;
- forbidden production effects during reconciliation: `NONE`.

## Финальная семантика

```text
engineering-compatible tier = 4
Authority-approved tier = 4
Runtime-enabled tier = 4 serial
production-proven tier = 1
Tier-4 natural cohort evidence = OPEN
incident frontier = CURRENT_SOURCE_SCOPE_EMPTY
product frontier = EXACT_TIER_RUNTIME_AUTHORITY_ACTIVATED
```

Exact re-entry:

```text
next genuine matching service failure
-> ordinary Matrix observation
-> fresh planner target/capacity gates
-> fresh cohort up to 4
-> fresh Candidate/Packet/lease
-> serial bounded execution
-> per-user + aggregate verification
-> circuit breaker
-> rollback or certified no-rollback
-> Outcome/Replay/Learning
-> CPS/OMP scope and tier reconciliation
```
