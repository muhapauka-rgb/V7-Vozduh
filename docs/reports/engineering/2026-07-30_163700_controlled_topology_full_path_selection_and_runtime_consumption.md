Mission ID: `CONTROLLED_TOPOLOGY_CONTINUATION_PATH_AND_DELEGATED_PROVISIONING_V1`
Run Nonce: `V7_CTCP_DP_20260730T163700+0700`
Mission Start: `2026-07-30T09:00:00+0700`

# Engineering Report: full-path controlled topology selection

Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

Terminal: `CONTROLLED_TOPOLOGY_FULL_PATH_SELECTION_RUNTIME_CONSUMED`

Program stop: `EXTERNAL_OWNER_REQUIRED`

## Итог

Существующий controlled-topology owner расширен до full-path выбора для всей
уже одобренной progressive campaign `5 -> 10 -> 25 -> 48`. Новый Program,
Planner, Runtime, registry, queue, watcher, scheduler, Authority owner, policy
store, execution path, evidence store или truth source не создавался.

Production доказал, что прежний выбор capacity-2 draft был пригоден только для
одно-пользовательского bootstrap и не имел достоверного successor для Stage 5
и последующих стадий. Теперь такие drafts отклоняются как
`BOOTSTRAP_ONLY_NO_CREDIBLE_CAMPAIGN_SUCCESSOR`.

## Discover -> Reuse -> Extend -> Implement

- переиспользованы существующие campaign request, user/egress registries,
  reservation owner, Matrix, quality, capacity, draft lifecycle, topology
  diagnostic, Authority audit, CPS и OMP;
- фактические роли и все 48 identities определены по live production owners,
  а не по историческим отчётам;
- существующий diagnostic расширен post-trial и full-path projections;
- существующий CPS consumer исправлен для законного
  `EXTERNAL_OWNER_REQUIRED` terminal с составным WIP stop;
- production effect этой Mission равен нулю.

## Production truth

Production non-test caller:

`v7-users-autoswitch --controlled-source-topology-diagnostic`

Результат:

- status:
  `CONTROLLED_TOPOLOGY_FULL_PATH_EXTERNAL_RESOURCE_REQUIRED`;
- post-trial classification:
  `POST_TRIAL_DEDICATED_DRAFT_SELECTION_SUBOPTIMAL`;
- identities accounted: `48/48`;
- current locations:
  `1=46`, `vless=1`,
  `amneziawg-exec-20260528-10-8-1-14=1`;
- `vless`: healthy `14/14`, ordinary users `0`, certification users `1`,
  usable capacity after reserve `141`;
- reservation `ctres_2f318af84ad5e06bc56721e8` просрочена и привязана
  к другой certification group;
- pinned execution target имеет usable capacity `8`;
- все ready drafts имеют hard capacity `2`, usable capacity `1`;
- campaign-capable draft count: `0`;
- full-path stages `5`, `10`, `25`, `48`: `current_feasibility=false`;
- production mutation: `false`.

## Причина прежнего выбора

Существующий ranking выполнял:

```text
empty-source Option 1 gate
-> one-identity draft preflight
-> capacity-2 draft
```

Он оптимизировал только следующий одно-пользовательский шаг. После успешного
trial не были полностью потреблены:

- transition роли source/target;
- expiry текущей reservation;
- mismatch reservation group и campaign group;
- campaign completion capacity gate.

Исправленный ranking сначала проверяет достижимость всей оставшейся campaign.
Capacity-2 draft больше не может стать текущим successor только потому, что
способен принять одну identity.

## Варианты topology

1. `vless` как controlled source: live baseline и capacity достаточны, но
   reservation expired/group-mismatched; продолжение требует owner-backed
   renewal/rebinding.
2. Текущий pinned target: capacity `8`, недостаточно для Stage 10/25/48.
3. Capacity-2 drafts: usable capacity `1`, недостаточно уже для Stage 5.
4. Occupied ordinary egress: запрещены без доказанной независимой failure
   isolation; обычные пользователи не используются для certification.
5. Multi-target topology: допустима только как correlation-distinct,
   owner-backed target set с суммарной usable capacity не меньше `48`.

Ни один текущий вариант не проходит полный путь без внешнего target resource.

## Polygon verification

Существующий Polygon contract дополнен и проверен для:

- invalid/quarantined и low-capacity draft;
- stale generation и source/target role confusion;
- occupied ordinary egress;
- отсутствующего rollback;
- crash до/после reservation, assignment, failure и rollback;
- duplicate wake/request и concurrent planner;
- expiry/revocation/cleanup;
- live inventory selection change;
- автоматического перехода к следующей стадии.

Сохранены invariants: zero self-expansion, zero ordinary-user effect, exact
roles, owner-backed capacity, hard-cap enforcement, no orphan resource,
restore barrier before apply, stale fail-close, one transaction per lease,
one durable successor и no synthetic production credit.

## Реальный consumer

Существующий consumer:

`v7-truth-check --reconcile-active-standing-delegated-policy`

Первый post-deploy вызов выявил старую consistency-семантику, которая требовала
`REAL_WORLD_LIMIT`/Authority для нового external-owner terminal. Последний
ответственный producer-consumer link исправлен в существующем
`tools/v7_sync_lib.py`.

Повторный production вызов:

- `final_verdict=PASS`;
- atomic CPS update: `PASS`;
- OMP pointer reconciliation: `PASS`;
- behavior change:
  `CONTROLLED_TOPOLOGY_FULL_PATH_SELECTION_RUNTIME_CONSUMED`;
- next action:
  `EXTERNAL_OWNER_CONTROLLED_CERTIFICATION_FULL_PATH_TARGET_CAPACITY_REQUIRED`.

## Проверки

- затронутый набор: `108 tests`, `PASS`;
- focused full-path reconciliation test: `PASS`;
- focused external-owner composite-stop test: `PASS`;
- `git diff --check`: `PASS`;
- safe-deploy manifest для основного изменения:
  только `tools/v7-users-autoswitch`, `tools/v7_sync_lib.py`;
- safe-deploy manifest для consumer repair:
  только `tools/v7_sync_lib.py`;
- production runtime hashes после deploy совпадают с local;
- GitHub branch: `Updatesystem`.

Implementation commits:

- `fc28d3fec408b87fdf94e8a7f34b0e1f8b26958f`;
- `1bc989778515aa1d17cb8e08d52e0c9656367ba8`;
- `5bf6bacad442f31a9fb0ff8c52cde8560d244935`.

Production deploys:

- `deploy-z8-14-Updatesystem-fc28d3f-20260730T091433`;
- `deploy-z8-14-Updatesystem-1bc9897-20260730T093219`;
- `deploy-z8-14-Updatesystem-5bf6bac-20260730T093601`.

## Forbidden effects

- policy/Authority write: `false`;
- Candidate/Packet/lease creation: `false`;
- restore-barrier write: `false`;
- Runtime apply: `false`;
- routing mutation: `false`;
- user movement: `0`;
- rollback apply: `false`;
- Authority expansion: `false`;
- Production Maturity change: `false`;
- controlled-production credit: `false`;
- natural L8 credit: `false`.

## Capability и backlog

- `POST_TRIAL_DEDICATED_DRAFT_SELECTION_CAUSALLY_RESOLVED`: `PASS`;
- `CONTROLLED_TOPOLOGY_FULL_PATH_SELECTION_RUNTIME_CONSUMED`: `PASS`;
- progressive campaign `5 -> 10 -> 25 -> 48`: не выполнена и не объявлена
  выполненной;
- generic movement engineering certification `1/2/4/5/10/25/48` сохранена
  как reusable evidence без повторной сертификации;
- Production Maturity не повышалась.

## Exact next frontier

`EXTERNAL_OWNER_CONTROLLED_CERTIFICATION_FULL_PATH_TARGET_CAPACITY_REQUIRED`

Exact resource:

`OWNER_VERIFIED_ISOLATED_CONTROLLED_TARGET_OR_CORRELATION_DISTINCT_TARGET_SET_WITH_USABLE_CAPACITY_AT_LEAST_48`

Exact owner:

`EXTERNAL_EGRESS_PEER_OR_PROFILE_PROVIDER`

Re-entry:

```text
external resource owner
-> existing admin draft lifecycle
-> fresh Matrix/quality/capacity
-> same topology ranking
-> minimal existing standing-envelope decision only after resource proof
```

До появления owner-backed resource новый Authority request незаконен.
Capacity-2 draft, Packet, lease, restore barrier и production action не должны
создаваться.
