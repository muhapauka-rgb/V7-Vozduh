# V7 Service Failure Cohort Adapter — Tier 4 qualification and Authority handoff

Date: `2026-07-28 04:22:44 +07`

Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

Method: `Discover → Reuse → Extend → Implement`

## Итог

Mission выполнена до предусмотренной независимой Authority boundary.

Точный инженерный terminal:

```text
GENERIC_MOVEMENT_CAPABILITY_REUSED
AND
SERVICE_FAILURE_ADAPTER_BRIDGE_QUALIFIED_TO_EXACT_MAXIMUM_TIER
```

Точный следующий legal continuation:

`EXACT_TIER_AUTHORITY_DECISION_REQUIRED`.

Новые Program, Mission group, Planner, Runtime, registry, queue, watcher,
scheduler, executor, Authority owner, certification owner, evidence store или
truth owner не создавались.

## Discover / Reuse

По смыслу и producer-consumer topology обнаружены и повторно использованы:

- historical tier owner:
  `admin_core.autonomy_trust_acceleration.build_historical_blast_radius_evidence`;
- generic governed movement:
  `tools/runtime-support/v7-user-switch`,
  `tools/v7-users-autoswitch`,
  `tools/v7-governed-canary-dry-run-cycle`;
- assignment и route truth owners;
- existing Candidate, Packet, lease, rollback/restore-settle, verification,
  Outcome, Replay и Learning owners;
- standing-policy Authority owner:
  `/etc/v7/policy.json` плюс append-only audit
  `admin_core/operator_execution.py`;
- atomic CPS/OMP consumer:
  `tools/v7-truth-check --reconcile-active-standing-delegated-policy`.

Объявленного invalidation trigger для исторического общего movement evidence
нет. Ступени 1/2/4/5/10/25/48, Polygon и controlled-production certification
не повторялись. Результат knowledge gate:

`RESULT_REUSED_VALID`.

Generic evidence fingerprint:

`7ad9511f521e0a906bd0e9dff33de401e9bbf86f4187722d61b27a48c11b7040`.

## Нормализованная общая capability

| Измерение | Owner-backed предел |
| --- | ---: |
| фактически пройденные scopes | `1,2,4,5,10,25,48` |
| assignment mutation | `48` |
| route verification | `48` |
| Outcome closure | `48` |
| certified no-rollback | `48` |
| Packet identity preservation | `25` |
| rollback apply | `4` |
| replay / duplicate suppression | `4` |
| serial cohort execution | `48` |
| parallel concurrent transactions | `1` |

`48_of_50` остаётся доказательством partial-scope selection, но не
partial-apply failure recovery. Service verification остаётся
scenario/adapter-bound. Capability evidence не является Authority.

## Найденный exact adapter gap

Общий movement executor уже существовал. Реальный gap состоял из четырёх
Tier-1-only связей:

1. standing-policy template;
2. runtime policy gate;
3. governed wrapper/systemd maximum;
4. cohort selection и containment.

Создание нового executor не требовалось. Существующие владельцы минимально
расширены до инженерно квалифицированных Tier 1/2/4:

- policy-derived immutable cohort `1`, `2` или `4`;
- concurrency всегда `1`;
- Candidate/Packet/lease только свежие;
- один Packet не может быть переиспользован;
- per-user route/service verification плюс aggregate cohort terminal;
- circuit breaker прекращает оставшуюся cohort после первой неуспешной
  транзакции;
- rollback/containment и final safe mode остаются существующими;
- fresh capacity, cooldown, anti-flap и target-health gates выполняются на
  каждом transaction/wave.

## Tier matrix

| Tier | Generic | Cohort | Capacity | Service verification | Rollback / containment | Packet / replay | Authority / Runtime | Exact residual |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | reused | PASS | live gate | PASS | PASS | PASS | ACTIVE / ACTIVE | NONE |
| 2 | reused | PASS | live gate | PASS | PASS | PASS | decision required / inactive | independent Tier-2 Authority |
| 4 | reused | PASS | live gate | PASS | PASS + circuit breaker | PASS | decision required / inactive | independent Tier-4 Authority |
| 5 | reused | supporting | live gate | selective | selective evidence | replay evidence missing above 4 | decision required / inactive | rollback/containment and replay evidence above 4 |
| 10 | reused | supporting | live gate | selective | selective evidence | replay evidence missing above 4 | decision required / inactive | rollback/containment and replay evidence above 4 |
| 25 | reused | supporting | live gate | selective | selective evidence | Packet PASS, replay missing above 4 | decision required / inactive | rollback/containment and replay evidence above 4 |
| 48 | reused | supporting | live gate | selective | selective evidence | Packet evidence missing above 25; replay missing above 4 | decision required / inactive | previous residuals plus Packet identity above 25 |

Точный максимум, где каждая mandatory bridge guarantee owner-backed:

`SERVICE_FAILURE_ADAPTER_COMPATIBLE_MAX = 4`.

При квалификации текущие безопасные target families `awg0` и `awg3` имели
запас для Tier 4. Target
`wireguard-1779454504-c43409` был `HARD_FULL` и потому не может быть выбран
fresh planner. Исторический capacity count не используется как permission:
каждая будущая транзакция обязана пройти свежий existing capacity gate.

## Production incident lane

Product Evolution не вызывал Matrix вручную и не использовал Codex как normal
wake. Existing Matrix timer продолжал Tier-1 drain независимо.

Во время deploy verification был краткий generation-transition:
новая transaction уже завершилась, а свежая Matrix scope projection ещё не
была потреблена. Existing consumer корректно вернул `STOP_SAFE`, не выполнил
никакого эффекта и после следующего штатного Matrix observation сам вернулся
в `PASS`. Это подтвердило fail-closed handoff; исправление Matrix не
потребовалось.

Fresh production caller после финального deploy:

`/usr/local/bin/v7-users-autoswitch --standing-delegated-policy-status`.

Owner-backed snapshot:

- incident: `sfinc_be20296fba3d8a6a33e58a583f1b58db`;
- generation: `egid_be6367407f70e591005185a2`;
- state: `OPEN`;
- affected: `22`;
- protected in current generation: `0`;
- unresolved: `22`;
- excluded/recovered: `0`;
- cumulative packet-bound lineage: `41`;
- causal-integrity invalid states: `NONE`;
- next consumer:
  `tools/v7_sync_lib.continue_omp_engineering_control_loop`;
- incident frontier:
  `CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN`.

Это snapshot, а не остановка drain. Следующий штатный Matrix generation может
изменить counts.

## Authority reconciliation

Exact Tier-4 approval отсутствовал. Policy и Runtime не изменялись.

Через существующий Authority audit создан один fresh request:

- request ID: `sdpauth_r1_ed99070cd98caa0f054ffb6e`;
- request hash:
  `ed99070cd98caa0f054ffb6e244cf901bde0034a84d0696cd33e5bb1385d820d`;
- audit record hash:
  `690d24c1101c74ad8b7badc91fd3b9c9670832223437ec954d6af41375b06bfb`;
- created:
  `2026-07-27T19:22:36.056237+00:00`;
- expires:
  `2026-07-28T19:22:36.056237+00:00`;
- requested tier / max users: `4`;
- max concurrent transactions: `1`;
- action class: `channel hard-fail failover`;
- source/target scope: existing planner safe target only;
- Candidate identity: fresh only;
- Packet generation: fresh immediately before execution;
- Packet reuse: forbidden;
- lease: required;
- verification: required;
- rollback or certified no-rollback: required;
- final safe mode: `OPEN`;
- self-expansion: forbidden;
- policy scope hash:
  `cdd21744e65ad49b69d0a88c9c3df7ee3244766cbdc71bee913bbd2b3c9d4ccb`;
- decision set:
  `APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY` / `DECLINE`.

Новый durable owner не создавался. Последний producer-consumer gap был
закрыт внутри существующей цепочки:

```text
append-only Authority audit
-> pending request projection
-> autoswitch status owner
-> production truth-check caller
-> atomic CPS/OMP projection
```

CPS теперь содержит ID, hash, expiry, tier, concurrency, action class, scope
hash и decision set. Сам request не выдаёт Authority и не активирует Runtime.

Текущие независимые значения:

- engineering compatible: `Tier 4`;
- Authority approved: `Tier 1`;
- Runtime enabled: `Tier 1`;
- concurrency: `1`;
- Product Evolution frontier:
  `EXACT_TIER_AUTHORITY_DECISION_REQUIRED`.

## Изменения

Commit `ed370be08152cfdea13117625eaea442709dcde3`:

- Tier 1/2/4 standing-policy templates внутри существующего Authority owner;
- policy-derived cohort size и cohort circuit breaker;
- governed wrapper использует текущий audited policy tier;
- systemd больше не hardcode-ит Tier 1;
- adapter tier matrix и exact Tier-4 product frontier;
- focused tests.

Commit `15ad943c8a4965146d7fc5d785e940baf6734235`:

- read-only pending request selection из существующего append-only audit;
- redacted production status projection;
- exact pending request validation и atomic CPS projection;
- tests pending→decided и CPS consumption.

## Проверки

- syntax / compile: `PASS`;
- focused new tests: `99 PASS`;
- full affected suite: `363 PASS`;
- stale/current fixtures: обновлены, permanent known failures отсутствуют;
- `git diff --check`: `PASS`;
- production non-test caller: `PASS`;
- existing CPS consumer: `PASS`;
- CPS post-write reread: `PASS`;
- causal integrity: `PASS`;
- invalid incident states: `NONE`.

Deploy выполнялся только через `tools/v7-safe-deploy`.

Первый adapter deploy:

`deploy-z8-14-Updatesystem-ed370be-20260728T021152`.

Финальный request-consumer deploy:

`deploy-z8-14-Updatesystem-15ad943-20260728T023230`.

Финальный manifest изменил только:

- `/usr/local/bin/v7_sync_lib.py`;
- `/usr/local/bin/v7-users-autoswitch`;
- `/usr/local/bin/admin_core/operator_execution.py`.

Allowlist: `PASS`; blockers: `NONE`.

## Forbidden effects

Engineering, deploy, request generation и CPS reconciliation дали:

- policy write: `false`;
- contract issuance: `false`;
- Authority expansion: `false`;
- Production Maturity change: `false`;
- Candidate creation: `false`;
- Packet/lease creation: `false`;
- restore-barrier write: `false`;
- Runtime apply: `false`;
- routing mutation: `false`;
- user movement: `0`;
- rollback apply: `false`.

Автономные Tier-1 Matrix transactions, происходившие параллельно под ранее
действующей standing policy, не являются эффектом этой engineering Mission.

## Final state

Incident lane:

`CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN`.

Product Evolution lane:

`EXACT_TIER_AUTHORITY_DECISION_REQUIRED`.

Engineering completion:

`GENERIC_MOVEMENT_CAPABILITY_REUSED AND SERVICE_FAILURE_ADAPTER_BRIDGE_QUALIFIED_TO_EXACT_MAXIMUM_TIER`.

Runtime остаётся Tier 1 до независимого точного решения по текущему request.
