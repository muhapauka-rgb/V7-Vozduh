# SNAPSHOT_CONSISTENCY_CONTRACT

Program: PROGRAM_SOURCE1_SNAPSHOT_SOURCE_CONSISTENCY_CLOSURE_AND_OPERATOR_VISIBLE_UNLOCK
Date: 2026-06-05

## Canonical Contract

Planner may trust required intelligence snapshots only when:

1. The snapshot family exists in the canonical snapshot root.
2. The snapshot envelope validates.
3. The snapshot family is FRESH or otherwise allowed by its family runtime behavior.
4. The confidence is acceptable for the family.
5. Required source_hashes match the planner's current post-refresh source inputs.
6. Pre-planner refresh did not report SOURCE_VOLATILE, timeout, exception, or invalid output.

## Ownership

- Source truth owner: existing runtime state files.
- Snapshot write owner: tools/v7-intelligence-snapshot-refresh.
- Snapshot root owner: existing /opt/v7/egress/state/intelligence.
- Planner validation owner: tools/v7-users-autoswitch.
- Governance owner: unchanged.
- Execution owner: unchanged.

## Runtime Weight

Heavy computation stays in snapshot refresh.

Runtime planner performs only:

- source reload after successful refresh
- hash comparison
- envelope/freshness/confidence checks
- advisory scoring from snapshots

## Decision -> Action

Condition: all contract clauses pass.
Decision: intelligence snapshots may be used as bounded advice.
Action: set intelligence_present=true and allow planner influence inside existing candidate scoring.
Executor: tools/v7-users-autoswitch.
Trigger: successful snapshot gate.
Written Evidence: routing_brain.snapshot_gate and candidate routing_intelligence.
Blocked Actions: autonomy, governance bypass, execution bypass.
Next State: operator_visible_candidate_ready.

