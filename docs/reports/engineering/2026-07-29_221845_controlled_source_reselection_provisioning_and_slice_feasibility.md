# Engineering Report: controlled-source reselection, provisioning and slice feasibility

Дата production verification: `2026-07-29T15:18:45Z`

Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

Mission:
`CONTROLLED_SOURCE_RESELECTION_PROVISIONING_AND_SLICE_FEASIBILITY_V1`

## Итог

Mission доведена до законной pre-Authority границы:

`CONTROLLED_SOURCE_NON_WAITING_EXIT_PATH_PRODUCTION_PREFLIGHT_READY`

Система больше не обязана ждать восстановления source `1`. Она каждый раз
строит компактную derived-карту всех текущих egress и выбирает минимальный
безопасный вариант из:

1. rebind на существующий пустой egress;
2. provisioning через существующий egress-draft lifecycle;
3. изолированный slice на занятом egress.

Новый Program, Planner, Runtime, registry, queue, watcher, scheduler, Authority
owner, evidence store или truth source не создан.

Production trial не выполнялся: независимое Engineering Authority решение
ещё не записано. Candidate, Packet, lease, restore barrier, routing mutation
и user movement отсутствуют.

## Discover -> Reuse -> Extend -> Implement

Переиспользованы существующие owners:

- `egress.registry` и `users.registry`;
- Service Matrix, diagnose, quality и capacity;
- per-user route/policy-table truth;
- `admin/v7-admin-api` egress-draft lifecycle;
- `tools/v7-egress-set-state`;
- `admin_core/operator_execution.py` append-only Authority audit;
- `tools/v7-users-autoswitch`;
- `tools/v7_sync_lib.py`;
- CPS и OMP.

Закрыты только доказанные gaps:

- не было общей compact capability map трёх вариантов;
- не было CAS-bound reserve/release для пустого controlled source;
- не было exact short-lived Authority request для source topology;
- CPS мог продолжать показывать старый source-recovery blocker;
- re-entry condition был статически привязан к `REBIND`;
- material Matrix/registry change мог оставить старый pending request и
  заблокировать fresh request исключением.

Последний gap закрыт внутри существующего append-only Authority audit:
material preflight change атомарно записывает
`MATERIAL_PREFLIGHT_CHANGED`, связывает stale и replacement request hashes и
навсегда запрещает решение по stale request. Это не Authority decision и не
topology effect. Идентичный semantic preflight по-прежнему переиспользует
активный request без новой записи.

## Production capability map

Текущая карта имеет fingerprint:

`9a8dee9051b7886f96bc4ca18b5fb910193e0055a7159216b77b260db1aaa52a`

| Egress | Live состояние | Ёмкость после reserve | Результат |
|---|---|---:|---|
| `1` | `0/14`, unstable, 48 certification users | `0` | current failed source; не target |
| `amneziawg-exec-20260528-10-8-1-14` | healthy, empty, stability below floor | `9` | fail-closed |
| `awg0` | healthy, 13 ordinary users, unstable | `129` | shared failure domain; fail-closed |
| `awg3` | healthy, 11 ordinary users, unstable | `131` | shared failure domain; fail-closed |
| `openvpn-1779388847-d2ad7c` | healthy, 2 ordinary + 1 certification | `0` | occupied and no capacity |
| `vless` | healthy, stable, empty | `142` | selected safe existing egress |
| `wireguard-1779454504-c43409` | healthy, 46 ordinary + 3 certification | `0` | occupied and no capacity |

### Option 1 — existing empty egress rebind

`PASS_WITH_ENGINEERING_AUTHORITY_BOUNDARY`

Selected resource: `vless`.

Доказано:

- healthy baseline: `true`;
- stability floor: `PASS`;
- ordinary identities: `0`;
- certification identities: `0`;
- free capacity after reserve: `142`;
- full 48-identity capacity: `true`;
- independently controllable whole-egress failure boundary: `true`;
- reversible empty-source reservation owner: `READY`.

### Option 2 — existing dedicated-source draft

`SAFE_FALLBACK_NOT_CURRENTLY_PREFERRED`

Existing ready draft:

`1-1779291887-55965c`

Он прошёл preflight/runtime/quarantine и поддерживает one-identity trial, но
его hard capacity равна `2`. После появления пригодного `vless` этот вариант
уступает Option 1 по implementation scope и campaign capacity.

### Option 3 — isolated slice

`UNSAFE_BY_PROVEN_INVARIANT`

Причины:

- whole-egress failure затрагивает ordinary users;
- отдельная policy table не изолирует interface/peer failure;
- ни один существующий owner не доказал независимый slice failure/restore.

Эквивалентный безопасный путь маршрутизируется в dedicated-source Option 2.

## Доказанная динамическая переоценка

В `2026-07-29T15:03:05Z` fresh production truth ещё не допускала `vless`, и
алгоритм выбрал Option 2 с draft `1-1779291887-55965c`.

После новой Matrix generation `vless` стал healthy/stable/empty. Повторная
диагностика автоматически выбрала Option 1. Старый request:

- request:
  `cstopauth_r1_dcaebdb7ae4ec2a0bf128149`;
- hash:
  `dcaebdb7ae4ec2a0bf1281490710253e509fbc0c6b4fb52224691d097101fdd8`;
- invalidation:
  `cstopinv_29a74ff7213c7ceb5bfae587`;
- reason: `MATERIAL_PREFLIGHT_CHANGED`.

Это production-доказательство, что система не фиксируется на одном канале:
она повторно читает все owner-backed каналы и меняет рекомендацию при
материальном изменении health/stability/capacity/isolation.

## Fresh exact Authority package

- request ID:
  `cstopauth_r1_473a60eb2551700399accf5f`;
- request hash:
  `473a60eb2551700399accf5f357f5c5c4353b2a5045967d511a854d582e5ff52`;
- created:
  `2026-07-29T15:17:51.877580+00:00`;
- expires:
  `2026-07-30T15:17:51.877580+00:00`;
- exact action:
  `REBIND_CONTROLLED_CERTIFICATION_SOURCE`;
- legal decisions:
  `APPROVE_REBIND_CONTROLLED_CERTIFICATION_SOURCE`, `DECLINE`;
- source: `1`;
- target: `vless`;
- certification identity: `10.7.0.100`;
- max users: `1`;
- max concurrent transactions: `1`;
- manifest hash:
  `f86df7db11f56965cba37c3f68410f86be387f9829eca64447f04f878519c945`;
- expected ordinary assignment delta: `NONE`;
- expected ordinary route delta: `NONE`.

Первый production caller вернул
`REGISTERED_AFTER_STALE_PREFLIGHT_INVALIDATION`. Повторный caller вернул
`ALREADY_REGISTERED_SEMANTIC_ACTIVE`, `audit_write=false`, тот же ID/hash.

CPS/OMP consumer записал:

`ENGINEERING_AUTHORITY_REBIND_CONTROLLED_CERTIFICATION_SOURCE_REQUIRED`

и exact re-entry:

`one exact independent REBIND_CONTROLLED_CERTIFICATION_SOURCE or DECLINE decision ...`

## Проверки

- первоначальная affected implementation campaign: `139 PASS`;
- truth/canary affected suite: `93 PASS`;
- финальная service-failure + egress lifecycle suite: `69 PASS`,
  `118.086 s`;
- targeted stale-preflight/duplicate tests: `3 PASS`;
- dynamic CPS action regression: `PASS`;
- production diagnostic caller: `PASS`;
- production request registration caller: `PASS`;
- повторный idempotent caller: `PASS`;
- `tools/v7-truth-check --all --json`:
  `PASS`, `FULLY_ALIGNED`;
- `tools/v7-convergence-status --json`:
  `PASS`, `ALIGNED`;
- local/GitHub/production commit до documentation closure:
  `394d0aecadfeb100fb45dfa5471e53dc9bda9cc2`;
- runtime deploy:
  `deploy-z8-14-Updatesystem-394d0ae-20260729T221721`.

Предупреждение truth относится только к сохранённым пользовательским
documentation-only изменениям; runtime blocker отсутствует.

## Git и safe deploy

- main implementation:
  `3605e8758a6c7dc0bab4fa763493afe14f0fd0a9`;
- dynamic CPS re-entry fix:
  `c02a2d8427adaba026f38c8b883ebe2c5ed2d059`;
- stale-preflight supersession:
  `394d0aecadfeb100fb45dfa5471e53dc9bda9cc2`;
- deploys:
  `deploy-z8-14-Updatesystem-3605e87-20260729T220139`,
  `deploy-z8-14-Updatesystem-c02a2d8-20260729T221023`,
  `deploy-z8-14-Updatesystem-394d0ae-20260729T221721`.

Каждый runtime manifest содержал только принадлежащие Mission файлы. Daemon
restart/enablement отсутствовал.

## Forbidden effects

- policy write: `false`;
- identity creation: `false`;
- assignment change: `false`;
- Candidate/Packet/lease creation: `false`;
- restore-barrier write: `false`;
- Runtime apply: `false`;
- routing mutation: `false`;
- user movement: `0`;
- rollback apply: `false`;
- Authority expansion: `false`;
- Production Maturity change: `false`;
- controlled production credit: `false`;
- Natural L8 credit: `false`.

## Capability и Production Maturity

Capability progress:

`CONTROLLED_SOURCE_NON_WAITING_EXIT_PATH_PRODUCTION_PREFLIGHT_READY`

Production Maturity: `UNCHANGED`.

Tier-48 engineering capability и campaign approval не повторялись и не
расширялись.

## Exact next

Текущий законный terminal:

`AUTHORITY_INPUT_REQUIRED:REBIND_CONTROLLED_CERTIFICATION_SOURCE`

На `APPROVE_REBIND_CONTROLLED_CERTIFICATION_SOURCE` существующий consumer
обязан заново проверить manifest/health/capacity/empty-source CAS и перейти
только к fresh Candidate/Packet/lease/restore-barrier preflight. Любая
production mutation остаётся за отдельной packet-bound Operational Authority.

На `DECLINE` тот же derived map исключает exact `vless` для decision lineage и
переоценивает Option 2/3; возврат к ожиданию source `1` запрещён, пока остаётся
другая безопасная owner-backed возможность.

Post-trial terminal
`CONTROLLED_SOURCE_NON_WAITING_EXIT_PATH_RUNTIME_PROVEN` не заявляется до
реальной independently authorized one-identity trial, verification,
rollback/no-rollback, Outcome, Replay, Learning и CPS/OMP consumption.
