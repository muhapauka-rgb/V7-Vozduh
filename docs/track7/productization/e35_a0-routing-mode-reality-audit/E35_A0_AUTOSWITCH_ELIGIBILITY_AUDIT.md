# E35.A0 Autoswitch Eligibility Audit

## Question

What controls whether autoswitch can select or move a user/channel today?

## Existing Eligibility Controls

Autoswitch eligibility exists and is significant.

Primary implementation:

```text
tools/v7-users-autoswitch
```

## Hard Blocking Gates

### Basic Channel Gates

Implemented in `_gate_basic`:

| Condition | Block Reason |
|---|---|
| egress disabled | `egress_disabled` |
| egress state maintenance/disabled/quarantine | `egress_state_*` |
| channel `manual_only` | `manual_only` |
| non-200 health code | `health_code_*` |
| severity not OK/WARN | `severity_*` |
| hard full in static mode | `hard_full` |
| reserve only for planned movement | `reserve_only` |

### Reservation Gates

Implemented in `_gate_reservation`:

| Condition | Block Reason |
|---|---|
| `canary_reserved` target for non-current assignment | `canary_reserved_production_assignment_blocked` |

Current canary-reserved target can be held only when it is already current.

### Group / Organization Gates

Implemented in `_gate_org`:

| Condition | Block Reason |
|---|---|
| egress not in group allowed pool | `not_in_group_allowed_pool` |
| egress excluded by group policy | `excluded_by_group_policy` |
| egress exclusive to another group | `exclusive_to_<group>` |
| egress ACL does not include user group | `not_in_egress_group_acl` |
| exclusive isolation conflict | `egress_in_use_by_other_group` |

Group `preferred_egress` is not a hard gate; it adds a reason and score preference.

### Quality Gates

Implemented in `_gate_quality`:

| Condition | Default / Meaning | Block Reason |
|---|---|---|
| avg Mbps below floor | default 15.0 | `avg_mbps_below_floor` |
| min Mbps below floor | default 10.0 | `min_mbps_below_floor` |
| stability below floor | default 0.45 | `stability_below_floor` |

### Service Gates

Implemented in `_gate_service` and `_gate_service_failures`:

| Condition | Impact |
|---|---|
| Trusted RU route class requires trusted RU metadata | hard block |
| Telegram hard-blocked when required | hard block |
| Multiple critical service failures | hard block |
| Persistent required service failure | hard block |
| Non-persistent single service failure | degraded reason, not immediate hard block |
| route class fitness FAIL | hard block |

### Load Gates

Implemented in `_gate_load`:

| Condition | Block Reason |
|---|---|
| failover users >= failover hard limit | `failover_full` |
| planned users >= hard limit | `planned_hard_full` |

### Safety Gates

Implemented in `_gate_safety`:

| Condition | Block Reason |
|---|---|
| target in safety quarantine | `egress_safety_quarantine` |
| failed verifications exceed limit | `egress_failed_verifications_limit` |
| target blocked for user | `target_blocked_for_user` |
| pair reversal in stability window | `pair_reversal_stability_window` |

## Admin Eligibility Surface

Admin exposes channel-level controls:

```text
Система может выбирать этот канал
Резервный канал
Лимит пользователей
Приоритет
Вес
Эксклюзивная группа
```

These write org egress policy metadata such as:

```text
manual_only
reserve_only
capacity_users
priority
weight
groups
exclusive_group
```

## Execution-Only Target Eligibility

Execution-only targets are expected to be isolated from autoswitch:

```text
autoswitch_allowed=false
rebalance_allowed=false
production_assignment_allowed=false
manual_only=1
reserve_only=1
```

Readiness tests reject an execution-only target with `autoswitch_allowed=true`.

## Verdict

```text
autoswitch_eligibility_controls_exist=true
channel_level_eligibility_exists=true
group_level_eligibility_exists=true
execution_target_autoswitch_exclusion_exists=true
per_user_autoswitch_exclusion_found=false
```

## E35.A Implication

E35.A should reuse these gates as admission checks, but must add explicit user-level ownership/mode controls before autonomous execution authority is expanded.
