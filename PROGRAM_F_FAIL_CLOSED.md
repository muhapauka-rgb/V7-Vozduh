# Program F Fail Closed

Date: 2026-06-01

## Fail-Closed Result

Program F failed closed at Stage 1 because approved packet evidence is missing.

This is expected and correct.

## Verified Conditions

- Missing approval: denied by process.
- Budget remains `1`.
- No bulk movement occurred.
- No apply outside packet occurred.
- No deploy occurred.
- No systemd change occurred.

## Not Verified In Live Execution

Because execution did not occur:

- duplicate packet replay was not exercised
- expired packet denial was not exercised
- stale hash denial was not exercised
- rollback packet replay was not exercised

replay_protection_verified=false
fail_closed_verified=true

