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

Восстановление contract visibility не подменяет physical topology. Первичный
ручной read-only вызов с неканоническим пустым state-path был отвергнут как
не-авторитетный и не использован для current truth. Канонический
`/opt/v7/egress/state` owner подтверждает existing-resource triple:
`vless -> 10.7.0.114 -> awg0`; source isolated для controlled condition,
active incident и exact certification identity существуют, target healthy,
capacity/verification/rollback supported, shared-target admission active и
ordinary-user delta равен `0`.

VLESS остаётся degraded/WARN. Это даёт нужное current failure lineage, но ещё
не production permission: перед effect обычный Matrix обязан вновь проверить
freshness, anti-flap, Candidate, Packet и lease.

## Доказательство автоматического re-entry

После deploy штатный `v7-service-matrix-refresh.timer` сам запускал Matrix;
Matrix не запускался вручную. Первый post-repair cycle убрал
`ct_m0f_standing_authority_audit_missing_or_duplicate`, но read-only canonical
selector обнаружил другой producer-consumer defect: несколько immutable L3
rows одной generation, включая `INCIDENT_SCOPE_ACCOUNTING_BROKEN`, создавали
ложный `AMBIGUOUS_ACTIVE_SERVICE_FAILURE_BINDING`.

Commit `4ba510a5` оставляет fail-closed две разные valid scope/generation,
но исключает только rows, нарушающие их собственный existing-owner scope law,
и выбирает newest OMP-consumed matching current projection. Production caller
после deploy вернул `CT_M0F_STANDING_CONTROLLED_FAILURE_READY` с incident
`sfinc_74ce6760a73dff445728ecd1f1aacba1`.

Следующий Matrix cycle в `2026-08-09T08:03:19Z` ещё безопасно остановился на
`ct_m0f_standing_validation_policy_denied`: его downstream
`v7-governed-canary-dry-run-cycle` оставался третьим consumer, читавшим лишь
active audit segment. Commit `d1a54d3a` перевёл все три CT validation paths
этого executor на тот же bounded rotated-audit reader; safe deploy прошёл.
Ни один из этих cycles не создал Candidate/Packet/lease, не записал policy,
не изменил runtime/routing и не переместил пользователей.

Следующая штатная Matrix generation обязана revalidate готовый triple и либо
создать fresh bounded sample, либо оставить новый exact live STOP_SAFE. Это
не `EXTERNAL_RESOURCE_REQUIRED`, не новый Authority request и не Stage-48
expansion.

## Следующий owner и граница

`ordinary v7-service-matrix-refresh.timer -> repaired CT-M0F Matrix consumer
-> current selector -> structured STOP_SAFE or fresh bounded sample`.

Нет новой Authority, external-resource request, Stage-48 expansion, routing
mutation, Packet/lease, rollback, L8 credit или Production Maturity change.
CT-M1 не начиналась.
