# BLOCK E11.16 Post-TTL Barrier Expiry and Generation Governance Report

block=E11.16
mode=LARGE_MULTI_THEORY_POST_TTL_GOVERNANCE_VALIDATION_AND_BOUNDED_FIX
canary_performed=false
cohort_execution_performed=false

## Executive Verdict

E11.16 found that the live barrier had not expired yet, so an actual live
post-TTL timer observation could not be performed truthfully inside the current
bounded window. The barrier had `81917` seconds remaining at the fresh snapshot.

To avoid mutating TTL or waiting indefinitely, E11.16 ran a counterfactual
expired-barrier dry-run on a temporary copy of live runtime state. That proved
post-TTL apply would regenerate movement pressure: `candidate_moves_total=4`
and `selected_moves=3` before the fix. The selected users were `10.7.0.11`,
`10.7.0.12`, and `10.7.0.14`; `10.7.0.15` was an additional switch decision.

Therefore barrier expiry was not safe as an authorization boundary. A bounded
runtime fix was deployed: expired restore barriers now fail closed until an
explicit generation/clearance marker is present.

## Final Answers

post_ttl_behavior_safe=true
barrier_expiry_safe=true
delayed_movement_after_ttl_observed=false
generation_governance_required=true
generation_fix_executed=true
apply_timer_final_state=held
runtime_checks_ok=true
regressions_observed=false
mini_cohort_readiness_after=CONDITIONAL
larger_cohort_readiness_after=NO-GO
unattended_apply_lifecycle_status=CONDITIONAL_WITH_GENERATION_GOVERNANCE
recommended_next_block=E11.17_GENERATION_CLEARANCE_REHEARSAL_OR_MINI_COHORT_PROMOTION_PACKET
execution_allowed_now=false

## Fix

fix_path_selected=RESTORE_BARRIER_POST_TTL_FAIL_CLOSED_CLEARANCE
runtime_fix_executed=true
rollback_performed=false

Runtime deploy:

- backup: `/usr/local/bin/v7-users-autoswitch.e11_16_backup_20260527T121213Z`
- previous SHA: `10e87444c6f522bdeca0a3d21f02e8819e6d4f5797653546deeb89f92bed0e60`
- installed SHA: `8a7b745e23e9ebe2031322440df5c6dfd22c1a4921a913ad2e5c1159fc9182f2`

New semantics:

- active barrier suppresses failover;
- expired uncleared barrier also suppresses failover;
- post-TTL failover requires explicit governed clearance through `cleared=true`,
  `allow_post_ttl_apply=true`, or `generation_clearance=true`;
- suppression reason after TTL is
  `restore_barrier_post_ttl_generation_clearance_required`.

## Evidence Verdict

Before fix, copied live-state expired-barrier dry-run:

```text
candidate_moves_total=4
selected_moves=3
selected_users=10.7.0.11,10.7.0.12,10.7.0.14
```

After fix, copied live-state expired-barrier dry-run:

```text
post_ttl_blocking=true
failover_quarantine=true
candidate_moves_total=0
selected_moves=0
```

Final live sanity:

```text
v7-users-autoswitch.timer=inactive
users.registry hash stable
egress.registry hash stable
switch-history count=2698
selected_moves=0
runtime checks OK
hidden movers absent
```

## Tests

mandatory_tests_completed=true

- `tools/v7-run-tests`: PASS, 90 tests.
- targeted reservation / diagnose / autoswitch policy / restore barrier /
  restore-settle / target-readiness / generation tests: PASS, 41 tests.
- `tools/v7-control-plane-governance-check --pretty`: PASS.
- `tools/v7-second-canary-target-readiness --pretty`: PASS, GO.
- `tools/v7-second-canary-target-readiness --json`: PASS, GO.
- `tools/v7-restore-settle-gate --pre-restore --pretty`: PASS, GO.
- `tools/v7-restore-settle-gate --pre-restore --json`: PASS, GO.
- runtime/repo diff and release lineage: PASS with known warnings.
- `py_compile`, `bash -n`, and `git diff --check`: PASS.

Detailed test summary:
`docs/track7/control-plane/e11_16-evidence/tests/mandatory-test-summary.md`.

## Final Mutation Statement

Runtime mutation performed: YES
Runtime mutation scope: bounded `/usr/local/bin/v7-users-autoswitch` generation-clearance fail-closed fix only.
User movement performed by this block: NO
Routing mutation performed by this block: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
