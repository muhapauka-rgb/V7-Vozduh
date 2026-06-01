# Block D1 Final Decision

Project: V7 Vozduh

Block: D1 - Autoswitch Safety Remediation And Decision Tree

Date: 2026-06-01

## Recommended Path

Combination:

```text
HOLD
CREATE_NEW_EXECUTION_TARGET
PLANNER_CAP
AUTOSWITCH_SHADOW_RETRY
```

Do not proceed to operator autoswitch yet.

## Ordered Actions

1. Fix `v7-autoswitch-safety-review` KV registry parser.
2. Add regression tests for enabled egress detection.
3. Add governance hold/exclusion semantics for certified execution cohorts.
4. Add capped proposal packet generation.
5. Create or certify a second execution target.
6. Rerun autoswitch shadow with budget `1`.
7. Only then evaluate operator-approved autoswitch.

## Verdicts

- `recommended_path_defined=true`
- `safe_to_continue=true` for remediation work
- `safe_to_continue_to_operator_autoswitch=false`

