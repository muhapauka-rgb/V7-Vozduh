# E11.2 WireGuard Waiver Decision

Waiver candidate:

```text
waiver_name=wireguard_stale_handshake_reserved_target
target=wireguard-1779454504-c43409
scope=one_user_second_canary_only
```

## Conditions Satisfied

```text
zero_user=true
quality_ok=true
route_ok=true
interface_up=true
interface_lower_up=true
exclusions_present=true
restore_governance_proven=true
rollback_clear=true
hidden_user_switch_observed=false
hidden_routing_sync_observed=false
live_handshake_fresh=true
bounded_blast_radius=one_user
```

## Residual Risk

The waiver accepts that strict readiness still sees `diagnose=SUSPECT`.
Although live WireGuard evidence is healthy, the diagnose persistence layer has
not been fixed in this block. A canary using this waiver would be a conditional
target-diversity canary, not a strict clean-target canary.

Not waived:

```text
reconcile failure
user-route failure
kill-switch failure
provisioning reconcile failure
hidden user-switch
hidden routing-sync
WireGuard interface missing/down
route_get failure
users.registry drift
unexpected user movement
restore-settle gate regression
rollback uncertainty
```

## Decision

```text
waiver_required=true
waiver_status=waiver_conditional
waiver_duration=single bounded second-canary window only
waiver_blast_radius=one_user
waiver_rollback_semantics=rollback candidate to previous egress only
```

Preferred path: reserve WireGuard first, then either fix diagnose semantics or
carry this explicit stale-handshake waiver into a fresh second-canary approval
packet.
