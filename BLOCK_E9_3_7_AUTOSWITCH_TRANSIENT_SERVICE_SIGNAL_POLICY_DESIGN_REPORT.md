# BLOCK E9.3.7 - Autoswitch Transient Service Signal Policy Design Report

Mode: read-only / policy design only.
Runtime mutation: no.
Autoswitch apply restore: forbidden.
Canary: forbidden.

## Inputs

E9.3.5 apply-restore execution was aborted before apply restore because planner-only state showed:

```text
selected_moves=3
candidate_moves_total=15
target=vless
reason=current_egress_not_eligible
```

E9.3.6 root cause:

```text
egress_1_ineligibility_root_cause=service_instagram_failed
telegram.status=DEGRADED
telegram.hard_blocked=false
root_cause_classification=MIXED_TRANSIENT_SERVICE_SIGNAL_AND_EXPECTED_FAILOVER_BEHAVIOR
max_failover_behavior_expected=true
apply_restore_safe_now=false
apply_should_remain_held=true
```

## Current Policy Problem

Current autoswitch policy treats non-Telegram service `ok=false` as a hard candidate block. If the blocked candidate is the user's current egress, the decision path marks the user with `current_egress_not_eligible` and enters failover selection.

For a shared egress, this can generate a broad candidate set from one transient service signal.

The current max-failover cap limits per-run movement, but it does not prevent repeated timer runs from continuing the same broad failover over time.

## Proposed Policy Model

Introduce a service-signal confidence layer before global egress ineligibility.

Policy states:

```text
OK
DEGRADED_SERVICE
CONDITIONAL_INELIGIBLE
HARD_INELIGIBLE
```

Single-service transient failure should become:

```text
DEGRADED_SERVICE
penalty_only
global_eligible=true
selected_moves=0
```

Hard global ineligibility should require one of:

- interface down/missing;
- egress disabled/maintenance/quarantine;
- Telegram or sentinel hard-block;
- route-class hard failure;
- repeated service failure across the configured persistence window;
- multiple critical services failing in the same window;
- safety quarantine signal.

## Proposed Defaults

```text
service_failure_persistence_samples=3
service_failure_persistence_window_seconds=180
service_failure_min_critical_count=2
global_ineligibility_confidence_threshold=0.75
current_egress_grace_window_seconds=120
post_restore_apply_suppression_window_seconds=120
max_failover_per_restore_stage=1
service_specific_degradation_mode=penalty_only
```

## E9.3.5 Counterfactual

Given:

```text
instagram failed once
telegram degraded but not hard-blocked
interface and route checks OK
```

Expected under refined policy:

```text
egress_1_state=DEGRADED_SERVICE
egress_1_global_eligible=true
selected_moves=0
candidate_moves_total=0 or warnings only
```

So yes, this policy would have prevented the E9.3.5 broad failover candidate set unless additional persistent/multi-signal evidence existed.

## Restore Implication

`apply_restore_safe_under_current_policy=false`.

The apply timer should remain held under the current policy. A code fix is required before broad unsupervised apply restore can be considered safe. A narrow exception remains possible only if a fresh planner-only sample shows `selected_moves=0` and the operator explicitly approves bounded apply restore for that sample.

## Fixture Tests

Repo-side design tests were added:

```text
tests/unit/test_v7_autoswitch_policy_design.py
```

They verify:

- Instagram single-sample failure is degraded, not hard ineligible;
- persistent Instagram failure becomes conditional ineligible;
- Telegram degraded without hard-block is degraded, not hard ineligible;
- interface down is hard ineligible;
- multiple critical service failures are conditional ineligible;
- restore stage suppresses broad movement without explicit approval.

These tests do not mutate runtime and do not deploy policy.

## Updated Governance

Updated documents:

- `docs/track7/control-plane/AUTOSWITCH_TRANSIENT_SERVICE_SIGNAL_POLICY.md`
- `docs/track7/control-plane/AUTOSWITCH_POLICY_THRESHOLDS_PROPOSAL.md`
- `docs/track7/control-plane/APPLY_RESTORE_APPROVAL_RULES.md`
- `docs/track7/control-plane/STAGED_AUTOSWITCH_RESTORE_MODEL.md`
- `docs/track7/control-plane/CANARY_GO_NO_GO.md`
- `docs/track7/control-plane/CONTROL_PLANE_RISK_MATRIX.md`
- `docs/track7/control-plane/SECOND_CANARY_TARGET_READINESS_RULES.md`
- `tools/v7-control-plane-governance-check`

## Final Answers

```text
current_policy_problem=single transient non-Telegram service failure can hard-block current egress and generate broad failover candidates
proposed_policy_model=service-signal confidence and persistence layer before global ineligibility
code_fix_required_before_apply_restore=true
apply_restore_safe_under_current_policy=false
apply_should_remain_held=true
recommended_next_step=implement bounded repo-side autoswitch policy fix, then rerun planner-only restore sample before any apply restore
execution_allowed_now=false
```

## Verification

```text
tools/v7-run-tests: OK, 56 tests
tools/v7-control-plane-governance-check --pretty: OK
tools/v7-second-canary-target-readiness --pretty: OK, second_canary_readiness=NO-GO
tools/v7-second-canary-target-readiness --json: OK, mutation=false
tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty: OK, runtime_governance=partial
tools/v7-release-lineage-check --release-dir releases/v7-runtime-20260523T174503Z --pretty: OK, release_object ready, provenance incomplete
py_compile admin/tools/governance: OK
git diff --check: OK
```

Expected governance warnings remain:

```text
runtime_manifest_not_supplied
source_worktree_dirty
release_provenance=incomplete
known production-only lineage gaps remain outside E9.3.7 scope
```

## Final Mutation Statement

```text
Runtime mutation performed: NO
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Autoswitch apply timer restored: NO
Canary performed: NO
```
