# E34.E Runbook Model

runbook_model_defined=true

## Runbook Contract

Every runbook must follow the same operator-independent structure:

```text
entry_conditions
required_evidence
plausible_causes
diagnosis_steps
allowed_actions
forbidden_actions
verification
closure_verdict
escalation_conditions
```

The runbook must never begin with an action. It begins with evidence collection.

## Required Runbooks

| Runbook | Entry conditions | Required evidence | Allowed actions | Verification | Closure |
| --- | --- | --- | --- | --- | --- |
| `TARGET_DEGRADED` | Target readiness drops, quality below floor, or target health checker reports degraded state. | Readiness output, capacity status, quality samples, target users, runtime checkers, audit tail. | Refresh validation, recertify, reduce eligibility, fail closed, rollback affected batches if active. | Target returns GO or is marked DEGRADED/EXPIRED. | Fixed, fail-closed, or escalated. |
| `CAPACITY_STALE` | Capacity TTL exceeded or validation age beyond stale threshold. | Capacity metadata, validation timestamp, evidence references, policy cap, hard limit. | Run recertification methodology, deny forward movement until fresh. | Status returns CERTIFIED or remains STALE/EXPIRED. | Certified or fail-closed. |
| `POLICY_CONFLICT` | Two or more policies produce incompatible admission decisions. | Active policies, policy priorities, scope, evaluation trace, affected batch. | Deny forward, request review, deactivate only through certified policy procedure. | Conflict gone and evaluation trace deterministic. | Resolved or escalated. |
| `SCHEDULER_BLOCKED` | Batch cannot be scheduled due to locks, reservations, capacity, or policy. | Batch metadata, lock ledger, reservation ledger, capacity state, policy decision, restore-settle. | Release stale locks if certified stale, reschedule, cancel, or escalate. | Scheduler has deterministic next state. | Scheduled, cancelled, or escalated. |
| `FAILED_RESTORE` | Restore verification fails or runtime remains UNKNOWN/BLOCKING after restore. | Restore logs, backup fingerprint, release fingerprint, runtime fingerprint, audit lineage, governance checks. | Keep runtime fail-closed, retry restore from certified backup, escalate lineage reconstruction. | Runtime/config/lineage/governance verification passes. | Restored or fail-closed. |
| `FAILED_BACKUP` | Backup missing, incomplete, unverifiable, stale, or corrupted. | Backup inventory, completeness scan, backup fingerprint, encryption status, retention state. | Create replacement backup via certified backup flow, block production certification. | Backup verification passes. | Backup certified or escalated. |
| `BAD_RELEASE` | Release fingerprint mismatch, certification invalid, deployment health failed, or rollback required. | Release object, manifest, provenance, runtime fingerprint, health checks, rollback release. | Deny promotion, rollback to certified release, revoke bad release. | Runtime matches rollback or fixed release expectations. | Rolled back, revoked, or escalated. |
| `RUNTIME_DRIFT` | Runtime differs from repo/release/config/deployment truth. | Runtime fingerprint, repo fingerprint, config fingerprint, deployment lineage, drift classification. | Block promotion, reconcile through certified release/deploy flow, escalate if lineage unknown. | Drift cleared or classified as blocking. | Converged or fail-closed. |

## Runbook Safety Rules

- If evidence is missing, action is denied except containment and rollback.
- If multiple plausible causes exist, the operator must compare them before remediation.
- If remediation changes runtime, it must be explicitly allowed by a non-architecture execution block or certified operational procedure.
- If verification fails, the problem cannot close as fixed.

## Architecture Decision Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- runbook_storage_format
- runbook_versioning_policy
- runbook_approval_authority
- runbook_ui_surface
```
