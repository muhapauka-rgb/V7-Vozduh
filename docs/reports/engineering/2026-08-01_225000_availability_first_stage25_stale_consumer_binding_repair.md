# Исправление stale binding Matrix consumer для Stage-25

Дата: 2026-08-01  
Статус: DEPLOYED_AWAITING_ORDINARY_MATRIX_TIMER_CALL

## Факт до исправления

Канонический owner `shared_production_target_capacity_projection` уже публиковал
`current_stage=25`, однако предыдущие Matrix events передавали executor
`campaign_stage=10`. Executor корректно завершал такие попытки как
`availability_first_stage_not_current`; ни Packet, ни lease, ни routing mutation,
ни user movement при этом не создавались.

Это был producer-consumer дефект чтения: вложенный `availability_campaign` является
append-only progress/history view и способен на короткое время показывать уже
потреблённый predecessor, тогда как `current_stage` — каноническая текущая
исполняемая проекция shared target-capacity owner.

## Исправление

- `tools/v7-service-matrix-refresh-all` выбирает Stage из канонического
  `projection.current_stage`, с безопасным fallback к историческому полю только
  когда canonical значение отсутствует.
- `tools/v7-governed-canary-dry-run-cycle` применяет и проверяет supplied Stage
  относительно того же `current_stage`.
- Добавлен regression test: `current_stage=25` при stale nested
  `availability_campaign.next_stage=10` обязан dispatch-ить Stage-25.

## Проверка

- Focused affected tests: `147` passed.
- Commit/GitHub: `bcef584908e7cc335a783a37cfc26349da8dfbc0`.
- Safe deploy: `deploy-z8-14-Updatesystem-bcef584-20260801T224920`.
- Deploy manifest: только `tools/v7-service-matrix-refresh-all` и
  `tools/v7-governed-canary-dry-run-cycle` отличались от production; allowlist PASS.
- Production binary hashes совпадают с source.
- Production topology diagnostic после deploy:
  `CONTROLLED_TOPOLOGY_AVAILABILITY_FIRST_AUTO_ADMITTED`,
  `current_stage=25`, `campaign_next=25`.
- `tools/v7-truth-check --all --json`: PASS.
- `tools/v7-convergence-status --json`: ALIGNED / FULLY_ALIGNED.

## Граница и следующий consumer

Ни Matrix, ни executor вручную не запускались. Активный
`v7-service-matrix-refresh.timer` остаётся единственным ordinary caller.
Следующий его естественный tick должен потребить Stage-25 через обычные live gates.
Итог будет либо owner-backed Stage-25 Outcome/receipt с successor, либо точный
fresh STOP_SAFE с durable automatic re-entry; внешний операторский wake для этого
не требуется.
