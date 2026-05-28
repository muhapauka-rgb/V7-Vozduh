# Restore Settle Gate Rules

Mode: governance and read-only validation.

## Purpose

E9.4.4 proved that a single clean planner sample before restoring `v7-users-autoswitch.timer` is not enough. The restore gate must prove that autoswitch state stays clean across a window, not just at one instant.

This document defines the required pre-restore and post-restore settle gates.

## Pre-Restore GO

Pre-restore apply authority may be considered for separate approval only when all of the following are true:

| Requirement | Rule |
|---|---|
| Consecutive samples | at least `3` planner-only samples |
| Timer coverage | samples span at least `2` full apply timer intervals |
| Selected moves | every sample has `selected_moves=0` |
| Telegram hard block | every sample has `telegram.hard_blocked=false` |
| Egress 1 eligibility | every sample has `egress_1_eligible=true` when users remain on egress `1` |
| Runtime checks | reconcile, user-route, kill switch, and provisioning checks are OK |
| Hidden movers | no `v7-user-switch` or `v7-routing-sync` process observed |
| Registry stability | `users.registry` hash stable across samples |
| Egress stability | `egress.registry` hash stable across samples |
| Planner output | planner output present and parseable |

Passing this gate does not start apply authority. It only permits a separate operator approval decision for apply restore.

## Pre-Restore NO-GO

Any one of these blocks apply restore:

- any sample has `selected_moves>0`;
- Telegram enters hard-block in any sample;
- egress `1` becomes blocked or ineligible in any sample;
- `users.registry` or `egress.registry` drifts;
- any required runtime checker fails;
- hidden `v7-user-switch` or `v7-routing-sync` appears;
- planner output is missing or unparseable;
- sample window is shorter than required and operator cannot extend it.

## Conditional State

`CONDITIONAL` is allowed only for insufficient sampling with otherwise clean evidence. It means:

```text
extend_sampling_window_before_restore_decision
```

It does not authorize restore.

## Post-Restore Settle GO

After apply authority is restored in a separately approved block, post-restore settle is clean only when:

| Requirement | Rule |
|---|---|
| Observation window | at least `2` full apply timer intervals |
| Movement count | `movement_count=0` for clean restore |
| Autoswitch output | selected moves remain empty or explicitly no-op |
| Runtime checks | reconcile, user-route, kill switch, and provisioning checks are OK |
| Hidden movers | no hidden `v7-user-switch` or `v7-routing-sync` |
| Registry state | registry changes only if separately classified as autoswitch recovery |

## Post-Restore NO-GO

Any timer-driven movement after restore must be classified separately from canary blast radius.

Broad failover, Telegram hard-block recurrence, or registry movement during settle means:

```text
next_canary_readiness=NO-GO
restore_governance_live_proven=false
```

## Movement Budget

Canary blast radius and restore blast radius are separate.

| Window | Allowed movement |
|---|---|
| Canary window | only the explicitly approved candidate user |
| Planner-only restore | none |
| Apply restore | none for clean restore; otherwise exact movement list requires separate approval |
| Post-restore settle | none for clean restore; any movement becomes autoswitch recovery classification |

## Tooling

`tools/v7-restore-settle-gate` implements a read-only checker for saved samples or fixtures.

It must not:

- run `systemctl stop/start/restart`;
- run `v7-users-autoswitch --apply`;
- run `v7-user-switch`;
- run `v7-routing-sync`;
- mutate route, nft, registry, egress, Direct/RU, proxy, kill switch, or runtime files.

## Current E9.4.5 Status

```text
restore_settle_gate_rules_created=true
pre_restore_required_samples=3
required_apply_timer_intervals=2
post_restore_settle_required=true
next_canary_readiness=NO-GO
execution_allowed_now=false
```

## E9.4.6 Fresh Observation Status

E9.4.6 ran a fresh read-only settle observation after the E9.4.4 Telegram hard-block window.

```text
fresh_restore_settle_observation_executed=true
samples_count=3
samples_span_seconds=68
apply_timer_intervals_covered=3.4
selected_moves_all_zero=true
telegram_hard_blocked_seen=false
egress_1_eligible_all_samples=true
users.registry_stable=true
egress.registry_stable=true
runtime_checks_ok=true
new_delayed_movements_observed=false
current_restore_settle_status=GO
restore_governance_live_proven=true_for_fresh_settle_window
execution_allowed_now=false
```

The historical E9.4.3/E9.4.4 delayed movement remains classified separately. E9.4.6 does not authorize canary execution; it reopens the path to a fresh approval packet or target refresh.
