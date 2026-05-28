# E11.12 Mini-Cohort Lifecycle Plan

mini_cohort_lifecycle_plan_completed=true
execution_allowed_now=false

## Future Execution Lifecycle

1. Fresh pre-checks
   - Verify `wireguard-1779454504-c43409_users=0`.
   - Verify target readiness `GO`.
   - Verify restore-settle gate `GO`.
   - Verify `selected_moves=0`.
   - Verify runtime checkers OK.
   - Verify hidden mover scan empty.
   - Verify candidates still match `10.7.0.11 current=1 table=1009` and `10.7.0.12 current=1 table=1010`.
2. Hold planner/apply
   - Planner and apply must be held before forward movement.
   - No manual autoswitch apply is allowed.
3. Move user 1
   - Previewed command: `v7-user-switch 10.7.0.11 wireguard-1779454504-c43409`.
   - Verify registry row, route table, `route_get`, WireGuard count, and runtime checkers.
4. Stagger
   - Wait at least one check interval before user 2.
   - Abort if any checker fails or hidden movement appears.
5. Move user 2
   - Previewed command: `v7-user-switch 10.7.0.12 wireguard-1779454504-c43409`.
   - Verify registry row, route table, `route_get`, WireGuard count equals `2`, and runtime checkers.
6. Observation window
   - Collect observations A/B/C.
   - Required: route/checkers OK, no hidden movers, no non-candidate movement, no target overload.
7. Rollback or keep
   - Default decision is rollback both users to `1`.
   - Keep requires explicit evidence that keep is safer than rollback and does not consume the reserved target beyond approved scope.
8. Planner restore
   - Restore planner first if held.
9. Restore-settle gate
   - Collect at least three samples across at least two apply timer intervals.
   - Gate must be `GO`.
10. Apply restore
   - Restore apply only after gate `GO`.
   - Do not run manual autoswitch apply.
11. Delayed monitoring
   - Collect at least three final samples: registry hash, switch-history, selected moves, WireGuard users, candidate routes, runtime checkers, hidden movers.
12. Final verdict
   - Publish explicit mutation statements and rollback/keep decision.

## Abort Conditions

- WireGuard users before execution is not `0`.
- Target readiness is not `GO`.
- Restore-settle gate is not `GO`.
- `selected_moves > 0`.
- Any runtime checker fails.
- Hidden `v7-user-switch`, `v7-routing-sync`, or `v7-users-autoswitch --apply` process exists.
- Candidate current egress/table differs from this packet.
- WireGuard users would exceed `2`.
- Any non-candidate user moves.

## Rollback Conditions

- Either candidate route check fails after movement.
- Runtime checker failure after either forward move.
- WireGuard quality degrades below readiness floor during observation.
- Any delayed autoswitch movement is observed.
- Partial failure after first user movement.
- Any ambiguity in route attribution.

movement_budget=2_users_max
stagger_timing=one_check_interval_between_users_minimum
delayed_monitoring_required=true
manual_autoswitch_apply_allowed=false
