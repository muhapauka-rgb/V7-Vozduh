# E11.1 WireGuard Waiver Analysis

Mode: read-only waiver analysis. No waiver approval or canary execution occurred.

## Current Waiver Need

Strict target readiness rejects WireGuard because:

```text
diagnose_status=SUSPECT
diagnose_reason=curl_ok_but_handshake_stale
```

The waiver is needed only for stale-handshake diagnose semantics, not for route, quality, Direct/RU, Trusted RU, or kill-switch issues.

## Waiver Preconditions

Waiver can be operationally acceptable only if all are true in the future live gate:

```text
zero_user=true
quality_ok=true
interface_UP_LOWER_UP=true
live_handshake_fresh=true
route_get_sane=true
Direct_RU_exclusion_present=true
Trusted_RU_exclusion_present=true
restore_settle_gate_status=GO
runtime_checks_ok=true
hidden_user_switch=false
hidden_routing_sync=false
selected_moves=0
rollback_clear=true
```

## Comparative Risk

| Target path | Status | Risk |
|---|---|---|
| WireGuard | best conditional | diagnose stale-handshake waiver only |
| target `1` | occupied | no clean isolation |
| `awg0` | low quality / missing exclusions in readiness snapshot | attribution mixed with poor target quality |
| `awg3` | low quality / missing exclusions in readiness snapshot | attribution mixed with poor target quality |
| OpenVPN | SUSPECT and noisier quality/fail-rate history | weaker than WireGuard |
| dedicated new egress | cleanest long-term | requires provisioning/mutation project |

## Waiver Classification

```text
waiver_status=waiver_conditional
waiver_required=true
waiver_no_go=false
waiver_not_needed=false
```

WireGuard waiver is acceptable as a conditional approval path if the objective is a bounded mechanics/target-diversity canary and the operator explicitly accepts stale-handshake diagnose risk. It is not a clean-target GO until diagnose semantics are fixed or refreshed.
