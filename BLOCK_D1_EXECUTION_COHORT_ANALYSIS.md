# Block D1 Execution Cohort Analysis

Project: V7 Vozduh

Block: D1 - Autoswitch Safety Remediation And Decision Tree

Date: 2026-06-01

## HOLD

Benefits:

- No movement.
- Preserves ten-user certification evidence.

Risks:

- Target remains full.
- Planner keeps treating the cohort as failover candidates unless hold semantics are added.

## ROLLBACK

Benefits:

- Frees execution target.

Risks:

- Sends ten users back to egress `1`.
- Conflicts with current hard-limit policy for egress `1`.
- Loses current cohort observation continuity.

## SPLIT

Benefits:

- Reduces target pressure while preserving partial cohort.

Risks:

- Requires new packet and capacity model.
- Could create mixed evidence unless carefully staged.

## CREATE_NEW_EXECUTION_TARGET

Benefits:

- Preserves current cohort.
- Creates headroom.
- Aligns with D0 decision.

Risks:

- Requires new infrastructure/certification block.

## Verdict

Recommended cohort strategy:

```text
HOLD current cohort + CREATE_NEW_EXECUTION_TARGET
```

`execution_cohort_decision_complete=true`

