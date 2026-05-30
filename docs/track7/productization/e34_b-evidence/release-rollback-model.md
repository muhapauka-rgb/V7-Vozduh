# E34.B Release Rollback Model

release_rollback_model_defined=true

## Definition

release rollback is the governed return from a deployed release to a known rollback release object.

## Rollback Identity

Each production release must include:

```text
rollback_release_id
rollback_release_fingerprint
rollback_compatibility_notes
rollback_required_config_fingerprint
rollback_preconditions
rollback_verification_steps
```

## Rollback Lineage

Rollback lineage records:

```text
rollback_event_id
source_release_id
target_release_id
reason
actor
started_at
completed_at
runtime_fingerprint_before
runtime_fingerprint_after
config_fingerprint_before
config_fingerprint_after
verification_result
previous_lineage_hash
```

## Rollback Provenance

Rollback target must itself be a release object with known provenance.

If rollback target is unknown, rollback may still be performed as emergency containment, but commercial certification remains degraded until lineage is reconstructed.

## Rollback Verification

Rollback is complete only when:

- runtime fingerprint matches rollback release expectation;
- config fingerprint matches rollback config expectation;
- runtime checkers pass;
- deployment lineage records rollback completed;
- operator visibility shows converged rollback release.

release_rollback_model_defined=true
