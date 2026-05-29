# BLOCK E32.1.2 Capacity Metadata Model Report

e32_1_2_completed=true

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

capacity_metadata_model_defined=true
required_fields_defined=true
authoritative_vs_derived_defined=true
capacity_status_model_defined=true
freshness_model_defined=true
governance_integration_defined=true
future_compatibility_confirmed=true

## Summary

E32.1.2 defines the formal metadata model for V7 capacity governance. The model separates historical certification from current execution eligibility and prevents metadata alone from authorizing movement.

The current certified target remains:

```text
target=amneziawg-exec-20260528-10-8-1-14
capacity_class=CLASS_10
certified_capacity=10
soft_limit=10
hard_limit=10
capacity_confidence=HIGH
```

## Required Fields

Core authoritative fields:

- `capacity_class`
- `certified_capacity`
- `capacity_status`
- `capacity_confidence`
- `soft_limit`
- `hard_limit`
- `active_policy_cap`
- `capacity_validation_time`
- `capacity_validation_method`
- `capacity_validation_evidence`
- `capacity_validation_version`
- `capacity_stale_after`
- `capacity_expiration`
- `max_concurrent_packets`

Core derived fields:

- `effective_batch_cap`
- `current_capacity`
- `available_capacity`
- `target_users_count`
- `last_readiness_status`
- `last_restore_settle_status`
- `last_runtime_checkers_status`
- `is_execution_eligible`

## Status Model

Defined states:

```text
UNKNOWN
CANDIDATE
VALIDATING
CERTIFIED
STALE
DEGRADED
EXPIRED
```

Only fresh `CERTIFIED` capacity permits forward movement approval. All other states fail closed for forward movement.

## Freshness Model

Initial bounded-operator TTLs:

```text
capacity_stale_after=24h
capacity_expiration=7d
approval_packet_ttl=30m
```

Initial production-pool TTLs:

```text
capacity_stale_after=6h
capacity_expiration=24h
approval_packet_ttl=15m or scheduler transaction TTL
```

Historical certification remains as audit truth, but operational eligibility expires.

## Governance Integration

Approval packets must bind capacity metadata:

- class;
- hard limit;
- policy cap;
- effective cap;
- validation evidence;
- expiration;
- registry hashes;
- readiness and restore-settle state.

Execution-time recheck must recompute current metadata and deny execution on stale, degraded, expired, or mismatched capacity state.

Rollback remains allowed during stale/degraded states as containment.

## Future Compatibility

The model supports:

- capacity classes;
- execution batches;
- future policy engine caps;
- scheduler reservations;
- max concurrent packet controls;
- production-pool architecture.

It does not grant production-pool authority by itself.

## Remaining Open Questions

- exact storage location for the capacity object;
- whether capacity metadata should live inline in `egress.registry` or in a sidecar state file;
- exact schema versioning mechanism;
- whether production-pool TTLs should be policy-specific or global;
- future reservation ledger storage and cleanup semantics.

recommended_next_block=E32_1_3_CAPACITY_CERTIFICATION_LIFECYCLE

## Evidence Files

- `docs/track7/productization/e32_1_2-evidence/current-metadata-intake.md`
- `docs/track7/productization/e32_1_2-evidence/required-capacity-fields.md`
- `docs/track7/productization/e32_1_2-evidence/authoritative-vs-derived.md`
- `docs/track7/productization/e32_1_2-evidence/capacity-status-model.md`
- `docs/track7/productization/e32_1_2-evidence/freshness-and-expiration.md`
- `docs/track7/productization/e32_1_2-evidence/governance-integration.md`
- `docs/track7/productization/e32_1_2-evidence/future-compatibility-review.md`
- `docs/track7/productization/e32_1_2-evidence/final-model-decision.md`
- `docs/track7/productization/e32_1_2-evidence/tests.md`

## Final Mutation Statement

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO

Autoswitch apply performed manually: NO

Canary performed: NO

Cohort performed: NO

