# BLOCK E25.7 CONTINUATION — Dedicated Profile Connectivity And Usability Report

## Verdict

`e25_7_continuation_completed=true`

The normalized activation pipeline remains safe, but the candidate profile is not usable. The blocker is target-local WireGuard connectivity, not governance.

## Final Answers

- `runtime_mutation_performed=true`
- `runtime_mutation_scope=dedicated execution target activation/remediation/removal only`
- `user_movement_performed=false`
- `routing_mutation_for_users=false`
- `candidate_user=10.7.0.11`
- `candidate_still_on_1=true`
- `normalized_interface=v7execwg0`
- `connectivity_root_cause=STALE_SERVER_PEER_OR_DEAD_PROFILE`
- `connectivity_fix_attempted=true`
- `connectivity_fix_successful=false`
- `handshake_successful=false`
- `rx_packets_present=false`
- `target_connectivity_usable=false`
- `table_off_enforced=true`
- `dns_side_effect_blocked=true`
- `global_route_side_effects_prevented=true`
- `target_readiness_final_status=NO-GO`
- `target_diagnose=FAIL_CONNECTIVITY`
- `target_load=UNKNOWN_NOT_USABLE`
- `dedicated_target_sustained_go=false`
- `quality_spikes_detected=false`
- `selected_moves_zero=true`
- `hidden_movers_absent=true`
- `runtime_checkers_ok=true`
- `first_movement_ready=false`

## Key Findings

The profile endpoint points back to the VPS public IP. Runtime routing treats that endpoint as local through `lo`.

No active listener was found on the profile endpoint port `51889`. Existing WireGuard listening ports did not include `51889`.

The interface could transmit but never received traffic:

- `latest-handshakes=0`
- RX stayed `0 B`
- TX increased during probes
- ping/curl through `v7execwg0` failed

Bounded remediation did not help:

- keepalive refresh failed;
- MTU `1200` failed;
- temporary target-local route table `1250` failed and was removed.

## Safety Result

No user moved. No user route table changed. The candidate stayed on egress `1`. The runtime remained clean after interface removal.

## Tests

- py_compile: PASS after redirecting pycache to `/tmp`
- targeted operator/endpoint tests: PASS, 18 tests
- full unittest discover: PASS, 116 tests
- endpoint inventory: PASS
- credential scan: PASS, only redacted placeholders found
- dangerous-call scan: PASS with expected evidence references only
- `git diff --check`: PASS

## Remaining Blockers

- `EXECUTION_PROFILE_UNUSABLE`
- `NO_HANDSHAKE`
- `NO_RX_PACKETS`
- `MISSING_OR_STALE_SERVER_SIDE_PEER`
- `NO_DEDICATED_EXECUTION_TARGET_READY`

## Recommended Next Block

`E25_8_REPLACEMENT_EXECUTION_PROFILE_REQUIRED`

The next step should acquire a genuinely external, server-side-valid outbound execution profile. Reusing this profile is unsafe unless the provider/server-side peer is repaired and proves handshake/RX before import.

## Final Mutation Statement

Runtime mutation performed: YES

If YES: only dedicated execution target activation/remediation/removal.

User movement performed: NO

Routing mutation for users performed: NO

Kill switch mutation performed: NO

Autoswitch apply performed manually: NO

Raw unsafe profile executed: NO

Canary performed: NO

Cohort performed: NO
