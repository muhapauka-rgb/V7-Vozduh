# Target-bound trial: production semantic deploy and Stage 25 checkpoint

Дата: 2026-08-01  
Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

## Зафиксированная истина

- Канонический campaign receipt Stage 10 остаётся валидным: `afstage_74d124e8951bfaccf499067a`. Решение: `REUSE_VALID_RECEIPT`; повторного Stage 10 credit нет.
- Предыдущий target-bound receipt `aftbound_5f9b9fc5e3aa23a407cbe440` доказал только target-specific scope `5` на `awg3`: все пять certification identities получили `Outcome/Replay/Learning`, затем вернулись на `vless`; ordinary users не затронуты.
- Commit `22de2622` развернут штатно через `tools/v7-safe-deploy` (deploy `deploy-z8-14-Updatesystem-2041537-20260801T162345`). Manifest содержал единственное несовпадение: `/usr/local/bin/v7-service-matrix-refresh-all`; restart, policy/barrier write, routing mutation и user movement отсутствовали.
- Проверки: `tests.unit.test_service_failure_episode` + `tests.unit.test_governed_canary_cli` — 145 PASS; `tools/v7-truth-check --all --json` — PASS; `tools/v7-convergence-status --json` — ALIGNED / `FULLY_ALIGNED`; local, GitHub и runtime commit — `2041537d685b1cb75ed6b333b4a32eb55fb0b1a6`.

## Семантическая граница

Deploy различает `TARGET_BOUND_TRIAL` и `CAMPAIGN_STAGE`: trial scope `10` для `awg3` относится к `campaign_next_stage=25` и не может снова зачесть Stage 10. Это production binary change; его следующий owner-backed Matrix event должен выдать эти поля в event projection.

## Текущий owner-owned execution

На момент checkpoint штатный `v7-service-matrix-refresh-all` уже запустил новый, **не дублирующий** target-bound predecessor: ранее на `awg3` был доказан предел 5, поэтому scope 10 является следующим target-specific bound, а не campaign Stage 10.

- Matrix parent: PID `2136914`.
- Governed parent: PID `2176526`, `--availability-first-stage 10 --availability-first-target-bound-trial-target awg3`.
- Наблюдаемый child Packet: `pkt_a0345931a63742acc9ee95cb`; operation `govexec_352713286131054a307de42f`; certification user `10.7.0.107`; `vless -> awg3`.
- Lease `execlease_5567834b7f4d20993414e0e4` уже `EXECUTION_FINISHED`; audit clearance owner-backed; live route подтверждён на `awg3`.
- Parent ещё завершает обязательные verification, Outcome, Replay, Learning и exact baseline reset. Его нельзя прерывать, перезапускать или сопровождать новым Candidate/Packet/lease.

## Stage 25: свежая capacity truth

Свежий read-only planner diagnostic после existing benchmark + quality compaction исключил ошибку stale snapshot. Сейчас Stage 25 не admitted: `awg0`, `awg3` и execution-only target ниже quality floors; `openvpn` и `wireguard` не имеют свободного безопасного capacity/reserve. Current owner status: `SHARED_PRODUCTION_TARGET_ACTION_CLASS_AUTHORITY_REQUIRED`.

Это не даёт права на новую Authority request, external capacity или ручной Matrix invoke. После terminal текущего target-bound trial existing Matrix/capacity owner обязан заново потребить receipt и либо самостоятельно admitted Stage 25 по действующему standing contract, либо сохранить точный safe boundary с автоматическим re-entry.

## Следующий consumer

`v7-service-matrix-refresh-all` -> existing availability-first Matrix consumer -> target-bound receipt reconciliation -> fresh multi-target Stage 25 capacity/allocation decision.

Запрещено до terminal текущего owner: ручной Matrix invoke, новый Packet/lease, reset/apply, policy/Authority write, routing mutation и user movement вне уже активного contract.
