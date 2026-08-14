# BLOCK E11.8 Target Reservation Enforcement Root-Cause And Fix Report

## Summary

E11.8 found and fixed the production autoswitch reservation enforcement gap.

The root cause was not one isolated stale state issue. `canary_reserved=true` existed in `egress.registry`, but production `v7-users-autoswitch` did not parse or enforce it. Planner, failover, rebalance, dynamic load, and apply selection all treated reserved WireGuard as a normal `GLOBAL_FAST` target after E11.6 made diagnose OK.

The bounded fix was deployed to `/usr/local/bin/v7-users-autoswitch` only. It prevents new production assignment to canary-reserved targets and deliberately does not drain existing users from WireGuard.

## Required Answers

reservation_enforcement_root_cause=canary_reserved_metadata_present_but_not_consumed_by_v7_users_autoswitch

root_cause_classification=MIXED_RESERVATION_METADATA_NOT_CONSUMED_PLANNER_IGNORES_RESERVATION_APPLY_TRUSTS_PLANNER_EXISTING_USERS_NOT_DRAINED

fix_path_selected=planner_destination_hard_block_without_drain

runtime_fix_executed=true

rollback_performed=false

wireguard_users_after=10

reservation_enforced=true

awg_regression_observed=false

restore_settle_gate_status=NOT_RERUN_LIVE_DEFAULT_LOCAL_FIXTURE_STALE

target_readiness_after=NO-GO

selected_target_after=NONE

second_canary_readiness_after=NO-GO_RESERVED_WIREGUARD_USERS_REQUIRE_DRAIN_PACKET

waiver_required_after=false

dedicated_test_egress_needed=false

recommended_next_block=E11.9_BOUNDED_WIREGUARD_RESERVED_TARGET_DRAIN_APPROVAL_PACKET

execution_allowed_now=false

## Fix Implemented

Repo and runtime `v7-users-autoswitch` now:

- parses `canary_reserved`;
- excludes reserved egresses from the production dynamic load pool;
- blocks reserved egresses as production destination candidates with `canary_reserved_production_assignment_blocked`;
- keeps already-present users on a reserved target if the target is healthy, marking them with `canary_reserved_current_hold_requires_separate_drain_approval`;
- does not perform automatic drain.

Runtime deploy:

- runtime_path=/usr/local/bin/v7-users-autoswitch
- backup_path=/usr/local/bin/v7-users-autoswitch.backup.e11_8_20260526T213348Z
- runtime_hash_after=5e3b1b479b8363cc9dfeb63bc8d0c87cc14de1ef9326912cea79086737734ec1

## Verification

Post-fix dry-run:

- candidate_moves_total=0
- selected_moves=0
- selected_to_wg=[]
- non_current_users_with_wg_blocked=6
- current_wg_users_held=10

Post-deploy timer observation:

- no new switch-history entries after deploy observation window;
- users.registry hash stayed stable;
- WireGuard user count stayed 10;
- journal showed `canary_reserved_production_assignment_blocked` for non-current WireGuard candidates;
- current WireGuard users were held, not drained.

## Readiness

WireGuard is no longer eligible for new production assignment, but it is still occupied by 10 production users. Therefore it is not a clean canary target yet.

Next safest step: prepare a bounded drain approval packet for the exact 10 users currently on WireGuard, with no canary execution and no broad autoswitch apply.

## Final Mutation Statement

Runtime mutation performed: YES — limited to `/usr/local/bin/v7-users-autoswitch` reservation enforcement logic only

User movement performed by this block: NO

Routing mutation performed by this block: NO

Kill switch mutation performed: NO

Autoswitch apply performed manually: NO

Canary performed: NO
