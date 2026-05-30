# E32.5.B Dispatch Model

dispatch_model_defined=true

## Dispatch Definition

Dispatch is a scheduler handoff to the execution path. Dispatch is not runtime mutation.

## Dispatch Preconditions

A READY schedule may become DISPATCHED only when:

- execution window is valid;
- not_before has passed;
- not_after has not passed;
- dependencies are satisfied;
- locks are available or owner transfer is valid;
- reservations are available and owner-matched;
- packet is valid and non-expired;
- policy is not DENY or REVIEW_REQUIRED;
- capacity is sufficient and not stale/degraded/expired/revoked;
- batch metadata and rollback manifest remain valid;
- execution-time recheck is required before movement.

## Dispatch Actions

Scheduler may:

- update schedule state to DISPATCHED;
- transfer scheduler ownership to execution owner;
- record dispatch audit event;
- pass batch_id, schedule_id, packet_id, reservation ids, and required recheck contract to execution path.

Scheduler may not:

- move users;
- change route tables;
- consume packet as execution;
- skip execution-time recheck;
- bypass locks or reservations;
- alter allowed users, target, rollback target, or blast radius.

## Failed Dispatch

If dispatch preconditions fail:

- schedule remains queued or waiting if recoverable;
- schedule becomes EXPIRED when time window expires;
- schedule becomes FAILED_CLOSED when hard safety gate fails;
- no runtime mutation occurs.

## Decision

dispatch_model_defined=true
