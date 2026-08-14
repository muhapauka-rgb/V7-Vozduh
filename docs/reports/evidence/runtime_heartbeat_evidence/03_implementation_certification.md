# Runtime Heartbeat Evidence 03 - Implementation Certification

Local implementation:

| File | Change |
| --- | --- |
| `tools/v7-users-autoswitch` | Added `--pre-planner-refresh={off,dry-run,write}`, `--pre-planner-refresh-command`, and timeout-bounded pre-planner refresh execution. |
| `tools/v7-users-autoswitch` | Added `plan.safety.intelligence_snapshots.pre_planner_refresh` evidence. |
| `tools/v7-users-autoswitch` | Refresh failures, timeouts, source volatility, invalid output, or forbidden `--apply` combination set snapshot gate `stop_required=true`. |
| `systemd/drafts/v7-autoswitch-planner.service` | Reused existing planner service and added `--pre-planner-refresh=write --pre-planner-refresh-command=/usr/local/bin/v7-intelligence-snapshot-refresh`. |
| `tests/unit/test_runtime_snapshot_fast_path.py` | Added pre-planner refresh success, failure fail-closed, and apply-forbidden tests. |

No new runtime authority was introduced. The refresh hook writes only the existing intelligence snapshot root through the existing snapshot refresh tool. It cannot move users, cannot apply autoswitch, and cannot bypass governance.

Written evidence location in runtime output:

```text
plan.safety.intelligence_snapshots.pre_planner_refresh
```

Important states:

| State | Meaning | Runtime behavior |
| --- | --- | --- |
| `DISABLED` | Default CLI behavior unless explicitly enabled. | Load existing snapshots. |
| `REFRESH_SUCCESS` | Existing snapshot refresh CLI wrote stable snapshots. | Load refreshed snapshots and continue planner. |
| `REFRESH_DRY_RUN_SUCCESS` | Refresh path validated without writes. | Load existing snapshots. |
| `SOURCE_VOLATILE` | Refresh detected source instability. | Fail closed; suppress selected moves. |
| `REFRESH_TIMEOUT` | Refresh exceeded timeout. | Fail closed; suppress selected moves. |
| `REFRESH_EXCEPTION` | Refresh command missing/unavailable. | Fail closed; suppress selected moves. |
| `REFRESH_OUTPUT_INVALID` | Refresh output not parseable. | Fail closed; suppress selected moves. |
| `SKIPPED_APPLY_FORBIDDEN` | Pre-planner refresh was requested with `--apply`. | Fail closed; suppress selected moves and apply. |

