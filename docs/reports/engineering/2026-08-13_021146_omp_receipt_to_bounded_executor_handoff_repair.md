# Repair: OMP receipt → bounded executor handoff

Дата: 2026-08-13

## Итог

`PASS_DEPLOYED_AND_PRODUCTION_CONSUMED`.

Исправлена существующая связь внутри ordinary Matrix path:

`service_failure_automation_obligation`
→ `OMP_CONSUMED receipt`
→ `tools/v7-service-matrix-refresh-all`
→ `tools/v7-users-autoswitch` bounded executor.

Ранее второй и последующие Matrix cycles корректно не создавали новую
obligation, но ошибочно передавали executor пустой вход и завершались
`STOP_SAFE_NO_CURRENT_SERVICE_FAILURE_OBLIGATION`.

## Причина и ремонт

Причина: immutable OMP exact-once receipt считался terminal для Matrix caller,
хотя он является durable handoff для следующего существующего consumer.

Ремонт в существующих owners:

- `tools/v7_sync_lib.py` читает только existing `closure-records.jsonl` и
  `l3-runtime-state.json`, возвращая obligation только при точном совпадении
  semantic fingerprint, Incident/Situation/Decision identity и текущего
  accounted scope;
- `tools/v7-service-matrix-refresh-all` использует этот handoff только когда
  advisory не выдал новую obligation;
- stale receipt, scope drift, recovery или identity mismatch остаются
  `NO_CURRENT_CONSUMED_HANDOFF` без Runtime effect.

Не созданы новые timer, queue, watcher, store, Planner, Authority или policy.

## Проверка

- Focused и полный `test_service_failure_automation_evolution` и
  `test_service_failure_episode`: `PASS`.
- Commit: `f2d84377`.
- Safe-deploy manifest: только `tools/v7_sync_lib.py` и
  `tools/v7-service-matrix-refresh-all`; forbidden effects отсутствуют.
- Production deploy: `deploy-z8-14-Updatesystem-f2d8437-20260813T020829`.
- Обычный systemd Matrix consumer (без ручного Matrix/autoswitch запуска)
  дошёл до existing bounded executor. Старый terminal исчез; получен честный
  terminal `STOP_SAFE_CURRENT_INCIDENT_NOT_ACTIONABLE` для
  `sfinc_762b70efa00784030a875fb3809300f8`.

## Текущий residual

Incident остаётся active с 11 users на failed source. Executor получил точную
current obligation, но Planner не выдал owner-backed actionable recommendation:
`current_incident_has_no_owner_backed_actionable_recommendation`.

Это не failure handoff и не разрешение на движение. Следующий existing consumer
— ordinary Matrix/Planner revalidation: при fresh healthy target, capacity,
policy и anti-flap gates он формирует новый Candidate/Packet/lease; иначе
сохраняется этот predicate-level STOP_SAFE с automatic re-entry на изменение
target/capacity/policy generations.

## Consistency

`tools/v7-truth-check --all --json`: `PASS`, `FULLY_ALIGNED`.

`tools/v7-convergence-status --json`: local/GitHub/production commit
`f2d84377a797cd88a6ca9d218cb5033c99a23992`, `PASS`.
