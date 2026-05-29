# E32.2.3 Observation Flow

observation_flow_defined=true

## Purpose

Observation flow validates the runtime after forward execution.

It ensures no delayed movement, hidden mover, route drift, or audit gap appears before rollback or completion.

## Entry

```text
EXECUTING -> OBSERVING
```

Entry requires:

- forward command or transaction completed;
- forward verification passed or identified exact rollback scope;
- audit forward event written;
- affected user set known.

## Required Samples

Minimum observation for proof-style batches:

```text
sample_count >= 3
```

Each sample should collect:

- current target per approved user;
- target users count;
- selected moves;
- hidden movers;
- runtime checkers;
- route_get or route state when applicable;
- target readiness when applicable;
- audit tail.

## Delayed Monitoring

Delayed monitoring may occur:

- during observation for retained batches;
- after rollback for proof-style batches;
- after containment for failure paths.

It must verify:

```text
delayed_movement_observed=false
unapproved_user_movement=false
routing_drift=false
runtime_checkers_ok=true
```

## Replay Readiness

Replay validation must be possible after forward execution has created an audit record.

Observation should ensure:

```text
packet_consumed_state_recorded=true
forward_event_auditable=true
```

## Audit Completion

Observation evidence must be attached to audit lineage before the batch can close.

## Exit Paths

Proof-style successful forward:

```text
OBSERVING -> ROLLBACK_READY
```

Future retained production-pool batch:

```text
OBSERVING -> COMPLETED
```

Observation failure:

```text
OBSERVING -> ROLLBACK_READY
```

or if no exact rollback scope:

```text
OBSERVING -> FAILED_CLOSED
```

## Observation Verdict

Observation flow is defined.

