# E32.5.B Runtime Impact

scheduler_runtime_impact_defined=true

## Runtime Boundary

Scheduler affects scheduling metadata and ownership handoff only.

```text
scheduler_is_runtime_mutation=false
```

## Allowed Runtime-Adjacent Effects

Scheduler may affect:

- queue state;
- schedule state;
- dispatch state;
- scheduler_owner;
- reservation ownership handoff;
- lock ownership handoff;
- execution handoff metadata;
- schedule audit lineage.

## Forbidden Runtime Effects

Scheduler may not affect:

- users.registry current egress;
- user route tables;
- production assignment;
- target selection;
- policy authority;
- capacity certification;
- packet execution consumption;
- autoswitch apply;
- kill switch state.

## Reservation Ownership

Scheduler may hold or transfer reservation ownership only as part of a batch-owned scheduling flow. It cannot consume capacity for a different batch.

## Lock Ownership

Scheduler may hold scheduler-owned BATCH_LOCK during queue and dispatch transitions. It must transfer ownership explicitly before execution.

## Execution Handoff

Execution handoff includes:

- schedule_id;
- batch_id;
- packet_id;
- owner transfer event;
- reservation ids;
- lock requirements;
- execution-time recheck contract;
- audit_lineage_id.

## Decision

scheduler_runtime_impact_defined=true
