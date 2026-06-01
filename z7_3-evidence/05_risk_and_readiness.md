# Z7.3 Evidence 05 - Risk and Readiness

## Risk Analysis

| Risk Area | Risk | Reason | Mitigation |
|---|---|---|---|
| Runtime risk | MEDIUM | Autoswitch is live runtime owner; metadata must not alter move selection | Keep operation fields output-only; tests assert selected move counts unchanged |
| Audit risk | LOW/MEDIUM | New audit call could add writes in unexpected modes | Emit terminal audit only in apply/runtime mode; do not audit default dry-run initially |
| Closure risk | LOW | Existing closure object type `runtime` can be reused | No closure schema/API change |
| Rollback risk | MEDIUM | Rollback must remain same operation, not separate lifecycle | Add rollback refs under existing apply result |
| Scheduler risk | LOW if untouched, HIGH if touched | Scheduler must not change | DO NOT TOUCH systemd |
| Duplication risk | MEDIUM | Existing operator/execution operation-like ids exist | Runtime operation id owned only by autoswitch |
| Test risk | LOW | Existing temp fixtures cover autoswitch plan behavior | Extend existing tests |

## What Is Already Ready

- Runtime owner.
- Planner generation.
- Selected move hash helper.
- Restore barrier checks.
- Apply/no-op result structure.
- Verification/rollback result rows.
- Audit metadata sink.
- Closure object model.
- Operator/governance operation id precedent.
- Autoswitch unit fixture harness.

## What Requires Metadata Wiring Only

- Operation envelope in autoswitch output.
- Operation id in selected moves.
- Operation id in apply/rollback rows.
- Closure target in operation output.
- Admin wrapper returning operation id from plan.

## What Requires Code Changes

- operation id creation helper,
- runtime snapshot hash helper,
- terminal state/reason mapping,
- terminal audit call.

## What Requires Tests

- operation envelope in no-op/dry-run plan,
- operation envelope with selected moves,
- restore-barrier denied terminal state,
- mocked apply/verify/rollback lineage,
- audit metadata construction.

## What Requires Future Work

- operator observability indexing live runtime operation audit records,
- break-glass operation id requirement,
- manual switch operation linkage,
- generic rollback operation linkage.

## Truth Source Audit

| Truth Source | Plan Result |
|---|---|
| Operation truth | Autoswitch creates runtime operation id; no new store |
| Runtime truth | Autoswitch remains owner |
| Lineage truth | Autoswitch output and audit metadata reference existing facts |
| Audit truth | `v7-audit-log` remains owner |
| Closure truth | Admin closure remains owner |
| Rollback truth | Autoswitch branch remains normal rollback owner |

## Readiness Verdict

The smallest safe implementation is understood and can proceed to Z7.4 if Z7.4 is an implementation stage with explicit permission to modify code.

