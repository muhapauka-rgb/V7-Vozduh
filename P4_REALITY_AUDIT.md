# P4 Reality Audit

Project: V7 Vozduh
Program: P4
Block: P4 Controlled Runtime Action Planning
Mode: Architecture / Discovery / Action Planning

## Scope

P4 designs how V7 can safely approach its first real action. P4 does not implement execution and does not mutate runtime.

## Repository Baseline

- Working tree: `/private/tmp/v7-convergence-c`
- Current branch: `v7-next`
- Local HEAD at audit time: `bc0bd5496ab454da15052c33392a1d641bfcceda`
- P3.E verdict present: `dryrun_certified=true`
- P3.E continuation verdict present: `safe_to_continue_to_controlled_runtime_action_planning=true`

## Mandatory Search Coverage

Searched repository for:

- operator approval
- approval center
- governance preview
- rehearsal preview
- execution contracts
- candidate workflow
- readiness
- verification
- rollback preview
- runtime dry-run
- runtime reports
- runtime observability
- action packets
- operator execution

## Existing Implementations Found

| Area | Existing location | Behavior | P4 decision |
| --- | --- | --- | --- |
| Operator packet validation | `admin_core/operator_execution.py` | Validates zero-movement packets, dual approval, TTL, runtime hash recheck, replay denial, and audit append records. | Reuse as governance boundary reference; do not execute. |
| Approval preview | `admin_core/operator_observability.py` | Builds approval preview, required roles, expiry, replay guard, rollback manifest and disabled execution contracts. | Reuse. |
| Governance preview | `admin_core/operator_observability.py` | Builds execution governance preview with contracts, barriers, replay rejection, rollback-bound execution and disabled actions. | Reuse. |
| Rehearsal preview | `admin_core/operator_observability.py` | Rehearses approval, recheck, stale runtime, replay, rollback and containment scenarios without mutation. | Reuse. |
| Execution preview APIs | `admin/v7-admin-api` | GET routes for execution contracts, events, readiness, validation, verification, rollback, blast radius and outcome previews. | Reuse as presentation and source refs. |
| Candidate workflow APIs | `admin/v7-admin-api` | GET routes for candidate detail, approval, governance, rehearsal, readiness, risks, explain and timeline. | Reuse. |
| Runtime dry-run APIs | `admin/v7-admin-api` | GET `/api/runtime/dry-run/summary` and `/api/runtime/dry-run/verification`. | Reuse as planning evidence. |
| Historical approval packets | `BLOCK_E*`, `docs/track7/productization/*` | Prior governed movement and approval packet reports. | Use as lineage and precedent only. |

## Current Reality

V7 already has many governance pieces:

- approval packet concepts
- dual confirmation rules
- runtime recheck logic
- replay denial
- rollback manifest previews
- observation window precedent
- execution preview surfaces
- candidate workflow surfaces
- dry-run prediction and verification

P4 must therefore define the complete controlled action model as a consolidation and planning layer over existing surfaces.

## Reuse Classification

- Reuse: dry-run summary, dry-run verification, execution preview APIs, candidate workflow APIs, operator approval preview, governance preview, rehearsal preview.
- Extend later: packet schema for non-zero controlled action planning, admin action packet presentation, runtime recheck checklist.
- Refactor later: no immediate refactor required in P4.
- Replace: none.
- Do Not Touch: existing action-capable tooling, systemd, deploy scripts, routing tools, autoswitch apply paths.

## Verdict

`reality_audit_complete=true`

