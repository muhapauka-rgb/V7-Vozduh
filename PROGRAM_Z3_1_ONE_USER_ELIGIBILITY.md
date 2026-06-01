# Program Z3.1 One User Eligibility

Date: 2026-06-01

## Verdict

one_user_eligible=true

## Eligible User

- user: `10.7.0.16`
- current egress: `vless`
- target egress: `awg3`
- move type: `failover`
- rollback target: `vless`

## Filtered Planner Result

Before remediation:

- candidate moves: `1`
- selected moves before guard: `1`
- selected moves after guard: `0`
- reason: `restore_barrier_clearance_selected_moves_exceed_budget`

After remediation:

- candidate moves: `1`
- selected moves: `1`
- guard: `restore_barrier_clearance_budget_and_generation_ok`
- generation ok: `true`

## Why Exactly One Can Pass

The filtered planner constrains:

- `--user 10.7.0.16`
- `--target-egress awg3`

This produces one selected move hash and one expected selected move count.

