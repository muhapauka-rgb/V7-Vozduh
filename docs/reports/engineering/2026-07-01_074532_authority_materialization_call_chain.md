# Authority Materialization Call Chain Audit

Дата: 2026-07-01 07:45:32 +0700

Вердикт: `MISSING_CALLER`

## Summary

`build_restore_barrier_clearance()` не был вызван для текущего L3 Production Validation candidate, потому что фактический L3 validation run пошел напрямую через `tools/v7-users-autoswitch`.

Этот путь является consumer/executor: он читает restore barrier и approved plan lock, проверяет их, затем решает apply / STOP_SAFE. Он не является producer materialized authority envelope и не вызывает `admin_core/operator_execution.py`.

Первый пропущенный executable call:

```text
L3 Production Validation selected candidate
  -> create/govern fresh approval packet + approved_plan_lock
  -> execute runtime action CREATE_RESTORE_BARRIER_CLEARANCE
  -> build_restore_barrier_clearance()
```

## Semantic Duplicate Audit

| Семантика | Статус | Existing owner |
| --- | --- | --- |
| Approved plan lock creation | `EXISTS_COMPLETE` | `admin_core/operator_execution.py::approved_plan_lock_from_selected` |
| Packet materialization from preview/plan | `EXISTS_COMPLETE` | `admin_core/operator_execution.py::packet_from_preview`, `packet_from_plan` |
| Restore barrier clearance build | `EXISTS_COMPLETE` | `admin_core/operator_execution.py::build_restore_barrier_clearance` |
| Restore barrier clearance write | `EXISTS_COMPLETE` | `admin_core/operator_execution.py::append_restore_barrier_clearance` |
| Runtime action dispatcher for clearance | `EXISTS_COMPLETE` | `admin_core/operator_execution.py::execute_packet(mode="runtime_action")` |
| Existing governed transaction caller | `EXISTS_COMPLETE` | `tools/v7-governed-canary-dry-run-cycle` |
| L3 execution consumer | `EXISTS_COMPLETE` | `tools/v7-users-autoswitch` |
| L3 Production Validation materialization caller | `MISSING` | Existing L3 Production Validation execution step has no call into operator execution materialization |

Need New Owner: `FALSE`.
Need New Runtime: `FALSE`.
Need New Architecture: `FALSE`.

## Complete Existing Call Graph

Existing governed transaction path that DOES reach `build_restore_barrier_clearance()`:

```text
tools/v7-governed-canary-dry-run-cycle
  -> execute_governed_transaction_with_guards()
  -> operator_execution_pipeline.governed_canary_knowledge_gated_dry_run_cycle()
  -> operator_execution.packet_from_preview()
  -> operator_execution.approved_plan_lock_from_selected()
  -> operator_execution.create_execution_lease_from_packet()
  -> operator_execution.execute_packet(mode="runtime_action")
  -> operator_execution.append_restore_barrier_clearance()
  -> operator_execution.build_restore_barrier_clearance()
  -> autoswitch-restore-barrier.json
  -> run_autoswitch_apply()
```

Existing CLI path that DOES reach `build_restore_barrier_clearance()`:

```text
tools/v7-operator-execution-packet
  -> admin_core.operator_execution.main()
  -> --packet + --execute-runtime-action
  -> execute_packet(mode="runtime_action")
  -> append_restore_barrier_clearance()
  -> build_restore_barrier_clearance()
```

Existing read-only preview path that DOES reach `build_restore_barrier_clearance()` without writing:

```text
tools/v7-operator-execution-packet
  -> admin_core.operator_execution.main()
  -> --packet + --preview-runtime-action
  -> execute_packet(mode="runtime_action_preview")
  -> preview_restore_barrier_clearance()
  -> build_restore_barrier_clearance()
```

Actual L3 Production Validation path that DID NOT reach `build_restore_barrier_clearance()`:

```text
OMP/operator approval intent
  -> /usr/local/bin/v7-users-autoswitch
  -> --pre-planner-refresh=write
  -> --emergency-failover-autonomy
  -> --mode guarded
  -> --max-selected-moves 1
  -> planner selects L3 candidate
  -> reads existing autoswitch-restore-barrier.json
  -> validates stale approved_plan_lock
  -> STOP_SAFE
```

`tools/v7-users-autoswitch` contains no executable call to:

- `operator_execution.execute_packet`;
- `operator_execution.packet_from_plan`;
- `operator_execution.packet_from_preview`;
- `build_restore_barrier_clearance`.

It only records `approval_packet_owner` and `restore_barrier_owner` as ownership metadata.

## Direct Callers

| Function | Direct callers |
| --- | --- |
| `build_restore_barrier_clearance()` | `preview_restore_barrier_clearance()`, `append_restore_barrier_clearance()` |
| `preview_restore_barrier_clearance()` | `execute_packet(mode="runtime_action_preview")` |
| `append_restore_barrier_clearance()` | `execute_packet(mode="runtime_action")` |
| `execute_packet()` | `admin_core.operator_execution.main()`, `tools/v7-governed-canary-dry-run-cycle`, unit tests |

## Production Trace

Actual candidate:

| Field | Value |
| --- | --- |
| user | `10.0.0.2` |
| source | `openvpn-1779388847-d2ad7c` |
| target | `vless` |
| move type | `failover` |

Expected production trace:

```text
OMP approval
  -> L3 Production Validation producer
  -> packet / approved_plan_lock materialized
  -> execute_packet(mode="runtime_action")
  -> build_restore_barrier_clearance()
  -> append_restore_barrier_clearance()
  -> restore barrier file
  -> autoswitch consumes fresh envelope
  -> apply / verify / rollback / learning
```

Actual trace:

```text
OMP approval intent
  -> v7-users-autoswitch
  -> planner selected one L3 candidate
  -> autoswitch consumed stale restore barrier
  -> approved_plan_lock_expired
  -> approved_plan_lock_user_source_mismatch
  -> restore_barrier_clearance_generation_expired
  -> STOP_SAFE before apply
```

## Missing Call Classification

| Question | Answer |
| --- | --- |
| Was `build_restore_barrier_clearance()` reached? | `NO` |
| Was the call blocked by authority? | `NO`; authority intent existed, but no materialization caller executed |
| Was the call blocked by policy? | `NO` |
| Was the call blocked by stale state? | `NO`; stale state blocked later in autoswitch consumer |
| Was the call never implemented for L3 PV path? | `YES` |
| Was the wrong caller used? | `YES`; L3 PV invoked consumer/executor directly instead of first invoking existing operator-execution materialization path |

## Broken Producer Consumer Link

Broken link:

```text
L3 Production Validation selected candidate
  -> admin_core/operator_execution.py runtime-action materialization
```

Producer that should have invoked it:

```text
L3 Production Validation execution step
```

Consumer:

```text
tools/v7-users-autoswitch
```

Callee:

```text
admin_core/operator_execution.py::execute_packet(mode="runtime_action")
```

Terminal callee:

```text
admin_core/operator_execution.py::build_restore_barrier_clearance()
```

Trigger:

```text
OMP/operator approval for exactly one L3 one-user Production Validation candidate.
```

Evidence:

```text
selected candidate exists, max users = 1, emergency failover mode, no apply before fresh envelope.
```

## Root Cause

Executable root cause:

```text
The L3 Production Validation step has no executable producer call that converts the selected L3 candidate into a fresh operator-execution packet and then invokes execute_packet(mode="runtime_action").
```

This is not:

- stale lock as root cause;
- missing `build_restore_barrier_clearance()`;
- missing restore-barrier owner;
- missing runtime consumer;
- architecture gap.

The stale lock is the downstream symptom. The missing producer call is the root cause.

## Minimal Executable Fix

Responsible owner:

```text
L3 Production Validation execution step, reusing admin_core/operator_execution.py
```

Minimal executable fix:

```text
Before invoking the L3 autoswitch apply path, the existing L3 Production Validation step must call the existing operator-execution materialization path:

selected L3 candidate
  -> packet_from_plan or packet_from_preview
  -> execute_packet(mode="runtime_action")
  -> fresh approved_plan_lock + restore-barrier clearance
  -> v7-users-autoswitch consumes fresh envelope
```

No redesign.
No architecture.
No speculative improvements.

