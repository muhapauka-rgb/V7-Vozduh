# Program Z3.1 Clearance Model

Date: 2026-06-01

## Verdict

clearance_model_understood=true

## How Clearance Is Generated

Clearance is a live restore barrier state with:

- `generation_clearance=true`
- `allow_post_ttl_apply=true`
- `clearance_max_selected_moves=N`
- `generation_token`
- `clearance_generation_id`
- `approved_selected_moves_hash`
- `clearance_expected_selected_moves`
- `clearance_expires_at`

## How Clearance Expires

Clearance expires if:

- `clearance_expires_at` is in the past
- planner generation id changes
- selected moves hash changes
- selected move count changes
- selected move budget exceeds `clearance_max_selected_moves`

## How Clearance Is Refreshed

Z3.1 refresh sequence:

1. Run filtered live planner with budget scope.
2. Read current planner generation id.
3. Read selected moves hash before guard.
4. Write generation-bound barrier clearance.
5. Immediately rerun filtered planner.
6. Require `clearance_generation_ok=true`.

## Important Finding

The planner generation can drift quickly because live runtime inputs change. Clearance must be used immediately after fresh planner recheck. Delayed use can correctly fail with:

`restore_barrier_clearance_generation_mismatch`

