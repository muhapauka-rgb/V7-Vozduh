# E9.1 Drift Analysis

Baseline:

```text
time=2026-05-25T14:57:32Z
users.registry=90afd3fb2a626726baee6d2106807f33de62240a674d0bb7a866e62e8c0a8334
egress.registry=67ac7afbac42b452f6d5be0ff1e3fc3cf3b3fae63ed72a7c18c6363a8e354d2f
candidate=10.7.0.15 current=vless table=1013 enabled=1
table_1013=default dev tun0 scope link
```

Samples:

| Sample | Time UTC | users.registry | egress.registry | Candidate | Table 1013 | Checks |
|---|---:|---|---|---|---|---|
| A | 14:58:10 | stable | stable | `vless` | `tun0` | OK |
| B | 14:59:16 | stable | stable | `vless` | `tun0` | OK |
| C | 15:00:20 | stable | stable | `vless` | `tun0` | OK |

## Drift Verdicts

```text
users.registry_stable=true
egress.registry_stable=true
candidate_assignment_stable=true
table_1013_stable=true
route_get_stable=true
switch_history_no_unexpected_movement=true
hidden_routing_sync_observed=false
hidden_user_switch_observed=false
routing_drift_observed=false
kill_switch_still_OK=true
reconcile_still_OK=true
provisioning_still_OK=true
```

## Interpretation

No delayed side effect was observed after E9. The first one-user canary and rollback did not leave visible drift in registry, route table 1013, route-get behavior, or switch history during the E9.1 monitoring window.
