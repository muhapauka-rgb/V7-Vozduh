# Polygon E2E five-user Runtime inventory gate — 2026-09-06

## Result

The fresh, owner-backed Runtime inventory fails closed before a physical
Polygon E2E run.  It proves the current substrate is not ready; it does not
prove a recovery result, latency, Production behavior, or user effect.

## Current owner evidence

The existing `v7-users-autoswitch --standing-delegated-policy-status` owner
reported a fresh controlled-certification-pool projection with fingerprint
`e94354f106c4289f2c53852d2d55b41c65f938a4badf59aea1605e079d9be174`.

- `total_enabled_certification_users`: 53.
- The greatest enabled certification count on one active source: 1.
- The greatest count on one isolated active source: 1.
- Required baseline: 5 existing certification users on one isolated source,
  with zero enabled non-certification users.
- The only healthy `EXECUTION_ONLY` certification target is empty and remains
  reserved for `operator_execution_governance`; it is not an ordinary target.

The owner returned the exact blocker:

`fewer_than_5_enabled_certification_users_on_one_active_controlled_source`

The current policy is a four-user hard-fail failover policy, not a five-user
controlled-certification substrate Authority.  The controlled-substrate
Authority status is `NONE`.  The present isolated source is unhealthy; no
healthy isolated source candidate is available.  Therefore no existing
consumer may lawfully prepare an Authority request, write a registry,
reassign a certification user, inject a fault, or run autoswitch.

## Contract correction

The Polygon evidence gate now requires five users rather than an invalid
one-user surrogate.  It also records a structurally complete over-seven-second
ledger as `VERIFIED_E2E_OVER_7S` while retaining `STOP_SAFE` for any scale
admission.  This avoids discarding a real causal measurement while preventing
1K or 10K escalation.

## Exact re-entry

The existing controlled-certification and Authority owners must first expose a
fresh lawful source/target pair and an exact five-user reuse-only Authority
record.  Its request must have zero new identities, preserve all ordinary-user
assignments and routes, and select five already enabled certification users on
one healthy isolated source.  Only then may the existing health-loop → Matrix
current consumer → governed autoswitch → route/kernel → required-service S11
chain execute a single physical-failure baseline.

No Runtime write, user movement, routing change, fault injection, mock, direct
switch, broad test, or Production action was performed by this inventory gate.
