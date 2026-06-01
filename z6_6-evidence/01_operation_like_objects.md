# Existing Operation-Like Objects

## Operation-Like Object Inventory

| Object | Strengths | Limitations | Ownership | Reuse Potential |
|---|---|---|---|---|
| Proposal | Has `proposal_id`, affected users, current/proposed target, reason, evidence link, status | Read-only/non-authoritative; does not execute | Admin proposal model | REUSE as pre-operation intent/input |
| Execution contract | Has `contract_id`, status vocabulary, users/targets, rollback manifest, validation/verification states | Preview-only/non-authoritative today; no runtime hooks | Admin execution contract model | REUSE as future contract lineage |
| Execution event | Has `event_id`, event type, contract linkage, status, affected users/targets | Event is not operation by itself | Admin execution event model | REUSE as timeline event identity |
| Operator approval packet | Has `operation_id`, `approval_id`, `packet_id`, expected hashes, expiry, approvals | Zero-move/currently limited; not general movement executor | `admin_core/operator_execution.py` / evidence | REUSE as approval lineage |
| Operator execution audit record | Has `operation_id`, `approval_id`, `packet_id`, verdict, `record_hash`, replay resistance | Append-only governance/audit, not runtime movement truth | `admin_core/operator_execution.py` | REUSE as audit-chain lineage |
| Selected move set | Has selected moves and selected-move hash | Ephemeral in autoswitch; not a full operation | `tools/v7-users-autoswitch` | REUSE as runtime scope/fingerprint |
| Autoswitch plan | Has planner generation, selected moves, barrier status, summary, apply_requested | Not currently linked to operation_id/audit/closure | `tools/v7-users-autoswitch` | REUSE as runtime plan stage |
| Autoswitch apply result | Has applied true/false, reason/results, rc/verify/rollback details | Not currently canonical operation record | `tools/v7-users-autoswitch` | REUSE as runtime terminal source |
| Restore barrier | Has enabled/active/expired/cleared/generation/token/hash/count fields | Not operation by itself; writer/closure fragmented | autoswitch consumes; Admin observes | REUSE as admission/barrier lineage |
| Audit event | Has timestamp, actor, action, component, object_type/object_id, result, request_id, hashes | `v7-audit-log` lacks explicit event_id; event alone not operation | `v7-audit-log` | REUSE as canonical audit evidence |
| Closure record | Has object_type/object_id, closure_state, reason, actor, timestamp | Closure alone does not define runtime truth | Admin closure model | REUSE as closure layer |
| Historical report operation summary | Has report-derived operation_id, state, movement/rollback/restore lineage | Historical/read-only, not live runtime truth | operator observability | REUSE as historical lineage |

## Partial Operation Object Verdict

An operation object partially exists in two places:

1. `operation_id` in operator observability and operator execution packets.
2. Autoswitch plan/apply result as runtime-owned operation facts.

Neither is complete alone.

Canonical Runtime Operation should be a semantic envelope that connects these existing objects by `operation_id` and lineage references.

## Do Not Promote to Operation Identity

- `proposal_id` because a proposal can be observation-only or superseded.
- `contract_id` because contracts are preview/read-only today and may be derived from proposal.
- `approval_id` because multiple approvals/denials can relate to one operation and replay protection should remain approval-scoped.
- selected-move hash because no-op operations and rollback operations may have no selected moves.
- restore-barrier generation because it is an admission/clearance identity, not operation identity.
- audit `object_id` because audit events cover many object types.
- closure key because closure can attach to proposal/evidence/runtime/release/trust/drift, not only operations.

