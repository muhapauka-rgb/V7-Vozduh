# P5.1 Fail-Closed Review

## Missing State

Missing required runtime registries fail closed:

- `operator_execution.runtime_recheck(...)` returns `DENY_STALE_RUNTIME`
- `v7-runtime-contract-validate` returns `status=fail`
- `v7-state-stale-check` returns `V7_STALE_RESULT=FAIL`

## Unknown State

Unauthenticated admin runtime APIs return `401 unauthorized`.

Unknown state is not treated as valid runtime truth.

## Unavailable State

Local `/opt/v7/egress/state` is unavailable.

Unavailable state blocks P5 retry.

## Stale State

Stale state is detected by age checks and runtime fingerprint status.

Stale state must not authorize P5.

## Invalid State

Invalid JSON or unreadable selected moves are rejected or classified as non-authoritative.

## Verdicts

- fail_closed_certified=true
- missing_state_fails_closed=true
- unknown_state_fails_closed=true
- unavailable_state_fails_closed=true
- stale_state_fails_closed=true
- invalid_state_fails_closed=true
