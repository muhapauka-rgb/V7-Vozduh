# Phase 4 Certification User Metadata Fix

Timestamp: 2026-07-03 10:35:38 Asia/Bangkok

## Summary

Phase 4 MEDIUM_BATCH execution remained blocked after the requested-source continuity deploy.

The governed owner invoked:

`v7-users-autoswitch --source-egress wireguard-1779454504-c43409 --max-selected-moves 10`

but `tools/v7-users-autoswitch` selected an unrelated observed failed source (`awg3`) as the active incident source. The requested controlled certification source was not recognized as a failed source even though the candidate itself was ineligible with `blocked=["egress_disabled"]`.

## Root Cause

`AutoswitchPlanner._load_users()` preferred `v7-state.json:users` when present and did not merge persistent metadata from `users.registry`.

Production evidence showed:

- `_l3_enabled_users_on_source("wireguard-1779454504-c43409")` returned 11 affected users.
- `_controlled_certification_failure_context("wireguard-1779454504-c43409")` returned `certification_users=[]`.
- `egress.registry` preserved `controlled_certification_source=1`.
- `users.registry` preserved `certification_user=1` for all 11 certification users.
- `v7-state.json:users` did not carry `certification_user=1`.

Therefore the same owner used live user assignment from `v7-state.json` but lost certification metadata that is owned by `users.registry`.

## Exact Owner And Function Changed

Owner: `tools/v7-users-autoswitch`

Function: `AutoswitchPlanner._load_users()`

Change:

- Always parse `users.registry`.
- When `v7-state.json:users` is present, merge registry metadata into `User.raw`.
- Preserve live state precedence for `current`, `table`, and `enabled`.

This reuses the existing `users.registry` owner and does not create a new owner, planner, runtime, authority, wake path, packet, or restore barrier path.

## Why Runtime Semantics Remain Unchanged

The patch only restores metadata visibility inside the existing planner owner.

Unchanged:

- Runtime Apply
- Authority
- Approved Plan Lock
- Restore Barrier
- Verification
- Rollback
- max-users enforcement
- batch ladder authority budgets
- incident source continuity rules

## Tests

Command:

`python3 -m unittest tests.unit.test_v7_users_autoswitch_policy tests.unit.test_governed_canary_cli`

Result:

`Ran 148 tests in 10.412s - OK`

Command:

`PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch tests/unit/test_v7_users_autoswitch_policy.py`

Result:

PASS

## Regression Added

Updated:

`test_controlled_certification_maintenance_produces_confirmed_current_channel_failure`

The test now reproduces the production shape:

- `v7-state.json:users` contains live users without `certification_user`.
- `users.registry` contains `certification_user=1`.
- controlled certification source is unavailable.

Expected result:

- `confirmed_current_channel_failure` is accepted.
- incident source is the controlled source.
- selected moves come only from the controlled source.

## Production Impact

Production impact before deploy: NONE.

Deploy status at report creation: pending safe deploy.

Users moved by this patch before deploy: 0.

## Current Execution Position

Certification Program Phase: Phase 4 MEDIUM_BATCH

Interrupted execution source:

`wireguard-1779454504-c43409`

Required continuation:

1. Safe deploy.
2. Verify convergence.
3. Recreate controlled degradation through `v7-egress-set-state`.
4. Resume Phase 4 with `--max-users 10 --approved-source wireguard-1779454504-c43409`.
5. Continue until PASS, HOLD, BLOCKED with terminal owner resolution, or CANONICAL_IMPOSSIBILITY.

## Automation Debt

Created:

- Registry/live-state metadata merge was manually diagnosed during certification.

Closed:

- Certification metadata visibility gap is implemented in the existing planner owner.

Remaining:

- None for this breakpoint until production validation proves the fix.

## Workflow Debt

Created:

- Manual controlled degrade -> planner probe -> restore loop was used for breakpoint evidence.

Classification:

- INTENTIONALLY_MANUAL during controlled production certification until the certification pipeline owns this diagnostic probe.

## Next Required Step

Safe deploy this implementation and resume Phase 4 MEDIUM_BATCH certification from the interrupted controlled source.
