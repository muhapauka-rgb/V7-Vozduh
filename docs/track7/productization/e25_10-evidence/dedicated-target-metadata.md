# E25.10 Dedicated Target Metadata

## Result

`dedicated_execution_target_created=false`

`metadata_attempted=true`

`metadata_rolled_back=true`

`target_readiness_final_status=NO-GO`

## Metadata Attempt

After target-local connectivity succeeded, one execution-only metadata row was appended for validation:

```text
id=amneziawg-exec-20260528-10-8-1-14
protocol=amneziawg
type=interface
interface=v7execwg0
test=interface
enabled=1
config=/etc/amnezia/v7execwg0.conf
role=EXECUTION_ONLY
priority=10
weight=1
soft_limit=1
hard_limit=1
manual_only=1
reserve_only=1
canary_reserved=true
execution_reserved=true
reservation_owner=operator_execution_governance
autoswitch_allowed=false
rebalance_allowed=false
production_assignment_allowed=false
service_tags=governance,execution
exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
```

Registry backup before append:

- `/opt/v7/egress/state/egress.registry.backup.e25_10_exec_import.20260528T143509Z`
- backup SHA256: `a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`
- registry SHA256 after append: `c82e336d96202e27f8966cfb7eb4ec36972e38743daf21eb32eb7eaea24f5ecd`

## Readiness Helper Result

`v7-second-canary-target-readiness` saw the new target but rejected it:

- selected target remained: `wireguard-1779454504-c43409`
- execution target status: `NO-GO`
- reasons:
  - `interface state unknown`
  - `load-state users count unknown`
  - `diagnose UNKNOWN`
  - `manual_only`
  - `reserve_only`
  - missing quality metrics

This confirms that target-local usability is not enough for movement readiness; the V7 readiness/diagnose/load layers need a dedicated execution-target integration path.

## Runtime Checker Result

The active metadata row caused runtime checkers to fail because the target was now treated as an enabled egress interface without kill-switch/provisioning rules:

- `v7-killswitch-check`: `FAIL`
- `v7-provisioning-reconcile-check`: `FAIL`
- failure reason:
  - `nat_v7execwg0_subnet=10.0.0.0/24 missing`
  - `nat_v7execwg0_subnet=10.7.0.0/22 missing`
  - `nat_v7execwg0=missing`
  - `mss_clamp_v7execwg0=missing`

No users were moved and user route checks remained correct, but leaving this metadata active would make runtime health non-clean.

## Rollback

The active metadata row was removed and `v7execwg0` was brought down.

- metadata removed: `true`
- interface down: `true`
- interface absent after rollback: `true`
- `users.registry` SHA256 after rollback: `bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- `egress.registry` SHA256 after rollback: `a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`
- candidate row after rollback: `ip=10.7.0.11 current=1 table=1009 enabled=1`
- user table `1009` after rollback: `default dev v7e356a192b79 scope link`

Runtime checkers after rollback:

- `v7-reconcile-check`: `OK`
- `v7-user-route-check`: `OK`
- `v7-killswitch-check`: `OK`
- `v7-provisioning-reconcile-check`: `OK`

## Decision

The external profile is usable, but the dedicated target is not yet movement-ready. The next block must add an execution-only egress integration path for NAT/MSS, diagnose/load/readiness metadata, and checker semantics without exposing it to autoswitch/rebalance.
