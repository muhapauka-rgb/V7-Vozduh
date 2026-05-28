# E9.4 Final Gate Decision Reconstruction

Source evidence:
- `docs/track7/control-plane/e9_4-evidence/final-planner-only-gate.txt`
- `docs/track7/control-plane/e9_4-evidence/final-planner-gate-classification.md`
- `docs/track7/control-plane/e9_4_1-evidence/current-post-policy-snapshot.txt`

## Final E9.4 gate result

E9.4 did not restore `v7-users-autoswitch.timer`. The final planner-only gate returned non-zero selected moves and the block aborted before mutation authority was restored.

```text
apply_restore_executed=false
apply_restore_aborted=true
selected_moves_count=3
candidate_moves_total=16
apply_timer_status=held/inactive
```

Selected moves:

| User | From | To | Planner reason | Current route status at gate |
|---|---|---|---|---|
| `10.7.0.5` | `1` | `vless` | `user_frozen_until_2026-05-26T01:00:19.598532+00:00`, `current_egress_not_eligible` | table `1003` default dev `v7e356a192b79`, route check OK |
| `10.0.0.2` | `1` | `vless` | `user_frozen_until_2026-05-26T01:07:39.350594+00:00`, `current_egress_not_eligible` | table `100` default dev `v7e356a192b79`, route check OK |
| `10.0.0.3` | `1` | `vless` | `user_frozen_until_2026-05-26T01:07:39.350692+00:00`, `current_egress_not_eligible` | table `101` default dev `v7e356a192b79`, route check OK |

The freeze reasons were anti-flap/safety annotations. They did not prevent failover in the `not current.eligible` path because the failover branch only gates on cooldown and does not check the `frozen` boolean.

## Exact blocker on egress `1`

In the abort sample, egress `1` was not blocked by the single Instagram sample alone. The egress had a Telegram hard block:

```text
egress=1
eligible=false
blocked=["telegram_required_telegram_down_14s"]
telegram.status=TELEGRAM_DOWN_14S
telegram.hard_blocked=true
telegram.bad_now=true
telegram.bad_for_seconds=49.0
telegram.score=0.0
telegram.reason=api.telegram.org:443=timeout; 149.154.167.50:443=timeout; 149.154.175.50:443=timeout; 91.108.56.177:443=timeout; 194.221.250.50:443=timeout
telegram.source=sentinel
```

The same candidate also showed a non-Telegram service degradation:

```text
service_instagram_degraded
service_instagram_failed_samples_1
service_signal_DEGRADED_SERVICE
route_class_VIDEO_OPTIMIZED_warn
```

That Instagram state is the expected post-policy behavior for a single transient service failure: degraded/penalty-only, not global ineligibility. The actual hard global ineligibility came from Telegram required hard-block semantics.

## Why the E9.3.8 policy fix did not suppress this failover

The deployed policy fix was scoped to suppress broad failover caused only by transient non-Telegram service failures. In source semantics:

- `service_signal_DEGRADED_SERVICE` does not block the candidate.
- `service_multiple_critical_failed` and persistent service failures can still block.
- `telegram_required_<status>` remains a hard block when `telegram.hard_blocked=true`.
- The restore-stage suppression gate only applies when the current candidate is blocked by service-signal-only reasons.

Because `blocked=["telegram_required_telegram_down_14s"]`, `_service_signal_only_block(current)` is false and the restore-stage service-signal suppression is intentionally bypassed.

## Current E9.4.1 snapshot comparison

The later E9.4.1 read-only snapshot shows recovery from the abort condition:

```text
selected_moves=[]
apply_result.applied=false
apply_result.reason=dry_run
egress=1 eligible=true
egress=1 blocked=[]
telegram state seen as degraded/OK, not hard-blocked
```

Current route/control-plane checks remained OK:

```text
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

## Verdict

The E9.4 abort was caused by a transient Telegram hard-block on egress `1`, not by the already-fixed single Instagram service failure class. The policy fix is not proven incomplete for its original target. Apply restore still remains unsafe unless a fresh final planner-only gate returns `selected_moves=0` or the operator explicitly approves the exact autoswitch movement list.

```text
root_cause_classification=TELEGRAM_HARD_BLOCK
confidence=high_for_E9_4_abort_sample
policy_fix_incomplete=false_for_single_non_telegram_service_failure
apply_restore_safe_now=false
apply_should_remain_held=true
```
