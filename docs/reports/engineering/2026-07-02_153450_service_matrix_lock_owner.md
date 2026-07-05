# V7 Service Matrix Lock Owner During Failed Post-Apply Verification

Timestamp: 2026-07-02_153450

Mode: READ_ONLY_FORENSIC

## Mission

Identify who held `/opt/v7/egress/state/service-matrix.lock` during the failed post-apply verification for the exact production execution:

- governed operation: `govexec_99a887e81cfa5a711d426f31`
- runtime operation: `runtime_autoswitch_649bef0fdf139f8297fe7015`
- user: `10.7.0.2`
- target: `vless`
- terminal result: `ROLLED_BACK`
- terminal reason: `verification_failed_rollback_completed`
- failed verifier: `v7-service-matrix-test vless telegram --timeout 5 --state-dir /opt/v7/egress/state`
- verifier failure: subprocess wrapper timed out after 10 seconds

No code, Runtime, Planner, Verification, service-matrix, routing, or production state was modified.

## Sources

- Production systemd journal for:
  - `v7-users-autoswitch.service`
  - `v7-autoswitch-planner.service`
  - `v7-telegram-sentinel.service`
- Production file metadata for:
  - `/opt/v7/egress/state/service-matrix.lock`
  - `/opt/v7/egress/state/service-matrix.json`
  - `/opt/v7/egress/state/operator-execution-lease.json`
- Source code:
  - `tools/v7-users-autoswitch`
  - `tools/v7-service-matrix-test`
  - `tools/v7-telegram-sentinel`
  - `tools/v7-service-matrix-refresh-all`

## Important Evidence Limit

`service-matrix.lock` is a kernel `flock` coordination file. The file inode does not persist historical lock owner PID, parent PID, or command line.

Observed file metadata:

- `/opt/v7/egress/state/service-matrix.lock`
  - size: `0`
  - mode: `600`
  - ctime: `2026-06-07 00:26:44.852618987 +0300`
  - mtime: `2026-06-07 00:26:44.852618987 +0300`

Therefore the lock file itself cannot prove the exact historical owner at the precise microsecond when verification attempted acquisition.

The owner must be proven from persisted process/journal payloads. Those payloads prove overlapping service-matrix writer ownership during the failed verification window.

## Lock Implementations

### Verification Path

`tools/v7-users-autoswitch::_verify_emergency_required_services()` runs:

```text
v7-service-matrix-test <target> <service> --timeout <timeout_sec> --state-dir <state_dir>
```

For this execution:

```text
v7-service-matrix-test vless telegram --timeout 5 --state-dir /opt/v7/egress/state
```

The wrapper timeout is `timeout_sec + 5`, therefore `10` seconds.

Source: `tools/v7-users-autoswitch:8659-8689`.

### Verifier Lock

`tools/v7-service-matrix-test::service_matrix_writer_lock()` opens:

```text
/opt/v7/egress/state/service-matrix.lock
```

and attempts:

```text
fcntl.flock(fd, LOCK_EX | LOCK_NB)
```

It sleeps and retries until `--lock-timeout-sec`, whose default is `90` seconds.

Source: `tools/v7-service-matrix-test:111-134`, `tools/v7-service-matrix-test:526`, `tools/v7-service-matrix-test:567`.

The verification caller does not pass `--lock-timeout-sec`; therefore the child can legally wait up to `90` seconds, but the parent kills it after `10` seconds.

### Telegram Sentinel Lock

`tools/v7-telegram-sentinel::service_matrix_writer_lock()` uses the same exclusive writer lock and writes Telegram service results into `service-matrix.json`.

Source: `tools/v7-telegram-sentinel:81-104`, `tools/v7-telegram-sentinel:480-482`.

### Planner Lifecycle Lock

`tools/v7-users-autoswitch::acquire_service_matrix_lock()` can also hold the same file lock for `planner_snapshot_packet_lifecycle` when `--pre-planner-refresh=write` is active.

Source: `tools/v7-users-autoswitch:508-560`.

## Execution Timeline

All times below are UTC.

| Time | Event | Evidence |
| --- | --- | --- |
| `07:59:44.664196` | `v7-users-autoswitch.service` started. | systemd journal |
| `07:59:44.665074` | `v7-autoswitch-planner.service` started. | systemd journal |
| `07:59:50.515234` | Planner process observed: `python3 /usr/local/bin/v7-users-autoswitch --pre-planner-refresh=write --pre-planner-refresh-command=/usr/local/bin/v7-intelligence-snapshot-refresh`, PID `1029085`. | systemd journal |
| `07:59:50.609159` | First planner service deactivated successfully. | systemd journal |
| approx `08:00:08` | Runtime apply succeeded for selected user; apply output recorded `last_switch=1782979208`. | governed execution payload |
| `08:00:14.285115` | `v7-telegram-sentinel.service` started. | systemd journal |
| `08:00:14.782926` | `v7-autoswitch-planner.service` started again. | systemd journal |
| `08:00:15.576449` | Planner runtime operation started: `runtime_autoswitch_683bf20f6d95fcbe8cfa1ce8`. | planner payload |
| `08:00:15.576449` to `08:00:23.162389` | Planner reports `service_matrix_lock.acquired=true`, owner `tools/v7-users-autoswitch`, scope `planner_snapshot_packet_lifecycle`, waited `0.0`, timeout `90`. | planner payload |
| after apply, before rollback | Route verification ran, then service verification launched `v7-service-matrix-test vless telegram --timeout 5`. | governed execution payload |
| before approx `08:00:25` | Service verification was killed by parent wrapper after `10` seconds: `timed out after 10 seconds`. | governed execution payload |
| approx `08:00:25` | Rollback completed; rollback output recorded `last_switch=1782979225`. | governed execution payload |
| `08:00:26.499241` | Planner process observed: `python3 /usr/local/bin/v7-users-autoswitch --pre-planner-refresh=write --pre-planner-refresh-command=/usr/local/bin/v7-intelligence-snapshot-refresh`, PID `1035893`. | systemd journal |
| `08:00:26.666795` | Second planner service deactivated successfully. | systemd journal |
| `08:00:26.723254` | Telegram sentinel final payload: `elapsed_sec=12.132`, `service_matrix_lock.held=true`, `inherited=false`, path `/opt/v7/egress/state/service-matrix.lock`. | sentinel payload |
| `08:00:26.827647` | `v7-telegram-sentinel.service` deactivated successfully. | systemd journal |
| `08:00:29.959040` | Governed cycle final payload logged the failed execution and rollback. | governed execution payload |
| `08:00:30.075371` | `v7-users-autoswitch.service` deactivated successfully. | systemd journal |

## Proven Lock Holder

The proven overlapping lock holder during the failed post-apply verification window is:

- owner unit: `v7-telegram-sentinel.service`
- executable: `python3 /usr/local/bin/v7-telegram-sentinel --threshold-seconds 14 --timeout 1 --no-autoswitch`
- observed PID: `1035685`
- lock path: `/opt/v7/egress/state/service-matrix.lock`
- lock state: `held=true`, `inherited=false`
- elapsed duration: `12.132` seconds
- service wall interval: `2026-07-02T08:00:14.285115Z` to `2026-07-02T08:00:26.827647Z`
- reason: Telegram sentinel writes Telegram service results into the shared service matrix.

The same window also contains a concurrent planner lifecycle writer:

- owner unit: `v7-autoswitch-planner.service`
- executable: `python3 /usr/local/bin/v7-users-autoswitch --pre-planner-refresh=write --pre-planner-refresh-command=/usr/local/bin/v7-intelligence-snapshot-refresh`
- observed PID: `1035893`
- lock owner field: `tools/v7-users-autoswitch`
- scope: `planner_snapshot_packet_lifecycle`
- decision: `service_matrix_writer_serialized_for_planner_lifecycle`
- acquired: `true`
- waited: `0.0`
- service wall interval: `2026-07-02T08:00:14.782926Z` to `2026-07-02T08:00:26.666795Z`
- payload interval: `2026-07-02T08:00:15.576449Z` to `2026-07-02T08:00:23.162389Z`

Because kernel `flock` ownership is not historically persisted, the exact PID holding the kernel lock at the precise verifier acquisition attempt is not directly recoverable. The strongest persisted proof is that `v7-telegram-sentinel.service` held the service-matrix writer lock across the verification timeout window, while the planner lifecycle writer also participated in the same lock domain.

## Wait Graph

```text
Runtime post-apply verification
  -> tools/v7-users-autoswitch::_verify_emergency_required_services()
  -> v7-service-matrix-test vless telegram --timeout 5 --state-dir /opt/v7/egress/state
  -> tools/v7-service-matrix-test::update_matrix()
  -> tools/v7-service-matrix-test::service_matrix_writer_lock()
  -> waiting for /opt/v7/egress/state/service-matrix.lock
  -> held by overlapping writer: v7-telegram-sentinel.service, PID 1035685
  -> concurrent writer domain: v7-autoswitch-planner.service, PID 1035893
  -> verifier parent wrapper timeout after 10 seconds
  -> service_verify_rc = 1
  -> rollback
```

## Questions

### 1. Who created `service-matrix.lock`?

The historical file creator is not persisted. The file ctime is `2026-06-07`, long before this execution, and the file is a zero-byte flock coordination file.

During this failed execution, the proven writer-lock holder was `v7-telegram-sentinel.service`. A concurrent planner lifecycle writer also acquired the same lock domain.

### 2. Which executable owned it?

Proven overlapping holder:

```text
python3 /usr/local/bin/v7-telegram-sentinel --threshold-seconds 14 --timeout 1 --no-autoswitch
```

Observed PID:

```text
1035685
```

Concurrent writer:

```text
python3 /usr/local/bin/v7-users-autoswitch --pre-planner-refresh=write --pre-planner-refresh-command=/usr/local/bin/v7-intelligence-snapshot-refresh
```

Observed PID:

```text
1035893
```

### 3. Which function created or acquired it?

For the proven overlapping holder:

```text
tools/v7-telegram-sentinel::service_matrix_writer_lock()
```

For the verifier that waited:

```text
tools/v7-service-matrix-test::service_matrix_writer_lock()
```

For the concurrent planner writer:

```text
tools/v7-users-autoswitch::acquire_service_matrix_lock()
```

### 4. Why was the lock required?

The lock serializes writers to the shared service matrix:

```text
/opt/v7/egress/state/service-matrix.json
```

It prevents concurrent matrix writers from interleaving updates.

### 5. Was it Planner, background refresh, periodic refresh, another verification, Autoswitch, updater, health scanner, or unknown?

Classification:

```text
LOCK_HELD_BY_SERVICE_MATRIX_WRITER
```

The proven overlapping holder is `v7-telegram-sentinel.service`, a service-matrix writer/health scanner for Telegram status.

There was also a concurrent Planner lifecycle writer using `tools/v7-users-autoswitch --pre-planner-refresh=write`.

### 6. Was the lock still active after Apply?

Yes.

Apply completed before service verification and rollback. The sentinel writer was active from `08:00:14.285115Z` through `08:00:26.827647Z`; rollback completed around `08:00:25Z`. Therefore the sentinel lock holder was still active after Apply and through rollback.

### 7. How long was it held?

Proven overlapping sentinel holder:

```text
12.132 seconds
```

Concurrent planner writer service wall duration:

```text
11.884 seconds
```

Verifier parent timeout:

```text
10 seconds
```

### 8. Was Verification waiting correctly?

Yes for the current implementation path.

`v7-service-matrix-test` is a writer path. It updates `service-matrix.json` and therefore must acquire the writer lock before writing.

### 9. Was the lock stale?

No evidence of a stale lock.

Both overlapping services finished normally:

- `v7-telegram-sentinel.service`: deactivated successfully at `08:00:26.827647Z`
- `v7-autoswitch-planner.service`: deactivated successfully at `08:00:26.666795Z`

The old mtime/ctime on the zero-byte lock file is not evidence of a stale `flock`; it is normal for a reusable lock file.

### 10. Did the lock owner finish normally?

Yes.

The proven sentinel holder finished normally. The concurrent planner writer also finished normally.

### 11. Was there a deadlock?

No deadlock is proven.

The evidence shows lock contention plus a verifier wrapper timeout shorter than the writer lock wait budget. The lock owners completed normally shortly after the verifier timed out.

### 12. Could Verification have safely bypassed the lock?

Not proven.

Current `v7-service-matrix-test` uses the writer path and does not expose a proven read-only verification mode in the inspected implementation.

### 13. Can Verification use a read-only path that does not require this writer lock?

No existing implemented path was found.

`v7-service-matrix-test` calls `update_matrix()` and `service_matrix_writer_lock()`. The CLI exposes `--lock-timeout-sec`, but no `--read-only` or `--no-write` verifier mode was found.

### 14. Would reducing timeout fix the root cause?

No.

Reducing the verifier timeout would make the verifier fail faster. The root cause is that post-apply verification uses a writer-locking service-matrix test path while overlapping service-matrix writers can hold the lock longer than the verifier parent timeout.

## Root Cause Classification

```text
LOCK_HELD_BY_SERVICE_MATRIX_WRITER
```

The failed post-apply verifier waited in the service-matrix writer lock domain. The proven overlapping holder was `v7-telegram-sentinel.service`, which held `/opt/v7/egress/state/service-matrix.lock` for `12.132` seconds. The verifier wrapper killed `v7-service-matrix-test` after `10` seconds before it returned a service result.

This was not a stale lock, not a lock leak, and not a deadlock.

## Safe Fix Direction

`PATCH_REQUIRED`

Minimal correction direction:

1. Preserve the writer lock for real writers.
2. Do not bypass locking.
3. Fix post-apply verification so it does not depend on the shared writer-lock path, or make the verifier lock wait budget explicitly bounded and aligned with the parent wrapper timeout.
4. Persist lock wait outcomes such as `LOCK_TIMEOUT`, lock path, waited seconds, and current verification operation identity so future rollbacks are diagnosable without reconstructing journal windows.

No broad automation, Planner, Runtime, Authority, Restore Barrier, routing, or production behavior was changed by this investigation.
