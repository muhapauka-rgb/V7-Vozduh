# Approved Plan Lock Committed Move Rehydration

## Summary

Controlled Production Certification Program Phase 4 reached a real implementation blocker after rollback cooldown expired.

The governed owner produced a valid approved plan lock for the open real incident `openvpn-1779388847-d2ad7c`, but Runtime Apply returned:

```text
approved_plan_lock_selected_moves_missing
```

## Production Evidence

| Field | Value |
| --- | --- |
| Payload | `/tmp/v7_gov_continuation_20260703T054133.json` on production |
| Incident source | `openvpn-1779388847-d2ad7c` |
| Selected users in approved lock | `10.7.0.12`, `10.7.0.13`, `10.7.0.15` |
| Authorized L3 budget | `25` |
| Requested max users | `10` |
| apply_executed | `False` |
| users_moved | `0` |
| verification_result | `NOT_RUN` |
| apply reason | `approved_plan_lock_selected_moves_missing` |

## Root Cause

The approved plan lock validation was valid and contained committed selected moves, but `tools/v7-users-autoswitch.apply()` treated the fresh empty `plan["selected_moves"]` as terminal.

That is wrong for governed execution after approval. The approved plan lock is the committed execution identity. A fresh planner result may be empty because cooldown, retry policy, or other post-approval state changed, but Runtime Apply must either consume the locked selected moves if the approved lock remains valid, or fail closed if the lock is invalid.

## Owner Changed

| Owner | Function |
| --- | --- |
| `tools/v7-users-autoswitch` | `_committed_selected_moves_from_approved_plan_lock()` |
| `tools/v7-users-autoswitch` | `apply()` |

## Implementation

`apply()` now:

1. Checks whether `plan["selected_moves"]` is empty.
2. Looks for a present and valid `approved_plan_lock_validation`.
3. Verifies selected move hash and selected move count against the operation identity.
4. Rehydrates committed selected moves from the approved lock.
5. Continues through the existing Atomic Envelope, L3 Eligibility, Runtime Apply, Verification, and Rollback path.

If the approved lock is missing, invalid, hash-mismatched, count-mismatched, or has no selected moves, the previous fail-closed behavior remains.

## Tests

| Test | Result |
| --- | --- |
| `python3 -m unittest tests.unit.test_v7_users_autoswitch_policy` | `PASS`, `123` tests |
| `PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch tests/unit/test_v7_users_autoswitch_policy.py` | `PASS` |

New regression test:

```text
test_apply_uses_valid_approved_lock_moves_when_fresh_plan_selected_moves_empty
```

## Production Impact

| Field | Value |
| --- | --- |
| New owner | `NO` |
| New Runtime | `NO` |
| New Planner | `NO` |
| New Authority | `NO` |
| Restore Barrier bypass | `NO` |
| Authority bypass | `NO` |
| Broad automation | `NO` |
| Max users changed | `NO` |
| Production deploy | `PENDING` |

## Next Step

Safe deploy the existing-owner fix, verify convergence, then resume the same governed L3 production validation path for `openvpn-1779388847-d2ad7c`. After that real incident reaches a terminal state, resume Phase 4 MEDIUM_BATCH controlled source certification.
