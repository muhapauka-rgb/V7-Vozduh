# P3.B Hook Contract Model

Project: V7 Vozduh
Block: P3.B Runtime Hook Dry-Run Foundation

## Purpose

A Hook Dry-Run Contract binds observed inputs, non-executable decision, evidence, verification plan, rollback simulation, freshness and retention metadata. It is a report contract, not an execution contract.

## Contract Fields

| Field | Meaning |
| --- | --- |
| `hook_contract_id` | Stable derived id for the hook report. |
| `created_at` | Contract creation time. |
| `trigger_type` | Passive trigger class: request, observation, scheduled read, or admin preview. |
| `scope` | Runtime, service, candidate, execution, rollback, readiness or trust scope. |
| `input_refs` | Canonical source references. |
| `input_hashes` | Hashes of source payloads where available. |
| `freshness` | Freshness class per input. |
| `ownership` | Source owner per input. |
| `decision` | One allowed output value only. |
| `decision_reasons` | Ordered gate and rule explanations. |
| `evidence` | Evidence refs, not duplicated source truth. |
| `simulation` | Impact, blast radius, route/service and readiness forecast refs. |
| `verification_plan` | Later evidence required to evaluate prediction quality. |
| `rollback_simulation` | Non-executable rollback feasibility preview. |
| `confidence` | Confidence score or qualitative class. |
| `authority_flags` | Explicit non-executable flags. |
| `expires_at` | Expiry time for stale output handling. |
| `retention_class` | P2.5/P3.A-compatible retention class. |

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
  "runtime_hooks_with_authority": false
}
```

## Contract Boundary

The hook contract may reference existing execution contracts. It must not become an execution contract and must not be consumable by an executor.

## Contract Verdict

`hook_contract_defined=true`

