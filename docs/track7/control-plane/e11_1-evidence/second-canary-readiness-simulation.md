# E11.1 Second Canary Readiness Simulation

Mode: read-only simulation only. No canary, user-switch, reservation, or route mutation was performed.

## Simulated Preconditions

```text
wireguard_reserved=true
restore_settle_gate_status=GO
runtime_checks_ok=true
wireguard_zero_user=true
wireguard_quality_ok=true
wireguard_exclusions_present=true
selected_moves=0
hidden_user_switch=false
hidden_routing_sync=false
```

## Expected Candidate

Current strict readiness tooling still uses:

```text
candidate_user=10.7.0.14
current_egress=vless
rollback_target=vless
table=1012
```

E10 fresh planning previously selected `10.7.0.11`. A future canary approval packet should choose the candidate fresh at execution-planning time. Either candidate remains one-user if still enabled, stable, and on `vless`.

## Expected Target

```text
selected_target=wireguard-1779454504-c43409
target_interface=v7e06a394c478
```

## Expected Readiness

If only reservation is added and diagnose remains `SUSPECT`:

```text
expected_second_canary_readiness=CONDITIONAL
remaining_blocker=stale_handshake_waiver_required
```

If reservation is added and diagnose semantics are fixed/refreshed to recognize the fresh live handshake:

```text
expected_second_canary_readiness=GO
remaining_blocker=none_if_restore_settle_and_runtime_checks_remain_OK
```

## Expected Blast Radius

```text
blast_radius=one_user
forward_preview=v7-user-switch <fresh_candidate> wireguard-1779454504-c43409
rollback_preview=v7-user-switch <fresh_candidate> vless
restore_lifecycle=staged_restore_with_restore_settle_gate
```

## Remaining Required Gates

- reservation metadata/tooling support approval;
- fresh candidate selection;
- fresh restore-settle gate;
- strict no hidden user-switch/routing-sync;
- runtime checks OK;
- explicit waiver if diagnose still `SUSPECT`.
