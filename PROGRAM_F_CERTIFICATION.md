# Program F Certification

Date: 2026-06-01
Final verdict: NOT_READY

## Required Verdicts

- operator_autoswitch_certified=false
- autonomous_execution_successful=false
- autonomy_reliable=false
- rollback_reliable=false
- replay_protection_verified=false
- fail_closed_verified=true
- bounded_autonomy_certified=false
- safe_to_continue_to_program_g=false

## Safety Verdict

- autonomous_budget<=1
- scope_expanded=false
- autoswitch_apply_outside_packet=false
- routing_changed_outside_scope=false
- deploy_performed=false
- users_moved=false
- autoswitch_apply_run=false

## Reason

The exact one-user packet is ready for approval, but not approved. Program F cannot prove autonomy while Stage 1 operator-approved movement is blocked.

