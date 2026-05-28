# E9.2 Candidate Selection

Mode: read-only approval packet only.

## Selected Candidate

```text
second_candidate_user=10.7.0.14
current_egress=vless
target_egress=1
rollback_target=vless
table=1012
enabled=1
current_route_table_default=default dev tun0 scope link
current_route_get=8.8.8.8 from 10.7.0.14 dev tun0 table 1012
current_ip_rule=1012: from 10.7.0.14 lookup 1012
```

Reason selected:

- it is a new user and is not the first-canary user `10.7.0.15`;
- it is enabled and currently on `vless`;
- it is in the same `10.7.0.0/22` user cohort as the first successful canary;
- table `1012` is adjacent to the live-proven table `1013`, but still distinct;
- read-only route evidence shows the current baseline is coherent;
- no recent `switch-history` entry for `10.7.0.14` appeared in the last 100 lines inspected;
- rollback target is explicit: `vless`;
- target `1` uses the same interface already live-proven for one-user mechanics in E9.

## Users Rejected Or Not Selected

| User | Decision | Reason |
|---|---|---|
| `10.7.0.15` | rejected | already used in E9; E9.2 must change the user variable |
| `10.7.0.7` | rejected | disabled |
| `10.0.0.2`, `10.0.0.3`, `10.0.0.6` | not selected | legacy `10.0.0.0/24` cohort; less comparable to E9 |
| `10.7.0.8`, `10.7.0.11`, `10.7.0.13` | eligible fallback | current baseline appears coherent, but `10.7.0.14` is closer to the live-proven route-table range |
| `10.7.0.2` through `10.7.0.12` | eligible fallback where enabled | not selected because E9.2 needs only one bounded candidate |

## Sensitivity Notes

No per-user evidence in this read-only pass identified `10.7.0.14` as Trusted RU/Gosuslugi-sensitive. This is not a privacy/safety proof. The proposed target `1` excludes `TRUSTED_RU_SENSITIVE,DIRECT_RU`, so the pre-execution gate must still confirm the canary is a generic route mechanics test and not a Trusted RU path test.

## Verdict

Candidate selection is acceptable for a second approval packet, but not executable without separate live approval and fresh pre-canary gates.
