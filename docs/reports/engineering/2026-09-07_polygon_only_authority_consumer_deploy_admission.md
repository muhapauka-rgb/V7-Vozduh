# POLYGON_ONLY Authority / consumer deploy admission

## Scope

This package extends existing `admin_core/operator_execution.py`,
`tools/v7-users-autoswitch`, and `tools/runtime-support/v7-user-switch` only.
It admits exactly one one-use `POLYGON_ONLY` action: five existing
certification identities, fixed controlled source and fixed shared target.
No ordinary identity, target fault/restart/quarantine/config/profile mutation,
or new owner is admitted.

## Evidence before deploy

- `tests.unit.test_operator_execution_packet` and
  `tests.unit.test_polygon_only_route_truth`: 111 passed.
- `bash -n tools/runtime-support/v7-user-switch`: passed.
- `git diff --check`: passed.
- The route invariant is a canonical projection of existing
  `v7-user-route-check` truth. Presentation timestamps are excluded; only an
  explicit `V7_USER_ROUTE_CHECK=OK` is usable. WARN, missing, failure, and
  timeout become pre-consumption STOP_SAFE.

## Required post-deploy evidence

Existing `v7-safe-deploy` must prove the exact Runtime revision and changed
file hashes, service state, canonical truth and convergence. Deployment alone
does not issue a contract, move a user, modify a route, or cause a fault.

