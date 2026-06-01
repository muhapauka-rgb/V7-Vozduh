# Operation Attributes and Timeline Model

## Mandatory Semantic Attributes

| Attribute | Required? | Owner / Source | Meaning |
|---|---:|---|---|
| `operation_id` | yes | operation semantic envelope / operator lineage | Canonical operation identity. |
| `created_at` | yes | creator/source | Operation lifecycle start timestamp. |
| `runtime_owner` | yes | ownership model | Must be `tools/v7-users-autoswitch` for runtime movement truth. |
| `operation_type` | yes | creator/runtime owner | movement, rollback, no-op, denial, cancellation, expiry, observation-bound runtime decision. |
| `source` | yes | scheduler/Admin/operator/runtime owner | scheduled, admin, operator, rollback, historical. |
| `scope` | yes | runtime owner/Admin intent | Users, targets, selected moves or no-op reason. |
| `planner_generation_id` | conditional | autoswitch | Required when planner stage exists. |
| `selected_move_count` | yes | autoswitch | Zero or nonzero selected move count. |
| `selected_move_hash` | yes | autoswitch/operator recheck | Fingerprint of selected move set; empty hash for zero moves. |
| `runtime_snapshot_hash` | conditional | operator/runtime recheck | Fingerprint for runtime recheck lineage. |
| `proposal_id` | optional | Admin proposal | Link to proposal input. |
| `contract_id` | optional | Admin execution contract | Link to contract/draft lineage. |
| `approval_id` | conditional | operator/Admin approval | Required if operator approval participated. |
| `packet_id` | optional | operator packet | Packet lineage. |
| `restore_barrier` lineage | conditional | autoswitch/Admin | Required if barrier affected admission or clearance. |
| `runtime_state` | yes | runtime owner | Current lifecycle state. |
| `runtime_verdict` | yes after terminal | runtime owner | Terminal runtime result. |
| `rollback_state` | conditional | runtime owner / rollback primitive | Required if rollback was possible, required, started, completed, or failed. |
| `rollback_verdict` | conditional | runtime owner / rollback primitive | Terminal rollback outcome. |
| `audit_verdict` | yes before closure | audit owner / closure owner | Audit complete/insufficient/blocking. |
| `closure_verdict` | yes for lifecycle end | closure owner | Open/verified/closed/expired/reopened semantics. |
| `audit_refs` | yes before closure | `v7-audit-log` / Admin | Canonical audit linkage. |
| `closure_ref` | yes when closed | Admin closure model | Closure object key and closure record info. |
| `evidence_refs` | optional but expected | Admin/operator observability | Evidence/report/supporting refs. |

## Timeline Model

An operation accumulates history as an ordered semantic timeline.

### Planner Stage

Attached by runtime owner.

Required lineage:

- planner generation;
- selected move count/hash;
- candidate/no-op/denial reason;
- policy/trust/capacity/barrier inputs that affected decision.

### Execution Stage

Attached by runtime owner.

Required lineage:

- execution start;
- selected moves executed;
- command/result summaries;
- affected users/targets;
- verification requirement.

### Rollback Stage

Attached by runtime owner or generic rollback primitive under owner boundary.

Required lineage:

- rollback reason;
- rollback scope;
- rollback target;
- rollback result;
- rollback verification/containment.

### Audit Stage

Attached by audit owner.

Required lineage:

- audit action/component;
- object linkage to operation;
- actor/source;
- result;
- timestamp;
- request/object identifiers;
- before/after hashes if relevant.

### Closure Stage

Attached by closure owner.

Required lineage:

- closure object key;
- closure state;
- closure reason;
- closure actor;
- closure timestamp;
- audit reference;
- runtime terminal state reference.

## Timeline Rule

Timeline facts are owned by the component that produces them. The Runtime Operation does not take ownership away from planner, audit, rollback, or closure. It links them.

