# E9.2.5 Candidate Refresh

Mode: read-only / approval packet only.

Candidate:

```text
candidate_user=10.7.0.14
current_egress=vless
table=1012
enabled=1
rollback_target=vless
```

Evidence source:

- `docs/track7/control-plane/e9_2_2-evidence/runtime-snapshot.txt`
- `docs/track7/control-plane/e9_2_3-evidence/current-state/users.registry`

Observed candidate state:

```text
ip=10.7.0.14 current=vless table=1012 enabled=1
route_get=8.8.8.8 from 10.7.0.14 dev tun0 table 1012
```

Rollback target:

```text
rollback_command=v7-user-switch 10.7.0.14 vless
expected_rollback_route=default dev tun0 table 1012
```

Candidate verdict:

```text
candidate_still_valid=true
rollback_feasible=true
candidate_noise_status=no_recent_switch_history_noise_in_E9_2_2_tail
```

E9.2.5 did not execute `v7-user-switch` and did not refresh live switch-history.
