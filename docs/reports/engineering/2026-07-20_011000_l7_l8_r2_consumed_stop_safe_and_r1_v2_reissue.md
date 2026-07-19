Mission ID: `V7_L7_L8_R2_CONSUMED_STOP_SAFE_AND_R1_V2_REISSUED_V1`
Run Nonce: `V7_L7_L8_R2_STOP_SAFE_20260720T011000+0700`

# Инженерный отчёт: R2 consumed STOP_SAFE и новый R1 v2

## Итог

Одноразовый R2 `engauth_r1_33cc5e04f86c20ff0607f7db` был атомарно связан с точными Candidate, Packet, lease и nonce, затем законно потреблён. Low-level execution control остановил транзакцию до forward apply. Production apply, verifier-triggered rollback и новый L7 Outcome Passport не возникли. Повтор под тем же approval не выполнялся и запрещён.

После STOP_SAFE certification user `10.7.0.16` возвращён штатным governed cleanup owner в исходный `vless`; table `1014` снова содержит `default dev tun0`, controlled source включён, lease terminal, Admin Safe Mode `OPEN`. Cleanup классифицирован только как `ENGINEERING_CLEANUP_NOT_L7_EVIDENCE`.

Терминал Mission: `R2_CONSUMED_STOP_SAFE_BEFORE_APPLY_R1_V2_REQUEST_PREPARED`.

## Точная причина

Packet identity был корректен: user `10.7.0.16`, source `wireguard-1779454504-c43409`, target `vless`, packet `pkt_preview_90ee9b46e1247a1ba8c56313`, lease `execlease_08682ad481af6e9bef0ca604`.

Apply owner вернул `autonomous_execution_control_stop_safe` по двум blocker:

- controlled window открылся с action class `USER_SWITCH`, а approved verifier path исполнялся как `EMERGENCY_FAILOVER`;
- после восстановления committed moves local `selected_hash` сохранил pre-rehydration identity `4f53...` вместо approved hash `ec18...`.

Оба blocker являются настоящими producer→consumer binding defect, а не CI, transport или real-world boundary.

## Исправление

В существующих owners выполнены минимальные изменения:

- exact Engineering Authority открывает и перепроверяет окно как `EMERGENCY_FAILOVER` на всех трёх control gates;
- `tools/v7-users-autoswitch.apply` после approved-lock rehydration повторно читает canonical operation hash до первого control decision;
- exact request проецирует только bound certification user/source/target в существующую decision surface;
- bounded service verifier активируется только при валидном exact R2 binding;
- exact post-consumption cleanup остаётся отдельным engineering evidence и не создаёт второй L7 credit.

245 focused tests прошли. Repair commit: `c299dbf3acd912aa10fc78b04d8379bb63fc9504`. Safe deploy: `deploy-z8-14-Updatesystem-c299dbf-20260720T010811`; manifest изменил только `tools/v7-users-autoswitch` и `tools/v7-governed-canary-dry-run-cycle`; deploy effects: routing/user/apply/restore/policy/Authority `NONE`.

## Evidence и классификация

Компактный terminal: `docs/reports/engineering/evidence/2026-07-20_011000_controlled_rollback_r2_consumed_stop_safe.json`.

Production artifact hashes сохранены для `/tmp/v7-r4-main.json`, `/tmp/v7-r4-refresh.json` и `/tmp/v7-r4-cleanup.json`. Durable consumption record hash: `c7fa115988379056d6af77cbedde5a167ecbc5389c3d5e217c7a66ed7a714ba7`.

Evidence class separation:

- R2 binding/STOP_SAFE: production governance and safety evidence;
- setup/cleanup: Engineering Evidence only;
- L7 material Outcome: `NONE`;
- L8 natural evidence: `NONE`;
- Authority/class/Production Maturity change: `NONE`.

Immutable set остаётся `outset_428a4e2ff440ed64bde5cb56` с пятью eligible controlled Passports. M6/M7 остаются `INSUFFICIENT_EVIDENCE`. Открытые cells не изменились: `rollback_and_no_rollback_present; natural_production_present`.

## Новый точный R1

Поскольку старый approval потреблён и `retry_allowed=false`, подготовлен новый независимый request:

- request: `engauth_r1_f89460c18394f8fee79c9724`;
- contract: `f89460c18394f8fee79c97244cb875fbbded2c14d8d46948b499e986ad270c22`;
- expiry: `2026-07-20T05:10:00+07:00`;
- packet: `docs/reports/engineering/evidence/2026-07-20_011000_controlled_rollback_authority_request_v2.json`.

Новый request сохраняет тот же bounded scope, но явно связывает consumed STOP_SAFE, repair commit/deploy и запрет переиспользования старого approval. Он сам по себе не разрешает setup, condition activation, apply или rollback.

## Следующий legal frontier

`DECIDE_CONTROLLED_ROLLBACK_AUTHORITY_REQUEST_engauth_r1_f89460c18394f8fee79c9724`

R3-R8 не активированы. R9 остаётся отдельной будущей программой. Controlled lane остановлен ровно на `ENGINEERING_AUTHORITY`; natural lane независимо остаётся capture-ready на lane-local `REAL_WORLD_LIMIT`.
