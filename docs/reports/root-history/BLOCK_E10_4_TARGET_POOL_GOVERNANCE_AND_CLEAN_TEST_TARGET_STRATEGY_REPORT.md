# V7 Vozduh — BLOCK E10.4 Target Pool Governance and Clean Test Target Strategy

Mode: read-only / strategy + approval design only.

## Executive Truth

E10.4 did not mutate runtime. It converts E10.3 target-pool truth into a strategy.

Current state:

```text
restore_settle_gate_status=GO
clean_zero_user_target_exists=false
selected_target=NONE
second_canary_readiness=NO-GO
execution_allowed_now=false
```

The current blocker is not canary mechanics or restore governance. The blocker is target-pool governance and capacity: there is no clean isolated target for the next canary.

## Target Pool Blocker

```text
target_pool_blocker=no_clean_reserved_zero_user_target
```

Details:

- `target 1` is occupied by six users.
- `awg0` is zero-user but low quality and missing Direct/RU + Trusted RU exclusions.
- `awg3` is zero-user but low quality and missing Direct/RU + Trusted RU exclusions.
- OpenVPN is zero-user but `SUSPECT` and below quality floor.
- WireGuard is zero-user and quality OK, but `SUSPECT` due stale-handshake semantics.
- No target is explicitly reserved from production autoswitch assignment.

## Strategy Decision

Primary next action:

```text
recommended_next_block=E10.5_WIREGUARD_STALE_HANDSHAKE_DIAGNOSTIC_AND_RESERVATION_FEASIBILITY_PACKET
```

Why:

- WireGuard is the best current conditional target.
- It is zero-user.
- It already has `DIRECT_RU` and `TRUSTED_RU_SENSITIVE` exclusions.
- Its quality passes target floor.
- Its only clean-target blocker is `diagnose=SUSPECT` / stale handshake.
- A read-only diagnosis can determine whether the `SUSPECT` state is a false negative, real risk, or waiver candidate.

Fallback:

```text
fallback_strategy=DEDICATED_CANARY_TEST_EGRESS
```

If WireGuard cannot be made clean or waiver-acceptable, the durable solution is a dedicated reserved canary/test egress that autoswitch cannot occupy with production users.

## Option Verdicts

| Option | Verdict | Reason |
|---|---|---|
| Dedicated canary/test egress | Best durable strategy | Creates repeatable isolation and clean attribution. Requires separate provisioning/metadata approval. |
| Temporarily reserve WireGuard | Best short-term path | Zero-user, quality OK, exclusions present; needs stale-handshake diagnosis and reservation approval. |
| Remediate awg0/awg3 | Not immediate | Both fail quality floor and lack exclusions; metadata alone is insufficient. |
| Add new egress capacity | Strong fallback | More work than WireGuard diagnosis, but best long-term if no existing target can be clean. |
| Accept occupied target | Not preferred | Mechanics-only evidence, not clean isolation; weak attribution. |

## Target Reservation Policy

Created:

```text
docs/track7/control-plane/TARGET_RESERVATION_POLICY.md
target_reservation_policy_created=true
```

Core rule:

```text
canary_reserved=true means autoswitch must not assign production users to that target.
```

Clean reserved target requirements:

- zero users by registry and load-state;
- diagnose OK or explicit waiver;
- quality OK;
- Direct/RU and Trusted RU exclusions present;
- rollback clear;
- restore-settle gate GO;
- runtime checks OK.

## Required Answers

```text
clean_zero_user_target_exists=false
target_pool_blocker=no_clean_reserved_zero_user_target
best_strategy=WIREGUARD_DIAGNOSE_THEN_RESERVE_OR_WAIVE
recommended_next_block=E10.5_WIREGUARD_STALE_HANDSHAKE_DIAGNOSTIC_AND_RESERVATION_FEASIBILITY_PACKET
dedicated_canary_target_needed=true
wireguard_waiver_path_recommended=true
awg_quality_remediation_needed=true
target_reservation_policy_created=true
second_canary_readiness=NO-GO
execution_allowed_now=false
```

## Mutation Statement

```text
Runtime mutation performed: NO
User movement performed by this block: NO
Routing mutation performed by this block: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
```

