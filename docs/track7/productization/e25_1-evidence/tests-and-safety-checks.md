# E25.1 Tests and Safety Checks

## JSON Validation

Command:

```text
python3 -m json.tool docs/track7/productization/e25_1-evidence/fresh-movement-approval-packet.json
python3 -m json.tool docs/track7/productization/e25_1-evidence/restore-settle-revalidation.json
python3 -m json.tool docs/track7/productization/e25_1-evidence/restore-settle-samples/*.json
```

Result: PASS.

## py_compile

Command:

```text
PYTHONPYCACHEPREFIX=.pycache-e25_1 python3 -m py_compile tools/v7-operator-execution-packet admin_core/operator_execution.py tools/v7-second-canary-target-readiness tools/v7-restore-settle-gate
```

Result: PASS.

Temporary `.pycache-e25_1` was removed after the check.

## Target Readiness Helper

Commands:

```text
tools/v7-second-canary-target-readiness --pretty
tools/v7-second-canary-target-readiness --json
```

Result: PASS.

Latest local helper smoke output showed:

- `approval_status=GO`
- `second_canary_readiness=GO`
- `selected_target=wireguard-1779454504-c43409`
- candidate `10.7.0.11` still valid on `1`
- `execution_allowed_now=false`

## Restore-Settle Helper

Commands:

```text
tools/v7-restore-settle-gate --pre-restore --state-dir docs/track7/productization/e25_1-evidence/restore-settle-samples --pretty
tools/v7-restore-settle-gate --pre-restore --state-dir docs/track7/productization/e25_1-evidence/restore-settle-samples --json
```

Result: PASS.

Gate result:

- `gate_status=GO`
- `sample_count=3`
- `apply_timer_intervals_covered=5.1`
- `selected_moves_by_sample=[0,0,0]`
- `registry_stable=true`
- `checkers_ok=true`
- `hidden_movers_observed=false`

## Targeted Unit Tests

Command:

```text
python3 -m unittest tests.unit.test_operator_execution_packet tests.unit.test_v7_second_canary_target_readiness tests.unit.test_v7_restore_settle_gate
```

Result: PASS.

Count: `26 tests`.

## Full Unit Suite

Command:

```text
python3 -m unittest discover tests
```

Result: PASS.

Count: `116 tests`.

## Packet Denial Validation

Command: in-memory packet validation against `fresh-movement-approval-packet.json`.

Result: PASS.

Validated denials:

- expired packet
- unauthorized user
- unauthorized target
- movement budget `2`
- stale users registry hash
- stale egress registry hash
- stale selected-move hash
- missing second confirmation
- wrong generation
- UI execution enabled
- autoswitch apply allowed
- kill switch mutation allowed

## Credential Scan

Command:

```text
rg -n "<credential/private-key/header patterns>" docs/track7/productization/e25_1-evidence BLOCK_E25_1_TARGET_READINESS_RECOVERY_AND_MOVEMENT_PACKET_REFRESH_REPORT.md
```

Result: PASS. No matches.

## Dangerous-Call Scan

Command:

```text
rg -n "(v7-user-switch|v7-routing-sync|v7-users-autoswitch\s+--apply|systemctl\s+(start|stop|restart)|ip\s+(route|rule)\s+(add|del)|nft\s+|iptables\s+|kill switch|kill-switch)" docs/track7/productization/e25_1-evidence tools/v7-operator-execution-packet admin_core/operator_execution.py
```

Result: PASS with expected documentation-only matches.

Expected matches were the E25.2-only forward/rollback command strings in the approval packet and execution-path decision. No command was executed in E25.1.

## Git Diff Check

Command:

```text
git diff --check
```

Result: PASS.

## Unavailable / Not Applicable

- Endpoint inventory was not re-run because E25.1 did not touch API routes.
- Static `/admin-v2` render smoke was not re-run because E25.1 did not touch UI.
- Audit chain validation was not applicable because E25.1 did not write approval/audit records.
