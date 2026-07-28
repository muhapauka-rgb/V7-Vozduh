# Engineering Report: T48-M8 Authority consumer и точный legal boundary

Дата: `2026-07-28`

Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

Mission: `V7_SERVICE_FAILURE_T48_M8_CONTROLLED_POOL_RECONCILIATION`

Итог: `ENGINEERING_COMPLETE_AT_EXACT_INDEPENDENT_AUTHORITY_BOUNDARY`

## 1. Исходное состояние

В production уже существовали и были повторно использованы:

- действующий standing delegated policy contract `sdpc_36bb4d9cc58ceac13287b973`;
- Authority-approved controlled-certification ceiling `48`;
- ordinary-production Runtime ceiling `4`;
- существующие `operator_execution`, autoswitch, audit, CPS и OMP owners;
- controlled-certification pool: четыре enabled certification identities всего, максимум три на одном active controlled source;
- exact source `wireguard-1779454504-c43409`;
- зарегистрированный request `cpsauth_r1_7b3cf7eab9af58a7a3839aaa`.

Новые Authority owner, registry, queue, watcher, planner, policy owner, execution path или evidence owner не создавались.

## 2. Найденный разрыв

Request producer и request validator уже существовали, но полный consumer lifecycle отсутствовал:

- не было append-only exact APPROVE/DECLINE consumer с actor provenance;
- не было межпроцессной exact-once защиты решения;
- не было fail-closed проверки expiry/hash/subscope;
- не было expiry-only semantic supersession;
- production status не отдавал решение следующему CPS/OMP consumer;
- detailed projection знала точный pending request, но top-level CPS frontier сворачивался обратно в общий `T48_M8_CONTROLLED_POOL_RECONCILIATION`, создавая риск повторного request/reconciliation loop;
- controlled Tier-48 и ordinary Tier-4 могли быть сведены старым scalar consumer в одну ось.

Root cause: `EXISTING_OWNER_PRODUCER_CONSUMER_AND_PROJECTION_ORDERING_GAP`.

## 3. Реализация через существующих owners

`admin_core/operator_execution.py` расширен внутри существующего Authority/audit owner:

- exact `APPROVE_CONTROLLED_CERTIFICATION_SUBSTRATE_AND_CAMPAIGN` / `DECLINE`;
- обязательный actor provenance;
- обязательные четыре coordinated subscopes;
- request/hash/freshness/owner/scope validation;
- append-only decision record;
- interprocess lock и duplicate/conflict suppression;
- expiry-only replacement с durable supersession link и неизменным semantic fingerprint;
- нулевые policy, registry, identity, routing, Runtime и user effects.

`tools/v7-users-autoswitch` расширен только как существующий read-only status consumer.

`tools/v7_sync_lib.py`:

- потребляет точный Authority status;
- разделяет controlled-certification и ordinary-production Runtime/evidence axes;
- сохраняет legacy scalar на ordinary-production ceiling;
- публикует exact pending/approved/declined/expired frontier;
- после approval допускает только существующий incremental M8 substrate successor;
- запрещает возврат точного pending request в generic pool loop.

OMP обновлён до `4.61`; CPS и оба OMP current-state pointer синхронизированы с точным legal terminal.

## 4. Проверки

Проверены:

- exact APPROVE записывается один раз;
- два concurrent consumers дают ровно одну decision record;
- exact duplicate возвращает `ALREADY_RECORDED_EXACT`;
- conflicting duplicate отклоняется;
- hash mismatch отклоняется;
- expired request отклоняется;
- неполный approval subscope отклоняется;
- отсутствующий actor отклоняется;
- DECLINE не допускает subscopes и не создаёт эффектов;
- expiry replacement возможен только после expiry, явно supersede’ит старый request и сохраняет semantic fingerprint;
- pending request становится единственным точным top-level CPS/OMP frontier;
- approved request становится безопасным incremental M8 successor;
- ordinary Runtime остаётся Tier-4 при controlled-certification ceiling Tier-48;
- CPS/OMP consistency и deterministic projection сохраняются.

Финальный affected suite: `359 tests`, `PASS`.

## 5. Git, deploy и production consumer

Коммиты:

- `7aa71ac7974ed503d8aef09e056fd16e806603a2` — Authority decision consumer, status projection, tests и Program V2.2;
- `a6141bf55259e513c53768c0a419f6ef7a3b4848` — exact top-level Authority frontier и CPS reconciliation.

Оба коммита отправлены в `origin/Updatesystem`.

Deploy выполнен только через `tools/v7-safe-deploy`.

Deploy `deploy-z8-14-Updatesystem-7aa71ac-20260728T205439`:

- `admin_core/operator_execution.py`;
- `tools/v7-users-autoswitch`;
- `tools/v7_sync_lib.py`.

Deploy `deploy-z8-14-Updatesystem-a6141bf-20260728T210241`:

- `tools/v7_sync_lib.py`.

Оба manifest: `PASS`, blockers `NONE`.

Production non-test caller:

```text
/usr/local/bin/v7-users-autoswitch --standing-delegated-policy-status
```

Production consumer result:

- policy status `PASS`;
- Authority-approved maximum `48`;
- controlled-certification Runtime maximum `48`;
- ordinary-production Runtime maximum `4`;
- controlled-production proven maximum `0`;
- ordinary-production proven maximum `4`;
- pool maximum on one source `3`;
- exact request status `PENDING`.

Source-side existing bridge:

```text
tools/v7-truth-check --reconcile-active-standing-delegated-policy --json
```

Результат: production status потреблён, CPS обновлён атомарно, post-write reread `PASS`, exact next action опубликован без external wake.

Local/production SHA-256 совпадают:

- `tools/v7_sync_lib.py`: `971bcb833dd1f218ff727aeef53ff7d420ee7e58b9ef92522738570ba4fe5396`;
- `tools/v7-users-autoswitch`: `350c340eba73ab92fe146c590e9b44c39420fe7831d0209e426f039707aae6d9`;
- `admin_core/operator_execution.py`: `84cdc588a0d55d9bed284d12dc8b785f4a274d156f7562c990162668bd1913c9`.

## 6. Authority decision и production effects

Текущее owner-backed decision evidence:

- request ID: `cpsauth_r1_7b3cf7eab9af58a7a3839aaa`;
- request hash: `7b3cf7eab9af58a7a3839aaa8a435cf3b2599c9794e5e6a68b6b585e29d7b6ef`;
- expires at: `2026-07-29T11:51:40.460318+00:00`;
- status: `PENDING`;
- decision ID: отсутствует;
- actor: отсутствует.

Поэтому substrate provisioning и campaign execution не начинались.

Подтверждённые запрещённые эффекты:

- policy write: `0`;
- contract issuance: `0`;
- identity/registry/assignment write: `0`;
- Candidate/Packet/lease creation: `0`;
- controlled condition: `0`;
- Runtime apply: `0`;
- routing mutation: `0`;
- user movement: `0`;
- rollback apply: `0`;
- Authority expansion: `0`;
- Production Maturity change: `0`;
- production evidence credit: `0`.

## 7. Точный legal terminal

```text
ENGINEERING_AUTHORITY_CONTROLLED_CERTIFICATION_SUBSTRATE_REQUEST_READY
```

Это не пассивная инженерная остановка и не повторный pool request. Вся безопасная инженерная часть текущего prompt завершена и задеплоена. Единственный оставшийся blocker — независимое решение существующего Authority owner по уже зарегистрированному exact request.

Re-entry:

```text
exact append-only APPROVE
-> existing production status consumer
-> atomic CPS/OMP residual
-> CONTROLLED_CERTIFICATION_SUBSTRATE_APPROVED_INCREMENTAL_POOL_REQUIRED
-> only the exact Tier-5 identity delta through existing owners

or

exact append-only DECLINE
-> no production effects
-> exact declined residual
```

Expiry не создаёт второй semantic request: допускается только linked expiry replacement с тем же semantic fingerprint и без одновременного второго active request.
