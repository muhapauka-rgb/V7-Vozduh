# Autoswitch Policy Thresholds Proposal

Status: repo-side defaults implemented in E9.3.8; runtime deploy not performed.
Scope: autoswitch service-signal refinement.
Runtime mutation: no.

## Proposed Knobs

| Knob | Proposed Default | Purpose |
|---|---:|---|
| `service_failure_persistence_samples` | `3` | Require repeated non-Telegram service failures before global ineligibility |
| `service_failure_persistence_window_seconds` | `180` | Window for repeated samples |
| `service_failure_min_critical_count` | `2` | Require at least two critical services failing for immediate conditional ineligibility |
| `hard_block_required_signals` | `interface_down,egress_disabled,egress_quarantine,telegram_hard_block,route_class_fail` | Signals that can still hard-block immediately |
| `per_service_penalty_weight` | `80` | Score penalty for one failed non-Telegram service |
| `telegram_degraded_penalty_weight` | `120` | Existing soft Telegram penalty preserved |
| `global_ineligibility_confidence_threshold` | `0.75` | Minimum confidence before current egress can become globally ineligible from service failures |
| `current_egress_grace_window_seconds` | `120` | Do not failover current egress on first transient service failure |
| `post_restore_apply_suppression_window_seconds` | `120` | After apply timer restore, suppress broad service-signal failover unless hard transport failure exists |
| `max_failover_per_restore_stage` | `1` | Stricter movement cap during supervised restore stage |
| `service_specific_degradation_mode` | `penalty_only` | Default action for single-service failures |

## Service Signal Classes

| Signal | Default Class | Default Effect |
|---|---|---|
| `instagram ok=false` single sample | soft | Penalty, warning, no global failover |
| `telegram DEGRADED` not hard-blocked | soft | Existing Telegram penalty, no global failover |
| `google_auth ok=false` single sample | soft-high | Larger penalty, no global failover without persistence |
| `youtube ok=false` single sample | soft | Penalty, no global failover |
| multiple critical service failures | conditional | Planner may propose movement; apply requires approval if restore stage |
| repeated same service failure across N samples | conditional | Limited movement allowed after confidence threshold |
| interface down/missing | hard | Immediate failover eligible |
| egress disabled/maintenance/quarantine | hard | Immediate failover eligible |
| Telegram hard-blocked | hard for Telegram-required class | Failover eligible for affected class |
| route class fitness FAIL | hard for that route class | Failover eligible for affected class |

## Confidence Calculation

Suggested minimum model:

```text
confidence = 0
+ 0.20 if service failed once
+ 0.20 for each repeated failure in window, capped at 0.60
+ 0.25 if two or more critical services fail
+ 0.50 if transport/interface failure
+ 0.50 if sentinel hard-block
+ 0.30 if quality history trend is degrading
- 0.25 if route/user/checkers are OK
```

Global ineligibility from service signals requires:

```text
confidence >= global_ineligibility_confidence_threshold
```

Transport hard failures bypass the confidence threshold.

## Restore-Stage Defaults

During staged apply restore:

```text
post_restore_apply_suppression_window_seconds=120
max_failover_per_restore_stage=1
service_specific_degradation_mode=penalty_only
require_operator_approval_for_service_signal_failover=true
```

The restore stage should not convert a single service failure into multiple user movements.

## Expected E9.3.5 Behavior Under Proposal

Given:

```text
service_instagram_failed=true
telegram=DEGRADED
telegram.hard_blocked=false
interface=up
checkers=OK
```

Expected:

```text
egress_1_global_eligibility=ELIGIBLE
egress_1_service_state=DEGRADED_SERVICE
selected_moves=0
apply_restore_not_blocked_by_broad_failover
```

If Instagram failure persists for three samples or combines with another critical service failure, status becomes:

```text
egress_1_global_eligibility=CONDITIONAL_INELIGIBLE
apply_restore_requires_explicit_movement_approval
```

## Compatibility

This proposal does not remove current movement caps. It adds an eligibility confidence layer before failover selection.

It is compatible with:

- staged restore governance
- planner-only observation
- max failover limits
- anti-flap/cooldown
- route-class exceptions
- Telegram sentinel hard-block semantics

## E9.3.8 Implementation Status

Repo source `tools/v7-users-autoswitch` now includes these defaults as `DEFAULT_SERVICE_SIGNAL_POLICY`.

Runtime `/usr/local/bin/v7-users-autoswitch` was not deployed in E9.3.8.

Operational implication:

```text
apply_restore_safe_after_repo_fix=false_until_runtime_deploy_and_post_deploy_planner_proof
apply_timer_should_remain_held=true
execution_allowed_now=false
```

## E9.3.9 Runtime Deploy Status

Runtime `/usr/local/bin/v7-users-autoswitch` now contains the E9.3.8 threshold model.

```text
runtime_policy_deployed=true
runtime_policy_hash=d07a045bd9ad8470e872d4774ac776733a2051b36ec60507a6baf6ca9bab454b
post_deploy_selected_moves=[]
post_deploy_apply_result=no_selected_moves
apply_timer_should_remain_held=true
execution_allowed_now=false
```

Threshold behavior is now present in runtime, but apply restore is still a separate approval stage.

## E9.4.1 Threshold Interpretation

E9.4.1 confirmed the threshold model behaved as designed for the single Instagram failure class:

```text
service_instagram_failed_samples_1 -> DEGRADED_SERVICE
global_ineligibility_from_instagram=false
```

The E9.4 selected moves came from a separate hard signal:

```text
telegram_required_telegram_down_14s
telegram.hard_blocked=true
```

No threshold change is required for the original E9.3.8 fix. A separate design decision would be needed if Telegram hard-blocks should gain a restore-stage grace or confirmation window.

```text
policy_fix_incomplete=false
apply_restore_safe_now=false
apply_timer_should_remain_held=true
execution_allowed_now=false
```
