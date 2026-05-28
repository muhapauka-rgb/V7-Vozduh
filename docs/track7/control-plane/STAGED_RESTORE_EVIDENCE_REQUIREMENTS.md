# Staged Restore Evidence Requirements

Mode: governance design only. This document defines future evidence requirements and does not run any command.

## Stage A — Quiet Hold Evidence

Required evidence:

- timestamp;
- `v7-health.service` active;
- planner timer/service inactive;
- apply timer/service inactive;
- no `v7-users-autoswitch`;
- no `v7-user-switch`;
- no `v7-routing-sync`;
- `users.registry` hash;
- `egress.registry` hash;
- switch-history tail;
- route/rule snapshots;
- `v7-reconcile-check`;
- `v7-user-route-check`;
- `v7-killswitch-check`;
- `v7-provisioning-reconcile-check`.

## Stage B — Canary / Rollback Evidence

Required evidence:

- exact approved user;
- exact forward command;
- exact rollback command;
- pre/post candidate registry row;
- candidate route table before/after;
- route_get before/after;
- switch-history tail;
- process guard;
- four runtime checkers.

## Stage C — Planner-Only Restore Evidence

Required evidence:

- planner timer active/enabled;
- planner service last trigger;
- apply timer/service still inactive;
- no `v7-user-switch`;
- no `v7-routing-sync`;
- `users.registry` hash unchanged unless expected;
- switch-history unchanged;
- planner state files updated only as advisory/planner state.

## Stage D — Planner-Only Observation Evidence

Required evidence:

- at least two samples spaced by one planner period or more;
- selected/pending moves from planner output when available;
- movement reason classes;
- expected movement count;
- egress/user affected list;
- route/rule snapshots stable;
- four runtime checkers OK.

## Stage E — Apply Restore Approval Evidence

Required evidence before restoring apply:

- operator approval text;
- pending movement list or explicit `pending_moves=none`;
- maximum accepted movement count;
- accepted movement classes;
- rollback/containment plan for unexpected movement;
- explicit acknowledgement that apply restore is autoswitch recovery, not canary movement.

## Stage F — Post-Apply Settle Evidence

Required evidence after apply restore:

- apply timer active/enabled;
- apply service settled;
- movement count;
- movement list;
- movement classification;
- registry hash before/after;
- switch-history delta;
- route/rule delta;
- four runtime checkers OK;
- canary blast radius and restore blast radius reported separately.

## Evidence Verdict Fields

Future reports must include:

```text
canary_window_status=<quiet/failed/unknown>
restore_planner_status=<held/planner_only/restored/failed>
apply_restore_status=<held/approved/restored/failed>
post_restore_movement_classification=<none/autoswitch_recovery/unexpected/unknown>
execution_allowed_now=false
```

## E9.3.3 Evidence Addendum

E9.3.3 adds required evidence for any future planner-first rehearsal:

- final authority status after planner restore;
- explicit proof that `v7-users-autoswitch.timer` stayed inactive;
- explicit proof that `v7-users-autoswitch.service` stayed inactive;
- registry hashes before hold, during planner-only observation, and at final status;
- selected move summary from planner output;
- distinction between `planner_output_visible` and `pending_moves_visible`;
- observed pending movement count, or explicit `unknown` if journald truncation prevents exact count.

E9.3.3 observed:

```text
planner_output_visible=true
pending_moves_visible=true
pending_moves_count=3_observed
apply_timer_held=true
apply_process_observed=false
```
