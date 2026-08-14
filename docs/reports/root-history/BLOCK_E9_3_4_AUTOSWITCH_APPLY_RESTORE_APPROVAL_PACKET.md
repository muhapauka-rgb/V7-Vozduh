# BLOCK E9.3.4 — Autoswitch Apply Restore Approval Packet

Mode: read-only / apply restore approval only.

## Executive Verdict

```text
apply_restore_current_status=HELD
planner_only_active=true
apply_timer_held=true
pending_moves_visible=false
pending_moves_count=0_current
pending_moves_stable=false
pending_moves_safe_to_apply=false_without_separate_operator_approval
awg3_eligibility_conflict=true
approval_status=CONDITIONAL
recommended_action=KEEP_APPLY_HELD_UNTIL_SEPARATE_BOUNDED_APPLY_RESTORE_APPROVAL
execution_allowed_now=false
```

E9.3.4 does not restore `v7-users-autoswitch.timer` and does not execute autoswitch apply. It prepares the approval packet only.

## Current Authority Truth

Evidence: `docs/track7/control-plane/e9_3_4-evidence/current-authority-snapshot.txt`.

```text
v7-health.service=active/enabled
v7-autoswitch-planner.timer=active/enabled
v7-autoswitch-planner.service=inactive/static
v7-users-autoswitch.timer=inactive/enabled
v7-users-autoswitch.service=inactive/static
```

Interpretation:

- health authority is running;
- planner authority is restored;
- apply authority remains held;
- no `v7-user-switch` or `v7-routing-sync` process was observed;
- no manual `v7-users-autoswitch --apply` was executed.

## Runtime Health Gates

Across the current snapshot and planner-only samples:

```text
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
users.registry stable=true
egress.registry stable=true
```

No registry drift, user movement, routing drift, or kill-switch degradation was observed.

## Current Target Readiness Note

Evidence: `docs/track7/control-plane/e9_3_4-evidence/current-target-readiness.json`.

A fresh local copy of runtime state was captured into `docs/track7/control-plane/e9_3_4-evidence/current-state/` for read-only parsing by `tools/v7-second-canary-target-readiness --state-dir ...`.

That fresh state shows the prior second-canary candidate is not currently at the old baseline:

```text
candidate_user=10.7.0.14
expected_current_egress=vless
actual_current_egress=1
candidate_still_valid=false
```

This does not change the E9.3.4 apply-restore decision directly, but it does mean any future canary packet must be regenerated from current registry truth. The mandatory no-argument checker run can still read its older fallback evidence snapshot on this workstation; the E9.3.4-specific evidence file above is the current-state reference for this packet.

## Pending Moves Refresh

E9.3.3 had visible pending moves:

```text
10.7.0.5: 1 -> awg3
10.0.0.2: 1 -> awg3
10.0.0.3: 1 -> awg3
```

E9.3.4 repeated planner-only observation and reconstructed recent planner journal JSON. The fresh planner runs reported:

```text
candidate_moves=0
candidate_moves_total=0
selected_moves=0
apply_requested=false
apply_result.applied=false
```

Therefore the E9.3.3 pending movement list is not stable in the current evidence window. It was likely tied to the transient Telegram/down signal and anti-flap state described in E9.3.3.

## Risk Classification

Detailed classification: `docs/track7/control-plane/e9_3_4-evidence/pending-move-risk-classification.md`.

Key risks:

- apply restore can still create non-canary movement once the timer is active again;
- current selected movement count is zero, but prior restore behavior proved the timer can fire immediately and move users;
- `awg3` remains a governance conflict because the strict canary watcher rejects it while autoswitch previously considered it during failover;
- restoring apply authority is a platform autoswitch recovery stage, not a canary cleanup step.

## Approval Decision

```text
approval_status=CONDITIONAL
```

Why not GO:

- this block has no live apply-restore approval;
- E9.3.3 proved that apply restore can have broader-than-canary blast radius;
- awg3 eligibility mismatch remains unresolved;
- fresh zero selected moves must be rechecked immediately before any live restore.

Why not hard NO-GO:

- current planner-only state is quiet with zero selected moves;
- all four runtime checkers are OK;
- registry/routing evidence is stable;
- apply restore may be considered in a separate bounded block if the operator accepts the staged restore semantics.

## Safer Alternatives

| Option | Decision | Notes |
|---|---|---|
| A. Keep apply timer held | preferred now | preserves current staged state and avoids unapproved user movement |
| B. Restore apply with max movement count 1 | design only | requires tool support or explicit guard; not executed |
| C. Change autoswitch eligibility rules | future design | especially for awg3/canary quality mismatch |
| D. Fix awg3 quality/eligibility mismatch | future diagnostics | do not mutate in this block |
| E. Drain/rollback specific users | separate approval | user movement; not part of E9.3.4 |
| F. Supervised maintenance apply restore | best future live model | final planner-only sample, explicit movement limit, post-apply settle |

## Exact Next Step

Recommended next step:

```text
E9.3.5 bounded autoswitch apply restore approval/execution, only if operator approves:
1. fresh planner-only sample immediately before restore;
2. expected selected_moves=0 or exact accepted movement list;
3. max_apply_movements explicitly named;
4. v7-users-autoswitch.timer restore only;
5. post-apply settle evidence;
6. immediate abort if user movement exceeds approved list.
```

Until then:

```text
v7-users-autoswitch.timer must remain held
execution_allowed_now=false
```

## Required Final Answers

```text
apply_restore_current_status=HELD
planner_only_active=true
apply_timer_held=true
pending_moves_visible=false
pending_moves_count=0_current
pending_moves_summary=none in fresh E9.3.4 planner-only samples; previous E9.3.3 had 3 transient failover recommendations to awg3
pending_moves_stable=false
pending_moves_safe_to_apply=false_without_separate_operator_approval
awg3_eligibility_conflict=true
approval_status=CONDITIONAL
recommended_action=KEEP_APPLY_HELD_UNTIL_SEPARATE_BOUNDED_APPLY_RESTORE_APPROVAL
execution_allowed_now=false
exact_next_step=E9.3.5 bounded apply restore approval/execution with fresh planner-only sample and explicit operator approval
```

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
