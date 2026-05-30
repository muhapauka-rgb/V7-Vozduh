# E34.E Guided Rollback Model

guided_rollback_defined=true

## Rollback Principle

Rollback is a safety path with its own evidence, authorization, execution, verification, and closure. It is not an improvised undo.

Rollback remains allowed as containment when forward movement, release promotion, or production admission is denied.

## Rollback Types

| Rollback type | Entry conditions | Required evidence | Verification |
| --- | --- | --- | --- |
| Release rollback | Bad release, failed deployment health, provenance failure, runtime drift after deploy. | Current release, rollback release, manifest, fingerprints, deployment lineage, health checks. | Runtime and config fingerprints match rollback release; lineage records rollback. |
| Configuration rollback | Config regression, invalid config, service failure after config change. | Config snapshot, previous config fingerprint, config diff, service health, audit record. | Config fingerprint matches rollback target and services pass health checks. |
| Governance rollback | Batch failure, partial execution, invalid packet state, lock/reservation inconsistency. | Batch metadata, approval packet, rollback manifest, locks, audit lineage, affected users. | Affected users/routes return to rollback targets and audit chain remains valid. |
| Routing rollback | Routing decision or movement caused degraded access or wrong target. | Affected users, route tables, required services, routing proposal, rollback targets, target health. | Route tables and route_get match rollback targets; no unapproved users changed. |

## Rollback Flow

```text
rollback trigger
-> rollback evidence
-> rollback scope confirmation
-> rollback authorization
-> rollback execution
-> rollback verification
-> rollback closure
```

## Rollback Safety Rules

- Rollback scope must be explicit before action.
- Rollback target must be known and valid.
- Partial rollback requires containment and human review.
- Unknown rollback scope denies forward continuation and allows only containment/escalation.
- Rollback success does not automatically re-certify forward execution.

## Closure Verdicts

- `ROLLBACK_COMPLETED`
- `ROLLBACK_PARTIAL_CONTAINED`
- `ROLLBACK_FAILED_CLOSED`
- `ROLLBACK_ESCALATED`
