# ADR-V7-RUNTIME-MODEL

Status: Accepted
Date: 2026-06-25
Program: `V7.RUNTIME.DESIGN.PROGRAM`

## Context

V7 now has a canonical Decision Model, Safety-Bounded Authority, OMP, Current Program State, Event-Driven Autonomy Contract, execution packet owner, restore barrier, rollback, verification, feedback, learning, truth, and convergence.

The missing piece is not a new planner, governance layer, execution layer, truth source, daemon, timer, or event consumer.
The missing piece is a canonical design contract for how Runtime executes an already-approved decision through existing owners.

Runtime must remain thin.
Background builds knowledge.
Decision Model defines the decision.
OMP remains execution authority and optimizer.
Runtime spends prepared knowledge and stops safely when policy, safety, authority, packet, verification, rollback, or learning requirements are not met.

## Decision

Adopt `docs/reference/V7_RUNTIME_MODEL.md` as the canonical design for executable V7 Runtime.

Runtime executes existing Decision Model snapshots only.
Runtime does not invent decisions.
Runtime composes existing owners:

- Event-Driven Autonomy Contract;
- Current Program State;
- V7 Decision Model;
- Planner / Autoswitch;
- Safety-Bounded Authority;
- Execution Packet owner;
- Restore Barrier / Rollback;
- Runtime Readiness;
- truth/convergence;
- feedback;
- learning;
- OMP.

Need New Owner: FALSE.

## Runtime Pipeline

```text
Event
  -> Runtime Wakeup
  -> Read Current Program State
  -> Read Decision Snapshot
  -> Policy
  -> Safety
  -> Authority
  -> Packet
  -> Execute OR Stop
  -> Verify
  -> Rollback if needed
  -> Outcome
  -> Learning
  -> Update Current Program State
  -> Notify OMP
  -> Sleep
```

## Consequences

- Runtime is a lifecycle execution contract, not a decision owner.
- Existing owners remain authoritative.
- Stop is a valid runtime result.
- Runtime restart and duplicate detection must be idempotency-key based.
- Runtime failure behavior is fail-closed.
- Runtime learning must use only real observed outcomes.
- Current Program State is the volatile program continuation surface, not a new runtime truth source.
- Future implementation must begin with read-only preview/spec work and requires separate approval before apply, user movement, daemon/timer enablement, autonomous execution, or event consumer mutation.

## Forbidden

This ADR does not authorize:

- runtime code implementation;
- daemon or timer enablement;
- event consumer changes;
- autonomous execution;
- apply;
- user movement;
- planner changes;
- governance changes;
- execution path changes;
- truth source changes;
- synthetic evidence;
- floor changes;
- restore-barrier writes;
- rollback apply.

## Alternatives Considered

1. Create a new Runtime owner.
   - Rejected. Existing owners already cover wakeup, decision, policy, packet, restore barrier, execution, verification, rollback, feedback, learning, OMP, truth, and convergence.

2. Let Runtime decide.
   - Rejected. Decision != Execution. Runtime executes approved decision snapshots only.

3. Use timer-based runtime movement.
   - Rejected. ADR-EVENT-DRIVEN-AUTONOMY rejects blind timer movement.

4. Treat Current Program State as runtime truth.
   - Rejected. It is volatile program state and continuation state, not a runtime truth source.

## Affected Modules

- `docs/reference/V7_RUNTIME_MODEL.md`
- `docs/reports/V7_RUNTIME_MODEL_DESIGN_REPORT.md`
- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`

## Verification

Required verification:

- `tools/v7-truth-check --all --json`
- `tools/v7-convergence-status --json`

No runtime mutation, no apply, and no user movement.
