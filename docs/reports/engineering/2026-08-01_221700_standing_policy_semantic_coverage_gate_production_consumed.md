# Production Report — semantic coverage gate for shared targets

Дата: 2026-08-01 22:17 Asia/Bangkok  
Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Текущий CPS frontier: `CONTINUE_AVAILABILITY_FIRST_CONTROLLED_PRODUCTION_STAGE_25`

## Итог

Закрыт producer→consumer дефект в существующем `tools/v7-users-autoswitch`.
Компактная target-selection projection раньше сообщала
`SHARED_PRODUCTION_TARGET_ACTION_CLASS_AUTHORITY_REQUIRED`, хотя существующий
standing contract уже покрывал тот же certification-only эффект. Production
caller теперь возвращает `AUTO_ADMITTED_BY_EXISTING_STANDING_POLICY`.

Это не выдача Authority и не выполнение Stage 25. Единственный законный
следующий consumer — уже существующий Matrix → Planner → Candidate/Packet/lease
путь на свежей генерации.

## Входная доказательная база

- Target-bound trial `awg3`, scope `10` завершён receipt
  `aftbound_c9acb10f468db1c3a6ee805e`.
- Receipt подтверждает immutable allocation, capacity reservation, per-user и
  aggregate verification, Outcome, Replay, Learning и baseline reset.
- Этот receipt имеет класс `TARGET_BOUND_ONLY_NOT_CAMPAIGN_STAGE`; Stage 10
  ladder не был повторно зачтён.
- Активный contract: `sdpc_285af5fc6f4de20415c3e5b1`;
  hash `285af5fc6f4de20415c3e5b1d27a3c2f89d06db5a29af4a60bb88bdf26af2f4f`.

## Причина и исправление

Причина: compact selection owner строил shared-target allocation, но не
потреблял семантический scope активного Availability-First standing contract;
дополнительно поле `current_stage_feasible` учитывало только старый
controlled-rebind путь, а не готовую shared allocation.

Исправление в существующем owner:

- добавлен read-only `standing-policy-semantic-coverage-gate`;
- нормализуются action class, certification-only identity class, total Mission
  cohort, batch size, concurrency, target classifications, ordinary-user
  fences, verification, containment/rollback, freshness и запрет Natural L8;
- возможны только `AUTO_ADMITTED_BY_EXISTING_STANDING_POLICY`,
  `ENGINEERING_BINDING_GAP` или `GENUINE_AUTHORITY_EXPANSION_REQUIRED`;
- shared Stage-25 feasibility теперь является частью compact projection;
- никаких новых owner, registry, policy/Authority write или execution artifact
  не создано.

## Проверка

- Focused affected suite: `146` tests PASS.
- Commit/push: `530eadcf` (gate) и `fcadeb48` (compact feasibility alignment).
- Safe deploy manifests: PASS; изменялся только
  `tools/v7-users-autoswitch`.
- Deploy snapshot: `deploy-z8-14-Updatesystem-fcadeb4-20260801T221543`.
- Production non-test caller `--standing-delegated-policy-status` подтвердил:
  `status=AUTO_ADMITTED_BY_EXISTING_STANDING_POLICY`,
  `current_stage_feasible=true`, `campaign_completion_feasible=true`,
  semantic gate `ok=true`.
- Forbidden effects в production caller: policy/contract/Candidate/Packet/lease
  creation, restore barrier, runtime apply, routing mutation, user movement,
  rollback, Authority expansion и Production Maturity change — все отсутствуют.
- `tools/v7-truth-check --all --json`: PASS.
- `tools/v7-convergence-status --json`: PASS; local, GitHub и production
  совпадают на `fcadeb4808412a18febd0fe0f414f254600bd638`.

## Current legal state

Stage 25 не запускался вручную. CPS и OMP уже указывают
`CONTINUE_AVAILABILITY_FIRST_CONTROLLED_PRODUCTION_STAGE_25`; его должен
потребить текущий Matrix owner на новой live generation. Если свежие gates
изменятся, owner обязан дать exact STOP_SAFE/re-entry, а не использовать этот
report или исторические Packet/lease как разрешение.

Production Maturity: без изменений. Natural L8 credit: запрещён.
