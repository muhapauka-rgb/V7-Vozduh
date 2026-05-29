# E32.1.2 Final Model Decision

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

capacity_metadata_model_defined=true

## Final Metadata Shape

Recommended target-level capacity object:

```yaml
capacity:
  capacity_class: CLASS_10
  certified_capacity: 10
  capacity_status: CERTIFIED
  capacity_confidence: HIGH
  soft_limit: 10
  hard_limit: 10
  active_policy_cap: 10
  effective_batch_cap: 10
  current_capacity: 10
  available_capacity: 10
  capacity_reserved: 0
  max_concurrent_packets: 1
  capacity_validation_time: "<iso8601>"
  capacity_stale_after: "<iso8601>"
  capacity_expiration: "<iso8601>"
  capacity_validation_method:
    - TARGET_LOCAL_PROBE
    - LONG_WINDOW
    - GOVERNED_MOVEMENT_PROOF
    - ROLLBACK_REPLAY_RESTORE_PROOF
  capacity_validation_evidence:
    reports:
      - BLOCK_E30_2_TEN_USER_CAPACITY_REQUALIFICATION_AND_APPROVAL_PACKET_PREPARATION_REPORT.md
      - BLOCK_E30_3_FIRST_TEN_USER_GOVERNED_MOVEMENT_REPORT.md
      - BLOCK_E31_POST_TEN_USER_GOVERNANCE_REVIEW_REPORT.md
    evidence_dirs:
      - docs/track7/productization/e30_2-evidence
      - docs/track7/productization/e30_3-evidence
      - docs/track7/productization/e31-evidence
  capacity_validation_version: E32.1.2
```

## Authoritative Fields

- `capacity_class`
- `certified_capacity`
- `capacity_status`
- `capacity_confidence`
- `soft_limit`
- `hard_limit`
- `active_policy_cap`
- `capacity_validation_time`
- `capacity_stale_after`
- `capacity_expiration`
- `capacity_validation_method`
- `capacity_validation_evidence`
- `capacity_validation_version`
- `max_concurrent_packets`

## Derived Fields

- `effective_batch_cap`
- `current_capacity`
- `available_capacity`
- `target_users_count`
- `last_readiness_status`
- `last_restore_settle_status`
- `last_runtime_checkers_status`
- `is_execution_eligible`

## Status Model

Allowed statuses:

```text
UNKNOWN
CANDIDATE
VALIDATING
CERTIFIED
STALE
DEGRADED
EXPIRED
```

Only fresh `CERTIFIED` status permits nonzero forward movement capacity.

## Freshness

Initial bounded-operator defaults:

```text
capacity_stale_after=24h
capacity_expiration=7d
approval_packet_ttl=30m
```

Initial production-pool defaults:

```text
capacity_stale_after=6h
capacity_expiration=24h
approval_packet_ttl=15m or scheduler transaction TTL
```

## Governance Integration

Approval packets must bind capacity metadata, but execution-time recheck must recompute effective capacity and fail closed on conflicts.

Rollback remains allowed even if capacity becomes stale or degraded.

## Decision

capacity_metadata_model_defined=true
required_fields_defined=true
authoritative_vs_derived_defined=true
capacity_status_model_defined=true
freshness_model_defined=true
governance_integration_defined=true
future_compatibility_confirmed=true

recommended_next_block=E32_1_3_CAPACITY_CERTIFICATION_LIFECYCLE

