# E25.1 Execution Path Decision

## Decision

`movement_packet_consumer_connected=false`

`approved_raw_switch_fallback_prepared=true`

E25.1 does not connect or deploy a movement-capable packet consumer. The existing `tools/v7-operator-execution-packet` / `admin_core/operator_execution.py` path is intentionally zero-movement only and rejects movement packets by design. Extending that tool to invoke `v7-user-switch` would create a live movement-capable execution surface inside a preparation/recovery block, which is outside the safest bounded scope for E25.1.

## Approved E25.2 Fallback Boundary

The following raw commands are prepared for E25.2 only, and only after a fresh execution-time recheck returns GO:

Forward:

```text
v7-user-switch 10.7.0.11 wireguard-1779454504-c43409
```

Rollback:

```text
v7-user-switch 10.7.0.11 1
```

No other raw movement command is approved by E25.1.

## Mandatory E25.2 Gates Before Fallback

- `candidate_user=10.7.0.11` must still be on `1`.
- `target_readiness_status=GO`.
- `restore_settle_gate_status=GO`.
- `selected_moves=0`.
- Hidden movers absent.
- Runtime checkers OK.
- WireGuard target `wireguard-1779454504-c43409` still zero-user before forward movement.
- Registry hashes either match the fresh E25.1 packet or are re-bound in a fresh packet before execution.
- Movement budget remains exactly `1`.
- Allowed users remain exactly `["10.7.0.11"]`.
- Allowed targets remain exactly `["wireguard-1779454504-c43409"]`.
- Rollback target remains exactly `1`.

## Reasoning

Path A, a movement-capable packet consumer, remains the preferred production architecture, but it should be implemented in a block that is explicitly allowed to introduce and rehearse a movement-capable execution surface. E25.1 is a recovery and governance re-arming block with final movement forbidden. The safer bounded result is a fresh approval packet plus an explicitly constrained raw fallback for the next execution retry.

## Safety Result

- Runtime mutation performed by E25.1: NO.
- User movement performed by E25.1: NO.
- Routing mutation performed by E25.1: NO.
- Autoswitch apply performed manually: NO.
- Canary/cohort performed: NO.
