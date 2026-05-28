# BLOCK E11.9 Bounded WireGuard Reserved Target Drain And Clean Target Recovery Report

## Summary

E11.9 drained the existing production users from the reserved WireGuard target after E11.8 proved new production assignment was blocked.

The safest model was a sequential manual bounded drain of exactly the 10 users still on `wireguard-1779454504-c43409` to target `1`. The apply timer was held only during the drain window to prevent concurrent timer-driven movement, then restored after a clean post-drain planner gate.

Post-drain observation showed WireGuard stayed empty, autoswitch selected no moves, and all runtime checkers stayed OK.

## Required Answers

drain_executed=true

rollback_performed=false

drained_users=10.7.0.4,10.7.0.6,10.7.0.8,10.7.0.9,10.7.0.10,10.7.0.11,10.7.0.12,10.7.0.13,10.7.0.14,10.7.0.15

drain_model_selected=sequential_manual_bounded_drain_with_apply_timer_held

wireguard_users_after=0

reservation_enforced_after=true

reassignment_back_to_wireguard_observed=false

delayed_movements_observed=false

restore_settle_gate_status=GO_POST_DRAIN_SELECTED_MOVES_ZERO_AND_THREE_CLEAN_OBSERVATION_SAMPLES

runtime_checks_ok=true

target_readiness_after=GO

selected_target_after=wireguard-1779454504-c43409

second_canary_readiness_after=GO

clean_target_recovered=true

recommended_next_block=E11.10_FRESH_SECOND_CANARY_APPROVAL_PACKET_AFTER_CLEAN_TARGET_RECOVERY

execution_allowed_now=false

## Drain Execution

Approved drain scope:

- `10.7.0.4`
- `10.7.0.6`
- `10.7.0.8`
- `10.7.0.9`
- `10.7.0.10`
- `10.7.0.11`
- `10.7.0.12`
- `10.7.0.13`
- `10.7.0.14`
- `10.7.0.15`

Destination:

- target `1`
- interface `v7e356a192b79`

Every switch completed with `switch_rc=0`. For each user, `users.registry`, route table default route, and `ip route get` converged to target `1`.

## Verification

Pre-drain:

- selected moves: `0`
- hidden movers: none
- runtime checkers: OK
- WireGuard users: `10`

Post-drain:

- WireGuard users: `0`
- selected moves: `0`
- apply timer restored after clean gate
- observation samples A/B/C: WireGuard users stayed `0`
- runtime checkers stayed OK

Target readiness using the post-drain runtime snapshot:

- `selected_target=wireguard-1779454504-c43409`
- `target_readiness_after=GO`
- `second_canary_readiness_after=GO`

## Final Mutation Statement

Runtime mutation performed: YES — limited to temporary autoswitch apply hold/restore plus exact bounded drain execution.

User movement performed by this block: YES — `10.7.0.4`, `10.7.0.6`, `10.7.0.8`, `10.7.0.9`, `10.7.0.10`, `10.7.0.11`, `10.7.0.12`, `10.7.0.13`, `10.7.0.14`, `10.7.0.15`.

Routing mutation performed by this block: YES — only route tables `1002`, `1004`, `1006`, `1007`, `1008`, `1009`, `1010`, `1011`, `1012`, `1013` for the drained users.

Kill switch mutation performed: NO

Autoswitch apply performed manually: NO

Canary performed: NO
