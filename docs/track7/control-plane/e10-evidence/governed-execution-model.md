# E10 Governed Second Canary Execution Model

This is a future runbook model only. It was not executed in E10.

## Stage A - Hold Planner And Apply

Future command sequence, only after separate approval:

```bash
systemctl stop v7-autoswitch-planner.timer
systemctl stop v7-autoswitch-planner.service
systemctl stop v7-users-autoswitch.timer
systemctl stop v7-users-autoswitch.service
```

Required evidence:

- `v7-health.service` remains active;
- planner timer/service inactive;
- apply timer/service inactive;
- no `v7-users-autoswitch`, `v7-user-switch`, or `v7-routing-sync` process;
- users and egress registry hashes captured;
- runtime checks OK.

Abort if hold is not clean.

## Stage B - Execute One Canary Movement

Future command shape:

```bash
v7-user-switch <candidate_user> <approved_target>
```

E10 has no approved target, so this command is not instantiated for execution.

Movement budget:

```text
manual_canary_movements_allowed=1
candidate_user_only=true
any_other_user_movement=abort
```

## Stage C - Quiet Observation

Collect:

- users registry hash;
- switch-history tail;
- candidate route table;
- `ip route get`;
- `v7-reconcile-check`;
- `v7-user-route-check`;
- `v7-killswitch-check`;
- `v7-provisioning-reconcile-check`;
- process guard for autoswitch/user-switch/routing-sync.

Abort on any checker failure, route drift, or hidden mutation process.

## Stage D - Rollback Or Temporary Keep

Default safest path remains rollback after mechanics proof unless a separate approval explicitly permits a temporary keep.

Rollback command shape:

```bash
v7-user-switch <candidate_user> <rollback_target>
```

## Stage E - Restore Planner Only

Future command:

```bash
systemctl start v7-autoswitch-planner.timer
```

Apply timer must remain held.

Required evidence:

- planner timer active;
- apply timer inactive;
- selected moves observed but not applied;
- users registry unchanged after planner-only restore.

## Stage F - Restore-Settle Gate

Run the restore settle gate before apply restore:

```bash
tools/v7-restore-settle-gate --pre-restore --pretty
tools/v7-restore-settle-gate --pre-restore --json
```

GO requires:

```text
sample_count>=3
apply_timer_intervals_covered>=2
selected_moves_by_sample all zero
telegram_hard_blocked_by_sample all false
egress_1_eligible_by_sample all true when relevant
users.registry stable
egress.registry stable
checkers_ok=true
hidden_movers_observed=false
```

## Stage G - Restore Apply Only If Gate GO

Apply restore requires separate explicit approval after Stage F.

Future command:

```bash
systemctl start v7-users-autoswitch.timer
```

Never run `v7-users-autoswitch --apply` manually for canary restore.

## Stage H - Post-Restore Settle

Observe at least two full apply timer intervals.

Classify any movement as autoswitch recovery, not canary movement.

Next canary remains NO-GO if:

- broad failover appears;
- any movement reason is unclear;
- registry drift is unexpected;
- Telegram hard-block recurs;
- runtime checks fail.

## E10 Result

```text
restore_settle_gate_status=GO
candidate_user=10.7.0.11
selected_target=NONE
second_canary_approval_status=NO-GO
execution_allowed_now=false
```
