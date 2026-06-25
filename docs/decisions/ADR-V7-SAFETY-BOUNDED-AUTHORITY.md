# ADR-V7 Safety-Bounded Authority

Status: Accepted  
Date: 2026-06-25  
Commit: documentation commit containing this ADR  
Program: `V7.SAFETY_BOUNDED_AUTHORITY_PRINCIPLES`

## Context

V7 reached `AUTHORITY_BOUNDARY` because trust/suitability maturity and execution authority were being treated too closely.

The system already has the major architecture owners: planner, governed packet preview, restore barrier, rollback, verification, feedback, learning, trust inventory, decision surface, OMP, truth, and convergence.

The current blocker is not missing architecture. The current blocker is suitability, real outcomes, and the authority boundary before restore-barrier write or apply.

If real trust requires real outcomes, and real outcomes require governed action, then interpreting all governed action as blocked by insufficient trust creates a deadlock:

```text
need trust
  -> need outcomes
  -> need action
  -> need trust
```

## Decision

V7 separates Knowledge Maturity from Execution Authority.

## Principle

Trust decides autonomy tier.

Safety decides bounded action.

Knowledge Maturity answers how mature V7 is and which autonomy tier it may enter.

Execution Authority answers whether one exact bounded action may happen now.

## Consequences

- `70/70/70` remains the floor for `TIER_2+` and autonomous progression.
- No trust, confidence, prediction, suitability, or autonomy floor is lowered.
- No synthetic evidence is allowed.
- No new planner is created.
- No new governance is created.
- No new execution path is created.
- No new truth source is created.
- A `TIER_1` governed one-user canary can be prepared for explicit operator approval even while `TIER_2` remains blocked.
- Restore-barrier writes, runtime apply, user movement, rollback apply, daemon/timer enablement, and authority expansion still require explicit approval.

## Runtime Rule

Background builds knowledge.

Runtime spends knowledge.

Background systems may perform heavier analysis, including service knowledge, suitability, prediction, trust, recovery, capacity, history, learning, and snapshot work.

Runtime must remain thin:

```text
Event
  -> Current State
  -> Knowledge Snapshot
  -> Policy
  -> Safety
  -> Packet
  -> Execute/Stop
```

Runtime must not perform broad audits, broad analytics, or long historical recomputation during the event path.

## Alternatives Considered

1. Lower floors so governed action can run.
   - Rejected. This would distort autonomy maturity.

2. Synthesize evidence.
   - Rejected. Synthetic evidence is forbidden.

3. Build a new planner, governance layer, or execution layer.
   - Rejected. Existing architecture is certified complete with future optional extensions.

4. Treat all action as blocked until `TIER_2`.
   - Rejected. This prevents real outcomes from being generated safely under `TIER_1` explicit operator authority.

## Affected Modules

- `docs/reference/V7_ENGINEERING_PRINCIPLES.md`
- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
- Existing owners only: planner, packet preview, restore barrier, rollback, verification, feedback, learning, trust inventory, decision surface, truth, convergence.

## Reference Updates

- Add `V7_ENGINEERING_PRINCIPLES` to `docs/reference/V7_CANONICAL_REFERENCE.md`.
- Add the Engineering Principles row to `docs/reference/SYSTEM_MAP.md`.

## Related Reports

- `docs/reports/V7_FINAL_AUTONOMOUS_ROUTING_ARCHITECTURE_CERTIFICATION_REPORT.md`
- `docs/reports/V7_GOVERNED_CANARY_KNOWLEDGE_GATED_AUTONOMOUS_DRY_RUN_CYCLE_REPORT.md`
- `docs/reports/V7_AUTONOMOUS_ROUTING_EVOLUTION_PROGRAM_REPORT.md`
- `docs/reports/V7_MAXIMUM_REALITY_KNOWLEDGE_EXTRACTION_REPORT.md`
- `docs/reports/V7_AUTONOMY_GRADE_SUITABILITY_PROGRAM_REPORT.md`
