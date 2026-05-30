# E32.5.B Production Pool Compatibility

production_pool_compatible=true
routing_intelligence_future_compatible=true

## Capacity Program Compatibility

Scheduler is compatible with Capacity Program:

- it reads capacity state;
- it respects effective_batch_cap;
- it respects capacity reservation state;
- it cannot certify or override capacity;
- it blocks dispatch when capacity is impossible or stale.

## Execution Batches Compatibility

Scheduler is compatible with Execution Batches:

- it queues and dispatches batch objects;
- it does not alter batch scope;
- it does not bypass batch lifecycle;
- DISPATCHED is a handoff into batch execution path.

## Policy Engine Compatibility

Scheduler is compatible with Policy Engine:

- DENY blocks queue admission or dispatch;
- REVIEW_REQUIRED blocks dispatch;
- policy remains admission logic;
- scheduler does not become policy authority.

## Concurrency Controls Compatibility

Scheduler is compatible with Concurrency Controls:

- it respects locks;
- it respects reservations;
- it uses owner transfer;
- lock/reservation conflicts block dispatch.

## Production Pool Compatibility

Scheduling operations support production-pool needs:

- queued batch ordering;
- execution window enforcement;
- dependency resolution;
- dispatch readiness;
- blocked batch observability;
- fail-closed dispatch denial.

production_pool_compatible=true

## Routing Intelligence Future Compatibility

Scheduler remains separate from Routing Intelligence.

Routing Intelligence may later propose batches, but scheduler only orders, waits, blocks, or dispatches prepared/admissible batches.

routing_intelligence_future_compatible=true
