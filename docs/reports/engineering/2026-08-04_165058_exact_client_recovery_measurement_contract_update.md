# Engineering Report: exact client recovery measurement contract update

Дата: 2026-08-04T16:50:58Z

## Результат

Существующая `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1` обновлена до
V4.5. Новый Program, Mission, owner, store, daemon, Planner, Runtime или
Authority-система не создавались.

## Закрытые неоднозначности

1. Operational set содержит минимум пять отдельных samples: минимум один cold,
   минимум два warm, оставшиеся два могут независимо быть cold или warm;
   samples охватывают минимум две owner-backed generations.
2. Recovery подтверждает только fresh application payload/response probe из
   exact certification identity routing/fwmark/policy context с expected target
   egress fingerprint. Management route, cached socket, TCP connect, route
   visibility и kernel counters недостаточны.
3. Primary end-to-end clock начинается с первого failed observation, которое
   позднее связано с той же confirmed hard-failure generation. Threshold
   crossing не удаляет detection interval.
4. Каждый sample возникает только из отдельной independently admitted
   controlled-validation generation, необходимой текущему SLO residual.
   Идентичное уже доказанное свойство не повторяется без invalidation или новой
   требуемой condition.
5. Probe cadence, measurement resolution, clock domain и uncertainty являются
   обязательным evidence. Если uncertainty может изменить PASS/FAIL, terminal —
   `MEASUREMENT_UNCERTAINTY_STOP_SAFE`.

## Обязательные метрики

- `FAILURE_DETECTION_LATENCY`;
- `POST_CONFIRMATION_RECOVERY_LATENCY`;
- `FIRST_FAILURE_EVIDENCE_TO_CLIENT_RECOVERY_LATENCY` — основной пользовательский
  end-to-end SLO;
- отдельные closure и reset clocks.

## Новые обязательные terminals

- `EXACT_CLIENT_NETWORK_CONTEXT_TRAFFIC_PROBE_PROVEN`;
- `FIRST_FAILURE_EVIDENCE_TO_CLIENT_RECOVERY_CLOCK_PROVEN`;
- `MEASUREMENT_CADENCE_AND_CLOCK_UNCERTAINTY_PROVEN`.

## Effect boundary

Изменение обновляет только Program/OMP/CPS measurement contract. Production
transaction, Candidate, Packet, lease, restore-barrier write, routing mutation,
user movement, Authority expansion и Production Maturity change отсутствуют.

Exact successor остаётся `CT-M0F-E_ENGINEERING`; CT-M0F-V и CT-M1 остаются
dependency-blocked.

Terminal изменения:
`EXACT_CLIENT_RECOVERY_MEASUREMENT_CONTRACT_UPDATED`.
