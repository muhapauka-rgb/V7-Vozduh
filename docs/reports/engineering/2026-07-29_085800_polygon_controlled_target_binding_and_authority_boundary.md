# Engineering Report: dynamic controlled-target discovery and reselection

Дата production verification: `2026-07-29T08:55:24Z`

Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

Residual: `DYNAMIC_CONTROLLED_TARGET_DISCOVERY_RESELECTION_AND_ALLOCATION_V1`

## Итог

Инженерный дефект долгоживущей привязки controlled campaign к первому
`EXECUTION_ONLY` target устранён и production-consumed.

Существующие Matrix, registry, quality, capacity, assignment, Planner,
Authority audit, campaign и CPS/OMP owners теперь образуют один замкнутый
контур:

```text
fresh Matrix/registry/quality/capacity
-> compact all-egress inventory
-> full live admission
-> deterministic safety ranking
-> exact-target Authority boundary
-> immutable fresh allocation only after admission
-> material fingerprint re-entry
```

Новый Program, Planner, Runtime, registry, queue, watcher, scheduler, Authority
owner, evidence store или truth source не создавался.

Инженерный terminal:

`DYNAMIC_CONTROLLED_TARGET_SELECTION_RUNTIME_CONSUMED_WITH_EXACT_BOUNDARY`

Campaign terminal `SERVICE_FAILURE_CONTROLLED_PRODUCTION_OUTCOMES_CONSUMED_5_10_25_48`
не достигнут. Это не незакрытый engineering gap: текущая production truth
содержит два независимых live safety blocker.

## Закрытые дефекты

- `CAMPAIGN_TARGET_ID_ORDER_SELECTION_DEFECT`;
- `CAMPAIGN_TARGET_READINESS_SEMANTICALLY_INCOMPLETE`;
- `CAMPAIGN_TARGET_PINNING_WITHOUT_DYNAMIC_RESELECTION`;
- `CAMPAIGN_TARGET_INVENTORY_GENERATION_NOT_CONSUMED`.

Изменение `tools/v7-service-matrix-refresh-all` теперь селективно инвалидирует
уже существующие routing scenarios через producer-to-consumer binding с
`tools/v7-users-autoswitch`. Отдельная dependency map или registry не создана.

## Production inventory

Production caller:

`v7-users-autoswitch --controlled-target-selection-diagnostic`

Он прочитал все семь owner-backed egress, включая обычные, reserved,
controlled-only и непригодные targets.

| Target | Роль | Services | Пользователи | Current/5m/1h stability | Capacity после reserve | Controlled verdict |
|---|---|---:|---:|---|---:|---|
| `1` | `GLOBAL_FAST`, exact source | `0/14` | `48 certification`, `0 ordinary` | `0.0000/0.0001/0.0002` | `0` | source, не может быть target; внешний peer/profile не подтверждён |
| `amneziawg-exec-20260528-10-8-1-14` | `EXECUTION_ONLY`, exact approved target | `14/14` | `0` | `0.0948/0.1693/0.2202` | `9` | full live admission `STOP_SAFE`: stability и minimum throughput ниже floor |
| `awg0` | `GLOBAL_STABLE` | `11/14` в свежем Matrix | `13 ordinary` | ниже `0.45` | достаточно по generic policy | нет controlled permission/isolation; ordinary occupancy |
| `awg3` | `GLOBAL_STABLE` | `14/14` | `11 ordinary` | ниже `0.45` | достаточно по generic policy | нет controlled permission/isolation; ordinary occupancy |
| `openvpn-1779388847-d2ad7c` | `GLOBAL_FAST` | `14/14` | `2 ordinary + 1 certification` | выше `0.45` | `0`, registry hard limit исчерпан | нет controlled permission/isolation; ordinary occupancy |
| `vless` | `GLOBAL_FAST` | `14/14` | `0` | `0.3132/0.3199/0.3960` | `142` | stability ниже floor; нет controlled permission |
| `wireguard-1779454504-c43409` | `GLOBAL_FAST` | `14/14` | `46 ordinary + 3 certification` | `0.8428/0.8581/0.8890` | `0`, registry hard limit исчерпан | нет controlled permission/isolation; ordinary occupancy |

Production selection:

- inventory target count: `7`;
- ranked controlled targets: `0`;
- pinned target full live admission: `false`;
- selected target: `NONE`;
- legal target outcome:
  `NO_CURRENT_TARGET_CAPACITY_WITH_EXACT_OWNER_BOUNDARY`;
- target inventory fingerprint after deploy:
  `2b8a6a422a97ed56e3c5033366099ad48c30d3c78326da14f66d2efabab9bb39`.

Обычные healthy channels больше не скрыты от campaign diagnostic. Они
присутствуют с точными exclusion reasons, но не становятся certification
targets без controlled-use/isolation и Authority contract.

## Source-condition boundary

Fresh Matrix подтвердил exact source `1`:

- `0/14` reachable services;
- `48` dedicated certification identities;
- `0` ordinary identities;
- external resource:
  `AMNEZIAWG_REMOTE_PEER_OR_MATCHING_PROFILE_FOR_SOURCE_1`;
- external owner:
  `EXTERNAL_AMNEZIAWG_PEER_OR_CREDENTIAL_PROVIDER`;
- failed link:
  `EXTERNAL_AMNEZIAWG_PEER_RESPONSE_OR_MATCHING_PROFILE -> LOCAL_HANDSHAKE -> MATRIX_BASELINE`.

Текущий отказ нельзя автоматически переименовать в owner-created controlled
condition. До controlled degradation нужен доказанный healthy baseline либо
owner-backed matching replacement profile. Иначе последующий реальный
production outcome не будет законным controlled L7 evidence.

Поэтому CPS корректно сохраняет primary predecessor:

`EXTERNAL_OWNER_CONTROLLED_CERTIFICATION_SOURCE_BASELINE_REQUIRED`

и одновременно проецирует:

`CONTROLLED_TARGET_SELECTION_STATUS = NO_CURRENT_TARGET_CAPACITY_WITH_EXACT_OWNER_BOUNDARY`.

## Реальный consumer

Обычный production вызов:

`v7-service-matrix-refresh-all`

Результат:

- семь egress перепроверены;
- source `1`: `FAIL`, `0/14`;
- exact target: `OK`, `14/14`;
- passive event consumer: `PASS`;
- service-failure advisory consumer: `PASS`;
- OMP consumer: `PASS`;
- incident successor:
  `CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN`;
- bounded action: `STOP_SAFE_CURRENT_INCIDENT_NOT_ACTIONABLE`;
- action attempted: `false`;
- users moved: `0`.

Campaign target diagnostic был затем потреблён существующим
`tools/v7-truth-check --reconcile-active-standing-delegated-policy` owner и
атомарно записан в CPS/OMP.

## Проверки

- затронутые unit/integration проверки: `118` прошли до real-caller test;
- stale Polygon oracle с жёстким числом `62` заменён на смысловой invariant
  `affected == consumed > 0`;
- повторный real Polygon caller test: `PASS`, `331.823 s`;
- отдельная producer/consumer selective-map проверка: `PASS`;
- Permanent Polygon semantic campaign по фактическому change contract:
  `PASS`, coverage restored, forbidden effects absent;
- `git diff --check`: `PASS`.

Polygon не дал production или L7/L8 credit и не менял Runtime/Authority.

## Git и deploy

- implementation commit: `f568baacffb8ceb159e414fc1096b79470975eed`;
- residual-semantics commit: `a17463a432d01e5483d2cfaac302fbddfeecf674`;
- GitHub branch: `Updatesystem`;
- final deploy:
  `deploy-z8-14-Updatesystem-a17463a-20260729T155244`;
- deploy owner: `tools/v7-safe-deploy`;
- final changed production file:
  `tools/v7-users-autoswitch`;
- preceding bounded deploy changed only:
  `tools/v7_sync_lib.py`, `tools/v7-users-autoswitch`,
  `tools/v7-service-matrix-refresh-all`.

Ни один systemd unit не изменён и не включён.

## Forbidden effects

- Candidate created: `false`;
- Packet created: `false`;
- lease created: `false`;
- restore-barrier write: `false`;
- Runtime apply: `false`;
- routing mutation: `false`;
- user movement: `0`;
- rollback apply: `false`;
- Authority expansion: `false`;
- Production Maturity change: `false`.

## Exact re-entry

Программа должна автоматически re-enter через существующий Matrix -> OMP ->
CPS consumer при любом material fingerprint change.

Для source predecessor требуется:

`OWNER_VERIFIED_REACHABLE_REMOTE_PEER_WITH_MATCHING_KEY_MATERIAL_OR_REPLACEMENT_WORKING_PROFILE_FOR_THE_EXACT_APPROVED_SOURCE`

и затем fresh healthy Matrix baseline до owner-created controlled condition.

Для target predecessor требуется один из двух owner-backed результатов:

1. exact approved target стабильно проходит current/5m/1h floors и сохраняет
   stage capacity после reserve;
2. появляется controlled-eligible alternative, после чего exact-target
   Authority создаёт только narrow
   `REBIND_CONTROLLED_CAMPAIGN_TARGET` request.

Не требуется повторять Tier-48 capability certification, pool provisioning,
campaign approval или уже закрытые Polygon scenarios.
