# PROGRAM Z6.6 Existing Identity Discovery

Project: V7 Vozduh
Program: Z6.6 - Runtime Operation Model Design
Mode: READ ONLY
Date: 2026-06-02

## Constraint

Operation semantics only. No implementation, APIs, storage, runtime mutation, deploy, autoswitch apply, user movement, routing mutation, service restart, systemd/timer modification, cleanup, merge, or force push.

## Existing Identifiers

| Identifier | Owner | Scope | Lifetime | Truth Source | Collision Risk | Reuse Suitability |
|---|---|---|---|---|---:|---|
| `operation_id` | operator observability / execution packets / historical reports | Operation-like lineage identifier | Long-lived historical/operator lifecycle | `admin_core/operator_observability.py`, operator packets, reports | MEDIUM if report-derived only | REUSE as canonical semantic operation identity |
| `proposal_id` | Admin proposal model | Proposal input | Proposal lifecycle | `admin/v7-admin-api` proposal records | LOW when hash-derived | REUSE as linked input, not operation identity |
| `contract_id` | Admin execution contract model | Preview/execution contract | Contract lifecycle | `admin/v7-admin-api` execution contracts | LOW when hash-derived | REUSE as contract lineage, not operation identity |
| `event_id` | Admin execution event model | Execution event | Event lifecycle | execution event store | LOW when hash-derived | REUSE as event identity |
| `approval_id` | operator execution packet / audit chain | Operator approval/replay boundary | Approval validity window and replay history | `admin_core/operator_execution.py` | LOW when stable hash-derived | REUSE as approval/replay identity |
| `packet_id` | operator execution packet | Approval packet | Packet lifetime | operator packet evidence | MEDIUM | REUSE as packet lineage |
| `record_hash` | operator execution audit chain | Audit chain record | Permanent append-only record lineage | `admin_core/operator_execution.py` | LOW | REUSE as audit-chain integrity identity |
| `runtime_action_record_hash` | operator execution runtime-governance record | Zero-move runtime governance action | Permanent append-only governance record | `admin_core/operator_execution.py` | LOW | REUSE as support identity |
| `planner_generation_id` | autoswitch planner | Planner input generation | Valid until inputs change | `tools/v7-users-autoswitch` | LOW | REUSE as runtime generation identity |
| `selected_moves_hash` / `selected_move_hash` | autoswitch / operator execution | Selected move set | Valid for exact move set/generation | autoswitch plan; operator recheck | LOW | REUSE as selected-move fingerprint |
| `users_registry_hash` | operator execution / autoswitch generation inputs | User registry snapshot | Valid until registry changes | state file hash | LOW | REUSE as runtime fingerprint |
| `egress_registry_hash` | operator execution / autoswitch generation inputs | Egress registry snapshot | Valid until registry changes | state file hash | LOW | REUSE as runtime fingerprint |
| `runtime_snapshot_hash` | operator execution | Combined registry + selected-move snapshot | Valid until runtime snapshot changes | operator runtime recheck | LOW | REUSE as runtime snapshot identity |
| restore-barrier generation fields | autoswitch | Barrier clearance/generation identity | Barrier clearance lifetime | `autoswitch-restore-barrier.json` interpreted by autoswitch | MEDIUM if writer fragmented | REUSE as barrier lineage |
| `generation_token` | restore barrier | Clearance authorization marker | Until clearance expiry | barrier state | MEDIUM | REUSE as clearance proof, not operation identity |
| closure key `object_type:object_id` | Admin closure model | Closure object | Closure history lifetime | Admin closure records | MEDIUM if object_id not operation_id | REUSE for closure identity |
| audit `object_type/object_id/request_id` | `v7-audit-log` | Audit event linkage | Audit event lifetime | audit JSONL | MEDIUM because no first-class event_id in `v7-audit-log` | REUSE as audit linkage fields |
| `evidence_id` / `bundle_id` | Admin evidence/operator observability | Evidence references | Evidence lifecycle | evidence model/operator observability | LOW/MEDIUM | REUSE as evidence identity |

## Identity Verdict

No single current object fully owns Runtime Operation identity.

The closest existing identity is `operation_id`, already used by:

- historical operation summaries;
- operator observability detail/export/governance/rehearsal previews;
- operator execution packets;
- audit-chain records.

Z6.6 therefore defines `operation_id` as the canonical semantic operation identity, not as a new storage object.

All other IDs become lineage IDs attached to the operation.

