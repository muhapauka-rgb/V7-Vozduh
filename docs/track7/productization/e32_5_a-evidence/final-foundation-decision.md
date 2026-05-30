# E32.5.A Final Foundation Decision

scheduling_foundation_defined=true

## Decision Summary

E32.5.A defines the Scheduling Foundation for V7.

Scheduling is the time-ordering and dispatch-preparation layer. It is not runtime mutation authority and it is not Routing Intelligence.

## Certification Markers

```text
prior_architecture_loaded=true
scheduling_model_defined=true
schedule_type_taxonomy_defined=true
scheduling_metadata_model_defined=true
scheduling_lifecycle_defined=true
queue_admission_foundation_defined=true
dependency_model_defined=true
capacity_compatible=true
batches_compatible=true
policy_compatible=true
concurrency_compatible=true
routing_intelligence_future_compatible=true
scheduling_foundation_defined=true
```

## Core Decisions

- Scheduler is not authority.
- Scheduler is not runtime mutation.
- Scheduler is time-ordering layer.
- Scheduler does not choose users or targets.
- Scheduler does not bypass policy, capacity, locks, reservations, packets, execution-time recheck, rollback manifest, or audit.
- READY is not execution authority.
- DISPATCHED is a handoff to execution path, not movement.
- Dependencies must be acyclic and auditable.
- Expired schedules fail closed.

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- schedule_storage_backend
- queue_ordering_algorithm
- priority_weight_schema
- maintenance_window_source
- schedule_expiration_ttl_defaults
- dependency_graph_storage
- scheduler_owner_identity_model
- schedule_observability_schema
- emergency_schedule_authority
```

## Remaining Open Questions

- Which backend owns schedule metadata and queue state?
- Should queue ordering be strict priority, weighted fair, or policy-scored?
- How are maintenance windows sourced and audited?
- What TTLs should each schedule type use?
- Who may authorize emergency schedules?

## Final Decision

scheduling_foundation_defined=true

recommended_next_block=E32.5.B_SCHEDULING_OPERATIONS
