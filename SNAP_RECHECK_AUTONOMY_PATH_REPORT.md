# SNAP.RECHECK Autonomy Path Snapshot Mismatch Forensics

## 1. Mismatch Forensics

Current BA.1/TG.1 recheck saw:

- `snapshot_source_mismatch_service_scores_channel_service_scores`
- `dry_run_intelligence_snapshot_stop_required`
- `source_mismatch_families=["channel-service-scores","service-scores"]`

Production evidence from the bare runtime planner:

- command path: `/usr/local/bin/v7-users-autoswitch --pretty`
- terminal reason: `dry_run_intelligence_snapshot_stop_required`
- selected moves: `0`
- snapshot gate: `stop_required=true`
- stop families: `channel-service-scores`, `service-scores`

This is a real fail-closed snapshot gate response. It is not a false positive.

Evidence also shows the source moved after the last snapshot write:

- `service-scores.json`: `2026-06-12 22:53:41 +0300`
- `channel-service-scores.json`: `2026-06-12 22:53:41 +0300`
- `service-matrix.json`: `2026-06-12 22:54:00 +0300`

So the snapshots were fresh by TTL but stale by source lineage.

## 2. Path Comparison

SNAP.1.CLOSE certified the admin planner path:

```text
GET /api/autoswitch-plan
-> v7-users-autoswitch --pre-planner-refresh write --pre-planner-refresh-command v7-intelligence-snapshot-refresh --pretty
```

BA.1/TG.1 recheck used the legacy direct runtime read path:

```text
/usr/local/bin/v7-users-autoswitch --pretty
```

First divergence:

```text
SNAP.1 certified path: pre-planner refresh -> source reload -> snapshot gate
BA.1 direct path: existing snapshot read -> snapshot gate
```

That means the old SNAP.1 fix did not regress. The reappearing symptom came from a different execution path.

## 3. Owner Audit

| Area | Owner | Status |
| --- | --- | --- |
| service matrix source | service matrix writers | reused |
| service-scores snapshot | `admin_core/intelligence_workers.py` | reused |
| channel-service-scores snapshot | `admin_core/intelligence_workers.py` | reused |
| snapshot refresh | `tools/v7-intelligence-snapshot-refresh` | reused |
| runtime planner | `tools/v7-users-autoswitch` | reused |
| admin read-only planner path | `admin/v7-admin-api` | already fixed by SNAP.1 |
| BA.1 forensic direct path | manual direct runtime command | not certified as autonomy gate |

No duplicate snapshot owner, planner owner, or truth source was found.

## 4. Refresh Order Audit

Legacy direct path order:

1. read current service matrix;
2. read existing intelligence snapshots;
3. compare embedded snapshot source hashes against current source hashes;
4. fail closed if source changed after snapshot write.

Canonical path order:

1. run `v7-intelligence-snapshot-refresh`;
2. verify `source_stable=true`;
3. reload planner source inputs;
4. load refreshed intelligence snapshots;
5. run snapshot gate.

Production dry-run refresh before the bounded fix showed:

- `dry_run=true`
- `source_stable=true`
- `source_consistency_errors=[]`
- `users_moved=false`
- `runtime_behavior_changed=false`
- `governance_behavior_changed=false`

## 5. Root Cause

Classification: `DIFFERENT_EXECUTION_PATH`.

Detailed root cause:

The same fail-closed snapshot mismatch appeared because BA.1 recertification used the legacy direct planner command without canonical pre-planner refresh. SNAP.1 closed the admin read-only planner path, not every bare manual invocation of `v7-users-autoswitch --pretty`.

This is not:

- `OLD_ROOT_CAUSE_RETURNED`
- planner bug
- governance bug
- execution bug
- snapshot hash algorithm bug
- duplicate truth source

It is a path selection problem for autonomy certification evidence.

## 6. Fix Applied

No code fix was applied.

Reason:

Changing default `v7-users-autoswitch --pretty` to write snapshots would silently turn a broad read-only command into a runtime write path. That would be a hidden behavior change and is not safe as a bounded SNAP.RECHECK fix.

Bounded operational fix applied through existing owner:

```text
v7-users-autoswitch --pre-planner-refresh write --pre-planner-refresh-command v7-intelligence-snapshot-refresh --pretty
```

Result:

- pre-planner refresh: `REFRESH_SUCCESS`
- source reload changed keys: `[]`
- snapshot gate: `stop_required=false`
- source mismatch families: `[]`
- users moved: `0`
- apply executed: `false`

Canonical BA.1 one-user dry-run was then executed with:

```text
v7-users-autoswitch --pre-planner-refresh write --pre-planner-refresh-command v7-intelligence-snapshot-refresh --max-selected-moves 1 --pretty
```

Result:

- snapshot blocker closed;
- `source_mismatch_families=[]`;
- new terminal reason: `dry_run_restore_barrier_clearance_generation_expired`.

## 7. BA.1 Recheck

Post-refresh truth/convergence:

- truth-check: `PASS`
- convergence: `FULLY_ALIGNED`
- runtime action status: `READY_FOR_RUNTIME_ACTION`

Canonical BA.1 dry-run:

- pre-planner refresh: `REFRESH_SUCCESS`
- snapshot stop: `false`
- source mismatch families: `[]`
- apply executed: `false`
- users moved: `0`

New BA.1 blocker:

```text
restore_barrier_clearance_generation_expired
```

Additional detail:

- approved plan lock present: `true`
- approved plan lock valid: `false`
- reasons:
  - `approved_plan_lock_expired`
  - `approved_plan_lock_user_source_mismatch`

So BA.1 is no longer blocked by service-score/channel-service-score mismatch on the canonical path. It is now blocked by stale restore-barrier / approved-plan-lock evidence.

## 8. Final Verdict

Final verdict: `DIFFERENT_PATH_FIXED`.

Answers:

- same mismatch returning: `false`
- old SNAP.1 root cause returned: `false`
- different path: `true`
- root cause proven: `true`
- safe fix applied: `true`
- snapshot blocker closed on canonical path: `true`
- BA.1 ready for execution: `false`

New single blocker:

```text
restore_barrier_clearance_generation_expired
```

Safety:

- users moved: `0`
- apply executed: `false`
- autonomy enabled: `false`
- routing changed: `false`
- deploy executed: `false`

Safe next step:

```text
BA1_FRESH_ONE_USER_PACKET_AND_RESTORE_BARRIER_RECHECK
```

