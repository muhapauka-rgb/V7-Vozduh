# AUTONOMY.CANARY.1B Snapshot Gate, Restore Barrier, And Readiness Closure

Date: 2026-06-23  
Workspace: `/Users/ponch/Documents/New project`  
Branch: `Updatesystem`  
Runtime fix commit: `18afa72c`  
Mode: implementation + certification, no runtime apply

## 1. Scope

AUTONOMY.CANARY.1B continued the canary chain from the 1A blocker:

```text
Snapshot Gate -> Candidate Visibility -> Restore Barrier -> Readiness
```

The phase was not allowed to move users, enable autoswitch/daemon mode, create synthetic candidates/events/trust, lower floors, change planner/governance/execution semantics, or create a new truth source.

## 2. Root Cause

The 1A certified root cause was durable snapshot lifecycle behavior:

- A planner-owned refresh with `--pre-planner-refresh=write` cleared the snapshot gate inside that observe run.
- A normal production observe then returned to `dry_run_intelligence_snapshot_stop_required`.
- Therefore candidate visibility was real but not durable for the normal observe path.

The existing owner was `tools/v7-users-autoswitch`; the existing refresh owner was `tools/v7-intelligence-snapshot-refresh`.

## 3. Implementation

Smallest existing-owner fix:

- `tools/v7-users-autoswitch` now auto-enables the existing pre-planner snapshot refresh only for read-only `--mode observe` when no explicit pre-refresh mode is supplied.
- Explicit `--pre-planner-refresh` still wins.
- `--apply` does not auto-enable refresh.
- Refresh metadata records requested mode, effective mode, auto-enable state, and reason.

Files changed:

- `tools/v7-users-autoswitch`
- `tests/unit/test_runtime_snapshot_fast_path.py`

## 4. Tests

| Check | Result |
| --- | --- |
| `PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch` | PASS |
| `PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests.unit.test_runtime_snapshot_fast_path tests.unit.test_v7_users_autoswitch_policy` | PASS, 87 tests |
| `./tools/v7-safe-deploy --json` after commit | PASS |
| `./tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED --update-local-snapshot --json` | PASS |
| `./tools/v7-convergence-status --json` after deploy | PASS / ALIGNED |

Evidence directory:

`docs/reports/AUTONOMY_CANARY_1B_EVIDENCE/`

## 5. Production Snapshot Gate Result

After deploy, production normal observe:

- Command: `ssh v7-vps '/usr/local/bin/v7-users-autoswitch --mode observe --pretty'`
- `candidate_moves_total=8`
- `selected_move_count=0`
- `terminal_reason=dry_run_restore_barrier_clearance_generation_expired`
- `snapshot_gate.stop_required=false`
- `snapshot_gate.stop_families=[]`
- `pre_planner_refresh.auto_enabled=true`
- `pre_planner_refresh.requested_mode=off`
- `pre_planner_refresh.mode=write`
- `pre_planner_refresh.state=REFRESH_SUCCESS`

Verdict: snapshot gate is closed for the normal observe path.

## 6. Candidate Visibility

After snapshot gate closure, current production canary preview exposes real fresh movement pressure:

- `candidate_moves_total=8`
- Canary limited run selected one move before restore guard:
  - `10.0.0.2`
  - `awg3 -> wireguard-1779454504-c43409`
  - `move_type=failover`

Fresh generated packet preview:

- `packet_id=pkt_ddf85e1c87a9fc142b587a8f`
- `selected_move_count=1`
- `allowed_users=[10.0.0.2]`
- `allowed_targets=[wireguard-1779454504-c43409]`
- `runtime_action=CREATE_RESTORE_BARRIER_CLEARANCE`
- validation: `PACKET_VALID`

No packet execution, no restore barrier write, and no user movement were performed.

## 7. Restore Barrier Result

Production still blocks canary at restore barrier:

- `clearance_generation_ok=false`
- `clearance_generation_reason=restore_barrier_clearance_generation_expired`
- `current_generation_id=d4098562a46e2cb32db70bab1943d638637198b896423da9b633f79d8e250080`
- `approved_generation_id=1fd508b2fc82598d134f3defb598dd6593f0decd3da8437d953e788c3d3c098b`
- `clearance_expires_at=2026-06-13T19:29:19.851623+00:00`
- `approved_plan_lock_validation.ok=false`
- reasons:
  - `approved_plan_lock_expired`
  - `approved_plan_lock_user_source_mismatch`

The old approved lock was for 10 old `vless` moves. The fresh canary candidate is `10.0.0.2 awg3 -> wireguard-1779454504-c43409`. Reusing the old lock would be unsafe and is correctly rejected.

## 8. Restore Settle Gate

Read-only restore settle checks were clean:

| Check | Result |
| --- | --- |
| `tools/v7-restore-settle-gate --pre-restore --json` | `GO`, read-only, zero movement |
| `tools/v7-restore-settle-gate --post-restore --json` | `GO`, read-only, zero movement |

This means the settle gate surface is not the active blocker. The active blocker is missing fresh restore-barrier clearance for the fresh approved plan lock.

## 9. Readiness

Current readiness after 1B:

| Gate | State |
| --- | --- |
| Snapshot gate | CLOSED |
| Candidate visibility | VISIBLE |
| Fresh packet preview | VALID |
| Restore settle gate | GO |
| Restore barrier clearance | BLOCKED |
| Production apply | DISABLED |
| User movement | 0 |
| Canary readiness | NOT READY |

Trust inventory after deploy still reports:

- `autonomy_canary_1_ready=false`
- prediction confidence `36.599`
- secondary operator earned confidence `45.838`

Restore is the first hard runtime blocker in the chain. Confidence/prediction floors remain below final canary readiness but were not bypassed or changed.

## 10. Risk Assessment

The implemented change is read-only observe lifecycle plumbing:

- It reuses existing snapshot refresh and lock owners.
- It does not create a new planner, governance path, execution path, truth source, daemon, or scheduler.
- It does not write restore barrier clearance.
- It does not move users.
- It leaves apply requiring explicit governed action.

The next action, if approved as a separate governed phase, is to use the existing packet owner to execute the fresh restore-barrier clearance runtime action for the fresh packet, then re-run canary readiness. That action is a restore-barrier-only mutation, not user movement, but it is still a runtime write and was intentionally not performed in this phase.

## 11. Final Verdict

`CANARY_BLOCKED_BY_RESTORE`

Snapshot gate and candidate visibility are closed. Canary cannot proceed because the current restore barrier clearance is expired and belongs to an obsolete plan.

## 12. Final Alignment

Final checks were run after commit and push, with outputs written to `/tmp` to avoid creating new repository dirtiness.

| Check | Status |
| --- | --- |
| Local | PASS |
| GitHub | PASS |
| Runtime | PASS |
| Truth | PASS / FULLY_ALIGNED |
| Convergence | PASS / ALIGNED |
