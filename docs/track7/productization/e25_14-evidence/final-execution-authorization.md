# E25.14 Final Execution Authorization

## Result

`execution_authorized=false`

`forward_movement_executed=false`

`authorization_failure=users_registry_hash_mismatch`

## Why Authorization Failed

The E25.13 packet was still time-valid and the execution target was still `GO`, but the current live `users.registry` hash no longer matched the packet-bound hash.

Packet hash:

```text
packet_users_registry_hash=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c
```

Fresh execution-time hash:

```text
users_registry_hash=f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042
```

The candidate and target were still clean:

```text
candidate_row=ip=10.7.0.11 current=1 table=1009 enabled=1
target_readiness=GO
restore_settle_gate_status=GO
selected_moves_count=0
hidden_movers_count=0
runtime_checkers_ok=true
target_users=0
```

But the packet was no longer tied to the exact registry truth it approved. The current registry includes an additional active user row:

```text
ip=10.7.0.16 current=vless table=1014 enabled=1
```

This appears unrelated to the approved `10.7.0.11` blast radius, but E25.14 requires fail-closed behavior on unexplained registry drift before first real movement.

## Decision

No forward command was executed.

The approved raw fallback command remains unused:

```bash
v7-user-switch 10.7.0.11 amneziawg-exec-20260528-10-8-1-14
```

## Required Next Step

Create a fresh packet against the current registry hash and repeat execution-time recheck before attempting movement.
