# E32.4.A Final Foundation Decision

concurrency_foundation_defined=true

## Decision Summary

E32.4.A defines the formal concurrency foundation for V7 production-pool architecture.

The model introduces:

- protected resource inventory;
- owner-scoped lock model;
- reservation model;
- explicit ownership and transfer rules;
- race-condition prevention model;
- deadlock prevention model;
- compatibility with Capacity, Batches, and Policy.

## Certification Markers

```text
resource_inventory_defined=true
lock_model_defined=true
reservation_model_defined=true
ownership_model_defined=true
race_condition_model_defined=true
deadlock_prevention_defined=true
capacity_compatible=true
batches_compatible=true
policy_compatible=true
concurrency_foundation_defined=true
```

## Core Decisions

- Forward movement requires exact locks, valid reservations where applicable, current packet state, fresh runtime truth, and valid batch ownership.
- Rollback remains allowed only for exact known scope when forward movement is denied or containment is required.
- Lock ordering is deterministic and global.
- User locks are acquired in canonical sorted order.
- Packet consumption is single-use and protected by PACKET_LOCK.
- Capacity is reserved atomically to prevent target overcommit.
- Policy can influence admission but cannot own runtime mutation.

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

- Which storage backend provides atomic lock and reservation semantics?
- Should audit sequencing be native in the audit store or protected by AUDIT_LOCK?
- What lock TTLs should production use for large batches?
- Which service owns owner heartbeat truth?
- Should reservation conflicts auto-expire or always require operator review?

## Final Decision

concurrency_foundation_defined=true

recommended_next_block=E32.4.B_CONCURRENCY_OPERATIONS
