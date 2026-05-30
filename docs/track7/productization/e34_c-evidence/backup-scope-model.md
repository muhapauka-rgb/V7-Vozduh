# E34.C Backup Scope Model

backup_scope_defined=true

## Scope Classes

| Artifact | Backup Class | Rationale |
| --- | --- | --- |
| Governance artifacts | REQUIRED | Required to preserve capacity, batches, policy, concurrency, scheduling, and execution boundaries. |
| Routing Intelligence artifacts | REQUIRED | Required to preserve required_services interpretation, service health logic, proposal logic, and confidence rules. |
| Configuration | REQUIRED | Runtime behavior depends on config, registries, policy, service matrices, and environment schema. |
| Release objects | REQUIRED | Restore must know which release is valid and deployable. |
| Deployment lineage | REQUIRED | Restore must reconstruct which release was deployed and how. |
| Audit lineage | REQUIRED | Governance and provenance need append-only history. |
| Policies | REQUIRED | Policy admission and operator rules must survive restore. |
| Capacity metadata | REQUIRED | Batch limits and target certification must survive restore or fail closed. |
| Batch metadata | REQUIRED | In-flight and historical batch records must be recoverable. |
| Scheduling metadata | REQUIRED | Scheduled work, holds, and timing decisions must be recoverable or safely cancelled. |
| Operator data | REQUIRED | Approvals, review decisions, incidents, and notes are part of recovery evidence. |
| Volatile probe samples | OPTIONAL | Useful for diagnostics but not always required for minimum restore. |
| Derived caches | EXCLUDED | Rebuild from authoritative state after restore. |
| Runtime counters | EXCLUDED | Not authoritative unless explicitly stored as audit/state records. |
| Secrets in plaintext | EXCLUDED | Backup secret references or encrypted secret bundles, not plaintext evidence. |

## Backup Classes

- REQUIRED: restore cannot be certified without it.
- OPTIONAL: improves diagnosis but restore can proceed without it.
- EXCLUDED: should be regenerated or never stored in backup.

## Safety Rule

If an artifact affects user movement, routing, governance admission, release provenance, or rollback, it is REQUIRED unless explicitly classified otherwise with an architecture decision.

backup_scope_defined=true
