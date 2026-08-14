# BLOCK E25.8 — Replacement Execution Profile Required Report

## Verdict

`e25_8_completed=true`

E25.8 found and tested one plausible external replacement profile, but it did not become usable. The system still needs an operator-provided or provider-repaired external execution profile before the first dedicated-target movement can proceed.

## Final Answers

- `runtime_mutation_performed=true`
- `runtime_mutation_scope=replacement execution profile normalized activation/validation/removal only`
- `user_movement_performed=false`
- `routing_mutation_for_users=false`
- `replacement_candidate_found=true`
- `best_replacement_candidate=/etc/wireguard/vps.conf`
- `best_candidate_protocol=wireguard`
- `existing_dead_profile_reused=false`
- `existing_profile_repair_successful=false`
- `endpoint_self_reference=false`
- `server_side_peer_valid=false`
- `normalized_interface=v7execwg0`
- `handshake_successful=false`
- `rx_packets_present=false`
- `target_connectivity_usable=false`
- `dedicated_execution_target_created=false`
- `target_readiness_final_status=NO-GO`
- `sustained_go=false`
- `no_sample_below_floor=false`
- `candidate_user=10.7.0.11`
- `candidate_still_on_1=true`
- `selected_moves_zero=true`
- `hidden_movers_absent=true`
- `runtime_checkers_ok=true`
- `first_movement_ready=false`
- `recommended_target=NONE`

## What Happened

The failed E25.7 profile was not reused. It remains rejected because its endpoint points back to the VPS itself and no server-side listener/peer was available.

The best replacement candidate was `/etc/wireguard/vps.conf`. It looked structurally safer:

- external endpoint;
- no hooks;
- no DNS side effect;
- normalizable full-tunnel profile.

The profile was quarantined, redacted, normalized with `Table=off`, and activated only as `v7execwg0`.

## Connectivity Result

The replacement profile failed at the WireGuard peer layer:

- endpoint reachable by ICMP;
- UDP endpoint probe reported reachable;
- outbound UDP handshake packet observed;
- no inbound UDP reply captured;
- `latest-handshakes=0`;
- RX remained `0`;
- ping/curl via `v7execwg0` timed out.

Bounded variants also failed:

- `/32` with MTU `1200`;
- `/24` with MTU `1280`;
- `/24` with MTU `1200`.

## Safety Result

No users moved. No user route tables changed. The test interface was removed and active config was archived.

## Remaining Blockers

- `NO_USABLE_REPLACEMENT_EXECUTION_PROFILE`
- `SERVER_SIDE_PEER_INVALID_OR_STALE`
- `NO_HANDSHAKE`
- `NO_RX_PACKETS`
- `NO_DEDICATED_EXECUTION_TARGET_READY`

## Recommended Next Block

`E25_9_OPERATOR_MUST_PROVIDE_EXTERNAL_EXECUTION_PROFILE`

The next profile must be generated from a known-good external provider/server-side peer and should prove handshake/RX in quarantine before it is considered for execution metadata.

## Final Mutation Statement

Runtime mutation performed: YES

If YES: only replacement execution profile activation/validation/removal; no dedicated target metadata was created.

User movement performed: NO

Routing mutation for users performed: NO

Kill switch mutation performed: NO

Autoswitch apply performed manually: NO

Raw unsafe profile executed: NO

Canary performed: NO

Cohort performed: NO
