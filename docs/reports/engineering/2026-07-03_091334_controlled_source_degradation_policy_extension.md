# Controlled Source Degradation Policy Extension

Timestamp: 2026-07-03T09:13:34+0700

## Summary

The Controlled Production Certification Program did not terminate at the previous `POLICY_PROHIBITION`.

The required resolution was converted into the next Engineering Mission and implemented through existing owners only.

Previous blocker:

- Phase: `PHASE4_MEDIUM_BATCH`
- Blocking owner: `v7-egress-guard` invoked by `v7-egress-set-state`
- Terminal owner classification: `POLICY_PROHIBITION`
- Reason: ordinary egress lifecycle mutation intentionally blocks `maintenance|disabled` while enabled users remain assigned.

Implemented capability:

- add a controlled-certification-only guard path for Certification Users on marked Certification Sources;
- preserve ordinary production safety behavior unchanged;
- allow future controlled source degradation only when the source and every assigned enabled user are explicitly marked for certification.

No production mutation, deployment, user movement, Runtime change, Planner change, Authority change, Restore Barrier change, new owner, or new execution path was performed in this implementation step.

## Owners Reused

| Owner | File | Function / contract |
| --- | --- | --- |
| Egress lifecycle guard | `tools/runtime-support/v7-egress-guard` | blocks ordinary assigned-user lifecycle mutation; now supports explicit controlled certification scope |
| Egress lifecycle state owner | `tools/v7-egress-set-state` | passes `--controlled-certification` only when explicitly requested |
| Safe deploy owner | `tools/v7_sync_lib.py` | approved deploy package now includes the existing egress lifecycle executables |

## Changed Files

- `tools/runtime-support/v7-egress-guard`
- `tools/v7-egress-set-state`
- `tools/v7_sync_lib.py`
- `tests/unit/test_v7_egress_lifecycle_guard.py`
- `tests/unit/test_v7_sync_tools.py`

## Contract Added

Controlled certification mode is explicit and fail-closed.

Source is eligible for controlled certification lifecycle mutation only if the egress registry row contains one of:

- `controlled_certification_source=1`
- `certification_source=1`
- `certification_pool=1`
- `certification_group=<value>`

Every enabled assigned user on that source must contain one of:

- `certification_user=1`
- `certification_pool=1`
- `certification_group=<value>`

Otherwise the guard blocks with:

- `controlled_certification_source_not_marked`
- `non_certification_users_assigned`

Default behavior remains unchanged:

- assigned enabled users still produce `reason=users_assigned`;
- ordinary `v7-egress-set-state maintenance|disabled` remains blocked;
- no broad automation is enabled.

## Deploy Owner Gap Found And Closed Locally

The first post-implementation safe-deploy preflight found that the modified egress lifecycle executables were not part of `tools/v7_sync_lib.APPROVED_DEPLOY_FILES`.

Classification:

- `OWNER_INVOCATION_MISSING`

Resolution:

- extend existing safe deploy owner allowlist to include:
  - `/usr/local/bin/v7-egress-guard`
  - `/usr/local/bin/v7-egress-set-state`

This is not a new deploy path. It is the existing deploy owner recognizing existing runtime lifecycle owners.

## Tests

Command:

```text
python3 -m unittest tests.unit.test_v7_egress_lifecycle_guard tests.unit.test_v7_sync_tools
```

Result:

```text
Ran 30 tests in 5.797s
OK
```

Command:

```text
bash -n tools/runtime-support/v7-egress-guard tools/v7-egress-set-state tools/v7-safe-deploy
```

Result:

```text
PASS
```

Command:

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7_sync_lib.py tests/unit/test_v7_egress_lifecycle_guard.py tests/unit/test_v7_sync_tools.py
```

Result:

```text
PASS
```

## Production Impact

Production impact: `NONE`

Deploy performed: `NO`

Users moved: `0`

Production source state changed: `NO`

## Current Capability State

Local implementation is complete and tested.

Production certification is not complete until the existing safe deploy path delivers the changed owners and Phase 4 resumes from the interrupted certification phase.

## Remaining Required Resolution

Continue through existing owners:

1. Commit and push the implementation through the canonical branch.
2. Run the existing safe deploy owner.
3. Verify deployed hashes for:
   - `/usr/local/bin/v7-egress-guard`
   - `/usr/local/bin/v7-egress-set-state`
4. Materialize Certification Source / Certification User markers through existing production registry owners.
5. Resume Phase 4 `MEDIUM_BATCH` from the interrupted controlled-source certification mission.

## Next Engineering Task

`SAFE_DEPLOY_CONTROLLED_CERTIFICATION_EGRESS_LIFECYCLE_EXTENSION`

