# BLOCK E27.2 First Two User Governed Movement Report

## Executive Summary

e27_2_completed=true
first_two_user_governed_movement_executed=true
two_user_governed_execution_certified=true

This block executed the first real governed two-user movement and default rollback:

- 10.7.0.11: `1 -> amneziawg-exec-20260528-10-8-1-14 -> 1`
- 10.7.0.12: `1 -> amneziawg-exec-20260528-10-8-1-14 -> 1`

No other users moved. Routing mutation was limited to route tables `1009` and `1010`. Autoswitch apply, canary, cohort beyond the approved two users, UI execution, broad routing sync, and kill switch control mutation were not performed.

## Approved Scope

candidate_user_A=10.7.0.11
candidate_user_B=10.7.0.12
forward_target=amneziawg-exec-20260528-10-8-1-14
rollback_target=1
movement_budget=2
blast_radius=2
execution_method=APPROVED_RAW_FALLBACK_ONLY

## Fresh Recheck And Authorization

Evidence:

- `docs/track7/productization/e27_2-evidence/execution-time-recheck.md`
- `docs/track7/productization/e27_2-evidence/fresh-approval-packet.json`
- `docs/track7/productization/e27_2-evidence/final-execution-authorization.md`

Fresh runtime recheck:

- users_registry_hash=f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042
- egress_registry_hash=13ae747486e30b4ad527c28343529f580fc400867981557845708c34385dd4ed
- candidate_user_A_current=1
- candidate_user_B_current=1
- route_table_1009=`default dev v7e356a192b79`
- route_table_1010=`default dev v7e356a192b79`
- target_users=0
- target_capacity_soft_limit=2
- target_capacity_hard_limit=2
- target_readiness=GO
- restore_settle_gate_status=GO
- selected_moves_count=0
- hidden_movers_present=false
- runtime_checkers_ok=true
- execution_authorized=true

Packet:

- packet_id=packet-7c1ba2e91060db60d6852069
- approval_id=approval-5cc17be9cad9fe2b30743238
- operation_id=e27-2-two-user-movement-20260528T223043Z
- packet_hash=310302c0e3e81b4896b6417294e16b898770fdc9a38d80fced3ed0cc2334671a
- packet_file_sha256=5e6d0a14054924d34bcce32bdc0df7feee6991641d61911603cf7a72252c9763
- packet_non_expired_at_authorization=true

## Forward Movement

Evidence:

- `docs/track7/productization/e27_2-evidence/forward-execution.md`
- `docs/track7/productization/e27_2-evidence/forward-verification.md`

Commands executed:

- `v7-user-switch 10.7.0.11 amneziawg-exec-20260528-10-8-1-14`
- `v7-user-switch 10.7.0.12 amneziawg-exec-20260528-10-8-1-14`

Result:

- exit_code_A=0
- exit_code_B=0
- forward_success=true
- target_users=2
- route_table_1009=`default dev v7execwg0`
- route_table_1010=`default dev v7execwg0`
- users.before.forward_sha256=f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042
- users.after.forward_sha256=b67212d81a2806f2e078317a41162a8a489c866ddf0fa617770d98e8d6ea0979
- forward_audit_record_hash=9a4cdede05bbd6fc158ed46a30b6ebfdc2a95114ad90a57e2bc0b122cc98cef0

The users.registry diff changed only:

- `10.7.0.11 current=1` to `current=amneziawg-exec-20260528-10-8-1-14`
- `10.7.0.12 current=1` to `current=amneziawg-exec-20260528-10-8-1-14`

The route diff changed only:

- table `1009`: `v7e356a192b79 -> v7execwg0`
- table `1010`: `v7e356a192b79 -> v7execwg0`

## Forward Observation

Evidence:

- `docs/track7/productization/e27_2-evidence/observation-A.md`
- `docs/track7/productization/e27_2-evidence/observation-B.md`
- `docs/track7/productization/e27_2-evidence/observation-C.md`

Observation timestamps:

- A: 2026-05-28T22:35:42Z
- B: 2026-05-28T22:36:07Z
- C: 2026-05-28T22:36:30Z

All samples:

- candidate_user_A_current=amneziawg-exec-20260528-10-8-1-14
- candidate_user_B_current=amneziawg-exec-20260528-10-8-1-14
- target_users=2
- selected_moves_count=0
- hidden_movers_present=false
- runtime_checkers_ok=true

## Rollback

Evidence:

- `docs/track7/productization/e27_2-evidence/rollback-execution.md`
- `docs/track7/productization/e27_2-evidence/rollback-verification.md`

Commands executed:

- `v7-user-switch 10.7.0.11 1`
- `v7-user-switch 10.7.0.12 1`

Result:

- rollback_executed=true
- rollback_success=true
- target_users=0
- route_table_1009=`default dev v7e356a192b79`
- route_table_1010=`default dev v7e356a192b79`
- users.after.rollback_sha256=f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042
- rollback_audit_record_hash=08ea660df685b3ae53422ac756aa08d7632259f5e33f391b1887cc73fae0d016

Rollback restored users.registry to the exact pre-forward hash.

## Post-Rollback Settle And Delayed Monitoring

Evidence:

- `docs/track7/productization/e27_2-evidence/post-rollback-restore-settle.md`
- `docs/track7/productization/e27_2-evidence/delayed-monitoring-A.md`
- `docs/track7/productization/e27_2-evidence/delayed-monitoring-B.md`
- `docs/track7/productization/e27_2-evidence/delayed-monitoring-C.md`

Post-rollback restore-settle:

- restore_settle_gate_status=GO
- sample_count=3
- apply_timer_intervals_covered=2.9
- selected_moves_by_sample=[0,0,0]
- registry_stable=true
- egress_registry_stable=true
- checkers_ok=true
- hidden_movers_observed=false
- moved_users=[]

Delayed monitoring:

- delayed_movement_observed=false
- unapproved_user_movement=false
- routing_drift=false
- runtime_checkers_ok=true
- target_users=0 in all samples
- both approved users remained on rollback target `1`

## Replay Validation

Evidence:

- `docs/track7/productization/e27_2-evidence/replay-validation.md`

Initial replay helper result was `REPLAY_NOT_CONSUMED` because the evidence helper used an order-dependent grep against JSON audit records. The forward audit record was present. The helper was bounded-fixed to parse JSON by `packet_id` and `event`, then replay validation was rerun.

Final replay result:

- used_forward_records=1
- verdict=DENY_REPLAY
- movement_executed_during_replay=false
- routing_mutation_during_replay=false
- replay_audit_record_hash=74378f991a3641f3f88b5deddf925bc5305e1a8d502ab01903c96d02f5802b9d
- replay_rejection_verified=true

## Tests

Evidence:

- `docs/track7/productization/e27_2-evidence/tests.md`

Test summary:

- py_compile/compileall: PASS after sandbox cache-prefix retry
- targeted unit tests: PASS, 29 tests
- full unittest discover: PASS, 119 tests
- packet JSON validation: PASS
- restore-settle JSON validation: PASS
- runtime checkers: PASS
- readiness helper: GO
- restore-settle helper: GO
- hidden mover scan: PASS, no hidden movers
- credential scan: PASS, 0 matches
- dangerous-call scan: PASS_WITH_EXPECTED_HITS for approved forward/rollback commands only
- git diff --check: PASS

## Final Answers

e27_2_completed=true
first_two_user_governed_movement_executed=true

candidate_user_A=10.7.0.11
candidate_user_B=10.7.0.12
forward_target=amneziawg-exec-20260528-10-8-1-14

forward_success=true
rollback_executed=true
rollback_success=true

only_approved_users_moved=true
routing_mutation_limited_to_candidates=true

delayed_movement_observed=false
replay_rejection_verified=true

runtime_checkers_ok=true
restore_settle_gate_status=GO

two_user_governed_execution_certified=true

remaining_blockers=NONE
recommended_next_block=E28_SMALL_COHORT_GOVERNED_MOVEMENT_PREPARATION

## Final Mutation Statement

Runtime mutation performed: YES
If YES: only approved two-user forward movement and rollback

User movement performed: YES
If YES: only `10.7.0.11` and `10.7.0.12`

Routing mutation for users performed: YES
If YES: only route tables `1009` and `1010`

Kill switch control/toggle mutation performed: NO
Autoswitch apply performed manually: NO
Raw unsafe profile executed: NO
Canary performed: NO
Cohort performed: NO

