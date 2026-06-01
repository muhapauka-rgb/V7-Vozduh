# Z7.2 Evidence 00 - Lineage Inventory

Program: PROGRAM Z7.2 - Operation Wiring Design  
Project: V7 Vozduh  
Branch target: v7-next  
Mode: READ ONLY design

## Discovery Gate Result

Existing lineage, metadata, IDs, hashes, references, audit metadata, closure metadata, runtime outputs, rollback outputs, and selected-move outputs were inventoried before designing wiring.

Baseline from Z7.1:

```text
Runtime -> Operation -> Audit -> Closure
PARTIAL -> PARTIAL -> PARTIAL -> PARTIAL
```

## Existing IDs and Hashes

| Field | Current Owner | Current Reality | Classification |
|---|---|---|---|
| `operation_id` | Operator/governance/historical model | Exists outside live autoswitch runtime | REUSE, EXTEND |
| `proposal_id` | Admin proposal layer | Proposal/evidence lineage | REUSE |
| `approval_id` | Operator execution governance | Packet replay/audit identity | REUSE |
| `packet_id` | Operator execution governance | Packet lineage | REUSE |
| `contract_id` | Admin execution contract store | Read-only/non-authoritative execution model | REUSE, DO NOT PROMOTE |
| `event_id` | Admin execution event store | Read-only event identity | REUSE |
| `request_id` | `v7-audit-log`, Admin event normalization | Audit correlation identity | REUSE |
| `record_hash` | Operator execution governance | Append-only governance audit hash | REUSE |
| `planner_generation_id` | `tools/v7-users-autoswitch` | Runtime input generation hash | REUSE |
| `selected_move_hash` | `tools/v7-users-autoswitch`, operator recheck | Internal/expected selected-move fingerprint | REUSE, EXTEND |
| `runtime_snapshot_hash` | `admin_core/operator_execution.py` | Governance recheck hash, not live autoswitch hash | REUSE, EXTEND |
| `before_hash` / `after_hash` | `v7-audit-log` | Audit metadata fields | REUSE |
| closure object key | Admin closure model | `object_type:object_id` | REUSE |

## Existing Runtime Outputs

`tools/v7-users-autoswitch` already emits:

- runtime plan root JSON,
- `summary`,
- `selected_moves`,
- `safety.generation.planner_generation_id`,
- `safety.restore_barrier`,
- `apply_result`,
- move results,
- verification results,
- rollback results.

Missing from live runtime output:

- `operation_id`,
- operation lifecycle state,
- canonical selected move hash on every operation,
- canonical runtime snapshot hash,
- audit references,
- closure references.

## Existing Audit Metadata

`v7-audit-log` already supports:

- `request_id`,
- `object_type`,
- `object_id`,
- `user_ip`,
- `result`,
- `before_hash`,
- `after_hash`,
- arbitrary `metadata`.

Design implication:

- `operation_id` does not require a new audit schema owner.
- It can be carried as `object_id` when `object_type=runtime_operation`, and also inside `metadata.operation_id`.

## Existing Closure Metadata

Admin closure model supports:

- `object_type`,
- `object_id`,
- `closure_state`,
- `closure_reason`,
- `closure_actor`,
- `closure_timestamp`,
- closure audit through `audit_admin`.

Design implication:

- Runtime operation closure can reuse `object_type=runtime` or a narrowed existing-compatible object convention such as `runtime_operation` only if Admin closure allow-list later accepts it.
- To avoid new truth source in design, the closure key should be operation-owned: `object_id=<operation_id>`.

## Duplication Audit

Planned wiring must not create:

- a new operation store,
- a new audit sink,
- a new closure store,
- a new rollback store,
- a new selected move owner,
- a new runtime owner,
- a new scheduler,
- a second lifecycle engine.

Planned wiring is safe if it only extends existing runtime output and existing metadata fields.

