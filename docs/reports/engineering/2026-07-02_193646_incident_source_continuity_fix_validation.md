# Incident Source Continuity Fix Validation

Timestamp: 2026-07-02_193646

## Summary

Incident source continuity was implemented and deployed through the standard safe deployment path. The fix successfully changed the production L3 governed selection from an unrelated `wireguard -> vless` rebalance candidate to the failed-source incident candidate:

- user: `10.7.0.2`
- source: `openvpn-1779388847-d2ad7c`
- target: `vless`
- move_type: `failover`
- transition: `READY`

Production certification is still not complete. Runtime Apply did not move the user. The next blocker is selected move identity/lifetime at approved plan lock / restore barrier / apply boundary.

## Changed Files

- `tools/v7-users-autoswitch`
- `tests/unit/test_v7_users_autoswitch_policy.py`

## Patched Owner And Functions

- Owner: `tools/v7-users-autoswitch`
- Function: `AutoswitchPlanner._l3_active_incident_source_context`

Implemented behavior:

- Preserves `incident_source` independently from `selected_move.current_egress`.
- Recovers a lost or stale incident source from confirmed failed-source observation.
- Chooses hard current-channel failure before service-only failure.
- Keeps max-users bounded by existing emergency failover policy.
- Does not bypass Planner, Authority, Restore Barrier, Runtime, or Verification.

## Commits

- `a3ea3c22` - `Fix L3 incident source continuity recovery`
- `70e83550` - `Fix stale L3 incident source recovery`
- `b9b1118b` - `Prioritize hard failed L3 incident sources`

Branch pushed:

- `Updatesystem`

## Tests

Passed:

- `PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests.unit.test_v7_users_autoswitch_policy`
  - 119 tests OK
- `PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests.unit.test_governed_canary_cli`
  - 17 tests OK
- `PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch tests/unit/test_v7_users_autoswitch_policy.py`
  - OK

Regression coverage added:

- lost incident source recovers from confirmed failed-source observation
- stale persisted incident source does not override larger failed-source observation
- hard current-channel failure wins over larger service-only failure

## Safe Deploy

Safe deploy command:

`python3 tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED --update-local-snapshot --json`

Deploy result:

- blockers: `[]`
- GitHub: `GITHUB_ALIGNED`
- local: `LOCAL_ALIGNED`
- deployed commit: `b9b1118b8b58fc98f1b1ba2dc7feaa08107a7d3a`
- production hash for `/usr/local/bin/v7-users-autoswitch`: `7123abd0468aac90fe634ad92bd81112bd905f63fd65c96325969f2427888e46`

## Production Validation

Heartbeat restored through approved systemd path:

- `systemctl start v7-users-autoswitch.timer`
- service: `/usr/local/bin/v7-governed-canary-dry-run-cycle --execute-l3-production-validation --confirm-l3-production-validation EXECUTE_L3_PRODUCTION_VALIDATION_APPROVED --max-users 1`

Timer was stopped after validation to avoid additional repeated no-execution cycles:

- `systemctl stop v7-users-autoswitch.timer`

Production selection after fix:

- transition status: `READY`
- user: `10.7.0.2`
- source: `openvpn-1779388847-d2ad7c`
- target: `vless`
- move_type: `failover`
- reason includes: `current_egress_not_eligible`, `emergency_failover_autonomy_authorized`

Execution outcome records after fix:

- `terminal_state=DENIED`
- `terminal_reason=approved_plan_lock_selected_moves_missing`
- `terminal_outcome_classification=NO_EXECUTION`
- `verification_result.success=false`
- `verification_result.verify_rc=null`
- `verification_result.service_verify_rc=null`
- `rollback_required=false`

Additional repeated dry-run records:

- `dry_run_restore_barrier_clearance_budget_and_generation_ok`
- `dry_run_selected_moves_available`

## Remaining Users On Failed Source

Failed source:

- `openvpn-1779388847-d2ad7c`

Remaining enabled users:

- count: `10`
- users: `10.7.0.2`, `10.7.0.4`, `10.7.0.6`, `10.7.0.8`, `10.7.0.9`, `10.7.0.10`, `10.7.0.11`, `10.7.0.12`, `10.7.0.13`, `10.7.0.15`

## Production Impact

- Deploy performed: YES
- Users moved: `0`
- Runtime Apply executed successfully: NO
- Verification executed: NO
- Rollback executed: NO
- Broad automation enabled: NO
- Max users per governed cycle increased: NO

## Certification Result

NOT CERTIFIED.

The incident source continuity defect is fixed far enough for production Planner/Governed Owner selection to choose the correct failed-source L3 candidate. The system still does not complete user movement because selected move identity is not preserved into Runtime Apply.

## Next Blocker

First remaining blocker:

- `approved_plan_lock_selected_moves_missing`

Owner boundary:

- `tools/v7-governed-canary-dry-run-cycle`
- `admin_core/operator_execution.py`
- `tools/v7-users-autoswitch --apply`

Safe correction direction:

- Continue from approved plan lock / restore barrier selected move lifetime.
- Prove why the approved selected move exists at transition time but is missing when Runtime Apply validates the approved lock.
- Do not change incident_source selection again unless this downstream proof points back to it.

