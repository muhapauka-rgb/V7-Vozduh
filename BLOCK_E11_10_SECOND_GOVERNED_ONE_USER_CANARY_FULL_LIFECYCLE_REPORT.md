# BLOCK E11.10 Second Governed One-User Canary Full Lifecycle Report

## Summary

E11.10 started a governed one-user canary and E11.10-closeout completed the
missing lifecycle. The canary candidate `10.7.0.3` had been moved from `awg0`
to the reserved WireGuard target `wireguard-1779454504-c43409`.

Fresh closeout evidence showed the candidate was still on WireGuard, planner
and apply timers were held, runtime checkers were OK, and no hidden
`v7-user-switch` or `v7-routing-sync` process was observed. However, the
pre-rollback settle observation saw `selected_moves=1` in samples B/C, so a
keep decision was not safe.

The closeout executed the default rollback:

```text
v7-user-switch 10.7.0.3 awg0
```

Only `10.7.0.3` changed. Planner was restored first, the restore-settle gate
returned `GO`, apply timer was restored only after that gate, and delayed
monitoring across three samples stayed clean.

## Required Answers

```text
canary_executed=true
candidate_user=10.7.0.3
forward_from=awg0
forward_to=wireguard-1779454504-c43409
rollback_executed=true
rollback_target=awg0
keep_decision=false
only_one_user_moved=true
delayed_movements_observed=false
restore_settle_gate_status=GO
runtime_checks_ok=true
target_readiness_after=GO_WIREGUARD_ZERO_USER_RESERVED_HEALTHY
second_canary_lifecycle_status=CLOSED_ROLLED_BACK_AND_SETTLED
next_stage_readiness=GO_FOR_POST_E11_10_GOVERNANCE_REVIEW_NO_EXECUTION
recommended_next_block=E11.11_POST_CLOSEOUT_GOVERNANCE_REVIEW_OR_PRODUCTION_RUNTIME_GOVERNANCE_HARDENING
execution_allowed_now=false
```

## Evidence

- `docs/track7/control-plane/e11_10-evidence/forward-canary-verification.txt`
- `docs/track7/control-plane/e11_10-evidence/canary-observation-combined.txt`
- `docs/track7/control-plane/e11_10_closeout-evidence/fresh-live-state.txt`
- `docs/track7/control-plane/e11_10_closeout-evidence/rollback-verification.txt`
- `docs/track7/control-plane/e11_10_closeout-evidence/staged-restore-settle.txt`
- `docs/track7/control-plane/e11_10_closeout-evidence/final-monitoring.txt`

## Closeout Classification

```text
is_10_7_0_3_still_on_wireguard_before_closeout=true
other_users_moved_after_observation_C=false_during_closeout_window
autoswitch_reassigned_anything_during_closeout=false
wireguard_reserved=true
wireguard_healthy=true
routing_consistent=true
checkers_ok=true
```

The switch history contains broader autoswitch movement before E11.10 and
before the closeout window. During this closeout, the only user movement was
the approved rollback of `10.7.0.3`.

## Restore Lifecycle

Planner/apply state at closeout start:

```text
v7-autoswitch-planner.timer=inactive
v7-users-autoswitch.timer=inactive
```

After rollback:

```text
planner_restore=performed
planner_settle_samples=A,B,C
planner_settle_selected_moves=0,0,0
planner_settle_registry_hash_stable=true
planner_settle_runtime_checks_ok=true
restore_settle_gate_status=GO
apply_restore=performed_after_gate_GO
```

Final monitoring:

```text
final_samples=A,B,C
users_registry_hash_stable=true
egress_registry_hash_stable=true
switch_history_count_stable=true
selected_moves=0,0,0
wireguard_users=0,0,0
runtime_checks_ok=true
delayed_movements_observed=false
```

## Final Mutation Statement

Runtime mutation performed: YES

User movement performed by this closeout: YES — only `10.7.0.3`
rollback-related movement, `wireguard-1779454504-c43409 -> awg0`.

Routing mutation performed: YES — only route table `1001` for `10.7.0.3`.

Kill switch mutation performed: NO

Autoswitch apply performed manually: NO

New canary performed: NO

E11.10 canary closed: YES

