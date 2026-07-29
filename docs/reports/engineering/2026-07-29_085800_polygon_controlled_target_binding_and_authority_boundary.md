# V7: привязка Polygon controlled-target и точная Authority-граница

Дата: 2026-07-29
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`
Mission: `V7_SERVICE_FAILURE_T48_M8_CONTROLLED_POOL_RECONCILIATION`

## Итог

Устранён инженерный тупик `unhealthy exact controlled source -> no Planner-safe
target`. Новый Program, Planner, Runtime, registry, watcher, queue, scheduler
или evidence store не создавались.

Повторно использованы существующие owners:

- 48 уже созданных certification-only identities группы
  `t48-d27d985e237c` на source `1`;
- существующий `EXECUTION_ONLY` Polygon egress
  `amneziawg-exec-20260528-10-8-1-14`;
- `admin_core/operator_execution.py` как Authority/audit owner;
- `tools/v7-users-autoswitch` как Matrix/Planner owner;
- `tools/v7-governed-canary-dry-run-cycle` как существующий
  Candidate/Packet/lease/cohort consumer;
- `tools/v7_sync_lib.py` как CPS/OMP projection owner.

## Production discovery

- source `1`: 48 certification users, 0 ordinary users, Matrix `0/14`,
  `14` hard failures;
- Polygon target: 0 users, `14/14`, fresh handshake, role
  `EXECUTION_ONLY`, `execution_reserved=true`, `canary_reserved=true`,
  reservation owner `operator_execution_governance`;
- target остаётся `autoswitch_allowed=false`,
  `rebalance_allowed=false`, `production_assignment_allowed=false`;
- смешанный WireGuard source не использован: на нём находятся ordinary users;
- новый pool и новые identities не создавались.

## Реализованный producer-consumer link

```text
existing controlled failed source + existing 48-user certification pool
-> separate execution-only controlled-target projection
-> exact coordinated Authority request
-> exact approved-request Planner admission
-> existing M8/M9 Candidate/Packet/lease/cohort path
```

Обычный Planner по-прежнему отклоняет execution-only target. Исключение
включается только когда production audit подтверждает точный request ID/hash,
source/target, controlled-only contract и текущие isolation/health/capacity
gates.

Existing-pool consumer теперь умеет exact-once потребить
`REUSE_EXISTING_VALID_POOL` без создания или повторной классификации
identities.

## Проверка и deploy

- focused/full affected unit tests: `183 PASS`;
- truth-check tests: `27 PASS`;
- initial implementation commit:
  `aa110e0cdf0262d133eae64eac891de2d6da652f`;
- GitHub `Updatesystem`: совпал с local перед deploy;
- safe-deploy manifest: только
  `admin_core/operator_execution.py`,
  `tools/v7-users-autoswitch`,
  `tools/v7-governed-canary-dry-run-cycle`,
  `tools/v7_sync_lib.py`;
- deploy:
  `deploy-z8-14-Updatesystem-aa110e0-20260729T085443`;
- production non-test status caller подтвердил реальный Polygon target и
  сохранение ordinary-user запретов;
- routing mutation, Packet, lease, user movement, rollback apply, Authority
  expansion и Production Maturity change: `NONE`.

## Fresh exact request

- request ID:
  `cpsauth_r1_0b5151b3c3a33fd6ced157ab`;
- request hash:
  `0b5151b3c3a33fd6ced157ab7eb272357f41ac3f700a68864e917c1cfc6e7c7c`;
- expires:
  `2026-07-30T01:56:04.769524+00:00`;
- source: `1`;
- target: `amneziawg-exec-20260528-10-8-1-14`;
- pool strategy: `REUSE_EXISTING_VALID_POOL`;
- new identities: `0`;
- stages: `5 -> 10 -> 25 -> 48`;
- max concurrent transactions: `1`;
- status: `PENDING`.

Heartbeat реально потребил новый frontier и атомарно установил:

`ENGINEERING_AUTHORITY_CONTROLLED_CERTIFICATION_TARGET_REQUEST_READY`.

## Evidence separation и остаток

Polygon доказал и подготовил exact controlled opportunity, но не создавал
production Outcome. Поэтому:

- M8 ещё не завершена;
- M9 stages `5/10/25/48` ещё не выполнены;
- controlled-production proven maximum остаётся `0`;
- ordinary Runtime maximum остаётся `4`;
- M10 и ordinary Runtime verdict ещё не исполнялись.

Текущий legal terminal:

`ENGINEERING_AUTHORITY_CONTROLLED_CERTIFICATION_TARGET_REQUEST_READY`.

Re-entry:

точный unexpired request получает одно owner-backed
`APPROVE_CONTROLLED_CERTIFICATION_SUBSTRATE_AND_CAMPAIGN` либо `DECLINE`;
после approval существующий M8 consumer повторно проверяет target health,
capacity, isolation и все live gates и продолжает без нового Program.
