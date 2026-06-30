# Emergency Runtime Autonomy UI / Tests

## Summary

Admin UI plan view now exposes emergency autonomy status, incident context, source, target, selected users, blast radius, cooldown, execution mode and blocker.

## Action Performed

Added read-only emergency status fields to existing admin plan materialization.

## Files Changed

- `admin/v7-admin-api`
- `tests/unit/test_v7_users_autoswitch_policy.py`

## Users Moved

NO.

## Authority Impact

No authority expansion.

## Runtime Impact

No runtime behavior changed by UI.

## Restore / Rollback Status

UI shows execution blocker and emergency authorization state.

## Verification Result

Relevant tests passed locally:

- `python3 -m unittest tests.unit.test_v7_users_autoswitch_policy`
- `python3 -m unittest tests.unit.test_api3_read_only_views`
- `PYTHONPYCACHEPREFIX=/private/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch admin/v7-admin-api`

## Tests

Autoswitch policy tests: 92 passed.
Admin read-only tests: 10 passed.
Compilation: PASS.

## Production Impact

Production validation not executed yet.
Safe deploy and one-user production movement remain pending.

## Canonical Changes

NONE.

## Next Step

Run truth/convergence, commit intended implementation, then deploy only through existing safe deployment owner before any production validation.

