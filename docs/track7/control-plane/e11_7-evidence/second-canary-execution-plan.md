# E11.7 Second Canary Execution Plan

Status: not approved for execution.

The normal governed lifecycle remains:

1. Pre-check current runtime truth.
2. Hold planner and apply authority.
3. Execute exactly one approved `v7-user-switch`.
4. Observe quiet window.
5. Roll back or keep only by explicit approval.
6. Restore planner only.
7. Run restore-settle gate across at least two apply intervals.
8. Restore apply only if gate is `GO`.
9. Run post-restore settle monitoring.
10. Publish final verdict.

Abort conditions for the next approval attempt:

- target readiness is not `GO`;
- target is not zero-user by registry and load-state;
- selected target is not `wireguard-1779454504-c43409`;
- restore-settle gate is not `GO`;
- selected moves are nonzero before hold;
- hidden `v7-user-switch` or `v7-routing-sync` exists;
- any reconcile/user-route/killswitch/provisioning check fails;
- rollback target is unclear;
- candidate current assignment changes before execution.

E11.7 live decision:

```text
execution_plan_status=BLOCKED_TARGET_OCCUPIED
approved_forward_command=NONE
approved_rollback_command=NONE
movement_budget=0
emergency_containment=not_applicable_no_live_block
```

Next valid live canary execution plan can be generated only after a fresh
target-pool block proves a zero-user clean target again.
