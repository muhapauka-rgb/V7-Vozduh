# Post-Policy Candidate Move Matrix

Evidence sources:
- `docs/track7/control-plane/e9_4-evidence/final-planner-only-gate.txt`
- `docs/track7/control-plane/e9_4-evidence/final-planner-gate-classification.md`
- `docs/track7/control-plane/e9_4_1-evidence/current-post-policy-snapshot.txt`

## E9.4 final planner-only gate

```text
candidate_moves_total=16
selected_moves_count=3
selected_target=vless
reason=current_egress_not_eligible
apply_result.applied=false
```

| User | Current egress | Proposed target | Exact blocker | Selected | Capped by failover limit | Target chosen reason | Safe to apply now? | Rollback/containment implication |
|---|---|---|---|---|---|---|---|---|
| `10.7.0.5` | `1` | `vless` | current egress `1` blocked by `telegram_required_telegram_down_14s`; user also frozen until `2026-05-26T01:00:19.598532+00:00` | yes | yes, part of 3 selected moves | `vless` was best eligible failover target in sample | no | would mutate table `1003`; requires explicit movement approval |
| `10.0.0.2` | `1` | `vless` | current egress `1` blocked by `telegram_required_telegram_down_14s`; user also frozen until `2026-05-26T01:07:39.350594+00:00` | yes | yes, part of 3 selected moves | `vless` was best eligible failover target in sample | no | would mutate table `100`; requires explicit movement approval |
| `10.0.0.3` | `1` | `vless` | current egress `1` blocked by `telegram_required_telegram_down_14s`; user also frozen until `2026-05-26T01:07:39.350692+00:00` | yes | yes, part of 3 selected moves | `vless` was best eligible failover target in sample | no | would mutate table `101`; requires explicit movement approval |
| other enabled users on `1` | `1` | `vless` candidate set | same current-egress hard block inferred from summary `candidate_moves_total=16` | no | yes, not selected by max failover cap | same failover target class | no | apply restore could select more users on later ticks if hard block persisted |

## Target choice

The selected target was `vless` because it was the best eligible failover target in the final E9.4 sample:

- `vless` candidate was eligible.
- egress `1` was rejected for `telegram_required_telegram_down_14s`.
- `awg0` was rejected for stability below floor.
- `awg3` was rejected for min Mbps/stability below floor.
- OpenVPN and WireGuard were rejected for `severity_SUSPECT`.

## Current E9.4.1 planner state

The later E9.4.1 snapshot no longer shows selected moves:

```text
selected_moves=[]
egress_1_eligible=true
egress_1_blocked=[]
```

This means the E9.4 abort sample captured a real but transient hard Telegram/sentinel condition. The apply timer should still remain held until a fresh bounded E9.4-style restore gate is explicitly approved and passes.

## Classification

```text
candidate_moves_count=16
selected_moves_count=3
selected_moves_summary=10.7.0.5:1->vless,10.0.0.2:1->vless,10.0.0.3:1->vless
vless_target_reason=best_eligible_failover_target_when_egress_1_telegram_hard_blocked
max_failover_behavior_expected=true
apply_restore_safe_now=false
apply_should_remain_held=true
```
