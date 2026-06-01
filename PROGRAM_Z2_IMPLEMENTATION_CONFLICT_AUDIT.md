# Program Z2 Implementation Conflict Audit

Date: 2026-06-01

## Verdict

implementation_conflict_audit_complete=true

No parallel movement engine was created.

## Existing Implementations

| Area | Existing implementation | Z2 decision |
| --- | --- | --- |
| Autoswitch planner | `tools/v7-users-autoswitch` | Reuse as canonical planner/apply authority. |
| Proposal cap | `tools/v7-autoswitch-proposal-cap` | Reuse as bounded proposal source. |
| Safety review | `tools/v7-autoswitch-safety-review` | Reuse for read-only safety/capacity preflight. |
| Operator packet audit | `tools/v7-operator-execution-packet`, `admin_core/operator_execution.py` | Reuse pattern, but keep zero-movement semantics untouched. |
| Movement execution | `v7-user-switch` through existing runtime tooling | Do not duplicate. Z2 does not invoke it from repo tests. |
| Rollback | Existing rollback command model and approval packets | Reuse rollback target in policy contract. |
| Verification | Existing readiness, restore-settle, route checks | Reuse as runtime evidence; no new runtime checker. |

## Z2 Implementation

Z2 adds a narrow governance layer:

- `admin_core/hybrid_approval.py`
- `tools/v7-hybrid-approval-contract`
- `tests/unit/test_v7_hybrid_approval.py`

It validates hybrid approval, fingerprints, target substitution, runtime recheck, replay protection, and append-only audit records. It does not execute routing changes.

## Difference From Existing Operator Execution

`admin_core/operator_execution.py` is intentionally zero-movement only. Z2 does not modify that contract. Instead, Z2 adds a separate approval contract that can authorize bounded autonomy and record the authorization while leaving actual movement to the existing runtime movement authority.

## Conflict Decision

- Reuse: autoswitch planner, proposal cap, safety review, movement authority, rollback concepts.
- Extend: admin governance validation with hybrid approval fingerprints.
- Refactor: none.
- Replace: none.
- Do Not Touch: systemd, deploy scripts, `v7-user-switch`, existing zero-movement packet consumer.

## Safety

- duplicate_execution_engine_created=false
- duplicate_movement_engine_created=false
- runtime_mutation_performed=false
- users_moved=false

