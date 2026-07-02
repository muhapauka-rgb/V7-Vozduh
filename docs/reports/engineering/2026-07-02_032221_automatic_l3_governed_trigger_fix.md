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

Delivered.

- Commit: `ea939c69903e16c9c9ad90f43573c669052bc650`
- Branch: `Updatesystem`
- Safe deploy dry-run: PASS
- Safe deploy apply: PASS
- Deployed service unit hash:
  - local: `a4a6d477895ef723f3c3962ce3c965159655689b52cb154f457fa43890d183a2`
  - production: `a4a6d477895ef723f3c3962ce3c965159655689b52cb154f457fa43890d183a2`
- Production service command after deploy:

```text
ExecStart=/usr/local/bin/v7-governed-canary-dry-run-cycle --execute-l3-production-validation --confirm-l3-production-validation EXECUTE_L3_PRODUCTION_VALIDATION_APPROVED --max-users 1
```

The existing production timer was enabled after deploy:

```text
systemctl enable --now v7-users-autoswitch.timer
```

Timer state after enable:

- `v7-users-autoswitch.timer`: active
- Triggered service owner: `v7-governed-canary-dry-run-cycle`

## Production Validation Status

Automatic governed trigger validated in production.

Observed timer-triggered process chain:

```text
v7-users-autoswitch.timer
-> v7-users-autoswitch.service
-> /usr/local/bin/v7-governed-canary-dry-run-cycle --execute-l3-production-validation ... --max-users 1
-> /usr/local/bin/v7-users-autoswitch --emergency-failover-autonomy --mode guarded --max-selected-moves 1 --user 10.7.0.3 --target-egress awg0 --apply --verify
```

Successful production outcome:

- user: `10.7.0.3`
- source: `openvpn-1779388847-d2ad7c`
- target: `awg0`
- terminal state: `APPLIED`
- terminal reason: `selected_moves_applied`
- terminal outcome classification: `SUCCESS`
- verification: PASS (`verify_rc=0`, `service_verify_rc=0`)
- rollback required: false
- registry after execution: `ip=10.7.0.3 current=awg0 table=1001 enabled=1`

Remaining failed-source users after validation:

- `openvpn-1779388847-d2ad7c` users in registry: `10`

Subsequent automatic cycles invoked the same governed owner but stopped safely on existing downstream gates, including:

- `approved_plan_lock_selected_moves_missing`
- `dry_run_restore_barrier_clearance_generation_mismatch`
- `dry_run_restore_barrier_clearance_selected_moves_hash_mismatch`

This means the automatic trigger/scheduler defect is fixed. Remaining incomplete evacuation is now downstream plan-lock / restore-barrier continuity for subsequent users, not failure to invoke the governed L3 owner.

## Next Required Action

Investigate the next downstream blocker for subsequent automatic users:

- owner: `admin_core/operator_execution.py` / restore barrier approved-plan-lock path
- observed blocker: `approved_plan_lock_selected_moves_missing`
- scope: continuation after the first timer-triggered governed success
