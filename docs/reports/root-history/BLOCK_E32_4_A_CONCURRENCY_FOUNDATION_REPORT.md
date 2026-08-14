# BLOCK E32.4.A Concurrency Foundation Report

e32_4_a_completed=true

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

concurrency_foundation_defined=true

resource_inventory_defined=true
lock_model_defined=true
reservation_model_defined=true
ownership_model_defined=true
race_condition_model_defined=true
deadlock_prevention_defined=true

capacity_compatible=true
batches_compatible=true
policy_compatible=true

## Summary

E32.4.A defines the V7 concurrency foundation for future production-pool architecture.

The model covers protected resources, lock ownership, reservation ownership, race-condition prevention, replay-race prevention, deadlock prevention, and integration with Capacity Program, Execution Batches, and Policy Engine.

This block is read-only architecture work. It performed no runtime mutation, user movement, routing mutation, autoswitch apply, UI execution, canary, or cohort execution.

## Foundation Decisions

Concurrency protects:

- users;
- targets;
- capacity;
- approval packets;
- batches;
- audit lineage;
- reservations;
- scheduler jobs.

Concurrency primitives:

```text
USER_LOCK
TARGET_LOCK
BATCH_LOCK
PACKET_LOCK
AUDIT_LOCK
CAPACITY_RESERVATION
TARGET_RESERVATION
BATCH_RESERVATION
```

## Lock Order

```text
1. BATCH_LOCK
2. PACKET_LOCK
3. USER_LOCKS(sorted by canonical user key)
4. TARGET_LOCK
5. AUDIT_LOCK
```

No actor may acquire an earlier lock after holding a later lock.

## Fail-Closed Rules

- Missing required lock denies forward movement.
- Unknown owner denies forward movement.
- Stale lock denies forward movement until recovered with evidence.
- Capacity overcommit denies admission.
- Packet replay race returns DENY_REPLAY.
- Batch double execution is denied by BATCH_LOCK plus state compare-and-set.
- Rollback remains allowed only for exact known rollback scope.

## Integration Verdict

```text
capacity_compatible=true
batches_compatible=true
policy_compatible=true
```

Capacity remains a gate, not an authority. Batches remain the execution workflow. Policy remains admission logic and never becomes runtime mutation authority.

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- lock_storage_backend
- reservation_ledger_storage_backend
- fencing_token_format
- canonical_user_sort_key
- exact_lock_ttl_values
- owner_heartbeat_source
- stale_lock_recovery_authority
- audit_sequence_authority
- scheduler_operator_owner_transfer_protocol
```

## Remaining Open Questions

- Which backend provides atomic lock and reservation semantics?
- Should audit sequencing be native in the audit store or protected by AUDIT_LOCK?
- What lock TTLs should production use for large batches?
- Which service owns owner heartbeat truth?
- Should reservation conflicts auto-expire or always require operator review?

recommended_next_block=E32.4.B_CONCURRENCY_OPERATIONS

## Evidence Files

- `docs/track7/productization/e32_4_a-evidence/concurrency-resource-inventory.md`
- `docs/track7/productization/e32_4_a-evidence/lock-model.md`
- `docs/track7/productization/e32_4_a-evidence/reservation-model.md`
- `docs/track7/productization/e32_4_a-evidence/ownership-model.md`
- `docs/track7/productization/e32_4_a-evidence/race-condition-model.md`
- `docs/track7/productization/e32_4_a-evidence/deadlock-prevention-model.md`
- `docs/track7/productization/e32_4_a-evidence/integration-review.md`
- `docs/track7/productization/e32_4_a-evidence/final-foundation-decision.md`
- `docs/track7/productization/e32_4_a-evidence/tests.md`

## Final Mutation Statement

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO

Autoswitch apply performed manually: NO

Canary performed: NO

Cohort performed: NO
