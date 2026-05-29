# E32.2.1 Batch Definition

execution_batch_defined=true

## Definition

An `execution_batch` is a bounded, auditable set of governed runtime actions that may be authorized, executed, observed, rolled back, and replay-denied as one controlled unit.

An execution batch is not authority by itself. It is an architecture object that binds scope, approval, capacity, rollback, evidence, and audit lineage.

## Purpose

The purpose of an execution batch is to make governed movement scalable without weakening the rules proven in one-user, two-user, four-user, and ten-user executions.

It provides:

- exact action scope;
- exact allowed user set;
- exact target set;
- exact movement budget;
- exact rollback manifest;
- exact execution window;
- capacity gate integration;
- audit lineage.

## Required Boundaries

Every batch must be bounded by:

- `allowed_users`;
- `source_targets`;
- `destination_target`;
- `rollback_targets`;
- `movement_budget`;
- `blast_radius`;
- `execution_window`;
- `approval_packet_id`;
- `capacity_requirements`;
- `audit_lineage_id`.

## Relationship To Approval Packet

The approval packet authorizes the batch.

The batch defines the intended scope. The packet binds that scope to fresh runtime truth:

- registry hashes;
- capacity state;
- restore-settle state;
- readiness state;
- selected-move state;
- exact user and target set;
- expiration.

Execution is allowed only when execution-time recheck proves the packet still matches live truth.

## Relationship To Rollback Manifest

Every forward-capable batch must carry a rollback manifest before execution.

Rollback manifest must include:

- exact user set;
- original source target per user;
- route table per user when applicable;
- rollback target per user;
- rollback order if order matters;
- containment rule if forward verification fails.

## Relationship To Capacity

Batch capacity is gated by the certified Capacity Program:

```text
batch_size <= effective_batch_cap
batch_size <= available_capacity
capacity_status == CERTIFIED
capacity_confidence >= required_confidence
```

Capacity does not authorize the batch. It only gates whether the batch can be considered eligible for approval and execution.

## Definition Verdict

Execution batch is defined as a scoped governance container, not a runtime authority.

