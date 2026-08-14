# Safety Gap And Closure

## Discovered Gap

The first live governed apply attempt failed closed:

- `terminal_state=NOOP`
- `terminal_reason=no_selected_moves`
- `apply_result.applied=false`

Root cause:

The planner needed fresh intelligence snapshots at execution time. Plain apply could not run pre-planner refresh, so a service matrix source hash mismatch could reopen between approval preparation and guarded apply.

## Closure

Commit:

`97609a2744ffb24c9d2ba53ba744e92e446337ee`

Change:

Added an explicit bounded apply refresh gate to `tools/v7-users-autoswitch`.

The refresh is allowed with apply only when all of these are true:

- `--allow-pre-planner-refresh-with-apply` is present;
- `--pre-planner-refresh write` is present;
- `--user` is present;
- `--target-egress` is present;
- `--max-selected-moves 1` is present.

All other apply plus refresh combinations remain fail-closed.

## Verification

Tests passed:

- targeted runtime snapshot fast path tests;
- runtime policy tests;
- operator execution packet tests;
- full unittest regression: 312 tests.

Deployment:

- safe deploy completed;
- no users moved during deploy;
- no autoswitch apply during deploy;
- truth-check returned `FULLY_ALIGNED`.

