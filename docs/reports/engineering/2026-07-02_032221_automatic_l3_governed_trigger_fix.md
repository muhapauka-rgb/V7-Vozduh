# Automatic L3 Governed Trigger Fix

Timestamp: 2026-07-02_032221 UTC

## Mission

Fix the smallest missing wiring link that prevented a confirmed production channel failure from automatically invoking the existing bounded governed L3 production validation owner.

## First Blocker

The production automation loop did not invoke the governed L3 owner.

Production evidence before the fix:

- `v7-users-autoswitch.service` executed `/usr/local/bin/v7-users-autoswitch --apply` directly.
- `v7-users-autoswitch.timer` was inactive and no timer instance was scheduled.
- The direct autoswitch apply path is treated by Runtime wake policy as timer/blind polling, not as a legal L3 wake source.
- The existing governed L3 owner had already been proven in production with one real user moved and verification PASS, but it was not wired into the production timer loop.

## Changed Files

- `systemd/v7-users-autoswitch.service`
- `tools/v7_sync_lib.py`
- `tools/v7-autoswitch-install-systemd`
- `tests/unit/test_v7_sync_tools.py`

## Exact Wiring Change

`systemd/v7-users-autoswitch.service` now invokes:

```text
/usr/local/bin/v7-governed-canary-dry-run-cycle --execute-l3-production-validation --confirm-l3-production-validation EXECUTE_L3_PRODUCTION_VALIDATION_APPROVED --max-users 1
```

instead of:

```text
/usr/local/bin/v7-users-autoswitch --apply
```

## Existing Owner Reused

The invoked owner is:

- `tools/v7-governed-canary-dry-run-cycle`

It continues to use the existing chain:

- Planner: `tools/v7-users-autoswitch`
- Authority / packet / lease: `admin_core/operator_execution.py`
- Runtime action transition: `admin_core/operator_execution_pipeline.py`
- Restore barrier: existing operator execution restore barrier path
- Runtime apply and verification: `tools/v7-users-autoswitch --apply --verify`

No new Runtime, Planner, Authority, Restore Barrier owner, Packet owner, Wake owner, or execution path was created.

## Deployability Fix

`tools/v7_sync_lib.py` now includes `/etc/systemd/system/v7-users-autoswitch.service` in the approved deploy files, so the canonical safe deploy path can deliver the service unit and trigger `systemctl daemon-reload`.

`tools/v7-autoswitch-install-systemd` now installs `/usr/local/bin/v7-governed-canary-dry-run-cycle` alongside the existing autoswitch binaries, so the existing installer remains consistent with the service unit.

## Safety Properties

- Broad automation remains disabled.
- Runtime automation remains false in the governed owner result.
- Authority is not expanded.
- Runtime is not bypassed.
- Restore barrier is not bypassed.
- Planner is not bypassed.
- The production timer no longer calls direct autoswitch apply.
- The governed L3 action remains bounded to `--max-users 1`.

## Tests

Targeted tests:

```text
python3 -m unittest tests.unit.test_v7_sync_tools tests.unit.test_governed_canary_cli
Ran 41 tests
OK
```

Compile checks:

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7_sync_lib.py tools/v7-governed-canary-dry-run-cycle
sh -n tools/v7-autoswitch-install-systemd
PASS
```

Full unit discovery:

```text
python3 -m unittest discover tests/unit
Ran 646 tests
OK
```

## Production Delivery Status

Pending at report creation.

## Production Validation Status

Pending at report creation.

## Next Required Action

Deploy the committed wiring fix with `tools/v7-safe-deploy`, then enable the existing `v7-users-autoswitch.timer` so the production automation loop can invoke the governed L3 owner.
