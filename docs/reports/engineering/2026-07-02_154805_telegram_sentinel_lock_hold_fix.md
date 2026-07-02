# V7 Telegram Sentinel Lock Hold Fix

Timestamp: 2026-07-02_154805

Mode: Discover -> Reuse -> Extend -> Implement

## Summary

Fixed `tools/v7-telegram-sentinel` so the service-matrix writer lock protects only the shared matrix mutation boundary:

```text
read latest service-matrix.json
merge Telegram rows in memory
atomic write service-matrix.json
```

The implementation does not modify Planner selection logic, Runtime safety gates, Authority, Restore Barrier, service verification, Telegram verification, broad automation, or user movement.

## Source Of 12 Second Behavior

Production evidence showed the long sentinel run as:

```text
elapsed_sec = 12.132
service_matrix_lock.held = true
```

Source-code inspection found that Telegram network probes already execute before `service_matrix_writer_lock()` in `tools/v7-telegram-sentinel::main()`.

Therefore `12.132` was the full sentinel cycle duration, not a directly persisted lock-hold duration. The previous payload did not include `held_sec` or `waited_sec`, so the exact historical lock hold duration was not persisted.

The production systemd configuration explains the cycle shape:

- unit: `/etc/systemd/system/v7-telegram-sentinel.service`
- drop-in: `/etc/systemd/system/v7-telegram-sentinel.service.d/10-advisory-first.conf`
- effective command:

```text
/usr/local/bin/v7-telegram-sentinel --threshold-seconds 14 --timeout 1 --no-autoswitch
```

- timer: `/etc/systemd/system/v7-telegram-sentinel.timer`
- cadence:

```text
OnBootSec=30s
OnUnitActiveSec=4s
AccuracySec=1s
```

`--threshold-seconds 14` is a grace threshold for declaring Telegram hard-down after repeated bad samples. It is not a lock-hold value.

`--timeout 1` is the per-endpoint TCP probe timeout. It can contribute to total sentinel elapsed time when many egresses are checked, but the fixed design keeps that network work outside the writer lock.

No manual override changing threshold or timeout was found beyond the advisory drop-in that adds `--no-autoswitch`.

## Exact First Bad Lock Boundary

The current code did not hold the writer lock during `check_telegram()` network probes.

The remaining bad boundary was narrower:

```text
with service_matrix_writer_lock(...):
    for item in items.values():
        update_matrix(...)
```

`update_matrix()` reloaded and rewrote the full `service-matrix.json` for each egress item while the writer lock was held.

That made lock scope larger than the required shared-file mutation boundary.

## Fix Location

Changed:

- `tools/v7-telegram-sentinel::service_matrix_writer_lock()`
- `tools/v7-telegram-sentinel::merge_matrix_item()`
- `tools/v7-telegram-sentinel::update_matrix_items()`
- `tools/v7-telegram-sentinel::main()`

Added:

- `tests/unit/test_telegram_sentinel_lock_scope.py`

## Old Lock Scope

```text
acquire service-matrix.lock
for each checked egress:
    read service-matrix.json
    merge one Telegram row
    atomic write service-matrix.json
release service-matrix.lock
```

## New Lock Scope

```text
perform Telegram probes outside lock
build item results in memory
acquire service-matrix.lock
read latest service-matrix.json once
merge all Telegram rows in memory
atomic write service-matrix.json once
release service-matrix.lock
```

## Lock Hold Evidence Added

`service_matrix_writer_lock()` now reports:

- `waited_sec`
- `held_sec`
- `released`

This prevents future investigations from using total sentinel `elapsed_sec` as a proxy for lock hold time.

## Data Integrity

The fix keeps:

- the existing `service-matrix.lock`;
- exclusive writer serialization;
- reload of latest `service-matrix.json` inside the lock;
- atomic temp-file write and `os.replace()`;
- existing Telegram row schema;
- existing `update_matrix()` compatibility wrapper for callers/tests that update a single row.

## Tests

Added tests prove:

1. `v7-telegram-sentinel` does not hold `service-matrix.lock` during Telegram network probing.
2. `v7-telegram-sentinel` acquires `service-matrix.lock` only after probes and holds it for matrix write.
3. `service-matrix.json` write remains atomic.
4. Existing service rows are preserved during Telegram merge.
5. Concurrent writer wait does not corrupt the matrix.
6. Lock is not left held when probe fails.
7. Lock is released if matrix write fails.
8. Existing sentinel behavior still produces a correct Telegram matrix row.

Executed:

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests.unit.test_telegram_sentinel_lock_scope
```

Result:

```text
Ran 7 tests
OK
```

Executed:

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-telegram-sentinel tests/unit/test_telegram_sentinel_lock_scope.py
```

Result:

```text
OK
```

Executed:

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests.unit.test_v7_users_autoswitch_policy
```

Result:

```text
Ran 113 tests
OK
```

Executed:

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests.unit.test_governed_canary_cli
```

Result:

```text
Ran 17 tests
OK
```

Executed:

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests.unit.test_service_aware_policy tests.unit.test_runtime_snapshot_fast_path tests.unit.test_egress_quality_compact_lifecycle
```

Result:

```text
Ran 24 tests
OK
```

## Production Validation

Read-only production configuration audit was performed.

No deploy was performed.

No production sentinel cycle was manually run.

No governed L3 validation was run.

No users were moved.

Production validation of the deployed code hash and measured live `held_sec` remains pending because deployment was not performed in this task.

## Remaining Blocker

No local implementation blocker remains for the sentinel lock scope.

Remaining production step:

1. Deploy the updated `tools/v7-telegram-sentinel`.
2. Observe the next natural `v7-telegram-sentinel.timer` cycle or run one explicitly authorized read-only sentinel cycle.
3. Confirm production payload includes short `service_matrix_lock.held_sec`.
4. Then rerun bounded governed L3 validation only if authorized.
