# Duplication And Identifier Audit

## Existing Identifiers

| Identifier | Owner | Meaning | Conflict With `operation_id`? |
|---|---|---|---|
| `planner_generation_id` | `tools/v7-users-autoswitch` | Hash of planner inputs | No; should be referenced by operation |
| `selected_move_hash` / clearance selected hash | Autoswitch restore-barrier logic | Fingerprint of selected move set | No; should be lineage attribute |
| `runtime_snapshot_hash` | `admin_core/operator_execution.py` | Hash of registry hashes + selected move hash for zero-budget recheck | Potential semantic overlap; do not redefine differently without naming scope |
| `request_id` | `tools/runtime-support/v7-audit-log`, Admin audit | Audit event/request correlation id | No; audit event id, not runtime operation id |
| `operation_id` in P2.7/Admin/operator views | Admin/operator candidate workflow | Candidate/preview operation id for productized workflow | Potential naming collision; runtime autoswitch id must be scoped/type-qualified |
| `event_id` | Admin execution/event views | Execution event id | No |
| `record_hash` | `admin_core/operator_execution.py`, `admin_core/operator_observability.py` | Hash-chain record identity | No; operation can reference record hash |
| `contract_id` | Execution contracts | Stored execution contract identity | No; not runtime autoswitch cycle |
| `approval_id` | Operator rehearsal/governance preview | Approval packet identity | No |
| `proposal_id` | Candidate/proposal surfaces | Proposal identity | No |
| `packet_id` | Approval packet docs/models | Packet identity | No |
| `correlation_id` | `tools/v7-observability-summary` | Observability summary correlation | No direct conflict |

## Operation Envelope Duplication Risk

The proposed operation envelope would duplicate existing structures if it attempts to become:

- an operation store,
- a replacement for `apply_result`,
- a replacement for audit JSONL,
- a replacement for Admin closure,
- a replacement for selected-move state files,
- a replacement for runtime recheck packet hashes.

It does not duplicate existing truth if constrained to:

- one in-cycle lineage object in autoswitch output,
- references to existing `planner_generation_id`,
- references to selected move hash,
- references to `runtime_snapshot_hash`,
- references to existing audit/closure targets.

## `operation_id` Naming Boundary

`operation_id` already exists in Admin/operator candidate workflows. Runtime autoswitch can still add an `operation_id` if the envelope makes the type explicit:

```text
operation_type = "runtime_autoswitch"
operation_owner = "tools/v7-users-autoswitch"
```

Recommended id semantics:

- one operation id per autoswitch runtime cycle,
- not equal to `request_id`,
- not equal to `planner_generation_id`,
- stable for one emitted output,
- derived from runtime owner + generation + selected move hash + timestamp or run nonce,
- never used as a new persisted store key unless future phases explicitly approve that.

## Terminal State Duplication

`apply_result.applied` and `apply_result.reason` already encode terminal/no-op status. A new `terminal_state` duplicates them unless it is a normalized derivative.

Safe model:

- keep `apply_result` unchanged,
- derive `operation.terminal_state` from `apply_result`,
- derive `operation.terminal_reason` from existing no-op/apply/verify/rollback facts.

Unsafe model:

- letting `terminal_state` contradict `apply_result`,
- making Admin read `terminal_state` instead of `apply_result` before tests cover migration.

## Truth Source Verdict

No duplicate operation truth is needed. The only safe target is output lineage wiring inside the existing autoswitch runtime owner.
