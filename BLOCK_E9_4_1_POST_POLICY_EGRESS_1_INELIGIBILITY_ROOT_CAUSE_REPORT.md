# Block E9.4.1 Post-Policy Egress 1 Ineligibility Root-Cause Report

## Scope

Mode: read-only / post-policy autoswitch root-cause only.

No apply restore, canary, user-switch, routing-sync, routing mutation, policy apply, Direct/RU mutation, Trusted RU refresh, proxy apply, kill-switch mutation, deploy, or runtime file mutation was performed.

## Evidence

Created/read:

- `docs/track7/control-plane/e9_4_1-evidence/current-post-policy-snapshot.txt`
- `docs/track7/control-plane/e9_4_1-evidence/e9-4-final-gate-decision.md`
- `docs/track7/control-plane/e9_4_1-evidence/egress-1-eligibility-matrix.md`
- `docs/track7/control-plane/e9_4_1-evidence/post-policy-candidate-move-matrix.md`

Referenced prior E9.4 evidence:

- `docs/track7/control-plane/e9_4-evidence/final-planner-only-gate.txt`
- `docs/track7/control-plane/e9_4-evidence/final-planner-gate-classification.md`
- `docs/track7/control-plane/e9_4-evidence/post-abort-safety.txt`

## Current Runtime Authority

```text
v7-health.service=active
v7-autoswitch-planner.timer=active
v7-users-autoswitch.timer=inactive/held
autoswitch apply authority restored=false
execution_allowed_now=false
```

Runtime policy file under review:

```text
runtime_path=/usr/local/bin/v7-users-autoswitch
expected_runtime_policy_hash=d07a045bd9ad8470e872d4774ac776733a2051b36ec60507a6baf6ca9bab454b
```

## E9.4 Final Gate Reconstruction

E9.4 correctly aborted before restoring `v7-users-autoswitch.timer` because the final planner-only gate returned selected moves:

```text
apply_restore_executed=false
apply_restore_aborted=true
candidate_moves_count=16
selected_moves_count=3
selected_moves_summary=10.7.0.5:1->vless,10.0.0.2:1->vless,10.0.0.3:1->vless
reason=current_egress_not_eligible
```

All selected moves were failover candidates from egress `1` to `vless`.

## Post-Policy Egress 1 Root Cause

The post-policy root cause for the E9.4 selected moves was not the single Instagram failure by itself.

The final E9.4 sample showed egress `1` hard-blocked by Telegram:

```text
egress=1
eligible=false
blocked=["telegram_required_telegram_down_14s"]
telegram.status=TELEGRAM_DOWN_14S
telegram.hard_blocked=true
telegram.bad_now=true
telegram.bad_for_seconds=49.0
telegram.score=0.0
telegram.source=sentinel
```

The same candidate also showed:

```text
service_instagram_degraded
service_instagram_failed_samples_1
service_signal_DEGRADED_SERVICE
```

That is the expected E9.3.8/E9.3.9 policy behavior: one non-Telegram transient service failure becomes degraded/penalty-only. It does not globally block the egress.

The decisive hard blocker was:

```text
telegram_required_telegram_down_14s
```

## Why The Policy Fix Did Not Prevent This

The policy fix was designed to prevent broad failover from a single transient non-Telegram service failure. It does that by treating one failed non-Telegram sample as `DEGRADED_SERVICE` rather than hard ineligibility.

Telegram hard-block semantics are separate. In `tools/v7-users-autoswitch`, when Telegram is required and the sentinel says `hard_blocked=true`, the planner blocks the candidate with `telegram_required_<status>`. That is not a service-signal-only block, so the restore-stage service-signal suppression gate does not apply.

Therefore:

```text
policy_fix_incomplete=false_for_original_single_non_telegram_failure_class
telegram_hard_block_behavior=expected_current_policy
```

## Current E9.4.1 State

The later E9.4.1 read-only snapshot shows the transient hard condition had cleared or softened:

```text
selected_moves=[]
apply_result.applied=false
apply_result.reason=dry_run
egress_1_eligible=true
egress_1_blocked=[]
```

Current checks remained OK:

```text
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

This means the E9.4 abort was not evidence of permanent routing breakage or persistent egress `1` ineligibility. It was a real transient autoswitch hard-block state observed at the final gate.

## Classification

```text
post_policy_egress_1_root_cause=telegram_required_telegram_down_14s
root_cause_classification=TELEGRAM_HARD_BLOCK
confidence=high_for_E9_4_abort_sample_medium_for_current_recovered_state
selected_moves_count=3
candidate_moves_count=16
max_failover_behavior_expected=true
```

## Apply Restore Safety

Apply restore is not safe right now as an automatic action, because the last attempted restore gate aborted on non-zero selected moves and this block is read-only only.

The current planner snapshot is improved, but a new live restore attempt must repeat the bounded final planner-only gate immediately before restoring apply authority.

```text
apply_restore_safe_now=false
apply_should_remain_held=true
execution_allowed_now=false
```

## Remediation Path

Recommended next step:

1. Keep `v7-users-autoswitch.timer` held.
2. Treat E9.4.1 as root-cause classification, not apply-restore approval.
3. Next live block should be a fresh bounded E9.4 retry or E9.4.2 approval packet:
   - collect final planner-only gate immediately before restore;
   - proceed only if `selected_moves=0`;
   - otherwise require explicit operator acceptance of the exact movement list.

Optional future design work:

- Add a Telegram hard-block grace/confirmation policy if transient Telegram sentinel hard-blocks are considered too aggressive for restore stages.
- Keep single non-Telegram service failures as penalty-only; no evidence here requires reverting that fix.

## Final Answers

```text
post_policy_egress_1_root_cause=telegram_required_telegram_down_14s
root_cause_classification=TELEGRAM_HARD_BLOCK
confidence=high_for_E9_4_abort_sample_medium_for_current_recovered_state
selected_moves_count=3
candidate_moves_count=16
selected_moves_summary=10.7.0.5:1->vless,10.0.0.2:1->vless,10.0.0.3:1->vless
policy_fix_incomplete=false
apply_restore_safe_now=false
apply_should_remain_held=true
recommended_next_step=keep_apply_timer_held_and_run_fresh_bounded_apply_restore_gate_only_by_separate_approval
execution_allowed_now=false
```

## Mutation Statement

```text
Runtime mutation performed: NO
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Autoswitch apply timer restored: NO
Canary performed: NO
```
