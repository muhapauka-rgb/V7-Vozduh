# E32.2.2 Authoritative Batch Fields

authoritative_fields_defined=true

## Principle

Authoritative batch fields are stored facts. They define scope, identity, user/target boundaries, approval linkage, rollback contract, timing, and audit lineage.

Derived fields may not override authoritative fields.

## Field Matrix

| Field | Purpose | Authority | Update Rule | Validation Rule |
| --- | --- | --- | --- | --- |
| `batch_id` | Unique batch identity | Batch creator | Immutable after creation | Must be unique and prefixed. |
| `batch_type` | Defines permitted action family | Batch creator / policy | Immutable after approval | Must be one known batch type. |
| `batch_generation` | Prevents stale plan reuse | Batch ledger | Increment on replacement | Must match approval packet generation. |
| `batch_status` | Tracks batch lifecycle | Batch ledger | Append-only transition | Must follow allowed status graph. |
| `allowed_users` | Exact users in scope | Approval plan | Immutable after approval | No wildcard; non-empty for movement. |
| `source_targets` | Expected source target per user | Runtime snapshot | Immutable after approval | Must match execution-time recheck. |
| `destination_target` | Exact forward target | Approval plan | Immutable after approval | Must be eligible for batch type. |
| `rollback_targets` | Allowed rollback targets | Approval plan | Immutable after approval | Must cover all affected users. |
| `rollback_manifest` | Executable rollback contract | Approval plan | Immutable after approval except containment addendum | Must be complete before forward execution. |
| `movement_budget` | Max forward user movement | Approval plan | Immutable after approval | For exact movement, equals `len(allowed_users)`. |
| `blast_radius` | Max affected users | Approval plan | Immutable after approval | Must be >= movement budget and exact for movement batches. |
| `approval_packet_id` | Packet binding | Approval system | Set before approval; immutable after | Required before execution authorization. |
| `execution_window` | Time-bounded execution interval | Approval plan | Immutable after approval | Must include `created_at` and expire before execution if stale. |
| `capacity_requirements` | Required target capacity | Capacity gate | Immutable after approval | Must satisfy E32.1 capacity model. |
| `operator_context` | Human-readable reason and program context | Operator / governance record | Append-only notes | Required for operator-driven batches. |
| `audit_lineage_id` | Connects batch to audit records | Audit system | Immutable after creation | Required for approval and execution. |
| `created_at` | Creation timestamp | Batch ledger | Immutable | Must be RFC3339 UTC. |
| `expires_at` | Expiration timestamp | Batch ledger / approval | Immutable after approval | Must be after creation and before execution. |
| `parent_batch_id` | Parent relationship for staged or rollback batch | Batch ledger | Immutable after creation | Required for child batch; nullable otherwise. |
| `child_batch_ids` | Child relationships for staged plans | Batch ledger | Append-only | Children must reference same parent. |

## Authority Boundaries

Batch metadata is authoritative for scope, but not for execution permission.

Execution permission remains derived from:

- approval packet validity;
- execution-time recheck;
- capacity gate;
- runtime gate;
- restore-settle gate;
- audit/replay constraints.

## Update Rules

Safe update types:

- append status transition;
- append audit reference;
- append child batch id;
- append denial reason;
- append containment note.

Unsafe update types:

- changing allowed users after approval;
- changing destination target after approval;
- changing rollback manifest after forward execution without containment record;
- increasing movement budget after approval;
- extending expiry without a fresh approval packet.

## Authoritative Field Verdict

Authoritative fields are defined and maintain exact scope without becoming execution authority.

