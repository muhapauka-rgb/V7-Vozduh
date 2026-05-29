# E28 Tests

date_utc=2026-05-29T06:18:00Z

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false
autoswitch_apply_performed=false
canary_performed=false
cohort_performed=false

## Tests Run

1. command=`PYTHONPYCACHEPREFIX=.pycache-e28 python3 -m compileall admin_core tools tests`
   result=PASS

2. command=`audit tail JSON parse validation`
   result=PASS
   audit_tail_records=26
   audit_tail_parse_errors=0

3. command=`v7-reconcile-check`
   result=PASS
   evidence=`docs/track7/productization/e28-evidence/e28-test-reconcile.out`

4. command=`v7-user-route-check`
   result=PASS
   evidence=`docs/track7/productization/e28-evidence/e28-test-user-route.out`

5. command=`v7-killswitch-check`
   result=PASS
   evidence=`docs/track7/productization/e28-evidence/e28-test-killswitch.out`

6. command=`v7-provisioning-reconcile-check`
   result=PASS
   evidence=`docs/track7/productization/e28-evidence/e28-test-provisioning.out`

7. command=`v7-second-canary-target-readiness --execution-target-id amneziawg-exec-20260528-10-8-1-14 --pretty`
   result=PASS
   readiness=GO
   evidence=`docs/track7/productization/e28-evidence/e28-test-readiness.out`

8. command=`v7-restore-settle-gate --pre-restore --state-dir /tmp/e28/restore-settle-samples --pretty`
   result=PASS
   restore_settle=GO
   evidence=`docs/track7/productization/e28-evidence/e28-test-restore-settle.out`

9. command=`hidden mover scan`
   result=PASS
   hidden_movers_present=false
   evidence=`docs/track7/productization/e28-evidence/e28-test-hidden.out`

10. command=`credential-pattern scan over docs/track7/productization/e28-evidence`
    result=PASS
    note=only earlier script variable names matched before they were renamed; final scan clean.

11. command=`dangerous-call scan over docs/track7/productization/e28-evidence`
    result=PASS_WITH_EXPECTED_HITS
    expected_hits=forbidden command names appear only in hidden mover scan patterns and boundary documentation; no execution of v7-user-switch/autoswitch apply/routing sync.

12. command=`git diff --check`
    result=PASS

unavailable_tests=NONE

