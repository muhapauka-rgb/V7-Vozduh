# E34.C Restore Scope Model

restore_scope_defined=true

## Restore Types

| Restore Type | Goal | Reconstructs | Allowed Result |
| --- | --- | --- | --- |
| minimum_restore | Bring governance/release evidence back enough to inspect and fail closed. | release objects, deployment lineage, audit index, core config schema. | Read-only review and containment. |
| full_restore | Restore normal production control-plane operation. | all REQUIRED backups, current release, config, governance state, RI state, audit lineage. | Production eligible after verification. |
| disaster_restore | Recover after server/disk/system loss. | release objects, backups, lineage, configs, services, audit, rollback target. | Production eligible only after convergence checks. |
| cold_start_restore | Build a new runtime from repo/release plus backup state. | release object, config, lineage, backup manifest, operator approvals. | Staging until runtime/config fingerprints converge. |

## Restore Phases

1. Load backup manifest.
2. Verify backup fingerprint and lineage.
3. Restore release/provenance records.
4. Restore configuration and governance state.
5. Restore audit lineage.
6. Reconstruct derived caches.
7. Verify runtime/release/config convergence.
8. Run restore-settle/read-only governance checks.
9. Mark restore status.

## Fail-Closed Rules

- Restore does not authorize user movement.
- Incomplete restore stays RESTORE_REVIEW or RESTORE_FAILED_CLOSED.
- If audit lineage cannot be restored, forward movement remains denied.
- If release lineage cannot be restored, runtime is not production-certified.

restore_scope_defined=true
