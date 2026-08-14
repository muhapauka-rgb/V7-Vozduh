# WG Canary Root Cause Report

Project: V7 Vozduh

Program: WG_CANARY_FORENSICS

Mode: READ ONLY

Date: 2026-06-13

## Executive Summary

Channel:

`wireguard-1779454504-c43409`

is excluded from production routing because it is intentionally marked:

```text
canary_reserved=true
```

and `tools/v7-users-autoswitch` hard-blocks canary-reserved channels as production destinations with:

```text
canary_reserved_production_assignment_blocked
```

The channel is not excluded because it is unhealthy.

Current evidence says it is healthy:

```text
service_score=100.0
stability=0.859072
samples=30
users=0
manual_only=0
reserve_only=0
role=GLOBAL_FAST
```

Final answer:

This is an intentional governance reservation that may now be stale relative to the current BA.3/autonomy goals, but it is not stale in code. The code is enforcing exactly what the registry says.

## 1. Channel Registry

Current production registry row from captured production state:

```text
id=wireguard-1779454504-c43409
protocol=wireguard
type=interface
interface=v7e06a394c478
test=interface
enabled=1
config=/etc/wireguard/v7e06a394c478.conf
role=GLOBAL_FAST
priority=20
weight=100
soft_limit=1
hard_limit=2
manual_only=0
reserve_only=0
service_tags=google,telegram,instagram,global
exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
canary_reserved=true
reservation_reason=second_canary_target
reservation_owner=control_plane_governance
```

Meaning:

- channel is enabled;
- channel is not manual-only;
- channel is not reserve-only;
- channel is otherwise a normal `GLOBAL_FAST` production-capable channel;
- the special blocker is only `canary_reserved=true`.

## 2. Channel Metadata

Important metadata:

| Field | Value | Meaning |
| --- | --- | --- |
| `role` | `GLOBAL_FAST` | normal global routing role |
| `priority` | `20` | high-priority pool candidate |
| `weight` | `100` | strong ranking weight |
| `soft_limit` | `1` | cautious capacity |
| `hard_limit` | `2` | maximum load without capacity change |
| `manual_only` | `0` | not manually restricted |
| `reserve_only` | `0` | not reserve-only |
| `canary_reserved` | `true` | production assignment blocked |
| `reservation_reason` | `second_canary_target` | reserved for canary/testing |
| `reservation_owner` | `control_plane_governance` | governance owns the reservation |

The channel id contains timestamp `1779454504`, which maps to:

```text
2026-05-22T12:55:04Z
```

So the channel itself appears to be from the May 22 channel-import/provisioning period, before the later E10/E11 reservation decisions.

## 3. Channel Role And Labels

The role is not the blocker.

```text
role=GLOBAL_FAST
service_tags=google,telegram,instagram,global
```

This role would normally allow the planner to consider it.

The labels also include route exclusions:

```text
exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
```

That is good hygiene, not a production-pool block.

## 4. Channel State

Current captured stability state:

```text
wireguard-1779454504-c43409_avg_mbps=55.0827
wireguard-1779454504-c43409_min_mbps=47.32
wireguard-1779454504-c43409_stability=0.859072
wireguard-1779454504-c43409_samples=30
```

Current TRANSPORT.1 comparison:

```text
avg = 55.3763 Mbps
floor = 47.32 Mbps
stability = 0.8545
```

This is far above the current stability floor:

```text
0.45
```

Current EGRESS.1/STABILITY evidence also classified it as:

```text
healthy but canary-reserved
```

## 5. Channel Policy

The production policy block is implemented in `tools/v7-users-autoswitch`.

The registry parser loads:

```python
canary_reserved=bool_value(meta.get("canary_reserved") or reg.get("canary_reserved"))
```

The reservation gate then applies:

```python
if not egress.canary_reserved:
    return
if purpose == "current" and user.current == egress.id:
    candidate.reasons.append("canary_reserved_current_requires_separate_drain_approval")
    return
self._block(candidate, "canary_reserved_production_assignment_blocked")
```

The load pool also excludes it:

```python
if egress.canary_reserved:
    return False
```

So there are two enforcement points:

1. It cannot become a production destination candidate.
2. It is not counted as a healthy production load-pool member.

## 6. Governance Restrictions

The owner is explicit:

```text
reservation_owner=control_plane_governance
```

The reason is explicit:

```text
reservation_reason=second_canary_target
```

This means the block is not accidental.

It came from the earlier control-plane governance track where WireGuard was selected as a clean second canary target.

## 7. Creation History

The channel existed before reservation as a WireGuard candidate.

Earlier findings:

- E10.3 found `wireguard-1779454504-c43409` was zero-user and quality OK, but diagnose was still `SUSPECT`.
- E11.1 classified WireGuard as the best current target path, with stale-handshake-only diagnose semantics.
- E11.2 previewed adding:

```text
canary_reserved=true
reservation_reason=second_canary_target
reservation_owner=control_plane_governance
```

At that point the goal was not normal production routing. The goal was preserving a clean canary target.

## 8. Assignment History

E11.8 found that `canary_reserved=true` existed but was not yet fully consumed by autoswitch.

E11.8 fixed this by enforcing the reservation in `v7-users-autoswitch`.

E11.8 also deliberately did not auto-drain existing users.

E11.9 then drained exactly 10 users from WireGuard:

```text
10.7.0.4
10.7.0.6
10.7.0.8
10.7.0.9
10.7.0.10
10.7.0.11
10.7.0.12
10.7.0.13
10.7.0.14
10.7.0.15
```

After E11.9:

```text
wireguard_users_after=0
reservation_enforced_after=true
reassignment_back_to_wireguard_observed=false
target_readiness_after=GO
second_canary_readiness_after=GO
```

So current exclusion is the intended post-drain state: keep the channel clean.

## 9. Canary Flags

The effective canary flags are:

```text
canary_reserved=true
reservation_reason=second_canary_target
reservation_owner=control_plane_governance
```

The key flag is `canary_reserved`.

That one flag is enough to trigger:

```text
canary_reserved_production_assignment_blocked
```

## 10. Reserve Flags

The normal reserve/manual flags are not blocking it:

```text
manual_only=0
reserve_only=0
```

This is important.

The channel is not a generic reserve channel.

It is a governance-reserved canary channel.

## 11. Production Pool Flags

The channel does not explicitly deny production assignment with a separate field like:

```text
production_assignment_allowed=false
```

Instead, production assignment is denied by:

```text
canary_reserved=true
```

This is the production-pool control flag for canary reservation.

## 12. Who Blocks It

Two owners participate:

1. `control_plane_governance`
   - owns the reservation in `egress.registry`;
   - reason: `second_canary_target`.

2. `tools/v7-users-autoswitch`
   - consumes the reservation;
   - blocks destination eligibility;
   - excludes it from healthy production load pool.

## 13. Where It Is Blocked

Primary source of truth:

```text
/opt/v7/egress/state/egress.registry
```

Repository implementation:

```text
tools/v7-users-autoswitch
```

Relevant gates:

- `_gate_reservation`
- `_healthy_for_load`

Tests also certify this behavior:

- `tests/unit/test_best_available_pool_policy.py`
- `tests/unit/test_v7_users_autoswitch_policy.py`
- `tests/unit/test_service_aware_policy.py`

The tests explicitly expect canary-reserved channels to remain blocked for production assignment.

## 14. Why It Is Blocked

Original reason:

The channel was selected as a clean second canary target.

The reservation was meant to prevent autoswitch from placing normal production users onto it while canary/governance work needed a clean target.

The rule is conservative:

```text
canary target must not silently become production failover/rebalance target
```

That was correct at the time because previous evidence showed autoswitch could occupy test targets unless explicitly blocked.

## 15. Since When

Timeline:

| Date / Block | Event |
| --- | --- |
| `2026-05-22T12:55:04Z` | channel id timestamp suggests channel creation/import period |
| E10.3 | WireGuard identified as zero-user, quality OK, conditional target |
| E11.1 | WireGuard classified as best target path with stale-handshake-only issue |
| E11.2 | reservation metadata previewed: `canary_reserved=true` |
| E11.8 | reservation enforcement fixed in `v7-users-autoswitch` |
| E11.9 | 10 existing users drained; WireGuard became zero-user clean target |
| Current | still zero-user, healthy, blocked only by canary reservation |

## 16. Is It Intentional?

Yes.

It is intentional in three layers:

1. registry metadata says it is reserved;
2. autoswitch code enforces the reservation;
3. unit tests protect that behavior.

## 17. Is It Stale?

Technically:

```text
stale=false
```

The system is doing what the current registry says.

Operationally:

```text
possibly_stale_for_current_phase=true
```

The original reason was second-canary isolation. The project has since moved through much larger execution/autonomy tracks. Therefore the reservation may no longer match the current objective, but it must be removed only through an explicit governance decision.

It should not be silently removed by planner or autoswitch.

## 18. Would It Become Eligible If Canary Flag Removed?

Yes, based on current captured evidence.

If this field were removed:

```text
canary_reserved=true
```

then the known remaining production-pool checks look favorable:

| Check | Current value | Pass if flag removed? |
| --- | --- | --- |
| enabled | `1` | yes |
| role | `GLOBAL_FAST` | yes |
| manual_only | `0` | yes |
| reserve_only | `0` | yes |
| users | `0` | yes |
| service score | `100.0` | yes |
| Telegram | OK | yes |
| stability | `0.859072` | yes |
| health severity | OK in recent evidence | yes |
| route exclusions | `TRUSTED_RU_SENSITIVE,DIRECT_RU` | yes |

Caveat:

It has `soft_limit=1` and `hard_limit=2`, so it should not be treated as a large-capacity target without a separate capacity review.

## 19. Would Planner Then Have More Than One Healthy Channel?

Yes.

Current healthy production pool effectively has:

```text
vless
```

WireGuard is healthy but blocked.

If `canary_reserved=true` were removed and all current health values remain the same, the planner would have at least:

```text
vless
wireguard-1779454504-c43409
```

So:

```text
planner_would_have_more_than_one_healthy_channel=true
```

But:

```text
BA3_five_user_capacity_not_automatically_solved=true
```

because WireGuard currently has:

```text
soft_limit=1
hard_limit=2
```

It can improve channel diversity, but it does not by itself prove 5-user autonomy capacity.

## 20. Final Verdict

Final answers:

```text
channel=wireguard-1779454504-c43409
blocked_by=canary_reserved
block_reason=canary_reserved_production_assignment_blocked
block_owner=control_plane_governance + tools/v7-users-autoswitch
block_location=egress.registry + _gate_reservation + _healthy_for_load
health_block=false
policy_block=true
governance_block=true
manual_only=false
reserve_only=false
production_assignment_block_intentional=true
technically_stale=false
possibly_stale_for_current_phase=true
eligible_if_canary_removed=true
planner_healthy_channels_if_removed=>1
ba3_capacity_fully_solved_by_removal=false
```

Plain Russian summary:

WireGuard здоровый, но он специально припаркован как canary/test target. Его не пускает не качество и не planner, а governance-флаг `canary_reserved=true`. Если этот флаг снять, он почти наверняка станет вторым здоровым каналом в production pool, но из-за `soft_limit=1 hard_limit=2` это не означает автоматическую готовность к 5 пользователям.

Safe next step:

```text
WG_CANARY_DERESERVATION_GOVERNANCE_REVIEW
```

That review should decide one thing:

Can `wireguard-1779454504-c43409` be promoted from reserved canary target back into the normal production pool?
