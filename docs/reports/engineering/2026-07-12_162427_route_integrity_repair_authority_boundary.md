Mission ID: `V7_OMP_ROUTE_INTEGRITY_REPAIR_AUTHORITY_BOUNDARY_V1`
Run Nonce: `V7_ROUTE_REPAIR_AUTH_BOUNDARY_V1_A7086B0D3E7B`

# Граница полномочий для исправления Route Integrity

## Цель

Автоматически потребить transaction terminal `RUNTIME_ROUTE_INTEGRITY_FAILURE`, проверить существующих owners и определить, может ли исправление быть разложено на независимые one-user транзакции внутри `dap_default_tier1_readonly` без ослабления verification.

## Fresh Production Evidence

Read-only `v7-user-route-check` повторно подтвердил:

- `10.7.0.32`, table `1030`: assignment `wireguard-1779454504-c43409`, ожидаемый interface `v7e06a394c478` отсутствует, default route отсутствует, route leaks to public `ens3`;
- `10.7.0.38`, table `1036`: тот же disabled egress и тот же public `ens3` leak;
- все остальные проверенные user policy routes прошли;
- final route check: `FAIL`;
- production mutation: `NO`;
- user movement: `NO`;
- Safe Mode: `OPEN`.

## Existing Owners

Использованы существующие route-integrity checker, Planner advice, egress capacity/quality evidence, `v7-user-switch`, governed execution/verification/rollback owners, delegated policy и CPS/OMP. Новый owner, action class, Runtime или policy не создавались.

## Decomposition Verdict

`LEGAL_ONE_USER_DECOMPOSITION = NO`.

Причина: после первого one-user repair глобальный route-integrity verifier продолжит законно возвращать `FAIL` из-за второй stale assignment. Существующая governed transaction обязана откатить первый move. Последовательное исправление двух записей требует одного bounded repair operation с двумя serial mutations до общей global verification. Ослаблять verifier или временно принимать глобальный FAIL запрещено.

## Exact External Boundary

`PROGRAM_TERMINAL_CLASS = OPERATIONAL_AUTHORITY_OUTSIDE_ACTIVE_POLICY`.

Требуется только одноразовое Operational Authority для точного scope:

- users: только `10.7.0.32` и `10.7.0.38`;
- execution: serial, no concurrency;
- fresh evidence и owner-selected target для каждого user непосредственно перед execution;
- fresh operation, lease, binding и rollback identities;
- одна controlled repair operation;
- global route verification после обеих serial mutations;
- rollback/containment обоих users при failure;
- mandatory final Safe Mode `OPEN`;
- no permanent policy, threshold, action-class, blast-radius or authority expansion.

Ни один Candidate, target, packet, hash, decision, operation или lease данным отчётом не утверждён и не может быть переиспользован.

## No-Progress Fingerprint

Payload: current stop + route-integrity owner chain + two disabled-egress assignments + expected globally valid enabled-egress routes + exact authority next action.

`9de9264320871de4460d1641bed72f634a0d6ed6a99d4099b6cbe45f9146aee7`

## Result

- `OMP_CONTINUATION_REQUIRED = FALSE`
- `EXTERNAL_INPUT_REQUIRED = TRUE`
- `EXTERNAL_INPUT_TYPE = OPERATIONAL_AUTHORITY`
- `NEXT_MISSION_FORMED = TRUE`
- `PREMATURE_OPERATOR_RETURN = FALSE`
- `CURRENT_NEXT_ACTION_ID = APPROVE_EXACT_TWO_USER_ROUTE_INTEGRITY_REPAIR`
- `CAP-U01 = ACTIVE / INTENT_NOT_CLOSED`
- `USER_MOVEMENT = NO`
- `SAFE_MODE_FINAL_STATE = OPEN`

`OPERATIONAL_AUTHORITY_OUTSIDE_ACTIVE_POLICY`
