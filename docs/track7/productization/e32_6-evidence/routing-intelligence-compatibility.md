# E32.6 Routing Intelligence Compatibility

routing_intelligence_future_compatible=true

## Future Routing Intelligence Role

Routing Intelligence may later:

- propose movement;
- propose target;
- propose evacuation;
- propose rebalance;
- score candidates;
- recommend timing inputs.

## Routing Intelligence Boundary

Routing Intelligence may not:

- bypass policy;
- bypass capacity;
- bypass batch;
- bypass concurrency;
- bypass scheduler;
- bypass execution-time recheck;
- bypass approval packet;
- mutate runtime;
- move users;
- change routing.

## Attachment Model

Routing Intelligence should attach before Batch/Policy as an advisory proposal source.

The output of Routing Intelligence must become a proposed batch, then pass through:

```text
Batch -> Policy -> Capacity -> Concurrency -> Scheduling -> Execution-Time Recheck -> Execution
```

## Decision

routing_intelligence_future_compatible=true
