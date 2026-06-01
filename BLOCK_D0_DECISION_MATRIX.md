# Block D0 Decision Matrix

Project: V7 Vozduh

Block: D0 - Execution Cohort Decision Program

Date: 2026-06-01

## HOLD

Benefits:

- No user movement.
- Preserves the certified ten-user execution cohort.
- Allows continued observation.

Risks:

- Target remains at hard limit.
- No capacity headroom for Block D expansion.
- Admin API health remains unresolved.

Operational cost:

- Low.

Autonomy impact:

- Blocks future autonomous testing on this target.

## ROLLBACK

Benefits:

- Frees the execution target.
- Returns the system to a pre-execution cohort topology.

Risks:

- Moves ten users back to egress `1`.
- Egress `1` would exceed current hard-limit policy.
- Does not resolve admin health or trust risks.

Operational cost:

- Medium to high, because it requires a new rollback packet and observation window.

Autonomy impact:

- Reduces current execution evidence continuity.

## CREATE_NEW_EXECUTION_TARGET

Benefits:

- Preserves the current certified cohort.
- Adds headroom for future Block D work.
- Avoids overloading rollback egress `1`.
- Keeps autoswitch/rebalance disabled on current execution target.

Risks:

- Requires separate infrastructure/governance work in a future block.
- New target must be certified before use.

Operational cost:

- Medium.

Autonomy impact:

- Best path for future governed expansion.

## Matrix Verdict

`CREATE_NEW_EXECUTION_TARGET` is the recommended decision.

