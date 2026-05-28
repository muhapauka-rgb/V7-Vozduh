# E10 Fresh Second Canary Candidate Selection

Mode: read-only approval packet only.

Source evidence:

- `docs/track7/control-plane/e10-evidence/current-runtime-truth.txt`
- `docs/track7/control-plane/e10-evidence/current-state/users.registry`
- `docs/track7/control-plane/e10-evidence/current-restore-settle.json`
- `docs/track7/control-plane/e10-evidence/current-target-readiness.json`

## Current Runtime Truth

The old E9.2 candidate is stale.

```text
old_candidate=10.7.0.14
old_expected_current=vless
current_runtime_current=1
old_candidate_valid=false
```

Fresh enabled user state:

```text
10.0.0.2 current=vless table=100 enabled=1
10.0.0.3 current=vless table=101 enabled=1
10.0.0.6 current=vless table=104 enabled=1
10.7.0.2 current=vless table=1000 enabled=1
10.7.0.3 current=vless table=1001 enabled=1
10.7.0.4 current=vless table=1002 enabled=1
10.7.0.5 current=vless table=1003 enabled=1
10.7.0.6 current=vless table=1004 enabled=1
10.7.0.8 current=vless table=1006 enabled=1
10.7.0.9 current=vless table=1007 enabled=1
10.7.0.10 current=vless table=1008 enabled=1
10.7.0.11 current=vless table=1009 enabled=1
10.7.0.12 current=vless table=1010 enabled=1
10.7.0.13 current=vless table=1011 enabled=1
10.7.0.14 current=1 table=1012 enabled=1
10.7.0.15 current=1 table=1013 enabled=1
```

## Fresh Candidate

```text
candidate_user=10.7.0.11
current_egress=vless
rollback_target=vless
table=1009
enabled=1
route_get=8.8.8.8 from 10.7.0.11 dev tun0 table 1009
route_table_default=default dev tun0 scope link
current_route_check=OK
```

Selection rationale:

- enabled user;
- current egress is `vless`;
- route table is stable and matches registry;
- not the old stale candidate `10.7.0.14`;
- not currently occupying target `1`;
- not one of the delayed restore movement users called out in E9.4.4 (`10.7.0.5`, `10.0.0.2`, `10.0.0.3`);
- rollback target is explicit: `vless`;
- blast radius would be one user if a future canary is separately approved.

Candidate limitations:

- autoswitch safety state shows broad user freeze state in planner output;
- `vless` is overloaded in dynamic load (`vless_users=14`, `vless_status=FAILOVER_FULL`);
- no canary can be approved until a fresh target is also acceptable.

## Rejected Candidate Classes

| Candidate class | Reason |
|---|---|
| `10.7.0.14` | stale old candidate; current runtime has `current=1`, not `vless` |
| `10.7.0.15` | currently on egress `1`; not a clean second-canary candidate |
| `10.7.0.5`, `10.0.0.2`, `10.0.0.3` | explicitly involved in delayed restore movement root-cause history |
| disabled users | not eligible |

## Candidate Verdict

```text
candidate_user=10.7.0.11
candidate_status=CONDITIONAL
candidate_route_sane=true
candidate_rollback_clear=true
candidate_requires_target_approval=true
execution_allowed_now=false
```
