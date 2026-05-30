# E32.5.B Observability

scheduler_observability_defined=true

## Operator View

Operators must see:

- queue;
- queue ordering reason;
- schedule type;
- schedule status;
- blocked batches;
- waiting dependencies;
- waiting windows;
- waiting locks;
- waiting reservations;
- dispatch readiness;
- next safe action.

## Queue View Fields

```text
schedule_id
batch_id
schedule_type
schedule_status
queue_position
priority
requested_start
not_before
not_after
window_status
dependency_status
lock_reservation_status
admission_status
blocked_reason
ready_to_dispatch
next_safe_action
```

## Blocked Batch View

Blocked schedules must show:

- exact blocking gate;
- whether block is recoverable;
- whether block requires human review;
- whether schedule can wait;
- whether schedule should expire;
- whether cancellation is safe;
- whether regeneration is required.

## Dispatch Readiness View

Dispatch readiness must show:

- window valid;
- dependencies satisfied;
- packet valid;
- capacity sufficient;
- policy not DENY/REVIEW_REQUIRED;
- locks/reservations available;
- execution-time recheck required.

## Decision

scheduler_observability_defined=true
