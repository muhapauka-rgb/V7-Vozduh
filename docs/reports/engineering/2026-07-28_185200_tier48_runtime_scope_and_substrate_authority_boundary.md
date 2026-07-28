# V7 Engineering Report — Tier-48 runtime scope и controlled-substrate Authority boundary

Дата: 2026-07-28  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Mission/frontier: `V7_SERVICE_FAILURE_T48_M8_CONTROLLED_POOL_RECONCILIATION`  
Метод: `Discover -> Reuse -> Extend -> Implement`

## Итог

Исправлена опасная семантическая связь, при которой активный standing contract с `max_users=48` мог быть прочитан generic emergency-failover consumer как разрешение на cohort до 48 обычных production-пользователей.

После production deploy оси разделены:

- Authority-approved maximum: `48`;
- controlled-certification Runtime maximum: `48`;
- ordinary-production Runtime maximum: `4`;
- controlled-production proven maximum: `0`;
- ordinary-production proven maximum: `4`.

Tier-48 теперь выбирается только при одновременном доказательстве exact controlled source condition и certification-only классификации каждого пользователя exact cohort. В остальных production-контекстах применяется ordinary ceiling `4`.

## Discovery и reuse

Проверены существующие owners и связи, а не только имена:

- standing delegated policy и append-only Authority audit;
- `tools/v7-users-autoswitch` Planner/Matrix consumer;
- `admin_core/operator_execution.py` Authority owner;
- Controlled Production Certification Program;
- production provisioning entrypoints `v7-user-create`, `v7-user-create-from-ipam`, `v7-user-switch`, `v7-egress-set-state`;
- текущий controlled-certification pool.

Owner-backed pool projection:

- enabled certification users: `4`;
- active controlled sources: `1`;
- maximum users on one active controlled source: `3`;
- pool fingerprint: `fabe218d853bc10fc6900654517bb88939e170f8f5b08fb61acb520d6d975431`.

Существующее provisioning создаёт обычные production WireGuard identities. Атомарного разрешённого lifecycle «создать certification-only identity -> классифицировать -> назначить controlled source -> материализовать controlled condition -> выполнить progressive campaign» без независимого Authority decision не найдено. Поэтому автоматическое расширение pool было бы Authority bypass.

## Изменение

Production implementation commit:

`857c9dcf158b1d1867fbefbe20052b8ad6377813`

Изменены существующие owners:

- `tools/v7-users-autoswitch`;
- `admin_core/operator_execution.py`.

Добавлено:

1. Machine-readable разделение controlled и ordinary Runtime ceilings.
2. Fail-closed controlled-context validation.
3. Ordinary Runtime cap `4`.
4. Existing-owner builder/validator/registration для одного coordinated Tier-48 Engineering Authority request.
5. Production read-only entrypoint `--prepare-controlled-certification-substrate-authority-request`.
6. Независимые non-transitive subscopes:
   - identity provisioning;
   - certification classification/assignment;
   - controlled source condition;
   - progressive campaign `5 -> 10 -> 25 -> 48`.
7. Межстадийный reset/re-arm law и запрет implicit cross-grant.
8. Program V2.1: dual-axis law, coordinated Authority envelope, ordinary-runtime verdicts и no-progress law.

Standing policy и уже записанный Authority audit не переписывались. Contract не расширялся.

## Проверки

Focused/full affected test set:

`277 tests`, результат `PASS`.

Дополнительно:

- Python compile: `PASS`;
- safe-deploy manifest: `PASS`, blockers `[]`;
- manifest changed production files: только `admin_core/operator_execution.py` и `tools/v7-users-autoswitch`;
- production deploy: `deploy-z8-14-Updatesystem-857c9dc-20260728T185041`;
- production non-test caller `v7-users-autoswitch --standing-delegated-policy-status --pretty`: `PASS`;
- local/production implementation fingerprints совпадают:
  - `admin_core/operator_execution.py`: `c8a0ce69af28058b246dbbfcc84d2984f87fc5ef9da36b89c4a31ea241c1295b`;
  - `tools/v7-users-autoswitch`: `144d590302ee6bb9df2bc3660784a09438a14d5164a3d03fa727b5fd2e4aa23b`.

## Exact Authority package

Existing Authority owner зарегистрировал в `/opt/v7/audit/operator-execution-audit.jsonl` один request:

- request ID: `cpsauth_r1_7b3cf7eab9af58a7a3839aaa`;
- request hash: `7b3cf7eab9af58a7a3839aaa8a435cf3b2599c9794e5e6a68b6b585e29d7b6ef`;
- created: `2026-07-28T11:51:40.460318+00:00`;
- expires: `2026-07-29T11:51:40.460318+00:00`;
- decision set:
  - `APPROVE_CONTROLLED_CERTIFICATION_SUBSTRATE_AND_CAMPAIGN`;
  - `DECLINE`;
- target: до `48` certification identities;
- source: `wireguard-1779454504-c43409`;
- stages: `5`, `10`, `25`, `48`;
- max concurrent transactions: `1`;
- registration: `REGISTERED`.

Это один coordinated decision на весь campaign, а не четыре повторных approval. Одобрение не является исполнением: каждый stage остаётся у существующего owner, проходит fresh gates и не передаёт Authority следующему stage неявно.

## Forbidden effects

Во время reconciliation/request generation:

- policy write: `FALSE`;
- certification registry write: `FALSE`;
- identity creation: `FALSE`;
- assignment change: `FALSE`;
- controlled condition: `FALSE`;
- Candidate/Packet/lease creation: `FALSE`;
- routing mutation: `0`;
- user movement: `0`;
- rollback apply: `0`;
- Authority expansion: `FALSE`;
- Production Maturity change: `FALSE`.

Единственная запись — append-only request registration в существующем Authority audit owner.

## Legal terminal и re-entry

Текущий terminal:

`ENGINEERING_AUTHORITY_CONTROLLED_CERTIFICATION_SUBSTRATE_REQUEST_READY`

Re-entry:

1. Независимый owner-backed decision по exact unexpired request.
2. При `DECLINE` сохраняется точный residual без production effects.
3. При `APPROVE_CONTROLLED_CERTIFICATION_SUBSTRATE_AND_CAMPAIGN` существующие owners последовательно выполняют только явно разрешённые substrate stages.
4. После появления не менее пяти certification-only users на одном active controlled source автоматически re-enter существующий T48-M8 consumer.
5. Campaign идёт `5 -> reset/re-arm -> 10 -> reset/re-arm -> 25 -> reset/re-arm -> 48`, с fresh Candidate/Packet/lease, capacity, verification, containment и circuit breaker на каждом stage.

Программа не объявлена завершённой. Controlled Tier-48 production evidence не создано и не засчитано.
