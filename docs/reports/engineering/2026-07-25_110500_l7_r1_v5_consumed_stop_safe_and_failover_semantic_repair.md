Mission ID: `V7_L7_R1_V5_CONSUMED_STOP_SAFE_AND_FAILOVER_SEMANTIC_REPAIR_V1`
Run Nonce: `V7_L7_R1V5_FAILOVER_SEMANTIC_REPAIR_20260725T110500+0700`

# Engineering Report: v5 STOP_SAFE и repair failover-семантики

## Результат production caller

Fresh request `engauth_r1_b152de57ac3e4f557e1cfb9e` был потреблён ровно один раз. Setup переместил только certification user `10.7.0.16` на controlled source `wireguard-1779454504-c43409`; owner перевёл только этот source в `maintenance`. Foreground caller создал fresh Packet `pkt_preview_4bc5f394d570a2d74e1ba7db`, operation `govdry_516d8937254a245b1514a293` и transaction nonce `59c50167c1b3c8c72ee396b53f0f5839e8ff66f40eb64667`.

Low-level L3 gate остановил transaction до apply:

- terminal: `STOP_SAFE`;
- reason: `l3_execution_eligibility_stop_safe`;
- exact blocker: `l3_allows_failover_only`;
- apply: `FALSE`;
- users moved основной transaction: `0`;
- rollback: `NOT_ATTEMPTED`;
- L7 credit: `NONE`.

После terminal controlled source восстановлен в `enabled`, certification user возвращён на `vless`, route verification прошёл, lease terminalized, Admin Safe Mode `OPEN`. Ordinary customers, Authority и Production Maturity не изменялись.

## Root cause

Producer `admin_core.operator_execution_pipeline._preview_packet_for_candidate` формировал exact controlled candidate с action class `single-user governed candidate failover`, но не переносил его execution semantic в Packet. `operator_execution.selected_moves_from_preview` поэтому применял legacy default `move_type=governed_canary`.

Consumer `tools/v7-users-autoswitch._l3_execution_eligibility` корректно требует `move_type=failover` для `EMERGENCY_FAILOVER` и fail-closed остановил несовместимую семантику.

Blocker fingerprint: `dc2385ca7b4b5cf846423d474d8f112f219697054971727ab30deb844d7844e1`.

Отдельный live diagnostic `safe_target_required` сохранён. Repair не обходит capacity/service eligibility target; следующая generation обязана повторно доказать safe target.

## Исправление existing owners

- exact controlled engineering selection теперь явно производит `move_type=failover`;
- существующий surface merge переносит move type без создания нового Candidate owner;
- canonical recommendation execution contract сохраняет семантику;
- Packet preview включает move type в semantic identity, Decision Commit и rollback manifest;
- ordinary setup/cleanup и обычные governed candidates сохраняют default `governed_canary`;
- L3 safety, target eligibility, restore barrier, verification, rollback и one-use rules не ослаблены.

## Проверки

- `303` related unit tests: `PASS`;
- exact controlled selection/Packet regression: `PASS`;
- Polygon design-time tests и `--omp-polygon-design-time`: `PASS`;
- forbidden effects during repair tests: `NONE`.

## Legal terminal и next frontier

v5: `CONSUMED_STOP_SAFE_BEFORE_APPLY`, non-reusable.

Program: не terminal. Exact next action — safe deploy только изменённых runtime owners после manifest verification, production binary/caller alignment и только затем fresh generation-aware request. Повтор v5 или retry текущей repair generation запрещён.

Evidence: `docs/reports/engineering/evidence/2026-07-25_105500_controlled_rollback_r1_v5_terminal.json`.
