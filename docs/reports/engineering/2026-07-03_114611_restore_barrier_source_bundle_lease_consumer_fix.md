# Restore Barrier Source Bundle Lease Consumer Fix

## Summary

Controlled Production Certification Program resumed at Phase 4 `MEDIUM_BATCH` after the downstream proof guard deployment.

Repeat Phase 4 payload:

`/tmp/v7_phase4_medium_batch_after_proof_guard_20260703T074145.json`

Result:

- `final_verdict`: `STOP_SAFE`
- `transaction_status`: `STOP_SAFE`
- `stop_reason`: `l3_production_validation_downstream_proof_failed`
- selected users: `10.7.0.16` through `10.7.0.25`
- selected source: `wireguard-1779454504-c43409`
- selected targets: `awg0`, `awg3`, `vless`
- transition: `ok`
- selected move count: `10`
- `apply_executed`: `false`

The new proof guard correctly prevented a false PASS.

## Breakpoint

Runtime Apply was denied before user movement:

- owner: `tools/v7-users-autoswitch`
- function: `_validate_atomic_execution_envelope()`
- terminal reason: `atomic_execution_envelope_source_changed`
- mismatch: `source_bundle_hash`
- changed source key: `service_matrix`

## Producer Evidence

Restore Barrier had already accepted the source-bundle drift as a valid lease:

- `source_bundle_lease.ok = true`
- `source_bundle_lease.changed_source_keys = ["service_matrix"]`
- `source_bundle_lease.reason = restore_barrier_source_bundle_lease_service_matrix_only`
- selected move hash stable
- selected move count stable
- selected users stable
- selected targets stable
- hard source hashes stable:
  - `egress_registry`
  - `users_registry`
  - `service_preferences`

Restore Barrier clearance:

- `clearance_generation_ok = true`
- `clearance_generation_reason = restore_barrier_clearance_generation_match_source_bundle_lease`
- `clearance_max_selected_moves = 10`
- `clearance_expected_selected_moves = 10`

## Root Cause

The Runtime Apply consumer ignored the Restore Barrier prevalidated source bundle lease unless `snapshot_gate.source_bundle_lease_used` was also present.

In production, the authoritative lease was present on the Restore Barrier object, but `snapshot_gate.source_bundle_lease_used` was absent in the apply payload.

This caused `_source_bundle_stability_lease_validation()` to require a fresh pre-planner refresh success even though Restore Barrier had already proven that the only source drift was service-matrix-only and the semantic decision identity was stable.

## Owner Resolution

Blocking owner:

`tools/v7-users-autoswitch`

Exact function:

`_source_bundle_stability_lease_validation()`

Terminal classification:

`IMPLEMENTATION_DEFECT`

Required Resolution:

Reuse the existing Restore Barrier source bundle lease as prevalidated evidence when:

- `restore_barrier.source_bundle_lease.ok == true`;
- `restore_barrier.clearance_generation_reason == restore_barrier_clearance_generation_match_source_bundle_lease`;
- apply-side validation still independently verifies selected identity, allowed users, allowed targets, runtime snapshot, clearance budget, and expiration.

No new owner, Runtime, Planner, Authority, Restore Barrier, Wake, packet, or execution path was created.

## Fix

Changed:

- `tools/v7-users-autoswitch`

The Runtime Apply consumer now treats a valid Restore Barrier source bundle lease as prevalidated lease evidence.

The existing safety checks remain in place:

- only source-bundle-only mismatch can use the lease;
- runtime snapshot must stay stable;
- selected move hash/count must stay stable;
- allowed users and targets must match;
- clearance generation must be valid;
- clearance budget must cover the batch;
- clearance must not be expired.

## Tests

Added regression test:

- `test_governed_apply_accepts_restore_barrier_prevalidated_source_bundle_lease`

The test reproduces the production shape:

- Restore Barrier lease is valid;
- `snapshot_gate.source_bundle_lease_used` is absent;
- only `service_matrix` changes;
- selected identity stays stable;
- apply proceeds through existing governed path.

Commands:

`python3 -m unittest tests.unit.test_v7_users_autoswitch_policy tests.unit.test_governed_canary_cli`

Result:

- `Ran 150 tests`
- `OK`

Compile:

`PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch tests/unit/test_v7_users_autoswitch_policy.py`

Result:

- `PASS`

## Production Restoration

After the STOP_SAFE run, the controlled source was restored:

- `/usr/local/bin/v7-egress-set-state wireguard-1779454504-c43409 enabled --apply`
- route repair executed for certification users `10.7.0.16` through `10.7.0.40`
- `V7_USER_ROUTE_CHECK=OK`

## Next Step

Safe deploy this fix and rerun Phase 4 `MEDIUM_BATCH` from the interrupted certification phase.

