# VLESS passive capture consumer loop и operational terminal

Дата: 2026-07-25
Mission: `V7_VLESS_SERVICE_FAILURE_PASSIVE_CAPTURE_AND_SAFE_RESTORATION_V1`

## Итог

`ENGINEERING_REPAIR_COMPLETE_PRODUCTION_CONSUMED; VLESS_UPSTREAM_REPAIR_REMAINS_OWNER_BOUND`

Устранён последний producer → consumer дефект пассивного service-failure capture. Реальный VLESS канал при этом не восстановлен подменой конфигурации или массовым переносом пользователей: локальный `sing-box` и `tun0` работают, а upstream `vless-out` возвращает TCP `connection refused`. Ремонт самого endpoint либо отдельная user-protection транзакция требуют свежего owner-authorized контракта.

## Root cause и исправление

- Matrix запускается каждые 15 минут с randomized delay, а episode continuity была ровно 900 секунд. Поэтому продолжающийся отказ при каждом запуске становился новым `sample=1` и никогда не доходил до consumer.
- Continuity увеличена до 2100 секунд: обычный timer+jitter и один пропущенный интервал сохраняют один episode, длительный несвязанный разрыв создаёт новый.
- `tools/v7-service-matrix-refresh-all` после каждого production batch вызывает существующий consumer.
- `tools/v7-users-autoswitch --consume-passive-events-only` выполняет только Situation/Decision/Outcome/Replay/Learning capture и fail-closed отклоняет apply, Packet, lease, rollback и Authority flags.
- Сбой или отсутствие consumer публикуется в существующем Matrix artifact как `V7_PASSIVE_SERVICE_EVENT_CONSUMER_REPAIR`.
- Admin UI больше не выдаёт Runtime/config readiness за доступность сервисов и показывает progress устойчивого failure episode.

## Verification

- 171 focused unit/regression tests: `PASS`.
- Commit: `f338e2a6d8b0a207f7e6b60d037e5bc0407ad1b8`.
- Deploy: `deploy-z8-14-Updatesystem-f338e2a-20260725T205214`.
- Deploy manifest изменил только:
  - `tools/v7-users-autoswitch`;
  - `admin/v7-admin-api`;
  - `tools/v7-service-matrix-refresh-all`;
  - `tools/v7-service-matrix-test`.
- Deploy safety: autoswitch apply, routing mutation, user movement, restore-barrier write, policy/Authority change — `false`.

Реальный production timer после deploy сохранил продолжающийся VLESS episode как `failure_samples=2`, `bad_for_seconds≈914`, создал и автоматически потребил внешние service-failure события. Consumer записал 31 Situation/Trace/Outcome/Learning/Closure цепочку; повторный production caller вернул `already_consumed_idempotent`.

Репрезентативная VLESS запись:

- event: `sfe_2e76a65b580c02a89ef39b7566091967`;
- provenance: `EXTERNAL_UNATTRIBUTED`;
- evidence: `PROBE_OBSERVED_PRODUCTION_EVENT` → `NATURAL_PRODUCTION_CANDIDATE`;
- Situation: `situation_aa01d792e3d82899296f94fe`;
- Decision Trace: `decision_2dd4ec1f0734cc71e642a66d`;
- terminal: `STOP_SAFE_NO_ACTION`;
- replay: `NO_DRIFT`;
- Learning: `delta=0`, observation-only;
- execution, routing mutation, users moved, L7 credit, Natural L8 credit: `0/false`.

Fresh Matrix: VLESS `1/14` сервисов OK; 13 сервисов остаются недоступны.

## Final truth

- `tools/v7-truth-check --all --json`: `PASS`, `FULLY_ALIGNED`.
- `tools/v7-convergence-status --json`: `PASS`, `ALIGNED`.
- local = GitHub = production runtime linkage: `f338e2a6d8b0a207f7e6b60d037e5bc0407ad1b8`.

## Legal terminals

- Engineering capture/consumption: `COMPLETE_CONSUMED_PRODUCTION`.
- VLESS service restoration: `EXTERNAL_ENDPOINT_REPAIR_OR_FRESH_OWNER_AUTHORIZED_USER_PROTECTION_CONTRACT_REQUIRED`.
- `natural_production_present`: `OPEN`.
- Exact OMP frontier: `WAIT_FOR_QUALIFYING_NATURAL_PRODUCTION_EVENT_WITH_CAPTURE_READY`.

Ни старый Candidate/Packet/lease/Authority, ни это `EXTERNAL_UNATTRIBUTED` наблюдение не дают права на массовое движение пользователей, Authority promotion или изменение Production Maturity.
