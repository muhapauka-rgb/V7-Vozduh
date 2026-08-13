# Отчёт: operator-induced VLESS outage — capture и безопасное consumption

Дата: 2026-07-25 UTC  
Статус: `REPAIRED_AND_PRODUCTION_CONSUMED_NO_L7_L8_CREDIT`

## Факт события

- Класс: `OPERATOR_INDUCED_PRODUCTION_EVENT`; это **не** `NATURAL_L8` и не L7-транзакция.
- Канонический source-channel: `vless` (`egress.registry`, protocol `vless`, expected IP `77.110.103.131`).
- Неизменяемая source history: `/opt/v7/egress/state/egress-history.jsonl`.
- Failure episode: `2026-07-25T09:19:23+03:00` — `2026-07-25T09:33:55+03:00`, десять samples, code `000`.
- Первое восстановление в той же history: `2026-07-25T09:35:14+03:00`, code `200`.
- Trigger provenance: `operator-vless-external-unavailability-20260725T091923MSK`.

## Аудит и дефект

До исправления V7 видел сырую деградацию в `egress-history.jsonl` и service matrix, но не создавал source event в существующем `/opt/v7/events/service-failure-events.jsonl`; autoswitch consumer поэтому мог потреблять лишь старые/общие `NO_EXECUTION`, не этот инцидент.

Первый вариант repair также обнаружил несовпадение identity: refresh-result channel `1` не является каноническим VLESS identity `vless`. Последний ответственный producer→consumer разрыв исправлен в `tools/v7-service-matrix-refresh-all`: для `OPERATOR_INDUCED` mandatory declared canonical channel связывается с последним подтверждённым failure episode из существующего `egress-history.jsonl`. Это исключает захват другого текущего отказа и допускает capture уже восстановившегося реального события без синтеза.

Production deploys через `tools/v7-safe-deploy`:

- `b9297cd2` — capture-only producer/consumer contract;
- `357d184b` — canonical history/identity binding.

Оба manifest: `PASS`; runtime/user/routing/restore-barrier/rollback effects: `false`.

## Реальный owner chain

| Звено | Production result |
| --- | --- |
| Source event | `pevt_8243b864f82971fa46ee029e`, `v7.passive-production-failure-capture.v1` |
| Situation | `situation_7a784f6fdc35d7a257cf73dc` |
| Decision Trace | `decision_7cf45811d60e3a574b02202f` |
| Classification | `STOP_SAFE` → `STOP_SAFE_NO_ACTION` |
| Candidate / Packet / lease | `false / false / false` |
| Execution / user / routing mutation | `false / 0 / false` |
| Verification | source snapshot bound; execution absent; rollback `NOT_APPLICABLE` |
| Outcome | `v7.passive-production-event-outcome.v1` in `execution-events.jsonl` |
| Temporal | initial=true; event recovery is source-recorded; delayed owner observations remain `PENDING_PASSIVE_RECOVERY_OBSERVATION` |
| Replay | `replay_d767e65d71e25f7a63cdcbb2`, `NO_DRIFT`; second consumer invocation produced no duplicate |
| Learning | `learn_123bd978b3966427f66d688f`, `OBSERVATION_ONLY_NO_TRUST_OR_AUTHORITY_CHANGE` |
| Closure | `CAPTURED_STOP_SAFE` in `closure-records.jsonl` |

Producer: `tools/v7-service-matrix-refresh-all`. Consumer: `tools/v7-users-autoswitch._consume_passive_production_events`. Source partitions: `egress-history.jsonl`, `service-matrix.json`, `egress.registry`, `users.registry`; outcome partitions: `execution-events.jsonl`, `runtime-trust.jsonl`, `closure-records.jsonl`, `l3-runtime-state.json`.

## Evidence and program result

- No old Candidate, Packet, lease or Authority was reused.
- No synthetic evidence, Production Maturity update, Authority expansion, user movement, routing apply, packet execution or rollback apply occurred.
- This is a valid operator-induced observation and safe no-action terminal; it is not an eligible Outcome Evidence Passport.
- Passive L8 chain was **not** credited: this event was correctly excluded from natural evidence. `natural_production_present` remains open.
- Read-only evidence inventory returned `qualifying_natural_passports=0`, `authority_recommendation=INSUFFICIENT_EVIDENCE`, no authority or maturity mutation.

## Проверки

- `python3 -m unittest tests.unit.test_operator_induced_passive_capture tests.unit.test_v7_users_autoswitch_policy` — 156 passed.
- Production source event, caller/consumer, idempotent replay and L7/L8 evidence inventory — passed as above.

## Точный следующий frontier

`WAIT_FOR_QUALIFYING_NATURAL_PRODUCTION_EVENT_WITH_CAPTURE_READY`.

Необходимо пассивно захватить следующее действительно natural production событие через существующих owners; operator-induced VLESS событие не может закрыть этот критерий.
