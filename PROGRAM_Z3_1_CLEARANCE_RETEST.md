# Program Z3.1 Clearance Retest

Date: 2026-06-01

## Verdict

clearance_retest_passed=true

## Initial Retest

Initial clearance retest:

- candidate moves: `1`
- selected moves: `1`
- generation ok: `true`
- guard: `restore_barrier_clearance_budget_and_generation_ok`
- apply requested: `false`
- apply result: `dry_run`

## Drift Finding

After additional live reads, filtered gate later failed with:

`restore_barrier_clearance_generation_mismatch`

This confirmed that clearance is short-lived and generation-bound.

## Refresh Retest

Z3.1 refreshed clearance immediately and reran filtered planner:

- generation id: `af7bd1d112e0f52dafea36e5b3bdb86edd6d8fd74a1622748a463b0bf7a373fd`
- selected hash: `f07989c421144d900cb3bc38621267282c0fcedb4477d83bdc2e25417bd18cae`
- candidate moves: `1`
- selected moves: `1`
- generation ok: `true`
- guard: `restore_barrier_clearance_budget_and_generation_ok`
- apply requested: `false`
- apply result: `dry_run`

## Safety

- movement_executed=false
- autoswitch_apply_run=false
- users_moved_count=0

