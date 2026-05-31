# P3.A Dry-Run Contract Model

Project: V7 Vozduh
Block: P3.A Runtime Dry-Run Foundation

## Purpose

A Dry-Run Contract is a non-executable snapshot of runtime evidence, evaluated decision, simulation, verification and rollback previews.

It is not an execution contract and must not be accepted by any executor.

## Contract Fields

| Field | Meaning |
| --- | --- |
| `contract_id` | Stable dry-run contract id. |
| `created_at` | Report creation time. |
| `source_event_ids` | Normalized event ids used as input. |
| `input_snapshot_refs` | References to canonical state inputs. |
| `input_snapshot_hashes` | Hashes for reproducibility where available. |
| `scope` | Candidate, route, service, approval, rollback or readiness scope. |
| `candidate_ref` | Existing candidate/proposal/review reference where relevant. |
| `proposed_action` | Human-readable proposed action, never executable. |
| `decision` | `NO_ACTION`, `WOULD_MOVE`, `WOULD_BLOCK`, `WOULD_REVIEW` or `WOULD_ROLLBACK`. |
| `decision_reasons` | Ordered reasons and gate results. |
| `evidence_refs` | Canonical evidence references. |
| `simulation_refs` | Service impact, blast radius, readiness forecast and outcome preview refs. |
| `verification_plan` | How the prediction will later be checked. |
| `rollback_simulation` | Rollback prerequisites and predicted impact. |
| `authority_flags` | Explicit non-authority safety flags. |
| `expires_at` | Contract expiry for retention and stale-state handling. |
| `retention_class` | Retention category. |

## Required Authority Flags

```json
{
  "read_only": true,
  "derived_only": true,
  "preview_only": true,
  "non_authoritative": true,
  "execution_allowed_now": false,
  "runtime_mutation_performed": false,
  "routing_changed": false,
  "users_moved": false,
  "autoswitch_apply_run": false,
  "execution_engine_implemented": false,
  "runtime_hooks_implemented": false
}
```

## Reuse Boundary

The dry-run contract should reference existing execution contract previews when relevant, but it must not replace `EXECUTION_CONTRACTS_FILE` and must not become an execution truth source.

## Contract Verdict

`dryrun_contract_defined=true`

