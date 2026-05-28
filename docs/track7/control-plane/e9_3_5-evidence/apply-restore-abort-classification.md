# E9.3.5 Apply Restore Abort Classification

Mode: bounded live autoswitch recovery rehearsal.

No apply restore was executed. The final planner-only sample changed from the E9.3.4 zero-move state to a bounded-but-nonzero movement plan, so the apply timer restore was aborted before `systemctl start v7-users-autoswitch.timer`.

## Final Planner-Only Sample

```text
parsed_planner_messages=2
updated=2026-05-25T20:22:55.760184+00:00
apply_requested=False
candidate_moves=15
candidate_moves_total=15
selected_moves=3
different_or_non_keep_decisions=15
selected_moves_list_count=3
```

Selected moves:

| User | From | To | Move Type | Reason |
|---|---|---|---|---|
| 10.0.0.2 | 1 | vless | failover | current_egress_not_eligible |
| 10.0.0.3 | 1 | vless | failover | current_egress_not_eligible |
| 10.0.0.6 | 1 | vless | failover | current_egress_not_eligible |

Candidate decisions included 15 users on egress `1` with recommendation `1 -> vless`. The current egress `1` was rejected by planner logic because it was not eligible, with `service_instagram_failed` and Telegram degradation/warning evidence in the candidate scoring context.

## Abort Decision

```text
apply_restore_executed=false
apply_restore_aborted=true
apply_restore_emergency_containment=false
planner_only_prediction=selected_moves=3 candidate_moves_total=15 selected_target=vless reason=current_egress_not_eligible
actual_movements_count=0
actual_moved_users=none
predicted_vs_actual_match=n/a_not_executed
awg3_movements_observed=false
routing_drift_observed=false
hidden_routing_sync_observed=false
autoswitch_recovery_bounded=false_not_executed_due_final_planner_gate
restore_governance_proven=false_apply_restore_not_executed
```

## Verdict

The staged restore governance gate worked: apply restore remained held because final planner-only evidence showed nonzero pending movement. E9.3.5 therefore did not prove autoswitch recovery behavior; it proved that a final planner-only gate can prevent unapproved timer-driven movement.

## Mutation Statement

```text
Runtime mutation performed: NO
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Autoswitch apply timer restored: NO
Canary performed: NO
```
