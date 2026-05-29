# E27.2 Tests And Safety Checks

date_utc=2026-05-28T23:05:00Z

## Summary

total_test_groups=11
pass_groups=11
fail_groups=0
unavailable_groups=0
runtime_mutation_scope=approved_forward_and_rollback_only
unauthorized_movement_observed=false
autoswitch_apply_observed=false
kill_switch_mutation_observed=false

## Local Tests

1. command=`python3 -m compileall admin_core tools tests`
   result=RETRIED
   detail=initial run failed because macOS Python tried to write bytecode under `~/Library/Caches/com.apple.python/...`, outside sandbox permission.

2. command=`PYTHONPYCACHEPREFIX=.pycache-e27_2 python3 -m compileall admin_core tools tests`
   result=PASS
   test_count=all discovered Python files under admin_core/tools/tests compiled

3. command=`python3 -m unittest tests.unit.test_operator_execution_packet tests.unit.test_v7_second_canary_target_readiness tests.unit.test_v7_restore_settle_gate`
   result=PASS
   test_count=29

4. command=`python3 -m unittest discover`
   result=PASS
   test_count=119

5. command=`python3 -m json.tool docs/track7/productization/e27_2-evidence/fresh-approval-packet.json`
   result=PASS
   validation=packet_json_valid

6. command=`python3 -m json.tool docs/track7/productization/e27_2-evidence/post-rollback-restore-settle.json`
   result=PASS
   validation=restore_settle_json_valid

7. command=`credential-pattern scan over docs/track7/productization/e27_2-evidence`
   result=PASS
   matches=0
   note=no credential material found in generated E27.2 evidence

8. command=`rg -n "v7-user-switch|v7-users-autoswitch --apply|v7-routing-sync|kill-switch|killswitch|systemctl (start|stop|restart)|ip route (add|del|replace)|ip rule (add|del)|nft add|nft delete|iptables|wg-quick up|wg-quick down" docs/track7/productization/e27_2-evidence`
   result=PASS_WITH_EXPECTED_HITS
   expected_hits=approved `v7-user-switch` forward/rollback commands, hidden mover scan pattern, and checker file names
   forbidden_hits=none

9. command=`git diff --check`
   result=PASS

## Runtime Tests

10. command=`v7-reconcile-check && v7-user-route-check && v7-killswitch-check && v7-provisioning-reconcile-check && v7-second-canary-target-readiness --execution-target-id amneziawg-exec-20260528-10-8-1-14 --pretty && v7-restore-settle-gate --pre-restore --state-dir /tmp/e27_2/post-rollback-settle --pretty`
    result=PASS
    runtime_checkers=OK
    readiness=GO
    restore_settle=GO
    selected_moves_by_sample=[0,0,0]
    hidden_movers_observed=false

11. command=`ps -eo pid,ppid,etime,command | grep -E "v7-user-switch|v7-routing-sync|v7-users-autoswitch.*--apply" | grep -v grep || true`
    result=PASS
    hidden_movers_present=false

## Replay Validation

command=`bash /tmp/e27_2_remote.sh replay`
first_result=REPLAY_NOT_CONSUMED
root_cause=evidence helper used order-dependent grep for JSON audit records
bounded_fix=updated `/tmp/e27_2_remote.sh` replay lookup to parse audit JSON by packet_id and event
rerun_result=PASS
verdict=DENY_REPLAY
movement_executed_during_replay=false
routing_mutation_during_replay=false
