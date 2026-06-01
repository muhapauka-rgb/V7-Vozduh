# Block D2 Hold Semantics

Date: 2026-06-01

## Hold Rule Tested

The execution cohort current egress was held:

`amneziawg-exec-20260528-10-8-1-14`

## Result

The raw shadow plan contained `12` candidate moves:

- `10` candidates from the execution cohort target
- `2` candidates from `vless`

The proposal cap held all `10` execution cohort candidates with:

`current_egress_hold`

The remaining eligible proposal pool was `2`, and the budget `1` selected exactly one preview move from `vless` to `awg0`.

## Interpretation

Hold semantics work as a post-shadow operator guard. They do not alter planner scoring, runtime policy, routing, or registry state.

## Verdict

hold_semantics_working=true

