# E11.12 Target Capacity Analysis

target_capacity_analysis_completed=true
execution_allowed_now=false
selected_target=wireguard-1779454504-c43409

## Fresh Target State

```text
wireguard_reserved=true
wireguard_users=0
wireguard_soft_limit=1
wireguard_hard_limit=2
wireguard_load_status=OK
target_readiness=GO
restore_settle_gate=GO
selected_moves=0
```

Readiness quality for the selected target:

```text
diagnose=OK
avg_mbps=23.888
min_mbps=13.414
stability=0.5442
```

## Capacity Rule

WireGuard has `soft_limit=1` and `hard_limit=2`.

| Cohort size | Result |
| --- | --- |
| 1 user | below hard limit, reaches soft-limit threshold |
| 2 users | exactly equals hard limit, allowed only as bounded first mini-cohort |
| 3 users | exceeds hard limit, forbidden |

target_capacity_safe=true
capacity_safe_scope=exactly_2_users_max
three_user_cohort_allowed=false

## Autoswitch Interaction

Production autoswitch still treats `canary_reserved=true` as a production
assignment hard-block. The selected target is available only through a future
explicit governance movement manifest. E11.12 does not run that manifest.

```text
production_assignment_to_reserved_target=blocked
manual_future_movement_requires_separate_block=true
autoswitch_apply_performed=false
```

## Rollback Load

Both selected users currently live on target `1`. Rollback returns them to the
same target and restores the pre-cohort user distribution:

```text
10.7.0.11 rollback_target=1
10.7.0.12 rollback_target=1
rollback_net_effect=restore_original_state
```

The shared rollback target is an operational risk because target `1` currently
carries most production users, but rollback does not add new net load relative
to the pre-cohort state. This risk is acceptable only with staggered forward
movement, per-user verification, and immediate rollback on partial failure.

## Verdict

safe_capacity_verdict=CONDITIONAL_GO_FOR_EXACT_TWO_USER_PACKET_ONLY

The WireGuard target can safely support the first mini-cohort only at exactly
two users maximum. A three-user cohort is prohibited.
