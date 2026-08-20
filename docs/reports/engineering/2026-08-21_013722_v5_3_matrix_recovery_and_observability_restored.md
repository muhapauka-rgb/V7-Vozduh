# V5.3: Matrix recovery и восстановление наблюдаемости

Дата: 2026-08-21 01:37 MSK  
Track: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`  
Scope: read-only recovery verification  

## CURRENT MATRIX STATE

`MATRIX_STATE = WORKING`

Matrix не требовал production-исправления. Существующий timer запустил
существующий service, полный цикл завершился успешно, а state был записан.

Последний наблюдённый цикл:

| Поле | Факт |
|---|---|
| Start | `2026-08-21 01:31:39 MSK` |
| Finish | `2026-08-21 01:32:44 MSK` |
| Duration | `65.009 s` по systemd, `63.668 s` в lifecycle payload |
| Exit code | `0` |
| Service result | `success` / `Deactivated successfully` |
| Egress rows | `7` |
| Probe result | `6` rows OK, `vless` WARN, egress `1` FAIL; общий Matrix lifecycle status `OK` |
| Timer | `active (waiting)`, next trigger `01:46:56 MSK` |

## ROOT CAUSE

Корень прежнего блокера — не отказ Matrix, а разрыв наблюдаемости:

1. Локальный approved snapshot был старым (`22:07:15 MSK`) и показывал только
   `timer=active (waiting)`.
2. Текущий `v7-truth-check --runtime-readonly` не запрашивал last start/finish,
   exit code, service journal и mtime Matrix state.
3. Поэтому работающий Matrix ошибочно классифицировался как `UNKNOWN`.

Дополнительная семантическая особенность: после успешных probes compact summary
может содержать `total=0`, `elapsed_sec=0` и
`CERTIFICATION_SCOPE_DEFERRED_TO_EXISTING_CONTROLLED_OWNER`. Это compact
projection certification-only ветки, а не отсутствие выполненных probes. Полные
`total=7`, `ok_count=6` и `elapsed_sec=63.668` зафиксированы в service journal.

## FIX APPLIED

Production fix не применялся: `NONE`.

Причина: Matrix уже работал, а правила шага запрещали менять cadence, timeout,
service, Runtime, архитектуру или state flow. Наблюдаемость восстановлена через
существующий read-only production owner path; новый watcher, owner, registry и
источник истины не создавались.

## EVIDENCE BEFORE

- Runtime snapshot: `2026-08-20 22:07:15 MSK`.
- Timer: `active (waiting)`.
- Last service cycle, exit code, duration и state freshness: отсутствовали.
- `tools/v7-truth-check --runtime-readonly`: `NO-GO` из-за общего
  `runtime_local_commit_mismatch`, что не являлось Matrix failure evidence.

## EVIDENCE AFTER

### Последние циклы

Read-only journal дал следующие start/finish пары:

| Start | Finish | Duration |
|---|---|---:|
| 00:13:18 | 00:14:15 | 57 s |
| 00:29:15 | 00:30:32 | 77 s |
| 00:44:43 | 00:45:54 | 71 s |
| 01:00:31 | 01:01:39 | 68 s |
| 01:16:29 | 01:17:25 | 56 s |
| 01:31:39 | 01:32:44 | 65 s |

Средняя длительность: `65.7 s`, диапазон `56–77 s`.  
Интервалы start-to-start: `15:10–15:58`, среднее `15:40`.

Это согласуется с configured cadence `15 min + RandomizedDelaySec=60s`.

### State и summary freshness

- `service-matrix.json` stat mtime наблюдался около `01:33:52 MSK`, JSON
  содержит `items=7` и актуальный `updated` timestamp около `01:33:56 MSK`.
- `service-matrix-refresh-summary.json` stat mtime наблюдался около
  `01:33:54 MSK`; JSON schema валиден, projection завершён с
  `next_output=CERTIFICATION_SCOPE_DEFERRED_TO_EXISTING_CONTROLLED_OWNER`.
- State и summary были обновлены сразу после цикла и классифицируются как
  `FRESH` на момент проверки.

### Existing consumer visibility

Существующий `v7-users-autoswitch --controlled-target-selection-diagnostic`
выполнен с `read_only=true`. Он прочитал Matrix через owner pointer
`/opt/v7/egress/state/service-matrix.json` и получил свежие inventory/quality
данные (`inventory_measured_at=22:36:51Z`, quality `fresh=true`). Одновременно
зафиксировано:

- `candidate_packet_lease_created=false`;
- `routing_mutation=false`;
- `user_movement=0`;
- ordinary autoswitch service остаётся `inactive (dead)`.

Следовательно, consumer видит свежий state, но governed execution не запускался.

### Binary provenance

SHA-256 Matrix binaries совпадают локально и в production:

- `v7-service-matrix-refresh-all`:
  `6a23f6369b919d25ab16c85f33b600a518f2c06b2f69c14739f43fcece021936`;
- `v7-service-matrix-test`:
  `398e4c1c6ad5c3d3cf0d99d3f56ffd5ce987e189285e2e841a07f7c9d8dd5801`.

Общий local/runtime commit mismatch сохраняется как отдельный provenance
blocker и не исправлялся.

## RUNTIME EFFECT

- Timer/service lifecycle не изменялись.
- Matrix cadence, timeout и полный baseline не изменялись.
- FAST не включался.
- Matrix writer успешно записал state.
- Никаких новых owner, watcher, telemetry store или источников истины нет.

## PRODUCTION EFFECT

- Пользователи не перемещались.
- Маршруты не менялись.
- Candidate, Packet и lease не создавались.
- Fault injection не выполнялся.
- Наблюдение осталось read-only.

## T0-T11 TRACK POSITION

Блокер «Matrix lifecycle не подтверждён» снят. Можно вернуться к исходному
вопросу, но только с новой fresh Matrix generation:

```text
T0 failure
  → fresh Matrix/current state   [готово к re-entry]
  → exact current target/certification context
  → governed synthetic one-client dry-run
  → Candidate → Packet → Lease → Barrier
  → Apply → Verification → Traffic recovered
```

Фактического T0 failure и реального client movement в этом шаге не создавали и
не наблюдали.

## NEXT STEP IN T0-T11 TRACK

Существующий Matrix/Planner owner должен выполнить exact revalidation текущего
target/certification context. Если все freshness и safety gates сохраняются,
следующий bounded шаг — один governed synthetic-client dry-run. Ordinary clients,
маршруты и production apply остаются вне этого шага.

## CHECKS

- Live read-only systemd status/journal/state checks: PASS.
- Last service exit code: `0`.
- Effective cadence: measured and aligned with configured cadence.
- State freshness: `FRESH`.
- Consumer read-only visibility: PASS.
- Local truth check: PASS.
- Production mutation: `NONE`.

