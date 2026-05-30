# E32.5.C Future Compatibility

production_pool_compatible=true
routing_intelligence_future_compatible=true

## Production Pool Compatibility

Scheduling is compatible with future Production Pool because it defines:

- queue admission;
- queue ordering;
- dispatch handoff;
- execution windows;
- dependency resolution;
- blocked batch observability;
- fail-closed dispatch denial;
- owner handoff into execution path.

production_pool_compatible=true

## Routing Intelligence Future Compatibility

Scheduling remains separate from Routing Intelligence.

Routing Intelligence may later propose reasons, candidate users, or target recommendations, but scheduler only orders and dispatches prepared/admissible batches.

Scheduler cannot select users or targets and cannot turn a Routing Intelligence proposal into movement without the full governance path.

routing_intelligence_future_compatible=true

## Decision

production_pool_compatible=true
routing_intelligence_future_compatible=true
