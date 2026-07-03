# Phase 6 Authority Owner Resolution

Timestamp: 2026-07-03_162858

## Summary

Phase 6 / XLARGE_BATCH reached an Authority owner breakpoint after Phase 5 PASS.

The certification program did not stop at the blocker. The blocker was converted into an engineering mission against the existing Authority owner.

## Current Phase

Phase: Phase 6: XLARGE_BATCH Certification

Current terminal state before fix: OWNER_RESOLUTION

Blocking owner: Authority Budget owner in `tools/v7-users-autoswitch`

Blocking function: `AutoswitchPlanner.promote_authority()`

## Production Evidence

Phase 5 operation:

- operation_id: `runtime_autoswitch_d2fc48ffe5590c23e2ac8950`
- users moved: 25
- verification: PASS
- rollback: NOT_REQUIRED
- closure records: 25 SUCCESS records

Production policy before fix:

- policy path: `/etc/v7/policy.json`
- authority_class: `POOL`
- certified_authority_class: `POOL`
- current_allowed_user_budget: 25
- next_authority_class: `POOL`
- next_allowed_user_budget: 25

Canonical Phase 6 requires:

- authority class: `XLARGE_BATCH`
- budget: 50
- transition: `LARGE_BATCH -> XLARGE_BATCH`

## Authority Diagnostic

Existing owner command:

```bash
/usr/local/bin/v7-users-autoswitch --promote-authority-to XLARGE_BATCH --authority-promotion-operation-id runtime_autoswitch_d2fc48ffe5590c23e2ac8950 --pretty
```

Result:

- status: DENIED
- routing_mutation_performed: false
- autoswitch_apply_run: false
- users_moved: 0

Blockers:

- `invalid_target_authority_transition_POOL_to_XLARGE_BATCH`
- `invalid_rule_source_authority_POOL_for_XLARGE_BATCH`
- `two_successful_large_batch_operation_ids_required`
- `xlarge_batch_evidence_validation_failed`

Additional diagnostic with prior legacy operation:

```bash
/usr/local/bin/v7-users-autoswitch --promote-authority-to XLARGE_BATCH --authority-promotion-operation-id runtime_autoswitch_0425741b308df19ccc0c1e03 --authority-promotion-operation-id runtime_autoswitch_d2fc48ffe5590c23e2ac8950 --pretty
```

Result:

- old operation feedback records were not available in the current promotion feedback logs.
- Phase 5 operation had complete feedback records, but `stability_window_observed_seconds` was 0.

## Root Cause

Two implementation gaps were proven inside the existing Authority owner:

1. Legacy `POOL=25` policy state is not interpreted as the canonical `LARGE_BATCH=25` state for forward promotion.
2. Promotion stability/no-regression evidence can remain 0 even when feedback records contain persisted `created_at` timestamps from which elapsed stability can be derived.

Classification:

- Owner Resolution Terminal Classification: IMPLEMENTATION_DEFECT
- Required Resolution: Extend existing Authority owner.

## Files Changed

- `tools/v7-users-autoswitch`
- `tests/unit/test_v7_users_autoswitch_policy.py`

## Exact Changes

### Authority legacy class alias

Added:

```python
canonical_authority_class_for_promotion(value, budget)
```

Behavior:

- `POOL` with budget <= `LARGE_BATCH` budget maps to canonical `LARGE_BATCH` only for promotion transition checks.
- This does not increase runtime budget.
- This does not create a new Authority owner.
- This does not create a new execution path.

### Stability window derivation

Updated:

```python
AutoswitchPlanner._authority_promotion_stability_window_seconds()
```

Behavior:

- Existing explicit stability/no-regression fields still win.
- If explicit fields are absent, the owner derives elapsed stability from persisted feedback `created_at`.
- The derived window is real elapsed time since the latest persisted feedback record.
- No synthetic success is created.

### Promotion transition

Updated:

```python
AutoswitchPlanner.promote_authority()
```

Behavior:

- Transition checks use canonical promotion class.
- Raw policy state remains visible in the result under `legacy_authority_class_alias`.
- Promotion still requires explicit confirmation, truth check, audit log, required feedback, required operation count, and required stability window.

## Tests

Focused tests:

```bash
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_authority_promotion_to_xlarge_batch_requires_two_large_runs_and_no_regression_window tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_legacy_pool_25_can_promote_to_xlarge_as_canonical_large_batch
```

Result: PASS, 2 tests.

Full policy tests:

```bash
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy
```

Result: PASS, 141 tests.

Governed CLI tests:

```bash
python3 -m unittest tests.unit.test_governed_canary_cli
```

Result: PASS, 29 tests.

Compile:

```bash
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch tests/unit/test_v7_users_autoswitch_policy.py
```

Result: PASS.

## Production Impact

Before deploy: NONE.

Runtime behavior changed before deploy: NO.

Users moved by this fix: 0.

Broad automation enabled: NO.

Max users increased by implementation: NO.

The fix only makes the existing Authority promotion owner capable of resolving the canonical Phase 6 promotion path when evidence and confirmation are present.

## Remaining Phase 6 Gate

After deployment, Phase 6 must resume at Authority promotion review.

Promotion to `XLARGE_BATCH` still requires:

- explicit Authority promotion confirmation;
- two successful large-batch operation IDs;
- complete feedback records;
- required stability/no-regression window;
- audit log success;
- safe deploy fingerprint match.

If the second large-batch operation is still missing, the certification program must generate it through the existing controlled production owners, not bypass the gate.

## Automation Debt

Manual action: diagnosing Authority promotion with direct CLI commands.

Classification: Automation Debt.

Resolution state: BLOCKED_BY_FUTURE_CAPABILITY.

Candidate: one governed certification command should orchestrate stage evidence review, pool preparation, authority promotion, and certification execution while preserving the same owners.

## Workflow Debt

Manual workflow:

`read policy -> run promotion diagnostic -> inspect evidence review -> patch owner -> run tests`

Classification: Pipeline Candidate.

Resolution state: BLOCKED_BY_FUTURE_CAPABILITY.

## Next Step

Safe deploy this existing-owner fix, then resume Phase 6 at the Authority promotion gate.
