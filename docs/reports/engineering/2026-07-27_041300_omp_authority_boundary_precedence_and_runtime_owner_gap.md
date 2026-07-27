# OMP: приоритет Authority boundary и runtime-owner gap

Дата: `2026-07-27`

Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

## Что исправлено

Обнаружен дефект порядка в существующем `Continue OMP`: при уже открытой
`ENGINEERING_AUTHORITY` границе он мог выбрать независимый Polygon engineering
successor и заменить текущую CPS-проекцию. Это не затронуло production Runtime,
маршрутизацию, пользователей, Packet, lease, restore barrier или rollback, но
нарушало causal ownership CPS.

Исправление в существующих `tools/v7_sync_lib.py` и `tools/v7-truth-check`:

- любой `ENGINEERING_AUTHORITY`, `OPERATIONAL_AUTHORITY` или `REAL_WORLD_LIMIT`
  с `EXTERNAL_INPUT_REQUIRED=TRUE` теперь предшествует всем automatic successors;
- вызов возвращает легальный no-op `EXTERNAL_BOUNDARY_PREEMPTS_AUTOMATION`;
- CPS восстанавливается только через существующий atomic CPS owner;
- binary-only production вызов без source CPS больше не выдаёт traceback, а
  возвращает `BINARY_ONLY_SOURCE_CPS_UNAVAILABLE` с нулевыми effects.

## Доказательства

- focused tests: `25 PASS`;
- source-CPS caller: `PASS`,
  `ENGINEERING_AUTHORITY_EXTERNAL_BOUNDARY_PRESERVED`,
  `internal_iteration_count=0`;
- actual deploy: `deploy-z8-14-Updatesystem-7651001-20260727T111227`;
- production caller: structured `STOP_SAFE / BINARY_ONLY_SOURCE_CPS_UNAVAILABLE`,
  без Runtime, routing, user, Authority или Production Maturity effects;
- local, GitHub и production runtime commit: `7651001fcceb7c95dbfd20be5d685545d9708197`;
- final truth/convergence: `PASS / FULLY_ALIGNED`.

## Новое owner-backed расхождение

Read-only production inspection доказал, что Authority owner уже выдал и
сохраняет активный standing contract:

- request: `sdpauth_r1_906f2d2515016198d4c47727`;
- contract: `sdpc_f200a060c720a12669248105`;
- status: `ACTIVE`;
- expires: `2026-08-25T17:21:00.971884+00:00`;
- scope: только existing planner, `max_users=1`,
  `max_concurrent_transactions=1`, fresh Candidate/Packet/lease и все live gates.

Однако CPS продолжает показывать исходный request как ожидающий Engineering
Authority. Это не отсутствие пользовательского решения: это последний
producer-consumer gap `Authority policy/audit owner -> canonical CPS`.
Текущий truth gate ошибочно сверяет только source policy preview, а не
owner-backed active contract. Поэтому `FULLY_ALIGNED` здесь означает совпадение
commit/runtime snapshot, но не закрывает этот semantic reconciliation gap.

## Точный следующий frontier

`V7_SERVICE_FAILURE_STANDING_POLICY_ACTIVE_CPS_RECONCILIATION_V1`

Нужно минимально расширить существующие Authority/CPS/truth owners так, чтобы
read-only active-contract snapshot и audit provenance атомарно проецировались
в CPS. После этого existing Matrix consumer получает единственный допустимый
automatic successor: fresh matching service failure -> fresh Candidate -> fresh
Packet -> fresh lease -> live gates. Никакой старый Candidate, Packet, lease
или approval не используется; никакой move не создаётся ради проверки.
