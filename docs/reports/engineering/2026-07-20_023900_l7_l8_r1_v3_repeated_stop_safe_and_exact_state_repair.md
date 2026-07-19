Mission ID: `V7_L7_L8_R1_V3_REPEATED_STOP_SAFE_AND_EXACT_RUNTIME_TRUTH_REPAIR_V1`
Run Nonce: `V7_L7_L8_R1V3_REPEAT_STOP_20260720T023900+0700`

# Инженерный отчёт: R1 v3 повторный STOP_SAFE и ремонт exact runtime truth

Дата: `2026-07-20T02:39:00+07:00`  
Program: `V7_L7_L8_PRODUCTION_EVIDENCE_AND_AUTHORITY_EVOLUTION_PROGRAM_V1`  
Mission: `V7_L7_L8_R1_V3_REPEATED_STOP_SAFE_AND_EXACT_RUNTIME_TRUTH_REPAIR_V1`  
Terminal: `R1_V3_CONSUMED_REPEATED_BLOCKER_STOP_SAFE_REPAIR_DEPLOYED`

## Итог production-транзакции

Fresh request v3 `engauth_r1_5ecff8aa38fd049d142a030a` был автоматически допущен существующим policy owner без повторного запроса человеку и потреблён ровно один раз.

- Packet: `pkt_preview_132c81677ac5ab56b38ef8a7`.
- Operation: `govdry_2461ff1a39082df93931c814`.
- Apply: `false`.
- Users moved: `0`.
- Rollback attempted: `false`.
- L7 evidence: `NONE`.
- Terminal: `CONSUMED_STOP_SAFE_BEFORE_APPLY`.

Exact cleanup отдельным существующим owner восстановил certification user `10.7.0.16` на `vless`, включил controlled source и подтвердил Admin Safe Mode `OPEN`. Cleanup остаётся `ENGINEERING_CLEANUP_NOT_L7_EVIDENCE`.

## Root cause

Внешние причины STOP_SAFE повторили прежний fingerprint `d5a3338f8023562d9d803231eaf035d99d13c6aea0eaa528c552650b6a06cad1`:

- `approved_plan_lock_incident_source_mismatch`;
- `approved_plan_lock_user_source_mismatch`.

Новый точный producer→consumer разбор доказал два дефекта внутри существующего exact verifier:

1. `v7-egress-set-state` правильно записывал dynamic state `maintenance` в `egress-flags.state`, но consumer читал только статический `egress.registry` и получал `state=enabled`.
2. “Fresh” user check объединял актуальный `users.registry` со старым diagnostic snapshot `v7-state.json`, причём старый `current=vless` перекрывал реальное `current=wireguard-1779454504-c43409`.

Switch history не содержит перемещения между setup и STOP_SAFE: ложный `vless` был stale read, а не реальным user movement.

## Ремонт и deploy

Commit: `88ec9ab1e2009de6454fe465f033b84b7957bd1a`  
Safe deploy: `deploy-z8-14-Updatesystem-88ec9ab-20260720T023152`

- exact user identity теперь читается непосредственно из canonical mutable `users.registry`;
- dynamic egress state читается из существующего lifecycle owner `egress-flags.state` с fail-safe fallback;
- approved plan lock использует тот же canonical runtime user owner;
- обычная planning projection и Authority не расширялись.

Regression воспроизводит production race: registry уже на source, snapshot ещё на vless, registry source disabled, flags state maintenance. Совместный focused suite: `249 PASS`.

Deploy manifest изменил только `tools/v7-users-autoswitch`. Service restart не требовался. Deploy safety: autoswitch apply `false`, routing mutation `false`, user movement `false`, restore-barrier mutation `false`, policy/planner mutation `false`.

Production snapshot после deploy:

- commit `88ec9ab1e2009de6454fe465f033b84b7957bd1a`;
- binary SHA-256 `6137f9cd482cec992e669f55efba998d54b3c43ff707e4b3baf0f229a63f30db`;
- user `10.7.0.16` на `vless`;
- controlled source `enabled`;
- Safe Mode `OPEN`.

## Автоматизация и legal terminal

Пользовательское подтверждение не переиспользовалось. Именно standing policy `engrepair_fe6a2c49ae391f397330274a` автоматически создало fresh v3 с новыми Request, Packet, operation, lease и nonce.

Но тот же blocker fingerprint повторился после заявленного ремонта. Поэтому обязательный automatic stop condition сработал корректно: v4 не создаётся автоматически и v3 не запускается повторно. Это защищает от бесконечного production retry loop и не отменяет автоматизацию для следующего действительно нового distinct repaired blocker.

Текущий controlled terminal: `REPEATED_BLOCKER_FINGERPRINT_STOP_SAFE`. Natural L8 lane остаётся отдельно capture-ready на `REAL_WORLD_LIMIT`. Rollback/no-rollback evidence cell остаётся открытой. Authority expansion и Production Maturity change: `NONE`.

Compact evidence: `docs/reports/engineering/evidence/2026-07-20_023900_controlled_rollback_r1_v3_terminal.json`.
