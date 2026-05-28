# E9.3.6 Candidate Move Matrix

Source: `docs/track7/control-plane/e9_3_5-evidence/final-planner-only-classification.txt`.

Mode: read-only analysis. No moves were applied.

## Summary

```text
candidate_moves_count=15
selected_moves_count=3
from=1
to=vless
move_type=failover
reason=current_egress_not_eligible
max_failover_behavior_expected=true
```

Current route reality at E9.3.6 snapshot:

```text
current egress=1
current dev=v7e356a192b79
proposed vless dev=tun0
```

## Matrix

| Priority | User | Table | Current Egress | Current Dev | Proposed Target | Proposed Dev | Reason | Selected | Blocked By Limit |
|---:|---|---:|---|---|---|---|---|---|---|
| 1 | 10.0.0.2 | 100 | 1 | v7e356a192b79 | vless | tun0 | current_egress_not_eligible | yes | no |
| 2 | 10.0.0.3 | 101 | 1 | v7e356a192b79 | vless | tun0 | current_egress_not_eligible | yes | no |
| 3 | 10.0.0.6 | 104 | 1 | v7e356a192b79 | vless | tun0 | current_egress_not_eligible | yes | no |
| 4 | 10.7.0.3 | 1001 | 1 | v7e356a192b79 | vless | tun0 | current_egress_not_eligible | no | yes |
| 5 | 10.7.0.2 | 1000 | 1 | v7e356a192b79 | vless | tun0 | current_egress_not_eligible | no | yes |
| 6 | 10.7.0.4 | 1002 | 1 | v7e356a192b79 | vless | tun0 | current_egress_not_eligible | no | yes |
| 7 | 10.7.0.6 | 1004 | 1 | v7e356a192b79 | vless | tun0 | current_egress_not_eligible | no | yes |
| 8 | 10.7.0.8 | 1006 | 1 | v7e356a192b79 | vless | tun0 | current_egress_not_eligible | no | yes |
| 9 | 10.7.0.9 | 1007 | 1 | v7e356a192b79 | vless | tun0 | current_egress_not_eligible | no | yes |
| 10 | 10.7.0.10 | 1008 | 1 | v7e356a192b79 | vless | tun0 | current_egress_not_eligible | no | yes |
| 11 | 10.7.0.11 | 1009 | 1 | v7e356a192b79 | vless | tun0 | current_egress_not_eligible | no | yes |
| 12 | 10.7.0.12 | 1010 | 1 | v7e356a192b79 | vless | tun0 | current_egress_not_eligible | no | yes |
| 13 | 10.7.0.13 | 1011 | 1 | v7e356a192b79 | vless | tun0 | current_egress_not_eligible | no | yes |
| 14 | 10.7.0.14 | 1012 | 1 | v7e356a192b79 | vless | tun0 | current_egress_not_eligible | no | yes |
| 15 | 10.7.0.15 | 1013 | 1 | v7e356a192b79 | vless | tun0 | current_egress_not_eligible | no | yes |

## Containment Implication

The selected set was bounded by `autoswitch_max_failover_per_run=3`, but the candidate set was platform-wide for users currently on egress `1`. Restoring apply authority without explicit approval would therefore allow a non-canary recovery stage to move up to three users immediately and potentially more in later timer runs if the service signal remained bad.
