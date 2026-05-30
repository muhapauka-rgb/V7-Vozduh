# E32.4.A Concurrency Resource Inventory

resource_inventory_defined=true

## Scope

This inventory defines resources that can conflict when multiple operators, schedulers, or future production-pool flows evaluate or execute batches at the same time.

Concurrency controls are governance controls only. They do not authorize runtime mutation, user movement, routing mutation, autoswitch apply, canary, or cohort execution.

## Resource Inventory

| Resource | Conflict Cause | Severity | Required Protection |
| --- | --- | --- | --- |
| users | Two batches or operators attempt to move the same user, reserve the same user, or rollback the same user concurrently. | CRITICAL | USER_LOCK plus batch membership validation. |
| targets | Multiple batches target the same egress and may overcommit capacity or conflict with target maintenance. | HIGH | TARGET_LOCK for target mutation phases and TARGET_RESERVATION for planned use. |
| capacity | Two approved batches consume the same available capacity before execution-time recheck catches drift. | CRITICAL | CAPACITY_RESERVATION with atomic available-capacity calculation. |
| approval packets | A packet may be replayed, refreshed, cancelled, or consumed concurrently. | CRITICAL | PACKET_LOCK plus replay ledger check. |
| batches | A batch may be executed, cancelled, expired, or rolled back by competing actors. | CRITICAL | BATCH_LOCK and state transition compare-and-set semantics. |
| audit lineage | Concurrent writers can reorder or duplicate audit events if lineage is not append-only and sequenced. | HIGH | AUDIT_LOCK or append-only audit sequencing primitive. |
| reservations | Capacity or target reservations can be double-created, leaked, expired, or released by the wrong owner. | HIGH | RESERVATION ownership, TTL, and owner-scoped release rules. |
| scheduler jobs | Scheduler and operator may both attempt to admit or execute the same batch. | HIGH | SCHEDULER_JOB_LOCK and authority precedence rules. |

## Protection Principles

- USER_LOCK prevents conflicting per-user movement or rollback.
- TARGET_RESERVATION prevents target capacity overcommit before movement.
- PACKET_LOCK prevents concurrent consumption, replay, refresh, or cancellation.
- BATCH_LOCK serializes lifecycle transitions.
- Audit writes must remain append-only and ordered.
- Missing lock, stale lock, unknown owner, or inconsistent reservation state fails closed for forward movement.

## Decision

All listed resources require explicit concurrency protection before production-pool execution can be enabled.
