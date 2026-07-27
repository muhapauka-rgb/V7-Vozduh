# Matrix как основной runtime consumer active Service Failure drain

Дата: `2026-07-27`  
Статус: `COMPLETE_CONSUMED; active incident continues through existing Matrix owner`

## Причина работы

После подтверждения active VLESS incident в source CPS оставался уже отправленный, но не завершённый Codex wake. Сам production Matrix был реальным consumer следующей revalidation, однако валидатор CPS считал отсутствующий `PENDING_WAKE_ID` единственным допустимым путём достижения сформированной Mission. Это создавало ненужный observer loop и могло оставить bridge в состоянии `DISPATCHED` после прерывания процесса.

## Reuse и точечное исправление

Новый owner не создан. Использованы существующие:

- production `v7-service-matrix-refresh.timer` и `tools/v7-service-matrix-refresh-all`;
- source CPS и его atomic reconciliation owner;
- существующий OMP Continue consumer и heartbeat только как source-CPS mirror/watchdog;
- существующая standing Tier-1 policy и её live gates.

`tools/v7_sync_lib.py` теперь:

1. явно записывает `tools/v7-service-matrix-refresh-all` как `CURRENT_SERVICE_FAILURE_NEXT_REQUIRED_CONSUMER` active-incident successor;
2. принимает сформированный successor без отдельного Codex wake только при точном Matrix-owned contract;
3. fail-closed восстанавливает только старый прерванный bridge: если local lease отсутствует, а pending dispatch принадлежит exact active Matrix continuation, atomically снимает stale `PENDING_WAKE_ID` и фиксирует `MATRIX_RUNTIME_SUCCESSOR_ACKNOWLEDGED_V1`;
4. не повторяет OMP, не создаёт Candidate/Packet/lease и не производит production action при таком восстановлении.

Тест покрывает normal Matrix acknowledgement и stale-bridge recovery без повторного запуска.

## Production verification

- Safe deploy: `deploy-z8-14-Updatesystem-27b93d2-20260727T233520`.
- Local, GitHub и production runtime: commit `27b93d2aeec0fe23b5291e361e9db4d4f488beab`.
- Production Matrix timer: `enabled`, `active`; последний owner-backed trigger: `2026-07-27 19:24:42 MSK`.
- Production non-test heartbeat завершился `PASS` с `MATRIX_RUNTIME_SUCCESSOR_ACKNOWLEDGED`.
- CPS: `PENDING_WAKE_ID=NONE`, `REENTRY_ACTIVE_LEASE=NONE`, `WATCHDOG_STATE=ARMED_FALLBACK_ONLY`, `CURRENT_SERVICE_FAILURE_NEXT_REQUIRED_CONSUMER=tools/v7-service-matrix-refresh-all`.
- `tools/v7-truth-check --all --json`: `PASS`, `FULLY_ALIGNED`.
- `tools/v7-convergence-status --json`: `PASS`, `ALIGNED`.

## Границы и следующий шаг

Ни routing, ни users, ни Packet execution, ни rollback, ни Authority, ни Production Maturity этим исправлением не менялись. Current incident остаётся открытым; exact frontier: `CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN`.

Следующий fresh observation, revalidation и любой допустимый Tier-1 transaction принадлежат production Matrix и происходят только при current live gates. Codex больше не является operational executor этого drain: его роль — source-CPS mirror/watchdog при действительно потерянной доставке или инженерном дефекте.
