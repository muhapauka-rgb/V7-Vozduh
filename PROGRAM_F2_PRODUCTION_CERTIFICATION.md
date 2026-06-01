# Program F2 Production Autonomy Certification

Date: 2026-06-01
Final verdict: NOT_READY

## Required Verdicts

- approval_packet_created=false
- operator_autoswitch_certified=false
- autonomous_execution_successful=false
- autonomy_reliable=false
- rollback_reliable=false
- replay_protection_verified=false
- fail_closed_verified=true
- production_autonomy_certified=false

## Safety Verdict

- autonomous_budget<=1
- scope_expanded=false
- autoswitch_apply_outside_packet=false
- routing_changed_outside_scope=false
- deploy_performed=false
- users_moved=false

## Reason

The program found a stale target mismatch during mandatory fresh recheck. It failed closed as designed.

