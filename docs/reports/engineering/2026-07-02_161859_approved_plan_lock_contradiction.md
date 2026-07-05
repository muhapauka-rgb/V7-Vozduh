# Approved Plan Lock Contradiction Forensic

Created: 2026-07-02 16:18:59 Asia/Bangkok
Mode: READ_ONLY_FORENSIC
Production impact: NONE
Deploy performed: NO
Users moved: 0

## Mission

Determine whether the observed production state is canonical behavior or an implementation defect:

```text
approved_plan_lock_valid = true
approved_plan_lock_consumed = true
selected_moves_before_restore_barrier = 1
selected_moves_after_gate = 0
terminal_reason = approved_plan_lock_selected_moves_missing
```

No Planner, Runtime, Authority, Restore Barrier, or production state was modified.

## Target Execution

Persisted production artifacts used:

```text
/opt/v7/egress/state/operator-execution-lease.json
/opt/v7/egress/state/execution-events.jsonl
/opt/v7/egress/state/proposal-records.jsonl
/opt/v7/egress/state/closure-records.jsonl
/opt/v7/egress/state/runtime-trust.jsonl
```

The terminal outcome artifact that contains `approved_plan_lock_selected_moves_missing` is:

```text
operation_id = runtime_autoswitch_5cf1792f5557d5810ecfb9b6
created_at = 2026-07-02T09:02:56.574376+00:00
user = 10.7.0.5
terminal_state = DENIED
terminal_reason = approved_plan_lock_selected_moves_missing
terminal_outcome_classification = NO_EXECUTION
selected_move_hash = 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
l3_incident_key = 46ffebc776d1eb9fd256bf2a
```

The governed validation lineage recorded in the previous validation report was:

```text
operation_id = govexec_914712d4498b61e4e628e431
user = 10.7.0.5
source = awg0
target = vless
approved selected_move_hash = f9d49842548212334433eb9957674d9e3d08f2a13241e4e0f8413c87f1ddb8ff
```

The runtime source preview inside the lease contains:

```text
operation_id = runtime_autoswitch_f16337da689d38f97276fd24
operation_owner = tools/v7-users-autoswitch
planner_generation_id = 01a0068ee0706821dfd3d958b706a2661e7725fbf1274cb4d96dc72f515ec968
selected_move_count = 0
selected_move_hash = 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
terminal_state = DRY_RUN
terminal_reason = dry_run_restore_barrier_clearance_budget_and_generation_ok
```

## Frozen Object Identity

```text
terminal operation_id = runtime_autoswitch_5cf1792f5557d5810ecfb9b6
source_preview operation_id = runtime_autoswitch_f16337da689d38f97276fd24
planner_generation_id = 01a0068ee0706821dfd3d958b706a2661e7725fbf1274cb4d96dc72f515ec968
approved_plan_lock.lock_id = apl_a29cb724062923001faf910e
approved_plan_lock.lock_hash = 0fadb9bfa83fac60031a7a03403eb3a062cb14b5bf8f0d0995f823d80a694a44
approved_plan_lock.packet_id = pkt_134c7ab31ce4a90b3ae3c809
approved_plan_lock.selected_move_hash = f9d49842548212334433eb9957674d9e3d08f2a13241e4e0f8413c87f1ddb8ff
approved_plan_lock.selected_move_count = 1
approved user = 10.7.0.5
approved source = awg0
approved target = vless
move_type = failover
move reasons = current_egress_not_eligible, projected_load_target_adjusted
```

The post-gate operation hash is the empty selected-move hash:

```text
source_preview.operation.selected_move_count = 0
source_preview.operation.selected_move_hash = 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
```

## Transition Trace

### 1. Approved Plan Lock Validation

Producer:

```text
tools/v7-users-autoswitch::_approved_plan_lock_validation()
```

Source lines:

```text
tools/v7-users-autoswitch:5794-5922
```

Persisted output:

```text
present = true
ok = true
reason = approved_plan_lock_valid
selected_move_count = 1
selected_move_hash = f9d49842548212334433eb9957674d9e3d08f2a13241e4e0f8413c87f1ddb8ff
selected_users = ["10.7.0.5"]
selected_sources = ["awg0"]
selected_targets = ["vless"]
committed_apply_identity.ok = true
```

Result:

```text
selected move exists
count = 1
```

### 2. Locked Move Merge Into Plan

Producer:

```text
tools/v7-users-autoswitch::plan()
```

Source lines:

```text
tools/v7-users-autoswitch:5318-5339
```

Behavior:

```text
if approved_plan_lock.ok:
    selected = _merge_locked_moves_with_live_decisions(...)
    selected_moves_source = approved_plan_lock
    selected_before_restore_barrier = list(selected)
    authority_budget_gate.selected_moves_after_gate = len(selected)
```

Persisted output:

```text
authority_budget_gate.approved_plan_lock_used = true
authority_budget_gate.approved_plan_lock_scope = readiness_recheck
authority_budget_gate.selected_moves_after_gate = 1
```

Result:

```text
selected move still exists
count = 1
```

### 3. Restore Barrier Clearance Guard

Producer:

```text
tools/v7-users-autoswitch::plan()
```

Source lines:

```text
tools/v7-users-autoswitch:5351-5376
```

Persisted output:

```text
clearance_selected_moves_before_guard = 1
clearance_selected_moves_hash = f9d49842548212334433eb9957674d9e3d08f2a13241e4e0f8413c87f1ddb8ff
clearance_budget_exceeded = false
clearance_guard_reason = restore_barrier_clearance_budget_and_generation_ok
```

Result:

```text
restore barrier did not remove the selected move
count = 1
```

### 4. Intelligence Snapshot Gate

Producer:

```text
tools/v7-users-autoswitch::_apply_source_bundle_lease_to_intelligence_gate()
```

Consumer:

```text
tools/v7-users-autoswitch::plan()
```

Source lines:

```text
tools/v7-users-autoswitch:5377-5396
tools/v7-users-autoswitch:3075-3260
```

Persisted output:

```text
active = true
stop_required = false
snapshot_gate_decision = snapshot_gate_pass
snapshot_gate_source = approved_plan_lock_snapshot_gate
approved_plan_lock_consumed = true
selected_moves_after_gate = 1
```

Result:

```text
approved_plan_lock_consumed = true
selected move still exists
count = 1
```

### 5. Emergency Failover Autonomy Gate

Producer:

```text
tools/v7-users-autoswitch::_emergency_failover_authority_gate()
```

Source lines:

```text
tools/v7-users-autoswitch:955-1109
tools/v7-users-autoswitch:1208-1286
tools/v7-users-autoswitch:1364-1475
```

Input:

```text
selected_moves_before_gate = 1
approved_plan_lock.ok = true
restore_barrier.clearance_guard_reason = restore_barrier_clearance_budget_and_generation_ok
```

Move evidence producer:

```text
tools/v7-users-autoswitch::_emergency_failover_move_evidence()
```

Move evidence:

```text
user_ip = 10.7.0.5
current_egress = awg0
recommended_egress = vless
ok = false
blockers = ["required_service_failure_required"]
current_failures = []
current_channel_failure.confirmed = false
current_channel_failure.severity = OK
current_channel_failure.diagnose_reason = OK
current_channel_failure.affected_users_on_channel = 3
current_channel_failure.freshness.state = FRESH
```

Wake decision producer:

```text
tools/v7-users-autoswitch::_l3_wake_decision()
```

Wake output:

```text
decision = REJECT_WAKE
accepted = false
accepted_wake_sources = []
observed_events = []
blockers = ["confirmed_l3_wake_required"]
allowed_wake_sources = [
  "confirmed_current_channel_failure",
  "confirmed_service_failure",
  "recorded_runtime_resume",
  "verified_incident_resume"
]
rejected_wake_sources = [
  "blind_polling",
  "cron",
  "optimization_wake",
  "synthetic_wake",
  "timer"
]
```

Emergency gate output:

```text
enabled = true
mode = EMERGENCY_FAILOVER_AUTONOMY
ok = false
decision = block_emergency_failover
blockers = [
  "confirmed_l3_wake_required",
  "required_service_failure_required",
  "restore_barrier_required_for_emergency_failover"
]
selected_moves_before_gate = 1
selected_moves_after_gate = 0
```

Exact transition:

```text
tools/v7-users-autoswitch::_emergency_failover_authority_gate()
line 1109:
return bounded if gate["ok"] else [], gate
```

Result:

```text
FIRST selected move count change:
1 -> 0
```

### 6. Restore Barrier Execution Gate

Producer:

```text
tools/v7-users-autoswitch::plan()
```

Source lines:

```text
tools/v7-users-autoswitch:5414-5462
```

Persisted output:

```text
active = false
decision = pass
execution_blocked = false
execution_blocker = ""
selected_moves_before_gate = 0
selected_moves_after_gate = 0
```

Result:

```text
restore barrier execution gate did not remove the selected move.
It received an already-empty selected move list.
```

### 7. Runtime Apply Preflight

Producer:

```text
tools/v7-users-autoswitch::apply()
```

Source lines:

```text
tools/v7-users-autoswitch:7790-7823
```

Behavior:

```text
if not plan.get("selected_moves"):
    if approved_lock.get("present"):
        return {
            "applied": False,
            "reason": "approved_plan_lock_selected_moves_missing",
            "unsafe_blocker": reason,
            ...
        }
```

Persisted terminal outcome:

```text
terminal_state = DENIED
terminal_reason = approved_plan_lock_selected_moves_missing
apply_executed = false
users_moved = 0
verification_result.service_verify_rc = null
```

Result:

```text
Runtime Apply did not remove the selected move.
It reported the empty selected move list using an apply-layer approved-plan-lock fallback reason.
```

## Contradiction Test

Statements:

```text
A. approved_plan_lock_valid = true
B. approved_plan_lock_consumed = true
C. selected_moves_after_gate = 0
```

Can A+B+C legally be true simultaneously?

```text
YES
```

Proof:

1. `approved_plan_lock_valid = true` only proves the approved lock contains a valid selected move identity and matches requested scope.
2. `approved_plan_lock_consumed = true` is produced by the intelligence snapshot gate and proves the approved lock was consumed to pass the snapshot/materiality check.
3. The L3 canonical contract requires every mandatory gate to pass before execution. `docs/reference/capabilities/L3_EMERGENCY_AUTONOMOUS_FAILOVER.md` states:
   - L3 may start only when all mandatory entry conditions are true.
   - If any entry condition is false or unknown, L3 must `STOP_SAFE`.
   - Any failed mandatory gate produces `STOP_SAFE`.
   - Timer/cron/broad autoswitch loop are rejected triggers.
4. The selected move was removed after A and B by the later emergency failover autonomy gate because L3 wake/evidence was not accepted.
5. Therefore A and B do not imply C must be nonzero.

## Who Removed The Selected Move?

First producer:

```text
tools/v7-users-autoswitch::_emergency_failover_authority_gate()
```

Exact line:

```text
tools/v7-users-autoswitch:1109
```

Reason:

```text
gate["ok"] = false
return [] instead of selected moves
```

Why `gate["ok"]` was false:

```text
_emergency_failover_move_evidence() produced:
  required_service_failure_required

_l3_wake_decision() produced:
  confirmed_l3_wake_required
  REJECT_WAKE

approved_l3_production_validation_envelope produced:
  failed_conditions = ["l3_production_validation_mode"]

restore_barrier_required_for_emergency_failover was also added.
```

## Answers

1. Who produced `selected_moves_before_restore_barrier = 1`?

```text
tools/v7-users-autoswitch::plan()
after _approved_plan_lock_validation() and _merge_locked_moves_with_live_decisions()
```

2. Who produced `selected_moves_after_gate = 0`?

```text
tools/v7-users-autoswitch::_emergency_failover_authority_gate()
```

3. Which function changed the value?

```text
tools/v7-users-autoswitch::_emergency_failover_authority_gate()
```

4. Did approved_plan_lock_valid remain true?

```text
YES
```

5. Did approved_plan_lock_consumed remain true?

```text
YES
```

6. Why is selected move missing?

```text
Because a later mandatory L3 emergency gate failed closed and returned an empty selected-move list.
The approved lock was not invalidated.
```

7. Was selected move intentionally removed?

```text
YES, by fail-closed gate behavior.
```

8. Was selected move filtered?

```text
YES, by emergency_failover_autonomy gate.
```

9. Was selected move replaced?

```text
NO.
```

10. Was selected move invalidated?

```text
NO. The approved lock remained valid.
```

11. Was selected move consumed?

```text
The approved lock was consumed by the snapshot gate.
The move was then suppressed by the emergency failover autonomy gate.
```

12. Was selected move expired?

```text
NO.
```

13. Was selected move removed because of restore barrier, authority, budget, identity mismatch, packet mismatch, generation mismatch, or other?

```text
authority / wake-evidence gate
```

Exact blockers:

```text
confirmed_l3_wake_required
required_service_failure_required
restore_barrier_required_for_emergency_failover
```

14. First transition where selected move count changed:

```text
tools/v7-users-autoswitch::_emergency_failover_authority_gate()
selected_moves_before_gate = 1
selected_moves_after_gate = 0
```

## Object Lifetime

```text
Creation / selected move identity:
  approved_plan_lock.selected_moves[0]
  selected_move_hash = f9d49842548212334433eb9957674d9e3d08f2a13241e4e0f8413c87f1ddb8ff

Validation:
  _approved_plan_lock_validation()
  ok = true

Consumption:
  intelligence snapshot gate
  approved_plan_lock_consumed = true
  selected_moves_after_gate = 1

Filtering:
  _emergency_failover_authority_gate()
  selected_moves_before_gate = 1
  selected_moves_after_gate = 0

Removal:
  _emergency_failover_authority_gate()
  return [] because gate.ok = false

Runtime:
  apply() receives plan.selected_moves = []

Termination:
  terminal_reason = approved_plan_lock_selected_moves_missing
  terminal_state = DENIED
```

The selected move ceased to exist as an executable selected move at the emergency failover autonomy gate, not at Approved Plan Lock validation and not at Restore Barrier execution.

## Classification

The contradiction itself is canonical behavior:

```text
approved_plan_lock_valid=true
approved_plan_lock_consumed=true
selected_moves_after_gate=0
```

This means:

```text
The lock was valid.
The lock was consumed by the snapshot/identity path.
A later mandatory L3 authority/wake/evidence gate failed closed before apply.
```

The terminal reason is a generic apply-layer fallback because `apply()` only sees:

```text
approved_lock.present = true
plan.selected_moves = []
```

It does not prove that Approved Plan Lock removed the move.

## Verdict

```text
CANONICAL_BEHAVIOR
```

## Safe Fix Direction

No Approved Plan Lock or Restore Barrier patch is required by this contradiction.

The next execution breakpoint is the emergency failover autonomy / wake-evidence gate:

```text
current_channel_failure.confirmed = false
current_channel_failure.severity = OK
current_channel_failure.diagnose_reason = OK
current_failures = []
l3_wake_decision = REJECT_WAKE
blockers = confirmed_l3_wake_required, required_service_failure_required
```

Any future correction should continue from that same execution breakpoint and should not change Approved Plan Lock identity or Restore Barrier clearance behavior based on this contradiction.
