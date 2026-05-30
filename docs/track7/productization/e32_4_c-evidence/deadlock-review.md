# E32.4.C Deadlock Review

deadlock_prevention_valid=true

## Reviewed Controls

The deadlock review verified:

- global lock ordering;
- sorted user lock acquisition;
- lock timeout strategy;
- stale lock handling;
- owner transfer model;
- recovery behavior.

## Lock Ordering

Certified lock order:

```text
1. BATCH_LOCK
2. PACKET_LOCK
3. USER_LOCKS(sorted by canonical user key)
4. TARGET_LOCK
5. AUDIT_LOCK
```

No actor may acquire an earlier lock after holding a later lock.

## Timeout and Stale Lock Strategy

Locks require:

- TTL;
- owner identity;
- fencing token;
- purpose;
- resource identity;
- recovery audit event.

Stale locks deny forward movement until owner inactivity and safe recovery are proven.

## Owner Transfer Compatibility

Owner transfer remains compatible because:

- transfer is atomic relative to BATCH_LOCK;
- transfer cannot change allowed users, target, rollback target, or blast radius;
- transfer requires fencing token refresh and audit event;
- failed transfer leaves batch fail-closed for forward movement.

## Decision

deadlock_prevention_valid=true
