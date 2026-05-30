# E34.C Operator Recovery Model

operator_recovery_defined=true

## Guided Recovery

Operator workflow:

1. Select disaster or restore scenario.
2. Choose backup candidate.
3. Verify backup fingerprint and freshness.
4. Inspect backup scope completeness.
5. Select target release or rollback release.
6. Restore in read-only/containment mode.
7. Run restore verification.
8. Review drift and lineage status.
9. Promote to production only after convergence.

## Guided Verification

Operator must see:

- backup id and fingerprint;
- backup certification status;
- release id and fingerprint;
- config fingerprint;
- deployment lineage;
- audit lineage;
- restore status;
- blocked reasons;
- next safe action.

## Rollback Recovery

Rollback recovery uses the release rollback model:

```text
backup -> rollback_release_object -> restored_config -> runtime convergence -> rollback lineage
```

If rollback provenance is incomplete, operator may perform emergency containment but commercial status remains degraded.

## Evidence Collection

Every restore attempt must record:

```text
restore_event_id
operator
backup_id
release_id
restore_scope
started_at
completed_at
verification_result
drift_findings
lineage_result
next_safe_action
```

operator_recovery_defined=true
