# E9.2.2 Candidate 10.7.0.14 Refresh

Mode: read-only target selection only.

```text
candidate_user=10.7.0.14
enabled=1
current=vless
table=1012
assignment_file=egress=vless
route_get=8.8.8.8 from 10.7.0.14 dev tun0 table 1012
candidate_still_valid=true
```

Observed assignment file:

```text
egress=vless
last_switch=1779695678
fail_count=0
```

Current route baseline:

```text
table 1012 default dev tun0
route_get from 10.7.0.14 iif wg0 -> dev tun0 table 1012
```

Sensitivity:

- no per-user evidence in this pass marks `10.7.0.14` as Trusted RU / Direct RU sensitive;
- this is not a privacy proof;
- target selection must still prefer egress with explicit `exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU`.

Verdict:

```text
candidate_10.7.0.14_still_valid=true
target_selection_status=NO_SAFE_TARGET
```
