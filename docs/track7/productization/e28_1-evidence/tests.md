# E28.1 Tests

date_utc=2026-05-29T07:07:00Z

runtime_mutation_performed=true
runtime_mutation_scope=target_capacity_metadata_soft_limit_hard_limit_only
user_movement_performed=false
routing_mutation_performed=false
autoswitch_apply_performed=false
canary_performed=false
cohort_performed=false

## Tests Run

1. command=`PYTHONPYCACHEPREFIX=.pycache-e28_1 python3 -m compileall admin_core tools tests`
   result=PASS

2. command=`python3 -m unittest tests.unit.test_v7_second_canary_target_readiness tests.unit.test_v7_restore_settle_gate tests.unit.test_operator_execution_packet`
   result=PASS
   test_count=29

3. command=`json validation for capacity-probe/summary.json, long-window/summary.json, restore-settle.json`
   result=PASS

4. command=`v7-reconcile-check`
   result=PASS
   evidence=`docs/track7/productization/e28_1-evidence/e28_1-test-reconcile.out`

5. command=`v7-user-route-check`
   result=PASS
   evidence=`docs/track7/productization/e28_1-evidence/e28_1-test-user-route.out`

6. command=`v7-killswitch-check`
   result=PASS
   evidence=`docs/track7/productization/e28_1-evidence/e28_1-test-killswitch.out`

7. command=`v7-provisioning-reconcile-check`
   result=PASS
   evidence=`docs/track7/productization/e28_1-evidence/e28_1-test-provisioning.out`

8. command=`v7-second-canary-target-readiness --execution-target-id amneziawg-exec-20260528-10-8-1-14 --pretty`
   result=PASS
   readiness=GO
   evidence=`docs/track7/productization/e28_1-evidence/e28_1-test-readiness.out`

9. command=`v7-restore-settle-gate --pre-restore --state-dir /tmp/e28_1/restore-settle-samples --pretty`
   result=PASS
   gate_status=GO
   sample_count=3
   apply_timer_intervals_covered=6.0
   evidence=`docs/track7/productization/e28_1-evidence/e28_1-test-restore-settle.out`

10. command=`hidden mover scan`
    result=PASS
    hidden_movers_present=false
    evidence=`docs/track7/productization/e28_1-evidence/e28_1-test-hidden.out`

11. command=`credential-pattern scan over docs/track7/productization/e28_1-evidence`
    result=PASS
    matches=0

12. command=`dangerous-call scan over docs/track7/productization/e28_1-evidence`
    result=PASS_WITH_EXPECTED_HITS
    expected_hits=hidden mover scan pattern only
    forbidden_execution_hits=0

13. command=`git diff --check`
    result=PASS

unavailable_tests=NONE

