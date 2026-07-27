# Step 3: сверка active-drain, policy и tier-проекции

Дата: 2026-07-27 UTC
Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1` v1.5
Статус: `ACTIVE_WITH_DURABLE_SUCCESSOR`

## Итог

Исправлена существующая producer-consumer связь между read-only сверкой
standing delegated policy и CPS. Ранее такая сверка могла заменить активный
`CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN` старой проекцией ожидания
нового события. Теперь она сохраняет работающий Matrix drain и атомарно
публикует только подтверждённые границы текущего action class.

## Владелец и точная причина

- Runtime policy и append-only Authority audit остаются владельцами policy truth.
- `tools/v7-users-autoswitch --standing-delegated-policy-status` теперь выдаёт
  redacted machine-readable границы policy: class, `max_users=1`,
  `max_concurrent_transactions=1`, допустимые failure families, verification,
  rollback и expiry.
- CPS consumer `reconcile_active_standing_delegated_policy_to_cps()` больше не
  перезаписывает активный incident drain и fail-closed обрабатывает malformed
  runtime bounds.
- Во время первой production CPS-сверки был обнаружен `NameError` до записи
  CPS. Он исправлен отдельным минимальным commit и повторно развёрнут; ни один
  запрещённый effect не произошёл.

## Production-подтверждение

- Финальный runtime commit: `767f975e`.
- Штатный deploy manifest изменил только `tools/v7_sync_lib.py` во втором
  release; предшествующий release изменил только `tools/v7_sync_lib.py` и
  `tools/v7-users-autoswitch`.
- Реальный production caller вернул `PASS`: активный owner-backed контракт,
  один пользователь на транзакцию, одна одновременная транзакция,
  self-expansion запрещён, expiry enforced.
- Atomic CPS reconciliation: `PASS`.
- Пользователи не перемещались; routing/runtime apply, policy write, contract
  issuance, Candidate/Packet/lease, restore barrier, rollback, Authority и
  Production Maturity не изменялись.

## Current truth

- Incident frontier: `CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN`.
- Current source scope: `31 = 1 protected + 30 unresolved + 0 excluded/recovered`.
- Durable next consumer: existing `tools/v7-service-matrix-refresh-all` via
  enabled Matrix timer; Codex is not the production wake source.
- M7 tier verdict: `HOLD_CURRENT_TIER`.
- Current Authority-approved and Runtime-enabled tier: one serial user.
- Tiers 2, 5, 10 and bounded cohort: `SCOPE_MISMATCH`; historical larger-batch
  evidence is supporting only, not a current grant.

## Проверки

- Focused service-failure, external-reentry, policy и truth unit tests: `PASS`.
- `tools/v7-truth-check --all --json`: `PASS`, `FULLY_ALIGNED`.
- `tools/v7-convergence-status --json`: `PASS`.
- Local, GitHub и production runtime identity: commit `767f975e`.

## Legal terminal

`ACTIVE_WITH_DURABLE_MATRIX_SUCCESSOR`.

Это не terminal всей программы: 30 current-scope intents остаются открытыми.
Их последовательный Tier-1 drain продолжает существующий Matrix owner до
пустого source scope, recovery либо точного live blocker с durable re-entry.
