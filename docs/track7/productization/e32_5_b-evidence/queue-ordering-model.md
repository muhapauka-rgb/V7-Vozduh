# E32.5.B Queue Ordering Model

queue_ordering_defined=true

## Evaluated Models

| Model | Strength | Risk |
| --- | --- | --- |
| strict priority | Simple and predictable. | Starvation risk for lower priority batches. |
| weighted priority | Balances priority and fairness. | Requires clear weights and observability. |
| fair queue | Prevents starvation. | May delay urgent operational work. |
| policy-scored queue | Can encode risk and compliance signals. | Policy must remain admission logic, not runtime authority. |

## Recommended Model

Recommended ordering model:

```text
weighted_priority_with_fairness_floor
```

Queue order should be derived from:

- schedule_type;
- emergency_flag;
- requested_start;
- not_before;
- not_after;
- dependency readiness;
- capacity/reservation readiness;
- policy state;
- age in queue;
- fairness floor.

## Ordering Rules

- EMERGENCY may rise in priority only for exact approved scope.
- Policy DENY cannot be reordered into execution.
- REVIEW_REQUIRED cannot dispatch until review is complete.
- Schedules outside their window cannot dispatch regardless of priority.
- Dependency-blocked schedules cannot dispatch regardless of priority.
- Fairness floor prevents indefinite starvation of valid lower-priority schedules.

## Forbidden Ordering Behavior

Scheduler must not:

- choose users;
- choose targets;
- expand batch scope;
- bypass capacity;
- bypass locks;
- bypass packet validity;
- bypass execution-time recheck.

## Decision

queue_ordering_defined=true
