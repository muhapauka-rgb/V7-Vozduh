# E32.5.A Scheduling Lifecycle

scheduling_lifecycle_defined=true

## Lifecycle States

| State | Meaning | Allowed Transitions | Forbidden Transitions | Terminal |
| --- | --- | --- | --- | --- |
| DRAFT | Schedule exists but is not queued. | QUEUED, CANCELLED | DISPATCHED, READY | NO |
| QUEUED | Schedule admitted to queue but not ready. | WAITING_WINDOW, WAITING_DEPENDENCY, WAITING_LOCKS, READY, EXPIRED, CANCELLED, FAILED_CLOSED | DISPATCHED without ready checks | NO |
| WAITING_WINDOW | Waiting for not_before or execution_window. | READY, EXPIRED, CANCELLED, FAILED_CLOSED | DISPATCHED outside window | NO |
| WAITING_DEPENDENCY | Waiting for parent batch result. | READY, EXPIRED, CANCELLED, FAILED_CLOSED | DISPATCHED before dependency success | NO |
| WAITING_LOCKS | Waiting for locks or reservations to clear. | READY, EXPIRED, CANCELLED, FAILED_CLOSED | DISPATCHED with conflict | NO |
| READY | All scheduling preconditions currently pass. | DISPATCHED, EXPIRED, CANCELLED, FAILED_CLOSED | COMPLETED without batch lifecycle | NO |
| DISPATCHED | Scheduler transferred ownership to execution path. | Batch EXECUTING path, FAILED_CLOSED | QUEUED without audit | NO |
| EXPIRED | Schedule expired before dispatch. | none | any forward state | YES |
| CANCELLED | Operator or owning scheduler cancelled. | none | any forward state | YES |
| FAILED_CLOSED | Schedule failed due to hard gate or unsafe ambiguity. | none | READY, DISPATCHED | YES |

## Dispatch Rule

READY is not execution authority. DISPATCHED only means scheduler handed off to the execution path. Execution still requires execution-time recheck, packet validity, locks, reservations, and batch gates.

## Expiration Rule

A schedule expires when:

- not_after passes;
- execution_window closes;
- packet expires;
- dependency timeout occurs;
- emergency TTL expires;
- required metadata becomes invalid and cannot be refreshed safely.

## Decision

scheduling_lifecycle_defined=true
