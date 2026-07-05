# Governed Heartbeat Lifecycle Reconstruction

Timestamp: 2026-07-02 18:43:36 +07
Mode: DEEP_READ_ONLY_FORENSIC
Terminal outcome: FULL_LIFECYCLE_RECONSTRUCTED

## Summary

The persisted systemd flight recorder for `v7-users-autoswitch.timer` on 2026-07-02 contains one complete governed heartbeat activation episode:

```text
2026-07-02T12:00:23+03:00 timer started
2026-07-02T12:00:23+03:00 service cycle 1 started
2026-07-02T12:02:35+03:00 service cycle 6 started
2026-07-02T12:02:46+03:00 timer stopped
2026-07-02T12:02:58+03:00 last service cycle finished
```

Six service cycles were reconstructed without systemd gaps.

The timer stop was not the first execution divergence. The heartbeat was already producing non-useful execution before the stop. The earliest proven continuity break is earlier: after the successful failed-source evacuation of `10.7.0.3`, the successful failed-source incident closed and the next incident/attempt records no longer preserved the failed source as execution identity.

Earliest proven cause:

```text
incident continuity lost after the first successful failed-source move:
73eb29a94ce3010d80c9a73a CLOSED after moving 10.7.0.3
while openvpn-1779388847-d2ad7c still had remaining affected users
then subsequent incidents/attempts used failed_sources=[] or unrelated source identity
```

The final timer stop is a later terminal heartbeat loss, not the root execution cause of the failed evacuation.

## Evidence Sources

Production host:

```text
v3119922.hosted-by-vdsina.ru
```

Read-only sources:

- `journalctl -u v7-users-autoswitch.timer -u v7-users-autoswitch.service`
- `/opt/v7/egress/state/execution-events.jsonl`
- `/opt/v7/egress/state/l3-runtime-state.json`
- `/opt/v7/egress/state/v7-state.json`
- `/opt/v7/egress/state/operator-execution-lease.json`
- local source: `tools/v7-governed-canary-dry-run-cycle`
- local source: `tools/v7-users-autoswitch`
- local reports: `2026-07-02_032221_automatic_l3_governed_trigger_fix.md`, `2026-07-02_163435_current_channel_failure_lifetime_forensic.md`, `2026-07-02_181721_governed_timer_path_forensic.md`

No production writes were performed.

## Baseline Production Reality

The failed production source remained failed with users assigned.

```text
source = openvpn-1779388847-d2ad7c
diagnose_severity = FAIL
diagnose_reason = interface_down_or_missing
code = 000
avg_mbps = 0
min_mbps = 0
stability = 0
users = 10
```

Remaining enabled users observed on the source:

```text
10.7.0.2
10.7.0.4
10.7.0.6
10.7.0.8
10.7.0.9
10.7.0.10
10.7.0.11
10.7.0.12
10.7.0.13
10.7.0.15
```

## Pre-Flight Baseline: Last Known Correct Evacuation

The last proven correct failed-source execution:

| Field | Value |
|---|---|
| created_at | `2026-07-02T03:25:16.066855+00:00` |
| operation_id | `runtime_autoswitch_1367b9f8947a3359ad4ce4e4` |
| incident_key | `73eb29a94ce3010d80c9a73a` |
| user | `10.7.0.3` |
| source | `openvpn-1779388847-d2ad7c` |
| target | `awg0` |
| selected_move_hash | `77c81719cf94321b5d368ad79529909d633123d6e161040865746b297a9d5fb4` |
| terminal_state | `APPLIED` |
| terminal_reason | `selected_moves_applied` |
| verification | `verify_rc=0`, `service_verify_rc=0` |
| rollback | `rollback_required=false` |

Incident record:

```text
incident_key = 73eb29a94ce3010d80c9a73a
failed_sources = ["openvpn-1779388847-d2ad7c"]
selected_users = ["10.7.0.3"]
target_channels = ["awg0"]
status = CLOSED
closed_at = 2026-07-02T03:25:16.070790+00:00
terminal_state = APPLIED
terminal_reason = selected_moves_applied
```

This is the expected evacuation path.

## Earliest Persisted Continuity Break

The first post-success records no longer preserved failed-source continuity.

Immediately after the successful move:

| Time UTC | Operation | Incident | User | Source | Target | Terminal | Reason |
|---|---|---|---|---|---|---|---|
| `2026-07-02T03:25:25.344378+00:00` | `runtime_autoswitch_d1647765d7b998622d5c09ae` | `46ffebc776d1eb9fd256bf2a` | empty | empty | empty | `DRY_RUN` | `dry_run_restore_barrier_clearance_generation_mismatch` |
| `2026-07-02T03:25:30.844890+00:00` | `runtime_autoswitch_98e8a1391d306fafcbbf6c0d` | `dd5b6289529f22197e6694a7` | `10.7.0.3` | `openvpn-1779388847-d2ad7c` | empty | `DENIED` | `approved_plan_lock_selected_moves_missing` |
| `2026-07-02T03:25:47.838314+00:00` | `runtime_autoswitch_bc534a4c654d6bd6c818c514` | `dd5b6289529f22197e6694a7` | `10.7.0.2` | `openvpn-1779388847-d2ad7c` | empty | `DENIED` | `approved_plan_lock_selected_moves_missing` |

The relevant incident record for later repeated attempts:

```text
incident_key = 46ffebc776d1eb9fd256bf2a
status = SUSPENDED
incident_state = INCIDENT_OPEN_STOP_SAFE
opened_at = 2026-07-02T03:25:24.130173+00:00
updated_at = 2026-07-02T09:02:56.576622+00:00
failed_sources = []
failed_required_services = []
selected_users = []
target_channels = []
terminal_state = DENIED
terminal_reason = approved_plan_lock_selected_moves_missing
attempt_count = 15
```

This is the first proven continuity break:

```text
CONTINUES_INCIDENT -> LOSES_INCIDENT / LOSES_SOURCE / LOSES_SELECTED_MOVE
```

The original failed source still had affected users, but the subsequent incident identity no longer carried `failed_sources=["openvpn-1779388847-d2ad7c"]`.

## Complete Timer Flight Recorder

The production unit journal contains one complete `v7-users-autoswitch.timer` activation episode on 2026-07-02:

```text
2026-07-02T12:00:23+03:00 Started v7-users-autoswitch.timer
2026-07-02T12:00:23+03:00 Starting v7-users-autoswitch.service
2026-07-02T12:00:47+03:00 Finished v7-users-autoswitch.service
2026-07-02T12:00:47+03:00 Starting v7-users-autoswitch.service
2026-07-02T12:01:06+03:00 Finished v7-users-autoswitch.service
2026-07-02T12:01:08+03:00 Starting v7-users-autoswitch.service
2026-07-02T12:01:44+03:00 Finished v7-users-autoswitch.service
2026-07-02T12:01:44+03:00 Starting v7-users-autoswitch.service
2026-07-02T12:02:08+03:00 Finished v7-users-autoswitch.service
2026-07-02T12:02:08+03:00 Starting v7-users-autoswitch.service
2026-07-02T12:02:35+03:00 Finished v7-users-autoswitch.service
2026-07-02T12:02:35+03:00 Starting v7-users-autoswitch.service
2026-07-02T12:02:46+03:00 Stopped v7-users-autoswitch.timer
2026-07-02T12:02:58+03:00 Finished v7-users-autoswitch.service
```

Unit state after the episode:

```text
v7-users-autoswitch.timer ActiveState=inactive
v7-users-autoswitch.timer SubState=dead
v7-users-autoswitch.timer UnitFileState=enabled
v7-users-autoswitch.timer NextElapseUSecRealtime=
v7-users-autoswitch.timer LastTriggerUSec=Thu 2026-07-02 12:02:35 MSK
v7-users-autoswitch.service ExecMainStatus=0
```

## Complete Cycle Table

Each cycle below is one systemd `v7-users-autoswitch.service` run. The operation rows are all `execution-outcome-feedback` records persisted inside that service window.

### Cycle 1

| Field | Value |
|---|---|
| service window | `09:00:23Z` -> `09:00:47Z` |
| duration | 24s |
| timer trigger | `12:00:23 MSK` |
| governed owner | `/usr/local/bin/v7-governed-canary-dry-run-cycle --execute-l3-production-validation ... --max-users 1` |
| next trigger | happened immediately at `09:00:47Z` after service completion |
| cycle classification | `LOSES_INCIDENT`, `LOSES_SELECTED_MOVE`, `LOSES_RUNTIME`, `LOSES_VERIFICATION` |

Operations:

| Time UTC | Operation | Incident | User | Source | Target | Move Hash | Terminal | Reason |
|---|---|---|---|---|---|---|---|---|
| `09:00:32.298907` | `runtime_autoswitch_6f5743a0810c2def147d3780` | `46ffebc776d1eb9fd256bf2a` | empty | empty | empty | `4f53cda...b945` | `DRY_RUN` | `dry_run_restore_barrier_clearance_generation_expired` |
| `09:00:45.391807` | `runtime_autoswitch_ea850a74d6202ffbf1287179` | `46ffebc776d1eb9fd256bf2a` | `10.7.0.5` | empty | empty | `4f53cda...b945` | `DENIED` | `approved_plan_lock_selected_moves_missing` |

Changed from expected evacuation:

```text
expected source = openvpn-1779388847-d2ad7c
actual incident failed_sources = []
actual selected user = 10.7.0.5
service log shows current_egress=awg0, recommended_egress=vless for the denied move
```

### Cycle 2

| Field | Value |
|---|---|
| service window | `09:00:47Z` -> `09:01:06Z` |
| duration | 19s |
| next trigger | happened at `09:01:08Z` |
| cycle classification | `LOSES_INCIDENT`, `LOSES_SELECTED_MOVE`, `LOSES_RUNTIME`, `LOSES_VERIFICATION` |

Operations:

| Time UTC | Operation | Incident | User | Source | Target | Move Hash | Terminal | Reason |
|---|---|---|---|---|---|---|---|---|
| `09:00:47.962536` | `runtime_autoswitch_f2b73f6859e5ec4785f63a00` | `c71ba00048521ad4db3fc09d` | empty | empty | empty | `4f53cda...b945` | `DRY_RUN` | `dry_run_restore_barrier_clearance_selected_moves_exceed_budget` |
| `09:00:54.580741` | `runtime_autoswitch_0b9794261b80ea16f1d6bd0c` | `46ffebc776d1eb9fd256bf2a` | `10.7.0.5` | empty | empty | `4f53cda...b945` | `DRY_RUN` | `dry_run_restore_barrier_clearance_budget_and_generation_ok` |
| `09:01:04.429559` | `runtime_autoswitch_eee7e2b240622a89ddecdc7c` | `46ffebc776d1eb9fd256bf2a` | `10.7.0.5` | empty | empty | `4f53cda...b945` | `DENIED` | `approved_plan_lock_selected_moves_missing` |

Changed from previous:

```text
same broken 46ff incident continued
additional c71 DRY_RUN artifact appeared with no user/source
no Runtime Apply
no Verification
```

### Cycle 3

| Field | Value |
|---|---|
| service window | `09:01:08Z` -> `09:01:44Z` |
| duration | 36s |
| next trigger | happened immediately at `09:01:44Z` |
| cycle classification | `LOSES_INCIDENT`, `LOSES_SELECTED_MOVE`, `LOSES_RUNTIME`, `LOSES_VERIFICATION` |

Operations:

| Time UTC | Operation | Incident | User | Source | Target | Move Hash | Terminal | Reason |
|---|---|---|---|---|---|---|---|---|
| `09:01:14.672191` | `runtime_autoswitch_92013901ec3c940aa29f6d59` | `c71ba00048521ad4db3fc09d` | empty | empty | `vless` | `f9d498...b8ff` | `DRY_RUN` | `dry_run_selected_moves_available` |
| `09:01:24.894920` | `runtime_autoswitch_9e1f05e0fb32ad57759af1b2` | `46ffebc776d1eb9fd256bf2a` | `10.7.0.5` | empty | empty | `4f53cda...b945` | `DRY_RUN` | `dry_run_restore_barrier_clearance_budget_and_generation_ok` |
| `09:01:41.405408` | `runtime_autoswitch_00889e4a3e9a88fa1e263697` | `46ffebc776d1eb9fd256bf2a` | `10.7.0.5` | empty | empty | `4f53cda...b945` | `DENIED` | `approved_plan_lock_selected_moves_missing` |

Changed from previous:

```text
c71 selected_move_hash changed to f9d498...b8ff and target=vless
46ff still denied on approved_plan_lock_selected_moves_missing
```

### Cycle 4

| Field | Value |
|---|---|
| service window | `09:01:44Z` -> `09:02:08Z` |
| duration | 24s |
| next trigger | happened immediately at `09:02:08Z` |
| cycle classification | `LOSES_INCIDENT`, `LOSES_SELECTED_MOVE`, `LOSES_RUNTIME`, `LOSES_VERIFICATION` |

Operations:

| Time UTC | Operation | Incident | User | Source | Target | Move Hash | Terminal | Reason |
|---|---|---|---|---|---|---|---|---|
| `09:01:49.486690` | `runtime_autoswitch_9ac06cf6c6c9244caae0853a` | `c71ba00048521ad4db3fc09d` | empty | empty | `vless` | `f9d498...b8ff` | `DRY_RUN` | `dry_run_selected_moves_available` |
| `09:01:56.849722` | `runtime_autoswitch_d429ed212041e2397ec60da4` | `46ffebc776d1eb9fd256bf2a` | `10.7.0.5` | empty | empty | `4f53cda...b945` | `DRY_RUN` | `dry_run_restore_barrier_clearance_budget_and_generation_ok` |
| `09:02:06.684653` | `runtime_autoswitch_8a92a92f148a8b8ae223fec5` | `46ffebc776d1eb9fd256bf2a` | `10.7.0.5` | empty | empty | `4f53cda...b945` | `DENIED` | `approved_plan_lock_selected_moves_missing` |

Changed from previous:

```text
no material identity recovery
same c71 preview and 46ff denied pattern repeated
```

### Cycle 5

| Field | Value |
|---|---|
| service window | `09:02:08Z` -> `09:02:35Z` |
| duration | 27s |
| next trigger | happened immediately at `09:02:35Z` |
| cycle classification | `LOSES_INCIDENT`, `LOSES_SELECTED_MOVE`, `LOSES_RUNTIME`, `LOSES_VERIFICATION` |

Operations:

| Time UTC | Operation | Incident | User | Source | Target | Move Hash | Terminal | Reason |
|---|---|---|---|---|---|---|---|---|
| `09:02:15.715253` | `runtime_autoswitch_82f767c882235741557512c8` | `46ffebc776d1eb9fd256bf2a` | `10.7.0.5` | empty | empty | `4f53cda...b945` | `DRY_RUN` | `dry_run_restore_barrier_clearance_budget_and_generation_ok` |
| `09:02:29.207763` | `runtime_autoswitch_3514e88b51b50cef9f5d1c70` | `c71ba00048521ad4db3fc09d` | empty | empty | `vless` | `f9d498...b8ff` | `DRY_RUN` | `dry_run_selected_moves_available` |
| `09:02:32.747985` | `runtime_autoswitch_ebdd4d4ed3d5f9e568cf23ed` | `46ffebc776d1eb9fd256bf2a` | `10.7.0.5` | empty | empty | `4f53cda...b945` | `DENIED` | `approved_plan_lock_selected_moves_missing` |

Changed from previous:

```text
same broken alternation continued
no Runtime Apply
no Verification
```

### Cycle 6

| Field | Value |
|---|---|
| service window | `09:02:35Z` -> `09:02:58Z` |
| duration | 23s |
| timer stop | `09:02:46Z`, while service still running |
| next trigger | did not happen because timer was stopped |
| cycle classification | `LOSES_INCIDENT`, `LOSES_SELECTED_MOVE`, `LOSES_RUNTIME`, `LOSES_VERIFICATION`, `LOSES_TIMER` |

Operations:

| Time UTC | Operation | Incident | User | Source | Target | Move Hash | Terminal | Reason |
|---|---|---|---|---|---|---|---|---|
| `09:02:43.524504` | `runtime_autoswitch_f16337da689d38f97276fd24` | `46ffebc776d1eb9fd256bf2a` | `10.7.0.5` | empty | empty | `4f53cda...b945` | `DRY_RUN` | `dry_run_restore_barrier_clearance_budget_and_generation_ok` |
| `09:02:53.772596` | `runtime_autoswitch_d8b559565b101a7bab02318a` | `c71ba00048521ad4db3fc09d` | empty | empty | `vless` | `f9d498...b8ff` | `DRY_RUN` | `dry_run_selected_moves_available` |
| `09:02:56.574376` | `runtime_autoswitch_5cf1792f5557d5810ecfb9b6` | `46ffebc776d1eb9fd256bf2a` | `10.7.0.5` | empty | empty | `4f53cda...b945` | `DENIED` | `approved_plan_lock_selected_moves_missing` |

Changed from previous:

```text
same broken execution pattern repeated
timer stopped during the service run
service still exited success at 09:02:58Z
no next scheduled trigger
```

## Planner-Only Period After Timer Stop

After `v7-users-autoswitch.timer` stopped:

```text
v7-users-autoswitch.timer = inactive/dead
v7-autoswitch-planner.timer = active/waiting
```

Post-stop execution-events continued, but from planner-only cycles, not governed movement heartbeat. Examples:

| Time UTC | Operation | Incident | Target | Terminal | Reason |
|---|---|---|---|---|---|
| `09:04:22.915824` | `runtime_autoswitch_220eea6e4c1d21be23c82a34` | `c71ba00048521ad4db3fc09d` | `vless` | `DRY_RUN` | `dry_run_selected_moves_available` |
| `09:04:59.563654` | `runtime_autoswitch_07a3983531b668d2cf334c79` | `c71ba00048521ad4db3fc09d` | `vless` | `DRY_RUN` | `dry_run_selected_moves_available` |

No Runtime Apply or Verification occurred in the planner-only period.

## First Divergence

There are two useful levels:

### Earliest Proven Execution Divergence

Earliest proven divergence after a correct execution:

```text
2026-07-02T03:25:25.344378+00:00
operation_id = runtime_autoswitch_d1647765d7b998622d5c09ae
incident_key = 46ffebc776d1eb9fd256bf2a
failed_sources = []
selected_users = []
terminal_state = DRY_RUN
terminal_reason = dry_run_restore_barrier_clearance_generation_mismatch
```

Compared to the previous correct evacuation:

```text
previous incident = 73eb29a94ce3010d80c9a73a
previous failed_sources = ["openvpn-1779388847-d2ad7c"]
previous selected_users = ["10.7.0.3"]
previous source = openvpn-1779388847-d2ad7c
previous target = awg0
previous terminal_state = APPLIED
```

Changed field:

```text
failed_sources: ["openvpn-1779388847-d2ad7c"] -> []
selected_users: ["10.7.0.3"] -> []
source identity: openvpn-1779388847-d2ad7c -> empty/unpreserved
```

Owner:

```text
tools/v7-users-autoswitch L3 incident lifecycle / execution eligibility
```

Artifact:

```text
/opt/v7/egress/state/l3-runtime-state.json
/opt/v7/egress/state/execution-events.jsonl
```

### First Divergence In The Final Timer Episode

Cycle 1 was already divergent.

```text
cycle = 1
operation_id = runtime_autoswitch_6f5743a0810c2def147d3780
incident_key = 46ffebc776d1eb9fd256bf2a
failed_sources = []
terminal_state = DRY_RUN
terminal_reason = dry_run_restore_barrier_clearance_generation_expired
```

The final timer episode never reached a correct failed-source evacuation state.

## First Continuity Break

First continuity break:

```text
CONTINUES_INCIDENT -> LOSES_INCIDENT
```

Evidence:

```text
73eb29a94ce3010d80c9a73a:
  failed_sources = ["openvpn-1779388847-d2ad7c"]
  selected_users = ["10.7.0.3"]
  terminal_state = APPLIED
  status = CLOSED

46ffebc776d1eb9fd256bf2a:
  failed_sources = []
  selected_users = []
  terminal_state = DRY_RUN / DENIED
  status = SUSPENDED
```

This happened before the final timer stop.

## Incident Lifetime

| Incident | Opened | Closed | Status | Failed Sources | Selected Users | Terminal |
|---|---|---|---|---|---|---|
| `73eb29a94ce3010d80c9a73a` | `2026-07-02T03:25:00Z` | `2026-07-02T03:25:16Z` | `CLOSED` | `["openvpn-1779388847-d2ad7c"]` | `["10.7.0.3"]` | `APPLIED` |
| `46ffebc776d1eb9fd256bf2a` | `2026-07-02T03:25:24Z` | empty | `SUSPENDED` | `[]` | `[]` | `DENIED` |
| `c71ba00048521ad4db3fc09d` | `2026-07-02T03:25:06Z` | empty | `OPEN` | `[]` | `[]` | `DRY_RUN` |

Incident continuity stopped after `73eb29a94ce3010d80c9a73a` closed.

## Production Reality Comparison

| Time / Scope | Production Reality | Execution Reality | Verdict |
|---|---|---|---|
| `03:25:16Z` | OpenVPN source failed, user `10.7.0.3` affected | user `10.7.0.3` moved from OpenVPN to `awg0` | aligned |
| `03:25:25Z` | OpenVPN source still had remaining users | incident `46ff...` had `failed_sources=[]` | diverged |
| `09:00:23Z` cycle 1 | OpenVPN still failed, 10 users remained | incident `46ff...`, source empty, user `10.7.0.5` / wrong current source path | diverged |
| `09:02:56Z` cycle 6 | OpenVPN still failed, 10 users remained | `approved_plan_lock_selected_moves_missing`, no apply | diverged |
| post `09:02:46Z` | OpenVPN still failed, users remained | movement heartbeat stopped; planner-only DRY_RUN continued | diverged |

## State Machine

Observed legal/expected transition:

```text
FAILED_SOURCE_INCIDENT_OPEN
-> ONE_USER_SELECTED_FROM_FAILED_SOURCE
-> AUTHORITY/RESTORE_BARRIER
-> RUNTIME_APPLY
-> VERIFICATION_PASS
-> ONE_USER_SUCCESS
```

Expected continuation:

```text
ONE_USER_SUCCESS
-> SAME_FAILED_SOURCE_INCIDENT_REMAINS_OPEN
-> NEXT_REMAINING_USER_SELECTED_FROM_FAILED_SOURCE
-> NEXT_BOUNDED_GOVERNED_APPLY
```

Observed transition:

```text
ONE_USER_SUCCESS
-> INCIDENT_CLOSED
-> NEW/SUSPENDED INCIDENT WITH failed_sources=[]
-> RESTORE_BARRIER / APPROVED_LOCK MISMATCHES
-> DENIED / DRY_RUN
-> TIMER_STOP
-> PLANNER_ONLY_DRY_RUN
```

Unexpected transitions:

- `INCIDENT_CLOSED` while affected users remained.
- `failed_sources` became empty.
- selected user/source no longer represented failed OpenVPN evacuation.
- Runtime Apply and Verification were never reached in the final timer episode.
- Timer stopped after repeated non-executing cycles.

Missing transitions:

- no persisted transition from first success to same-source next-user incident continuation;
- no persisted Runtime Apply after the success incident;
- no persisted Verification after the success incident;
- no persisted automatic restart after timer stop.

## Root Cause Tree

```text
Timer stopped producing governed execution
  because v7-users-autoswitch.timer was stopped at 09:02:46Z
  and no next trigger was scheduled

But useful evacuation had already stopped before the timer stop
  because all six final timer cycles ended in DRY_RUN or DENIED
  and none reached Runtime Apply or Verification

Those cycles did not evacuate failed-source users
  because their incidents did not preserve failed source identity
  and approved selected moves were missing/mismatched

The earliest proven continuity break occurred after the first successful move
  because incident 73eb... closed after moving 10.7.0.3
  while production still had remaining users on openvpn-1779388847-d2ad7c
  and subsequent incident 46ff... had failed_sources=[]
```

Earliest proven cause:

```text
failed-source incident continuity was lost after the first success.
```

The timer stop is not the execution root cause. It is a later terminal heartbeat loss after the execution path was already broken.

## Loop Termination

Why did the heartbeat stop producing useful execution?

Primary execution answer:

```text
Incident divergence / source continuity break.
```

Final heartbeat answer:

```text
Heartbeat stop at 09:02:46Z prevented further governed cycles.
```

The stop did not create the first execution divergence. It ended an already non-useful loop.

## Persisted Evidence Limits

The following fields were not consistently persisted in `execution-events.jsonl` per operation:

- `planner_generation_id`
- explicit Wake decision
- full Authority result
- full approved plan lock object
- full restore barrier object
- Runtime eligibility matrix

However, the lifecycle is reconstructed at timer-cycle level from systemd journal, and at execution outcome level from persisted `execution-events.jsonl` plus `l3-runtime-state.json`. These are sufficient to prove the first continuity break and to classify the timer stop as not the earliest execution cause.

## Final Verdict

Terminal outcome: `FULL_LIFECYCLE_RECONSTRUCTED`

Number of reconstructed timer cycles: `6`

First divergent timer cycle: `cycle 1`

First overall continuity break:

```text
2026-07-02T03:25:25.344378+00:00
runtime_autoswitch_d1647765d7b998622d5c09ae
incident 46ffebc776d1eb9fd256bf2a
failed_sources=[]
```

Earliest proven cause:

```text
failed-source incident continuity was lost after the first successful failed-source move.
```

Timer stop:

```text
consequence / later terminal heartbeat loss, not the root execution cause.
```

Next required action:

```text
fix or certify incident-source continuity across bounded governed cycles,
then restore the existing governed heartbeat through approved production procedure
and rerun certification.
```
