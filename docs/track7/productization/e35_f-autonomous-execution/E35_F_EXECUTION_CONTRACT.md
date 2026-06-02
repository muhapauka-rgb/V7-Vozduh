# E35.F Execution Contract

## Purpose

The Execution Contract is the mandatory object that turns an approved proposal into an exact bounded action.

Execution without a contract must be impossible.

## Contract Fields

| Field | Purpose | Required |
|---|---|---|
| `contract_id` | Stable unique id | Yes |
| `contract_version` | Schema and generation guard | Yes |
| `created_at` | Creation time | Yes |
| `expires_at` | Short bounded lifetime | Yes |
| `created_by` | System/operator source | Yes |
| `execution_mode` | autonomous, operator_confirmed, rollback, containment | Yes |
| `autonomy_level` | Level 0-4 | Yes |
| `action_type` | forward movement, rollback, containment | Yes |
| `allowed_users` | Exact user set | Yes |
| `allowed_targets` | Exact forward targets | Yes |
| `rollback_manifest` | Exact rollback target per user | Yes |
| `movement_budget` | Max user movement count | Yes |
| `blast_radius` | Max affected user count | Yes |
| `source_evidence_bundle_ids` | Evidence lineage | Yes |
| `source_proposal_id` | Proposal lineage | Yes |
| `authority_verdict_id` | Authority lineage | Yes |
| `conflict_resolution_id` | Conflict lineage | Yes |
| `batch_id` | Batch lineage | Yes |
| `capacity_snapshot_hash` | Capacity binding | Yes |
| `policy_snapshot_hash` | Policy binding | Yes |
| `concurrency_reservation_id` | Lock/reservation binding | Yes |
| `runtime_trust_hash` | Runtime trust binding | Yes |
| `release_trust_hash` | Release trust binding | Yes |
| `users_registry_hash` | Runtime user truth binding | Yes |
| `egress_registry_hash` | Runtime target truth binding | Yes |
| `selected_moves_hash` | Hidden/delayed movement guard | Yes |
| `required_services` | Service requirements per user/group | Yes |
| `validation_requirements` | Deterministic pre-execution gates | Yes |
| `verification_requirements` | Deterministic post-execution checks | Yes |
| `observation_requirements` | Observation window requirements | Yes |
| `audit_requirements` | Required events and records | Yes |
| `replay_nonce` | Replay protection | Yes |
| `consumed_at` | Set after execution starts | Yes after execution |

## Contract Invariants

- `allowed_users` must be exact.
- `allowed_targets` must be exact.
- `movement_budget` must equal or exceed only the allowed user count, never broad wildcard scope.
- `blast_radius` must not exceed the allowed user count unless containment explicitly defines a narrower emergency exception.
- `rollback_manifest` must be complete before forward execution.
- Contract expiry denies forward execution.
- Contract hash mismatch denies execution.
- Replay denies execution.

## Contract Authority

The contract does not authorize itself.

It is valid only if all linked upstream verdicts remain fresh and consistent:

- Authority verdict;
- Conflict resolver;
- Capacity;
- Policy;
- Concurrency;
- Runtime Trust;
- Release Trust;
- Execution-time recheck.

## Contract Verdict

execution_contract_defined=true
runtime_mutation_performed=false
