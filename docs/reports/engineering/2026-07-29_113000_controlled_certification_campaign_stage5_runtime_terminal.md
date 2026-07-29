# Controlled Certification Campaign: runtime consumer и точный Stage-5 terminal

Дата: 2026-07-29

Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

Mission: `T48-M9`

## Итог

Утверждённая controlled-production кампания подключена к существующим Authority, Matrix, governed execution, Outcome, Replay, Learning, CPS и OMP owners. Реальный production Matrix caller дошёл до governed executor для Stage 5 и остановился на live L3 quality gate до apply.

Финальный честный verdict:

`CONTROLLED_CERTIFICATION_CAMPAIGN_RUNTIME_CONSUMER_PROVEN_STAGE_5_STOP_SAFE_LIVE_TARGET_QUALITY_AND_CAPACITY_BOUNDARY`

Кампания `5 -> 10 -> 25 -> 48` не объявляется завершённой. Текущий controlled production proven max равен `0`, следующий stage равен `5`.

## Authority и scope

- request: `cpsauth_r1_0b5151b3c3a33fd6ced157ab`;
- hash: `0b5151b3c3a33fd6ced157ab7eb272357f41ac3f700a68864e917c1cfc6e7c7c`;
- expiry: `2026-07-30T01:56:04.769524+00:00`;
- source: `1`;
- target: `amneziawg-exec-20260528-10-8-1-14`;
- certification-only identities on source: `48`;
- stages: `5,10,25,48`;
- max concurrent transactions: `1`;
- ordinary customer reclassification or movement: forbidden and absent.

## Что было переиспользовано и расширено

Новые owner, queue, watcher, registry, Planner, Runtime или Authority system не создавались.

Переиспользованы:

- append-only Authority audit owner в `admin_core/operator_execution.py`;
- certification identity и egress registry owners;
- `tools/v7-service-matrix-refresh-all`;
- `tools/v7-users-autoswitch`;
- `tools/v7-governed-canary-dry-run-cycle`;
- Outcome, deterministic Replay и Learning consumers;
- OMP heartbeat/re-entry owner;
- CPS и OMP pointer owners;
- `tools/v7-safe-deploy`.

Реализованы только недостающие связи:

1. campaign stage progress читается из существующего Authority audit;
2. Matrix выбирает только точный следующий stage и после успешного stage требует Outcome, Replay, Learning и baseline reset receipt;
3. exact approved execution-only target допускается в campaign path, но остаётся недоступен обычному autoswitch;
4. Matrix-owned campaign frontier больше не блокируется старым VLESS execution-feedback predecessor;
5. текущие OMP pointer-проекции атомарно выводятся из CPS и fail-closed валидируются.

## Production caller / consumer

Production Matrix result:

- incident: `sfinc_79c7265b16283934089d5119f65455dd`;
- obligation: `sfaob_b07ba85a824b5120a56c09c0`;
- standing contract: `sdpc_36bb4d9cc58ceac13287b973`;
- action attempted: `true`;
- governed transaction status: `STOP_SAFE`;
- stop reason: `l3_production_validation_transition_blocked`;
- action completed: `false`;
- runtime mutation: `false`;
- users moved: `0`;
- consumer verdict: `GOVERNED_TRANSACTION_STOPPED`.

Это доказывает реальную цепочку:

`approved campaign -> fresh Matrix observation -> campaign binding -> governed executor -> live gate -> STOP_SAFE`

Post-deploy source heartbeat:

- final verdict: `PASS`;
- priority: `CONTROLLED_CERTIFICATION_FRONTIER_PREEMPTS_GENERIC_POLYGON`;
- real consumer: `tools/v7-service-matrix-refresh-all`;
- next automatic action: `CONTROLLED_SERVICE_FAILURE_CERTIFICATION_STAGE_5_REQUIRED`;
- operator/Codex prompt: не требуется;
- старый VLESS feedback predecessor: не требуется;
- `PENDING_WAKE_ID`: `NONE`.

## Точный live blocker

Target service baseline остаётся доступным: `14/14` services, code `200`, assigned users `0`.

Но owner-backed quality state для exact target:

- current stability: `0.0354847`;
- 5m stability: `0.0372`;
- 1h stability: `0.0535`;
- policy minimum stability: `0.45`.

Registry capacity contract:

- `soft_limit=10`;
- `hard_limit=10`;
- role: `EXECUTION_ONLY`;
- `production_assignment_allowed=false`;
- `autoswitch_allowed=false`;
- `rebalance_allowed=false`.

Следствия:

1. Stage 5 может быть повторно допущен только после fresh live quality recovery и всех остальных gates.
2. Stage 10 остаётся на абсолютной текущей границе target capacity и требует fresh reserve/capacity admission.
3. Stage 25 и Stage 48 на этом target невозможны без owner-backed target-capacity изменения или нового отдельно одобренного controlled target.
4. Изменять hard limit техническим редактированием registry или обходить quality gate запрещено.

Автоматическая re-entry остаётся у существующего Matrix timer. Новый outage, повторная инженерная сертификация или ручное сообщение Codex не требуются. Если quality восстановится, тот же Stage-5 successor будет переоценён свежими gates. Для Stage 25/48 требуется отдельный владелец capacity/target решения; текущая Authority не расширяется автоматически.

## Исправленные producer-consumer gaps

### Heartbeat predecessor ordering

До исправления heartbeat пытался согласовать старый VLESS feedback перед независимым controlled campaign frontier и получал:

`execution_feedback_scope_binding_mismatch`

После исправления точный Matrix-owned campaign frontier направляется прямо existing Matrix consumer. VLESS execution feedback остаётся обязательным только для соответствующей VLESS lineage.

### CPS / OMP pointer binding

До исправления CPS показывал Stage 5, а OMP current pointers всё ещё показывали старый `ENGINEERING_AUTHORITY_CONTROLLED_CERTIFICATION_TARGET_REQUEST_READY`.

После исправления:

- CPS current stop: `NONE`;
- CPS current next action: `CONTROLLED_SERVICE_FAILURE_CERTIFICATION_STAGE_5_REQUIRED`;
- OMP current stop: `NONE`;
- OMP current next action: `CONTROLLED_SERVICE_FAILURE_CERTIFICATION_STAGE_5_REQUIRED`;
- CPS contradictions: `0`;
- OMP contradictions: `0`.

## Commits и deploy

- `a9a32f965eff2b776828366bb5d8ffb449557fbf` — campaign continuation, receipts, reset и Matrix consumer;
- `ebf433048b33d2f83b633435e85a88c4f860b3bb` — exact approved controlled target через campaign gates;
- `d04f08945e4810c0deea443cbc4034f4996681fe` — Matrix-owned heartbeat predecessor ordering;
- `7741e6197ffabe5fa900dbbbcf3a2115a2bbf01d` — атомарная CPS/OMP pointer reconciliation.

Последние deploy:

- `deploy-z8-14-Updatesystem-d04f089-20260729T111025`;
- `deploy-z8-14-Updatesystem-7741e61-20260729T112236`.

Safe-deploy manifests:

- для `d04f0894` изменён только `tools/v7-truth-check`;
- для `7741e619` изменён только `tools/v7_sync_lib.py`;
- blockers: `[]`.

## Проверки

- affected unit tests: `PASS`;
- exact heartbeat non-test caller: `PASS`;
- production deployed entrypoint boundary: fail-closed, zero effects;
- `tools/v7-truth-check --all --json`: `PASS`, `FULLY_ALIGNED`;
- `tools/v7-convergence-status --json`: `PASS`, `ALIGNED`;
- перед добавлением настоящего report local commit = GitHub commit = production commit:
  `7741e6197ffabe5fa900dbbbcf3a2115a2bbf01d`;
- deploy delta mismatches: `[]`.

## Forbidden effects

- ordinary users moved: `0`;
- certification users moved by failed Stage-5 attempt: `0`;
- runtime apply: `false`;
- routing mutation: `false`;
- rollback apply: `false`;
- restore-barrier write: не выполнялся этим reconciliation;
- Authority expansion: `false`;
- Production Maturity change: `false`;
- synthetic L8 evidence: `false`.

## Exact next frontier

`CONTROLLED_SERVICE_FAILURE_CERTIFICATION_STAGE_5_REQUIRED`

Durable automatic re-entry:

`fresh Matrix target quality/capacity observation -> existing campaign consumer -> fresh governed admission or exact STOP_SAFE`

Полное завершение кампании допустимо фиксировать только после owner-backed успешных stages `5,10,25,48`, полного Outcome/Replay/Learning consumption и baseline reset между stages. Текущее состояние является безопасным внешним live-gate/capacity terminal, а не ложным завершением.
