# CT-M0F: minimal slice, live selector and causal reconciliation

Дата: 2026-08-08 UTC  
Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Статус: `PARTIAL_ENGINEERING_CLOSURE; MATRIX_OWNED_NEXT_STEP`

## Что было проверено и исправлено

Широкий накопленный delta содержал независимый V3 persistent Authority/identity-provisioning путь. Он не был включён в CT-M0F: сохранён отдельной Git-веткой `codex/ctm0f-v3-preserved`, а минимальный production срез содержит только существующий owner `tools/v7-users-autoswitch`.

В selector обнаружен точный semantic defect: условие требовало ровно одну certification identity на failed source. Это смешивало transaction ceiling `max_users=1` с размером изолированного certification pool. Исправление допускает `>=1`, но по-прежнему выбирает только одну свежую identity на одну serial transaction. Тест покрывает pool из 40 identities.

После первой CPS bridge попытки найден старый causal defect: closed historical intent с устаревшим cumulative snapshot глобально блокировал живой incident. Existing passive causal projection owner восстановил 79 compact projections (`invalid_open_incidents=0`) без Candidate, Packet, lease, routing, user movement, rollback, Authority или Maturity effect. Затем causal gate был уточнён: closed legacy anomalies остаются append-only audit warnings; любая ошибка открытого incident остаётся `STOP_SAFE`.

## Production evidence

* Commits: `78e48f5e` (V3 exclusion), `55fc5951` (multi-identity source admission), `86d76384` (live-vs-historical causal gate).
* Safe-deploy preflight для обоих runtime commits: PASS; manifest изменял только `tools/v7-users-autoswitch`.
* Production selector после deploy: `CT_M0F_STANDING_CONTROLLED_FAILURE_READY`.
  * failed isolated source: `vless`;
  * selected scope: одна свежая certification identity (identity не сохраняется в отчёте);
  * safe shared target: `awg0`;
  * `eligible_source_count=1`, `shared_target_policy_admission.target_count=2`;
  * `ordinary_user_delta=0`, `stage48_credit=false`.
* Production causal status: PASS, `invalid_states=[]`, three open incidents, one closed historical audit warning.
* `tools/v7-truth-check --all --json`: PASS / `FULLY_ALIGNED`.
* `tools/v7-convergence-status --json`: PASS.

## Causal chain and boundary

```text
Matrix fresh observation
  -> existing selector admits one certification-only transaction
  -> existing planner creates fresh Candidate / Packet / lease
  -> standing-policy live gates
  -> bounded action, verification and closure
  -> compact causal scope -> CPS/OMP successor
```

Никакой action, Packet, lease, restore barrier, routing mutation или user movement не был создан или применён данной Mission. `V3`, Stage-48 campaign provisioning и Authority expansion не выполнялись.

## Exact next frontier

`CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN`.

Его producer — enabled ordinary Matrix/timer. Он должен создать новую owner-backed observation; только затем existing planner может материализовать fresh Candidate/Packet/lease и выполнить разрешённую standing-policy bounded transaction. Codex не заменяет этот wake ручным Matrix invocation и не создаёт synthetic evidence.
