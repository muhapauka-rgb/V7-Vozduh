# E34.A Deployment Lineage Model

deployment_lineage_defined=true

## Definition

deployment_lineage is the append-only chain that links release objects to runtime deployments, rollbacks, and certification evidence.

## Required Records

| Record | Purpose |
| --- | --- |
| release_created | Release object created from repo truth. |
| release_certified | Tests/provenance completed. |
| deployment_started | Operator/system began deployment. |
| deployment_completed | Runtime observed expected release/config fingerprints. |
| deployment_failed | Deployment did not converge. |
| drift_detected | Runtime/repo/config mismatch found. |
| rollback_started | Rollback initiated. |
| rollback_completed | Runtime converged to rollback release. |
| release_revoked | Release is no longer safe. |

## Lineage Fields

```text
lineage_event_id
event_type
timestamp
actor
release_id
deployment_id
previous_release_id
runtime_fingerprint_before
runtime_fingerprint_after
config_fingerprint_before
config_fingerprint_after
certification_refs
audit_hash
previous_event_hash
```

## Rollback Lineage

Rollback must preserve:

- source release;
- target rollback release;
- reason;
- runtime fingerprint before rollback;
- runtime fingerprint after rollback;
- config fingerprint after rollback;
- containment status.

## Fail-Closed Rule

If deployment lineage is missing or broken, production deployability status is UNKNOWN/BLOCKING until reconstructed or manually certified.

deployment_lineage_defined=true
