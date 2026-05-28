# BLOCK E9.4.2 — Fresh Bounded Apply Restore Retry Report

## Summary

E9.4.2 executed the approved bounded apply-restore retry after a fresh planner-only gate recovered from the previous Telegram hard-block.

The apply timer restore was clean. No user movement occurred. No routing drift was observed. No emergency containment was required.

## Evidence

- Pre-restore snapshot: `docs/track7/control-plane/e9_4_2-evidence/pre-restore.txt`
- Final planner-only gate: `docs/track7/control-plane/e9_4_2-evidence/final-planner-only-gate.txt`
- Immediate post-restore: `docs/track7/control-plane/e9_4_2-evidence/immediate-post-restore.txt`
- Observation samples:
  - `docs/track7/control-plane/e9_4_2-evidence/observation-A.txt`
  - `docs/track7/control-plane/e9_4_2-evidence/observation-B.txt`
  - `docs/track7/control-plane/e9_4_2-evidence/observation-C.txt`
- Verdict summary: `docs/track7/control-plane/e9_4_2-evidence/restore-verdict.md`

## Phase Results

```text
apply_restore_executed=true
apply_restore_aborted=false
final_planner_selected_moves=0
final_telegram_hard_blocked=false
egress_1_eligible=true
```

The final gate contained older journal entries with `telegram_required_telegram_down_14s`, but the latest gate decision showed no selected moves and egress `1` eligible.

Restore command executed:

```text
systemctl start v7-users-autoswitch.timer
```

Result:

```text
start_rc=0
v7-users-autoswitch.timer=active/enabled
manual_autoswitch_apply=false
manual_user_switch=false
manual_routing_sync=false
```

## Post-Restore Observation

Registry hashes remained stable:

```text
users.registry=045ff68dcd22267b19c839531307a433776b71886ff4c8018a50783452b81222
egress.registry=67ac7afbac42b452f6d5be0ff1e3fc3cf3b3fae63ed72a7c18c6363a8e354d2f
```

Observed timer-driven autoswitch runs:

```text
selected_moves=[]
apply_result.applied=false
apply_result.reason=no_selected_moves
```

Runtime checks:

```text
reconcile_ok=true
user_route_check_ok=true
kill_switch_ok=true
provisioning_ok=true
```

Movement/routing classification:

```text
actual_movements_count=0
actual_moved_users=[]
broad_failover_observed=false
routing_drift_observed=false
emergency_containment_performed=false
```

## Verdict

```text
restore_verdict=CLEAN_RESTORE
apply_restore_clean=true
autoswitch_recovery_bounded=true
current_canary_status=CONDITIONAL_APPLY_RESTORE_CLEAN_NEW_CANARY_APPROVAL_REQUIRED
execution_allowed_now=false
```

E9.4.2 proves the staged restore model can return apply authority cleanly when the final planner gate is clean.

It does not approve a new canary. Any next canary still requires a separate approval packet, fresh candidate/target evidence, and a bounded quiet-window execution plan.

## Exact Next Recommendation

Move to a read-only post-restore monitoring block before any new canary approval. That block should confirm there are no delayed autoswitch movements after the clean restore.

## Final Mutation Statement

```text
Runtime mutation performed: YES — limited to v7-users-autoswitch.timer restore only
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
```
