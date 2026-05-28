# E21 First Action Candidate Analysis

## Candidate A - One-User Bounded Movement

blast_radius=1_user
rollback=required
audit_needs=high
dual_confirmation_needs=high
runtime_recheck_needs=high
stale_risk=medium
replay_risk=medium
operator_ux_readiness=good
production_risk=medium
verdict=NOT_FIRST

Reason: movement governance is proven, but first operator-driven execution should validate approval persistence and runtime recheck before touching user routing.

## Candidate B - Two-User Movement

blast_radius=2_users
rollback=required
audit_needs=high
dual_confirmation_needs=high
runtime_recheck_needs=high
stale_risk=medium
replay_risk=medium
operator_ux_readiness=good
production_risk=high
verdict=NO_GO

Reason: two-user movement is promotion-clean as orchestration, but it is too large for the first real operator-driven execution action.

## Candidate C - Restore-Apply Bounded Rehearsal

blast_radius=potential_autoswitch_side_effects
rollback=complex
audit_needs=high
dual_confirmation_needs=high
runtime_recheck_needs=high
stale_risk=high
replay_risk=medium
operator_ux_readiness=good
production_risk=high
verdict=NO_GO

Reason: historical delayed apply-restore movement makes this a bad first action.

## Candidate D - Generation-Clearance No-Move Execution

blast_radius=zero_users_if_apply_held_and_budget_zero
rollback=fail_closed_clearance_revoke
audit_needs=medium
dual_confirmation_needs=medium
runtime_recheck_needs=high
stale_risk=medium
replay_risk=medium
operator_ux_readiness=good
production_risk=low_to_medium
verdict=CONDITIONAL

Reason: this is safer than user movement, but still mutates governance state. It requires production approval persistence, dual operator binding, and a final live recheck.

## Candidate E - Emergency Containment Rehearsal

blast_radius=control_plane_state
rollback=manual
audit_needs=high
dual_confirmation_needs=medium
runtime_recheck_needs=high
stale_risk=medium
replay_risk=low
operator_ux_readiness=medium
production_risk=medium
verdict=NOT_FIRST

Reason: containment must remain available for emergencies, not be used as a productization first action.

## Candidate F - Read-Only-To-Execution Transition Only

blast_radius=zero_runtime_users
rollback=approval_revocation
audit_needs=medium
dual_confirmation_needs=medium
runtime_recheck_needs=medium
stale_risk=low
replay_risk=medium
operator_ux_readiness=high
production_risk=low
verdict=GO_AS_FIRST_STEP

Reason: this validates the missing production approval/audit mechanics before any runtime governance state is changed.

## Selected First Action

selected_first_action=F_READONLY_TO_EXECUTION_TRANSITION_PACKET_WITH_ZERO_MOVE_GENERATION_CLEARANCE_AS_NEXT_BOUNDARY

The next block should first create a real append-only approval/audit record from the UI-generated packet, perform live runtime recheck, and stop before any user or routing mutation. If that succeeds, a zero-move generation-clearance action can be considered as the next bounded action.

UI-triggered execution remains forbidden. The first action should be CLI-run using a UI-generated packet and explicit operator identities.
