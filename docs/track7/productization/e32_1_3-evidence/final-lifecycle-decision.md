# E32.1.3 Final Lifecycle Decision

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

capacity_certification_lifecycle_defined=true

## Lifecycle

```text
UNCERTIFIED
  -> CANDIDATE
  -> VALIDATING
  -> CERTIFIED
  -> STALE
  -> RECERTIFYING
  -> CERTIFIED
```

Safety branches:

```text
CERTIFIED -> DEGRADED -> RECERTIFYING -> CERTIFIED
CERTIFIED -> EXPIRED -> RECERTIFYING -> CERTIFIED
CERTIFIED -> REVOKED -> CANDIDATE only after incident review
```

## Certification Authority

Current:

```text
OPERATOR_PLUS_EVIDENCE
```

Future:

```text
POLICY_ENGINE_WITH_OPERATOR_GOVERNANCE
```

## Promotion

Promotion requires complete evidence for the requested class. Metadata may record promotion only after validation and proof are accepted.

## Demotion

Demotion can be automatic on stale, degraded, expired, or revoked signals. Demotion always fails closed for forward movement.

## Recertification

Recertification depends on prior state:

- STALE requires refresh evidence.
- DEGRADED requires root-cause remediation and validation.
- EXPIRED requires full validation.
- REVOKED requires incident review and restart from CANDIDATE.

## Evidence

CERTIFIED requires:

- target-local validation;
- long-window validation;
- readiness GO;
- restore-settle GO;
- runtime checkers OK;
- class-sized governed movement proof;
- rollback proof;
- delayed monitoring;
- replay denial;
- audit chain validation.

## Architecture Decision Required

One decision remains open for future large classes:

```text
ARCHITECTURE_DECISION_REQUIRED=large_scale_certification_authority_for_CLASS_50_CLASS_100_AND_PRODUCTION_POOL
recommended_option=staged_production_pool_proof_after_policy_engine_controls_are_certified
```

This does not block E32.1.3 because current CLASS_10 and below use exact movement proof.

recommended_next_block=E32_1_4_CAPACITY_VALIDATION_METHODOLOGY

