# ADR-V7 Kernel and Program State Split

Status: Accepted
Date: 2026-06-25
Commit: documentation commit containing this ADR

## Context

OMP v2.2 became the execution authority and optimizer, but it still mixed stable scheduler rules with volatile current packet/state data.

This made future continuation prompts longer than necessary and encouraged repeated handoff copying.

## Decision

Create `docs/reference/V7_KERNEL.md` as the permanent Codex operating contract and `docs/programs/V7_CURRENT_PROGRAM_STATE.md` as volatile current state.

## Consequences

- OMP remains scheduler/optimizer.
- Kernel defines how Codex runs.
- Current Program State holds changing bottleneck/HLA/packet/metrics.
- Future prompts can be short: `Continue OMP`.
- No runtime behavior changes.
- No new planner, governance, execution, or truth source.

## Alternatives Considered

1. Keep all current state inside OMP.
   - Rejected because it turns OMP into a packet/state dumping ground and makes every volatile update look like scheduler change.

2. Use handoff files as the only current state.
   - Rejected because handoff files are useful for chat transfer, but they are not the stable program state owner.

3. Create a runtime state source.
   - Rejected. Runtime remains reality and verification, not a new documentation/control-plane state owner.

## Affected Modules

- `docs/reference/V7_KERNEL.md`
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
- `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`

## Reference Updates

- Add `V7_KERNEL_AND_STATE_SPLIT` to `docs/reference/V7_CANONICAL_REFERENCE.md`.
- Add V7 Kernel and V7 Current Program State rows to `docs/reference/SYSTEM_MAP.md`.

## Related Reports

- `docs/reports/V7_FINAL_AUTONOMOUS_ROUTING_ARCHITECTURE_CERTIFICATION_REPORT.md`
- `docs/reports/V7_GOVERNED_CANARY_KNOWLEDGE_GATED_AUTONOMOUS_DRY_RUN_CYCLE_REPORT.md`
- `docs/handoff/V7_CURRENT_STATE_SNAPSHOT.md`
- `docs/handoff/V7_AUTHORITY_BOUNDARY_AND_NEXT_ACTION.md`
