# V7: availability-first certification ladder и Authority boundary

Дата: 2026-07-30  
Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Класс доказательства: engineering + production deploy/caller, без production outcome credit  
Итог безопасной части: `AVAILABILITY_FIRST_CERTIFICATION_LADDER_ENGINEERING_DEPLOYED_AND_AUTHORITY_REQUEST_CONSUMED`

## Результат

Существующие владельцы расширены без создания нового Planner, Runtime, Authority, registry, queue, watcher или truth source. Реализован certification-only availability-first контур с автоматической лестницей точных cohort stages:

`1 -> 2 -> 5 -> 10 -> 25 -> 48`

Каждая ступень означает точный общий размер cohort после возврата к controlled baseline, а не добавочное число пользователей. После успешного Outcome существующий Matrix consumer публикует и потребляет следующую ступень без отдельного операторского подтверждения.

Production action не выполнялся. Authority не расширена. Production Maturity не менялась.

## Discover -> Reuse -> Extend -> Implement

Повторно использованы:

- `admin_core/operator_execution.py` как существующий Authority/policy/audit owner;
- `tools/v7-users-autoswitch` как существующий Planner и admission owner;
- `tools/v7-governed-canary-dry-run-cycle` как существующий governed execution owner;
- `tools/v7-service-matrix-refresh-all` как существующий event-driven Matrix consumer;
- `tools/v7_sync_lib.py` как существующий CPS/OMP projection owner;
- текущие inventory, assignment, Matrix, quality, capacity, Candidate, Packet, lease, restore-barrier, Outcome, Replay и Learning owners.

Закрытый engineering gap: прежний controlled campaign был привязан к одному exact target и не мог безопасно использовать появляющиеся shared targets или target set с совокупной ёмкостью. Новый контракт сохраняет обычные admission floors, но допускает certification-only `HEALTHY`, `DEGRADED_USABLE` и `LAST_RESORT_USABLE` target classes с отдельными начальными пределами, свежей проверкой и реальным outcome-gated ростом.

## Реализованный contract

- action class: `bounded availability-first controlled failover`;
- target выбирается только свежим существующим Planner;
- source не может быть target;
- восемь owner-backed capacity axes и fingerprints;
- target-specific safe bound и детерминированное multi-target allocation;
- совокупная capacity обязана покрывать точный immutable cohort;
- двойной учёт capacity запрещён;
- один concurrent transaction;
- свежие Candidate, Packet или Packet set и lease;
- Packet reuse запрещён;
- restore barrier до apply;
- per-user, per-target, aggregate и ordinary-user verification;
- cohort circuit breaker;
- bounded subset rollback/redistribution/containment;
- controlled baseline reset между ступенями;
- обычные identities, assignments и routes неизменны;
- shared-target fault injection и restart запрещены;
- hard-limit, credential, external-resource и self-expansion запрещены.

## Проверки

- focused suites: `151 passed`;
- service-failure episode suite: `30 passed`;
- combined affected suite: `259 passed, 1 failed`;
- единственный failure `test_verified_active_standing_policy_replaces_stale_authority_request` воспроизведён без изменений на clean detached baseline `b52fc168` и классифицирован как существующий несвязанный fixture/report-pointer defect;
- Python 3.9 и 3.11 compilation: PASS;
- production Python 3.9 incompatibility `dict[...] | None`/`set[...] | None` обнаружена Polygon до production consumption и устранена переходом на `Optional[...]`;
- Permanent Polygon: `64/64` affected scenarios consumed, `affected_coverage_restored=true`;
- Polygon invariants: semantic differential, mutation strength, protocol/configuration lifecycle, bounded repair path, calibration owner, real scenario consumer и forbidden-effects checks — PASS;
- Polygon evidence не засчитано как L7/L8 или production outcome.

## Commit и deploy

- source commit: `936f84665df0179116de86cef28ec73a40f430bb`;
- branch: `Updatesystem`;
- deploy: `deploy-z8-14-Updatesystem-936f846-20260730T151649`;
- safe-deploy manifest: PASS;
- изменены только:
  - `admin_core/operator_execution.py`;
  - `tools/v7-users-autoswitch`;
  - `tools/v7-governed-canary-dry-run-cycle`;
  - `tools/v7-service-matrix-refresh-all`;
  - `tools/v7_sync_lib.py`;
- systemd units, production policy и остальные runtime owners не изменялись;
- postdeploy manifest: `changed=[]`, `blockers=[]`, `final_verdict=PASS`.

## Production non-test caller

Deployed `v7-users-autoswitch --controlled-source-topology-diagnostic` реально вызвал новый production consumer.

До Authority decision:

- `availability_admitted=false`;
- `availability_status=STANDING_DELEGATED_AVAILABILITY_FIRST_POLICY_REQUIRED`;
- `campaign_next_stage=1`;
- `campaign_completed=false`;
- status: `CONTROLLED_TOPOLOGY_AVAILABILITY_FIRST_CONTRACT_REQUIRED`;
- все forbidden effects: false;
- users moved: `0`.

Это подтверждает, что код задеплоен и реально потребляется, но не подменяет production cohort outcome.

## Единственный Authority request

Через существующий append-only Authority owner зарегистрирован ровно один новый запрос:

- request ID: `sdpauth_r1_0e376dd30710b4ed3ea7e804`;
- request hash: `0e376dd30710b4ed3ea7e804c5a18c6252bc1106d2a7812eae6bd4e3fe460a52`;
- policy scope hash: `23f0f936faa12a90153106f3638c731d2dd4e7990ea4411cf87fdc4bd7cac535`;
- created: `2026-07-30T08:26:59.966418+00:00`;
- expires: `2026-07-31T08:26:59.966418+00:00`;
- decision set: `APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY`, `DECLINE`;
- active program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`;
- profile: `SERVICE_FAILURE_WITH_CONTROLLED_CERTIFICATION_AVAILABILITY_FIRST_V2`;
- maximum users per availability-first transaction: `48`;
- maximum concurrent transactions: `1`;
- certification identities only;
- ordinary identity/assignment/route delta: `0`;
- request сам не одобряет target, stage, Candidate, Packet, lease, restore barrier или apply.

Регистрация дала:

- `authority_granted=false`;
- `policy_write=false`;
- `runtime_apply=false`;
- `routing_mutation=false`;
- `users_moved=0`.

Штатный production-status consumer прочитал pending request, а `tools/v7-truth-check --reconcile-active-standing-delegated-policy --json` атомарно проецировал его в CPS и OMP с `final_verdict=PASS`.

## Точный legal terminal

`ENGINEERING_AUTHORITY_STANDING_DELEGATED_AVAILABILITY_FIRST_POLICY_DECISION_REQUIRED`

Это единственная оставшаяся независимая граница. До точного hash-bound решения запрещены:

- выдача или запись нового standing policy;
- Candidate, Packet или lease;
- restore-barrier write;
- runtime apply;
- routing mutation;
- user movement;
- rollback apply;
- Authority expansion;
- Production Maturity change.

После точного approval существующий Authority owner атомарно активирует только immutable V2 envelope. Следующее обычное Matrix generation заново проверит inventory, allocation, capacity, health, freshness и все live gates. Успешные ступени затем продолжаются автоматически через существующий Matrix -> governed executor -> Outcome -> Replay -> Learning -> CPS/OMP цикл без новых подтверждений между `1/2/5/10/25/48`. Decline оставляет систему в точном `STOP_SAFE`.

## Post-approval continuation

Точный запрос одобрен оператором и потреблён существующим Authority owner:

- decision ID: `sdpdec_c326063ca46db99c61d0b699`;
- contract ID: `sdpc_285af5fc6f4de20415c3e5b1`;
- contract hash: `285af5fc6f4de20415c3e5b1d27a3c2f89d06db5a29af4a60bb88bdf26af2f4f`;
- issued: `2026-07-30T16:56:59.965252+00:00`;
- expires: `2026-08-29T16:56:59.965252+00:00`;
- profile: `SERVICE_FAILURE_WITH_CONTROLLED_CERTIFICATION_AVAILABILITY_FIRST_V2`;
- policy write: `true`, строго как результат независимого точного Authority decision;
- Candidate/Packet/lease: `false`;
- runtime apply/routing mutation/users moved: `false/false/0`;
- Production Maturity change: `false`.

Первый атомарный CPS/OMP consumer выявил existing-owner semantic-binding defect: новый Matrix-owned frontier `CONTINUE_AVAILABILITY_FIRST_CONTROLLED_PRODUCTION_STAGE_1` ещё не входил в общую safe/reachable frontier normalization. Неверный CPS не был записан.

Исправление:

- availability stages `1/2/5/10/25/48` добавлены в существующий controlled-certification safe frontier classifier;
- generic capability projection сохраняет этот executable frontier;
- continuation semantics нормализованы как `CONTINUE_PROGRAM_FRONTIER`;
- Matrix timer признан существующим durable consumer, а не отсутствующим wake;
- добавлен regression-тест exact stage-1 projection.

Проверки исправления:

- targeted semantic tests: `2 passed`;
- affected availability/service-failure suites: `244 passed`;
- atomic reconciliation suite: `47 passed, 1 legacy failure`;
- legacy failure `test_02_real_world_limit_with_stop_safe_projection_fails` отдельно воспроизведён на clean detached pre-fix commit `ef17b42d` и не вызван исправлением;
- fix commit: `b54759e3820fb34472eaf4f554780500fcd42d06`;
- safe deploy: `deploy-z8-14-Updatesystem-b54759e-20260731T002318`;
- deploy manifest changed runtime path: только `tools/v7_sync_lib.py`;
- повторная production reconciliation: `PASS`;
- текущий durable successor: `CONTINUE_AVAILABILITY_FIRST_CONTROLLED_PRODUCTION_STAGE_1`;
- существующий `v7-service-matrix-refresh.timer` активен и владеет следующим обычным generation.
