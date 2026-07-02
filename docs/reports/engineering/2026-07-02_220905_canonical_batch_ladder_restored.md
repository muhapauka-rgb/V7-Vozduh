# Canonical Batch Ladder Restored

Timestamp: 2026-07-02 22:09:05 Asia/Bangkok

Verdict: CANONICAL_BATCH_LADDER_RESTORED

## Summary

The accidental intermediate authority ladder value `SMALL_BATCH = 2` has been removed from the canonical governed L3 ladder.

The governed owner contract from the previous implementation remains unchanged:

```text
requested_max_users <= authorized_l3_budget
```

Only the canonical ladder values and their affected tests/documentation were corrected.

## Restored Canonical Ladder

```text
CANARY        = 1
SMALL_BATCH   = 5
MEDIUM_BATCH  = 10
LARGE_BATCH   = 25
XLARGE_BATCH  = 50
FULL_INCIDENT = remaining affected users on the same active failed-source incident
```

`FULL_INCIDENT` is not broad automation. It is represented as a dynamic terminal class scoped to remaining affected users on the same active incident. No unrelated users, unrelated incidents, or cross-incident batching are introduced.

## Where Value 2 Appeared

The accidental value appeared as a canonical class ceiling in:

- `tools/v7-users-autoswitch::AUTHORITY_CLASS_BUDGETS`
- `tools/v7-users-autoswitch::DEFAULT_AUTHORITY_BUDGET_POLICY.next_allowed_user_budget`
- `tools/v7-users-autoswitch::_authority_bridge_model()`
- `tools/v7-users-autoswitch::_authority_certification_rules()`
- `tools/v7-users-autoswitch::_authority_full_action_matrix()`
- `tests/unit/test_v7_users_autoswitch_policy.py`
- `tests/unit/test_governed_canary_cli.py`
- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reports/engineering/2026-07-02_215400_governed_l3_authority_budget_contract.md`

Some unit tests still use `current_allowed_user_budget = 2` intentionally as a lower-than-class runtime cap in two-user fixtures. Those are not canonical ladder definitions and were left unchanged.

## Why It Was Accidental

`SMALL_BATCH = 2` came from an intermediate discussion artifact, not the intended production ladder. The requested canonical ladder defines SMALL_BATCH as five users, with subsequent promotion ceilings of ten, twenty-five, fifty, then dynamic full-incident scope.

## Updated Locations

### tools/v7-users-autoswitch

Updated:

- `AUTHORITY_CLASS_BUDGETS`
- `AUTHORITY_CLASS_NEXT`
- `AUTHORITY_CLASS_RANK`
- `AUTHORITY_PROMOTION_RULES`
- `DEFAULT_AUTHORITY_BUDGET_POLICY`
- `normalize_authority_class()`
- new `authority_class_budget()`
- `_authority_budget_policy()`
- `promote_authority()`
- `_authority_lifecycle_model()`
- `_authority_bridge_model()`
- `_authority_certification_rules()`
- `_authority_full_action_matrix()`
- `_authority_budget_gate()`

The legacy `POOL` code path remains present for existing unrelated pool/equivalence code, but it is no longer the canonical next governed L3 ladder step after `LARGE_BATCH`. The canonical next step is now `XLARGE_BATCH`.

### Tests

Updated:

- `tests/unit/test_governed_canary_cli.py`
- `tests/unit/test_v7_users_autoswitch_policy.py`

The tests now prove:

- CANARY default remains 1.
- SMALL_BATCH canonical ceiling is 5.
- MEDIUM_BATCH canonical ceiling is 10.
- LARGE_BATCH canonical ceiling is 25.
- XLARGE_BATCH canonical ceiling is 50.
- Legacy direct `LARGE_BATCH -> POOL` promotion is denied as non-canonical.
- A lower explicit current budget can still cap movement below a class ceiling.

### Documentation

Updated:

- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reports/engineering/2026-07-02_215400_governed_l3_authority_budget_contract.md`

## Tests

Governed canary CLI and autoswitch policy:

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests.unit.test_governed_canary_cli tests.unit.test_v7_users_autoswitch_policy
```

Result:

```text
Ran 141 tests
OK
```

Operator execution packet and pipeline:

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests.unit.test_operator_execution_packet tests.unit.test_operator_execution_pipeline
```

Result:

```text
Ran 77 tests
OK
```

Compile:

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch tools/v7-governed-canary-dry-run-cycle admin_core/operator_execution_pipeline.py tests/unit/test_governed_canary_cli.py tests/unit/test_v7_users_autoswitch_policy.py
```

Result:

```text
PASS
```

Diff hygiene:

```text
git diff --check -- tools/v7-users-autoswitch tests/unit/test_governed_canary_cli.py tests/unit/test_v7_users_autoswitch_policy.py docs/reference/V7_CANONICAL_REFERENCE.md docs/reports/engineering/2026-07-02_215400_governed_l3_authority_budget_contract.md
```

Result:

```text
PASS
```

## Production Behavior

Production behavior was not changed.

No deploy was performed.

No production movement was performed.

No certification state was changed.

No larger production batch was enabled.

Local production unit definition remains:

```text
ExecStart=/usr/local/bin/v7-governed-canary-dry-run-cycle --execute-l3-production-validation --confirm-l3-production-validation EXECUTE_L3_PRODUCTION_VALIDATION_APPROVED --max-users 1
```

Users moved by this task: 0

## Final Verdict

CANONICAL_BATCH_LADDER_RESTORED

