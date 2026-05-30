# E32.4.A Ownership Model

ownership_model_defined=true

## Ownership Principles

Ownership defines who may update, release, consume, or transition a protected resource.

Policy is not an owner of runtime mutation. Policy may influence admission decisions only.

## Ownership Table

| Object | Owner | Transfer Rules | Forbidden Transfers |
| --- | --- | --- | --- |
| lock | The actor that acquired it with a valid fencing token. | May transfer only through a recorded handoff event from scheduler to executor or executor to rollback controller. | Cannot transfer to policy, autoswitch, or unknown actor. |
| reservation | batch_id that created it. | May be released by the owning batch or emergency containment with audit record. | Cannot be consumed by a different batch. |
| approval packet | batch_id and packet_id pair. | May be refreshed only by the owning batch before execution; consumed once during approved execution. | Cannot be reused across batches or users outside allowed set. |
| batch | batch_id. | May move from operator ownership to scheduler ownership only if scheduled execution is explicitly approved. | Cannot be implicitly taken over by autoswitch or rebalance. |
| audit lineage | append-only audit writer with sequence authority. | Writer implementation may rotate, but sequence authority must be continuous. | Cannot rewrite or reorder prior events. |

## Owner Identity

Allowed owner identity forms:

```text
operator_session_id
scheduler_job_id
batch_id
rollback_operation_id
maintenance_operation_id
audit_writer_id
```

Unknown owner identity fails closed.

## Ownership Transfer Requirements

Every transfer must include:

- previous_owner;
- next_owner;
- object_id;
- fencing_token_before;
- fencing_token_after;
- reason;
- timestamp;
- audit_event_hash.

## Authority Boundaries

- Capacity may deny or constrain ownership but cannot move users.
- Batch may own execution workflow but cannot bypass policy or capacity gates.
- Policy may admit, deny, or require review but cannot own runtime mutation.
- Scheduler may own scheduled execution only after packet, reservation, capacity, runtime, and policy gates are valid.

## Decision

Ownership is explicit, auditable, non-implicit, and never transferred to policy, autoswitch, or unknown actors.
