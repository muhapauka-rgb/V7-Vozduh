# Approved Plan Lock Selected Move Loss Forensic

Timestamp: 2026-07-02 21:01:24 Asia/Bangkok

Mode: forensic + tests, no patch, no deploy, no production mutation.

## Mission

Investigate the hypothesis that the governed L3 execution loses the committed selected move between:

Planner -> packet_from_plan -> execute_packet -> approved_plan_lock -> restore_barrier -> v7-users-autoswitch --apply -> Runtime apply validation.

Production target:

- user: 10.7.0.2
- incident_source/source: openvpn-1779388847-d2ad7c
- target: vless
- incident_key: dd5b6289529f22197e6694a7
- observed terminal reason: approved_plan_lock_selected_moves_missing

## Verdict

The hypothesis is not confirmed for the latest governed production cycle.

The selected move is not lost in packet serialization, approved plan lock persistence, restore barrier persistence, or committed apply identity handoff.

The first proven transition from one selected move to zero selected moves occurs inside:

- file: tools/v7-users-autoswitch
- function: AutoswitchPlanner._emergency_failover_authority_gate()
- lines: 1124-1300
- exact return: `return bounded if gate["ok"] else [], gate`

The gate returns zero selected moves because:

- `duplicate_apply_attempt`
- `l3_retry_budget_exhausted`

The root blocker for the repeated production cycle is retry-budget/duplicate-attempt state, not selected_move serialization loss.

## Tests Run

Local regression tests:

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests.unit.test_governed_canary_cli
Ran 17 tests in 0.240s
OK

PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests.unit.test_v7_users_autoswitch_policy
Ran 119 tests in 10.108s
OK
```

Relevant existing regression coverage:

- `tests/unit/test_governed_canary_cli.py` proves governed owner writes selected move into restore barrier approved_plan_lock and passes packet identity into apply.
- `tests/unit/test_v7_users_autoswitch_policy.py::test_apply_uses_approved_plan_lock_when_recomputed_planner_would_select_zero` proves apply can consume approved_plan_lock when live planner recomputation would otherwise select zero.
- `tests/unit/test_v7_users_autoswitch_policy.py::test_committed_apply_identity_must_match_approved_plan_lock` proves committed packet/operation/selected_move_hash identity validation.
- mismatch regression proves invalid committed identity returns `approved_plan_lock_selected_moves_missing`.

## Code Contract Trace

### Planner selected move extraction

Source:

- `admin_core/operator_execution.py:selected_moves_from_plan()`
- lines 309-360

Behavior:

- extracts selected moves from `plan.selected_moves`, fallback `approved_candidate_moves_before_guard`, fallback decisions;
- preserves user/source/target/move_type and semantic fields;
- produces canonical selected move identity.

### Packet materialization

Source:

- `admin_core/operator_execution.py:packet_from_plan()`
- lines 2048-2121

Behavior:

- calls `selected_moves_from_plan(plan)`;
- refuses empty selected moves with `planner_snapshot_has_no_candidate_moves`;
- writes selected identity into packet expected fields;
- writes rollback manifest item with original source and target;
- writes `packet["approved_plan_lock"] = approved_plan_lock_from_selected(...)`.

### Approved plan lock creation

Source:

- `admin_core/operator_execution.py:approved_plan_lock_from_selected()`
- lines 424-473

Behavior:

- writes `selected_move_count`;
- writes `selected_move_hash`;
- writes `selected_moves[]` with `user_ip`, `current_egress`, `recommended_egress`, `move_type`;
- forbids executor reselection/replacement.

### Restore barrier persistence

Source:

- `admin_core/operator_execution.py`
- lines 1519-1555

Behavior:

- copies packet approved_plan_lock into restore barrier;
- writes approved lock id/hash;
- writes clearance budget and approved selected hash.

### Runtime lock consumption

Source:

- `tools/v7-users-autoswitch:_approved_plan_lock_validation()`
- lines 6013-6147

Behavior:

- reads `restore_barrier.approved_plan_lock.selected_moves`;
- requires non-empty user/source/target;
- validates count, hash, allowed users/targets, committed apply identity, incident_source, source assignment, target readiness;
- returns selected moves only when valid.

### Apply failure wording

Source:

- `tools/v7-users-autoswitch:apply()`
- lines 8026-8047

Behavior:

- if final `plan.selected_moves` is empty and an approved lock is present, apply reports `approved_plan_lock_selected_moves_missing`;
- this reason can therefore mean "selected moves are absent after downstream gates", not only "lock selected_moves are absent."

## Production Evidence

### Restore barrier backups prove selected move was persisted

Read-only production artifacts:

- `/opt/v7/egress/state/autoswitch-restore-barrier.json`
- `/opt/v7/egress/state/autoswitch-restore-barrier.json.backup-c1-20260702T123220Z`
- `/opt/v7/egress/state/autoswitch-restore-barrier.json.backup-c1-20260702T123245Z`
- `/opt/v7/egress/state/autoswitch-restore-barrier.json.backup-c1-20260702T123304Z`
- `/opt/v7/egress/state/autoswitch-restore-barrier.json.backup-c1-20260702T123429Z`

Common persisted lock facts:

```text
lock_present=true
lock_schema=v7.approved-plan-lock.v1
lock_operation_id=govexec_99a887e81cfa5a711d426f31
lock_selected_moves_len=1
lock_selected_move_count_field=1
lock_selected_move_hash=6bcd509336032e43e4a612d51229c536e46cf4b97f08c8733ebaac974d67db3b
lock_first_move.user_ip=10.7.0.2
lock_first_move.current_egress=openvpn-1779388847-d2ad7c
lock_first_move.recommended_egress=vless
lock_first_move.move_type=failover
allowed_users=["10.7.0.2"]
allowed_targets=["vless"]
clearance_expected_selected_moves=1
clearance_max_selected_moves=1
```

Conclusion:

The approved selected move was persisted into restore barrier. The lock was not empty.

### Governed apply command used committed identity

Production journal fragment for the latest governed cycle:

```text
/usr/local/bin/v7-users-autoswitch
  --apply
  --verify
  --user 10.7.0.2
  --source-egress openvpn-1779388847-d2ad7c
  --target-egress vless
  --approved-packet-id pkt_33abb0e694803e9b46dc442e
  --approved-operation-id govexec_99a887e81cfa5a711d426f31
  --approved-selected-move-hash 6bcd509336032e43e4a612d51229c536e46cf4b97f08c8733ebaac974d67db3b
  --approved-authority-generation 01a0068ee0706821dfd3d958b706a2661e7725fbf1274cb4d96dc72f515ec968
```

Conclusion:

The governed owner did not pass the wrong committed selected move identity to apply.

### Runtime approved lock validation passed

Production journal fragment:

```text
approved_plan_lock_validation:
  present: true
  ok: true
  reason: approved_plan_lock_valid
  selected_move_count: 1
  selected_move_hash: 6bcd509336032e43e4a612d51229c536e46cf4b97f08c8733ebaac974d67db3b
  selected_users: ["10.7.0.2"]
  selected_sources: ["openvpn-1779388847-d2ad7c"]
  selected_targets: ["vless"]

committed_apply_identity:
  ok: true
  reason: committed_apply_identity_valid
  requested_identity.selected_move_hash: 6bcd509336032e43e4a612d51229c536e46cf4b97f08c8733ebaac974d67db3b
  actual_identity.selected_move_hash:
    - 6bcd509336032e43e4a612d51229c536e46cf4b97f08c8733ebaac974d67db3b
    - 6bcd509336032e43e4a612d51229c536e46cf4b97f08c8733ebaac974d67db3b
    - 6bcd509336032e43e4a612d51229c536e46cf4b97f08c8733ebaac974d67db3b
```

Conclusion:

Runtime did read and validate the same committed approved plan lock.

### First selected move loss transition

Production journal fragment:

```text
approved_production_validation_envelope.ok=true
approved_production_validation_envelope.failed_conditions=[]

move_evidence:
  ok=true
  user_ip=10.7.0.2
  current_egress=openvpn-1779388847-d2ad7c
  recommended_egress=vless
  current_channel_failure.confirmed=true
  current_channel_failure.diagnose_reason=interface_down_or_missing
  current_channel_failure.freshness.state=FRESH
  current_failures:
    - youtube FAIL FRESH
    - instagram FAIL FRESH
    - telegram TELEGRAM_DOWN_14S FRESH
    - google FAIL FRESH
    - google_auth FAIL FRESH

wake:
  decision=ACCEPT_WAKE
  accepted=true
  accepted_wake_sources=["confirmed_service_failure", "confirmed_current_channel_failure"]

emergency_failover_autonomy:
  enabled=true
  selected_moves_before_gate=1
  selected_moves_after_gate=0
  retry_budget_per_incident=1
  previous_attempts=1
  semantic_attempt_signature=3298f8a2317664de6868dd5de7f29f138db6c859bf4b750d2e1097314deacd7d
  blockers=["duplicate_apply_attempt", "l3_retry_budget_exhausted"]
  decision=block_emergency_failover
  ok=false
```

Code transition:

```text
tools/v7-users-autoswitch:_emergency_failover_authority_gate()
  line 1276: if duplicate_consumed_attempts:
  line 1277: blockers.append("duplicate_apply_attempt")
  line 1278: if len(duplicate_consumed_attempts) >= gate["retry_budget_per_incident"]:
  line 1279: blockers.append("l3_retry_budget_exhausted")
  line 1288: gate["ok"] = bool(bounded) and not gate["blockers"]
  line 1289: gate["selected_moves_after_gate"] = len(bounded) if gate["ok"] else 0
  line 1300: return bounded if gate["ok"] else [], gate
```

Conclusion:

The first proven selected move count transition is:

```text
selected_moves_before_gate=1
selected_moves_after_gate=0
producer=tools/v7-users-autoswitch._emergency_failover_authority_gate
reason=duplicate_apply_attempt,l3_retry_budget_exhausted
```

## Why the Outcome Still Says approved_plan_lock_selected_moves_missing

After `_emergency_failover_authority_gate()` returns `[]`, the final plan has no selected moves.

Then `apply()` reaches:

```text
if not plan.get("selected_moves"):
    if approved_lock.get("present"):
        return {
          "applied": False,
          "reason": "approved_plan_lock_selected_moves_missing",
          ...
        }
```

Therefore the terminal reason is misleading for this production cycle. It is a downstream surface reason after emergency gate suppression, not proof that approved_plan_lock.selected_moves was missing.

## L3 Runtime State Evidence

Production `l3-runtime-state.json` for incident `dd5b6289529f22197e6694a7`:

```text
incident_source=openvpn-1779388847-d2ad7c
failed_required_services=["google","google_auth","instagram","telegram","youtube"]
attempt_count=50
attempts_len=50
status=SUSPENDED
```

Tail attempts repeatedly carry:

```text
semantic_attempt_signature=3298f8a2317664de6868dd5de7f29f138db6c859bf4b750d2e1097314deacd7d
terminal_outcome=NOT_EXECUTED_PHASE1
terminal_state=DENIED or DRY_RUN
selected_move_hash=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
```

The gate's `previous_attempts=1` comes from `_l3_incident_attempt_count()`, which counts attempts where `_l3_attempt_consumed_retry_budget()` returns true.

Relevant code:

```text
tools/v7-users-autoswitch:_l3_attempt_consumed_retry_budget()
  applied=true OR terminal_state in APPLIED/ROLLED_BACK/... OR terminal_outcome in SUCCESS/ROLLBACK_SUCCESS/...
```

The earlier real execution at `2026-07-02T08:00:28.202794+00:00` reached:

```text
user=10.7.0.2
source=openvpn-1779388847-d2ad7c
target=vless
terminal_state=ROLLED_BACK
terminal_reason=verification_failed_rollback_completed
terminal_outcome_classification=ROLLBACK_SUCCESS
selected_move_hash=6bcd509336032e43e4a612d51229c536e46cf4b97f08c8733ebaac974d67db3b
```

That historical rollback consumes the single retry budget for this same user/source/target semantic attempt.

## Questions Answered

1. Did Planner produce one selected move?

Yes. Production transition was READY and restore barrier persisted one lock move for `10.7.0.2 openvpn -> vless`.

2. Was the same selected move written into packet?

Yes by code contract, and production apply command used packet `pkt_33abb0e694803e9b46dc442e` with selected hash `6bcd...`.

3. Was the same selected move written into approved_plan_lock?

Yes. Restore barrier backups show `approved_plan_lock.selected_moves_len=1` and the exact move.

4. Was the same selected move written into restore_barrier?

Yes. Current and backup restore barrier files show the same lock identity.

5. Did apply receive same operation_id / selected_move_hash?

Yes. Apply command used `govexec_99a887e81cfa5a711d426f31` and `6bcd...`.

6. Did apply read same approved_plan_lock?

Yes. Runtime validation says `approved_plan_lock_valid` and `committed_apply_identity_valid`.

7. Where exactly did selected_moves become missing?

Inside `tools/v7-users-autoswitch:_emergency_failover_authority_gate()`, when it returned `[]` because `gate.ok=false`.

8. Classification?

Not packet serialization loss.
Not approved lock write bug.
Not restore barrier write bug.
Not apply replan/recompute bug.
Not selected hash mismatch.
Not stale restore barrier.
Not cleanup overwrite.

Classification:

```text
RETRY_BUDGET_DUPLICATE_ATTEMPT_BLOCKER
```

## Final Finding

The current blocker is not that the selected move is lost before apply.

The current blocker is:

```text
duplicate_apply_attempt + l3_retry_budget_exhausted
```

The original failed verification/rollback for the same user/source/target consumed the only retry budget for this semantic attempt. Subsequent governed cycles continue selecting the same user and same semantic attempt, then emergency gate suppresses it before Runtime apply. The user-facing terminal reason remains `approved_plan_lock_selected_moves_missing`, but that reason is a misleading final apply surface after gate suppression.

## Safe Next Direction

Do not patch packet serialization or approved plan lock identity for this symptom.

The next implementation question should be narrowly scoped:

Should a failed-source incident continuation, after one user's verification rollback consumes retry budget, select the next remaining affected user on the same incident_source instead of repeatedly selecting the duplicate exhausted semantic attempt?

If yes, the minimal correction direction is likely candidate selection / retry-budget interaction for incident continuation:

- preserve incident_source;
- exclude semantic attempts already consumed for the current incident when retry budget is exhausted;
- select the next remaining user where `current_egress == incident_source`;
- keep max-users=1;
- do not bypass Authority, Restore Barrier, Runtime, Verification, or rollback.

No patch was made in this report.
