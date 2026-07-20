Mission ID: `V7_L7_R1_V4_CONSUMED_STOP_SAFE_AND_RUNTIME_SNAPSHOT_BINDING_REPAIR_V1`
Run Nonce: `V7_L7_R1V4_BINDING_REPAIR_20260720T102000+0700`

# Инженерный отчёт: R1 v4 STOP_SAFE и ремонт runtime snapshot binding

## Результат production-цикла

Fresh one-use request `engauth_r1_220b4498e31ff22aa905b06c` был потреблён ровно один раз. Setup подготовил только certification user `10.7.0.16` на controlled source `wireguard-1779454504-c43409`; существующий lifecycle owner перевёл только этот source в `maintenance`. Затем foreground owner создал свежие Packet `pkt_preview_1e4b3f8b3d12bcca223a380a`, operation `govdry_fc6b801a0dfcf56787e2b91d` и nonce `8bad0410a3bada406b75463d91fef6a5d7e828d75e9e71b3`.

Перед apply atomic envelope остановил транзакцию с `atomic_execution_envelope_envelope_mismatch`; единственное расхождение — `runtime_snapshot_hash`. Source bundle и все exact operation-scoped source identities совпали. Apply не выполнялся, users moved `0`, routing mutation `false`, rollback attempted `false`. Поэтому L7 Passport и rollback evidence не созданы, а пять ранее eligible Passports и exact missing cells сохранены без изменения.

После terminal source штатно возвращён в `enabled`; cleanup вернул только certification user на `vless`. Итоговый Safe Mode — `OPEN`. Setup и cleanup остаются Engineering Evidence, а не L7.

## Last responsible producer → consumer

Packet producer `admin_core/operator_execution.py` строил operation-scoped `runtime_snapshot_hash` из нормализованных source identities. Low-level consumer `tools/v7-users-autoswitch._validate_atomic_execution_envelope` повторно вычислял этот redundant hash из raw registry-file SHA. Поэтому semantic source bundle проходил, но другой класс идентичности того же snapshot ложно останавливал apply.

Исправление ограничено существующим consumer: для operation-scoped envelope он теперь вычисляет runtime snapshot из тех же normalized `users_registry`, `egress_registry` и `selected_move_hash`. Raw/non-operation-scoped envelope сохраняет byte-level проверку; независимая source-bundle проверка продолжает fail-closed останавливать semantic drift.

## Проверка ремонта

- Новый regression воспроизводит like-for-like operation-scoped identity.
- Полный связанный suite: `252 tests`, `OK`.
- Permanent Polygon design-time: `PASS`; affected obligations materialized and consumed; semantic differential `PASS`; forbidden effects absent; Runtime/production mutation, packet execution, restore-barrier write, rollback apply, routing mutation и user movement — `false`.
- Authority impact: `NONE`.
- Production Maturity: `NO_CHANGE`, `66.9/100`.

## Legal terminal и продолжение

V4 terminal: `CONSUMED_STOP_SAFE_BEFORE_APPLY_REPAIR_READY_FOR_SAFE_DEPLOY`. Request v4, его Packet, lease и nonce не переиспользуются. Следующий допустимый шаг — commit/push и минимальный `tools/v7-safe-deploy` только `tools/v7-users-autoswitch`, затем production caller/truth/convergence. Лишь доказанная distinct deployed repair generation может создать fresh v5 one-use request в том же exact scope. Natural L8 остаётся отдельной passive capture-ready lane на `REAL_WORLD_LIMIT`.

Compact evidence: `docs/reports/engineering/evidence/2026-07-20_102000_controlled_rollback_r1_v4_terminal.json`.
