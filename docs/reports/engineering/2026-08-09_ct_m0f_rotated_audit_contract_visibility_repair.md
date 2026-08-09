# CT-M0F: восстановление visibility active standing contract после rotation audit

Дата: 2026-08-09.

## Вердикт

`AUTHORITY_CONSUMER_PROJECTION_DEFECT` — исправлен и safely deployed.
Предыдущий CT-M0F contract не был invalidated. Новый terminal
`INACTIVE_NO_VALID_STANDING_CT_M0F_POLICY` оказался ложной consumer projection,
а не доказательством отсутствия Authority, source или target.

## Предыдущая и текущая owner-backed truth

| Поле | Предыдущая подтверждённая truth | Свежая production reconciliation |
|---|---|---|
| Contract | `ctm0fsdpc_208482a67dc4103e5f0ef7b6` | тот же ID и hash, `ACTIVE` |
| Expiry | `2026-09-05T09:32:42.689887+00:00` | не истёк |
| Lifecycle | active | не frozen, не revoked, не killed |
| Decision | единственная exact approval | один matching decision record, actor provenance сохранён |
| Sample ledger | controlled-only | 0 valid, 1 safety-stopped; performance credit отсутствует |

Запрос и единственная Authority decision находятся в
`operator-execution-audit.jsonl.1` — штатном bounded rotation segment. Они не
являются duplicate conflicting records и не были изменены.

## Root cause и ремонт

`validate_ct_m0f_standing_validation_policy` принимал только текущий активный
audit file. После rotation он не видел legit approval в `.1` и выдавал
`ct_m0f_standing_authority_audit_missing_or_duplicate`. Одновременно
`read_live_execution_lineage_records` не включал CT-M0F request/decision/sample
record types в свой bounded durable set.

Исправлены только существующие owners:

- `admin_core/operator_execution.py` — CT request/decision/sample lineage
  читается через existing bounded rotated-audit reader;
- `tools/v7-service-matrix-refresh-all` — Matrix CT-M0F consumer использует
  тот же canonical lineage reader.

Добавлен regression test: active CT contract сохраняет visibility и может
создать fresh reservation после audit rotation. Фокусные и affected tests:
`153 passed`.

Deploy manifest: allowlist `PASS`, blockers отсутствуют; изменены только
`admin_core/operator_execution.py` и `tools/v7-service-matrix-refresh-all`.
Production hashes совпали с source. Production non-test policy consumer вернул
`VALID_ACTIVE_STANDING_CT_M0F_POLICY_REUSED`, без policy write, runtime apply
или user movement.

## Раздельная topology truth

Восстановление contract visibility не подменяет physical topology. Последний
read-only topology owner пока не видит active isolated certification source,
matching certification identity или admissible controlled target. Поэтому
следующий обычный Matrix cycle обязан заново решить именно эти live predicates;
он не имеет права создавать external-resource residual только из-за уже
исправленного audit lookup.

VLESS продолжает наблюдаться как degraded/WARN. Existing Planner способен
строить preparation к compatible target, но это ещё не production permission:
требуются current action recommendation, isolation, capacity, freshness,
anti-flap, Candidate, Packet и lease.

## Доказательство автоматического re-entry

После deploy штатный `v7-service-matrix-refresh.timer` сам запустил Matrix в
`2026-08-09T07:48:04Z`; Matrix не запускался вручную. Исправленный CT-M0F
consumer больше не выдал `ct_m0f_standing_authority_audit_missing_or_duplicate`.
Его exact terminal: `STOP_SAFE_CONTROLLED_SOURCE_PREDECESSOR_REQUIRED`, blocker
`ct_m0f_active_service_failure_causal_binding_required`.

Это отдельный, текущий physical predecessor, а не опровержение standing
contract: действие не начиналось, Candidate/Packet/lease не создавались,
policy не записывалась, runtime/routing не менялись, пользователей не
перемещали. Read-only selector в том же состоянии видит `0` eligible controlled
sources, `0` exact group-aligned certification identities и `0` distinct
controlled-admitted targets. Следовательно, `EXTERNAL_RESOURCE_REQUIRED` пока
не доказан: следующий тот же timer обязан заново проверить live topology и
либо построить fresh eligible sample, либо сохранить этот structured STOP_SAFE
с automatic re-entry.

## Следующий owner и граница

`ordinary v7-service-matrix-refresh.timer -> repaired CT-M0F Matrix consumer
-> current selector -> structured STOP_SAFE or fresh bounded sample`.

Нет новой Authority, external-resource request, Stage-48 expansion, routing
mutation, Packet/lease, rollback, L8 credit или Production Maturity change.
CT-M1 не начиналась.
