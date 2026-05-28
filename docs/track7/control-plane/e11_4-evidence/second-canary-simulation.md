# E11.4 Second Canary Simulation

## Scenario 1 - Diagnose Fixed First

Assumptions:

```text
wireguard_reserved=true
diagnose_semantics_fixed=true
wireguard_diagnose=OK
wireguard_zero_user=true
wireguard_quality_ok=true
restore_settle_gate=GO
runtime_checks_ok=true
hidden_user_switch=false
hidden_routing_sync=false
```

Expected outcome:

```text
expected_second_canary_readiness=GO_IF_FRESH_GATES_REMAIN_OK
expected_selected_target=wireguard-1779454504-c43409
waiver_required=false
blast_radius=one_user
restore_lifecycle=staged_planner_first_apply_after_settle_gate
delayed_movement_risk=bounded_by_restore_settle_gate
```

Remaining blockers:

- fresh candidate must be selected from current registry truth;
- WireGuard must remain zero-user;
- no Telegram hard-block or selected autoswitch moves may be active;
- all runtime checks must pass.

## Scenario 2 - Explicit Waiver Without Fix

Assumptions:

```text
wireguard_reserved=true
diagnose=SUSPECT
diagnose_reason=curl_ok_but_handshake_stale
live_wg_handshake_fresh=true
wireguard_zero_user=true
wireguard_quality_ok=true
restore_settle_gate=GO
operator_accepts_waiver=true
```

Expected outcome:

```text
expected_second_canary_readiness=CONDITIONAL
expected_selected_target=wireguard-1779454504-c43409
waiver_required=true
waiver_scope=one_user_only
blast_radius=one_user
restore_lifecycle=staged_planner_first_apply_after_settle_gate
```

Remaining blockers:

- strict readiness still reports `NO-GO`;
- approval packet must explicitly override strict `SUSPECT` with live `wg show` evidence;
- canary cannot be described as clean-target `GO`.

## Scenario 3 - No Fix And No Waiver

Expected outcome:

```text
expected_second_canary_readiness=NO-GO
selected_target=NONE
blocker=diagnose SUSPECT
```

## Simulation Decision

```text
best_path=diagnose_fix_first
fallback_path=stale_handshake_waiver_packet
direct_canary_now=false
execution_allowed_now=false
```

