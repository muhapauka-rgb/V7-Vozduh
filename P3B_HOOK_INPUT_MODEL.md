# P3.B Hook Input Model

Project: V7 Vozduh
Block: P3.B Runtime Hook Dry-Run Foundation

## Input Principle

Hooks consume existing evidence. They do not own the evidence and do not create canonical runtime state.

## Inputs

| Input | Canonical owner | Freshness rule | Retention rule |
| --- | --- | --- | --- |
| Health | Service matrix, sentinel, runtime checks | Must include observed timestamp or file age. | Source retention applies. |
| Capacity | Load summary, capacity readiness/checks | Stale capacity blocks positive recommendation. | Source retention applies. |
| Required services | Service matrix and route-class fitness | Missing required-service evidence produces `WOULD_BLOCK` or `WOULD_REVIEW`. | Source retention applies. |
| Runtime trust | Trusted RU diagnostic/decision and runtime trust store | Missing or stale trust blocks trust-sensitive decisions. | Source retention applies. |
| Release trust | Release trust store | Missing release trust blocks release-coupled decisions. | Source retention applies. |
| Candidate state | Proposal/evidence stores and candidate workflow | Candidate id and source refs must be stable. | Candidate retention applies. |
| Execution state | Execution contracts/events | Must reference existing contract/event ids. | Execution retention applies. |
| Audit state | Admin/operator audit logs | Audit tail may be summarized; canonical log remains source. | Audit retention applies. |
| Sentinel state | Sentinel state and daily observer JSONL | Stale sentinel evidence cannot authorize service recovery. | Sentinel retention applies. |
| Autoswitch inputs | Registries, switch policy, safety file, service matrix, restore barrier | Apply-capable inputs are read-only; missing safety blocks positive recommendation. | Source retention applies. |

## Freshness Classes

| Class | Meaning |
| --- | --- |
| `FRESH` | Input is within the accepted TTL for its source. |
| `STALE` | Input exists but is outside accepted TTL. |
| `MISSING` | Input is unavailable. |
| `CONFLICTING` | Input contradicts another canonical source. |
| `UNKNOWN` | Freshness cannot be determined. |

## Ownership Rules

- Hook reports must show source owner.
- Hook contracts must keep source refs and hashes where possible.
- Hook evaluation must fail closed on missing owner or conflicting ownership.
- Hook input snapshots are derived references, not copied truth.

## Input Verdict

`hook_input_model_defined=true`

