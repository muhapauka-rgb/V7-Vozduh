# BLOCK E9.3.3 — Staged Restore Planner-Only Rehearsal Report

## Scope

Mode: bounded live restore-governance rehearsal.

Allowed live mutation was limited to:

- stopping `v7-autoswitch-planner.timer`;
- stopping `v7-autoswitch-planner.service`;
- stopping `v7-users-autoswitch.timer`;
- stopping `v7-users-autoswitch.service`;
- restoring `v7-autoswitch-planner.timer` only.

No canary, user switch, routing sync, manual autoswitch apply, policy apply, Direct/RU mutation, Trusted RU refresh, proxy apply, kill switch mutation, route mutation, nft mutation, deploy, or registry edit was performed.

## Execution Summary

```text
rehearsal_executed=true
rehearsal_aborted=false
planner_restored=true
apply_restored=false
v7_health_active=true
apply_timer_held=true
apply_process_observed=false
user_movement_observed=false
routing_drift_observed=false
users.registry_changed=false
```

## Evidence Files

- `docs/track7/control-plane/e9_3_3-evidence/pre-rehearsal.txt`
- `docs/track7/control-plane/e9_3_3-evidence/pre-rehearsal-target-readiness.json`
- `docs/track7/control-plane/e9_3_3-evidence/pre-rehearsal-target-readiness.txt`
- `docs/track7/control-plane/e9_3_3-evidence/hold-confirmation.txt`
- `docs/track7/control-plane/e9_3_3-evidence/quiet-baseline.txt`
- `docs/track7/control-plane/e9_3_3-evidence/planner-restore-confirmation.txt`
- `docs/track7/control-plane/e9_3_3-evidence/planner-only-sample-A.txt`
- `docs/track7/control-plane/e9_3_3-evidence/planner-only-sample-B.txt`
- `docs/track7/control-plane/e9_3_3-evidence/planner-only-sample-C.txt`
- `docs/track7/control-plane/e9_3_3-evidence/final-authority-status.txt`
- `docs/track7/control-plane/e9_3_3-evidence/latest-planner-output.raw.txt`
- `docs/track7/control-plane/e9_3_3-evidence/latest-planner-journal.jsonl`
- `docs/track7/control-plane/e9_3_3-evidence/pending-move-analysis.md`

## Pre-Rehearsal State

Before hold:

- `v7-health.service` was active/enabled.
- `v7-autoswitch-planner.timer` was active/enabled.
- `v7-users-autoswitch.timer` was active/enabled.
- `v7-reconcile-check` was OK.
- `v7-user-route-check` was OK.
- `v7-killswitch-check` was OK.
- `v7-provisioning-reconcile-check` was OK.

Runtime baseline at the time of this block already had all enabled users on target `1`. This was caused by prior autoswitch activity before E9.3.3, not by this block.

## Hold Result

The approved hold stopped planner and apply authorities:

```text
v7-autoswitch-planner.timer=inactive
v7-autoswitch-planner.service=inactive
v7-users-autoswitch.timer=inactive
v7-users-autoswitch.service=inactive
v7-health.service=active
```

No real `v7-user-switch` or `v7-routing-sync` process was observed. Some process-guard lines include the SSH collection command itself because the grep pattern appeared in the command line; these are evidence collection artifacts, not runtime movers.

## Planner-Only Restore Result

Only `v7-autoswitch-planner.timer` was restored.

Final state:

```text
v7-health.service=active/running
v7-autoswitch-planner.timer=active/waiting
v7-autoswitch-planner.service=inactive/dead
v7-users-autoswitch.timer=inactive/dead
v7-users-autoswitch.service=inactive/dead
```

This achieved the staged restore target: planner active, apply held.

## Stability Results

Registry hashes stayed stable:

```text
users.registry=045ff68dcd22267b19c839531307a433776b71886ff4c8018a50783452b81222
egress.registry=67ac7afbac42b452f6d5be0ff1e3fc3cf3b3fae63ed72a7c18c6363a8e354d2f
```

Runtime checkers stayed OK in quiet baseline and planner-only samples:

```text
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

No route table drift was observed. No user movement was observed during the rehearsal. No autoswitch apply process was observed.

## Pending Move Analysis

Planner-only output was visible.

Samples A/B/C mostly reported:

```text
selected_moves=[]
apply_result.applied=false
```

The final authority status captured a later planner state with at least three pending failover recommendations:

```text
10.7.0.5: 1 -> awg3
10.0.0.2: 1 -> awg3
10.0.0.3: 1 -> awg3
```

Reason class: transient current-egress ineligibility under Telegram/down signal. These were not applied because `v7-users-autoswitch.timer` remained held.

```text
pending_moves_visible=true
pending_moves_count=3_observed
pending_moves_summary=10.7.0.5,10.0.0.2,10.0.0.3 -> awg3 failover recommendations
```

## Governance Verdict

```text
planner_only_stage_safe=true
apply_restore_status=HELD_REQUIRES_SEPARATE_APPROVAL
apply_restore_requires_separate_approval=true
future_canary_restore_sequence_safe=conditional_planner_only_stage_proven_apply_not_restored
second_canary_readiness=CONDITIONAL_STAGED_RESTORE_PROVEN_APPLY_APPROVAL_REQUIRED
execution_allowed_now=false
```

The planner-only stage is safe and useful. It exposes pending autoswitch movement before apply authority is restored.

The apply timer must remain held until a separate operator approval accepts:

- exact movement count;
- exact movement reasons;
- max allowed autoswitch recovery movement;
- post-apply settle checks;
- containment plan for unexpected movement.

## Exact Next Recommended Step

Prepare a separate `apply restore approval` block. It should approve or deny restoring `v7-users-autoswitch.timer` based on the pending movement list visible during planner-only observation. Until then, do not run another canary and do not restore apply authority.

## Final Mutation Statement

```text
Runtime mutation performed: YES — limited to temporary planner/apply hold and planner-only restore rehearsal
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Autoswitch apply timer restored: NO
Canary performed: NO
```
