# E25 Tests and Safety Checks

## Commands / Checks

- `tools/v7-operator-execution-packet --validate-only --packet docs/track7/productization/e24-evidence/first-bounded-user-movement-approval-packet.json --pretty`
  - result: PASS as fail-closed
  - verdict: `DENY_PACKET_INVALID`
  - record written: NO
  - runtime action performed: NO

- `tools/v7-restore-settle-gate --pre-restore --state-dir docs/track7/productization/e24_2-evidence/restore-settle-samples --json`
  - result: PASS
  - `gate_status=GO`
  - `sample_count=3`
  - `apply_timer_intervals_covered=5.75`

- `PYTHONPYCACHEPREFIX=.pycache-e25 python3 -m py_compile tools/v7-operator-execution-packet admin_core/operator_execution.py tools/v7-second-canary-target-readiness tools/v7-restore-settle-gate`
  - result: PASS

- `python3 -m unittest tests.unit.test_operator_execution_packet tests.unit.test_v7_second_canary_target_readiness tests.unit.test_v7_restore_settle_gate`
  - result: PASS
  - count: `26` tests

- `python3 -m unittest discover tests`
  - result: PASS
  - count: `116` tests

- packet JSON validation:
  - `docs/track7/productization/e24-evidence/first-bounded-user-movement-approval-packet.json`: PASS
  - `docs/track7/productization/e24_2-evidence/restore-settle-gate-result.json`: PASS

- runtime checkers:
  - `v7-reconcile-check=OK`
  - `v7-user-route-check=OK`
  - `v7-killswitch-check=OK`
  - `v7-provisioning-reconcile-check=OK`

- hidden mover scan:
  - no `v7-user-switch`
  - no `v7-routing-sync`
  - no `v7-users-autoswitch --apply`

- `git diff --check`
  - result: PASS

## Not Run / Not Applicable

- forward movement verification: not run because pre-execution gate failed.
- rollback verification: not run because no forward movement occurred.
- delayed monitoring after rollback: not applicable.
- replay/denial tests against a valid movement packet: not applicable because no valid movement packet consumer exists and packet is expired.
- endpoint inventory: not applicable; no API route changes.
- UI render: not applicable; no UI changes.

## Safety Verdict

- User movement: NO
- Routing mutation: NO
- Runtime mutation: NO
- Kill switch mutation: NO
- Autoswitch apply: NO
