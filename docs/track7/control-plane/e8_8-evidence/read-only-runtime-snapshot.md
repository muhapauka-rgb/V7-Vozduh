# E8.8 Read-Only Runtime Snapshot

Captured: `2026-05-25T13:57:37Z` and targeted follow-up `2026-05-25T13:58:49Z`.

No mutation commands were executed. The only remote actions were read-only `cat`, `grep`, `systemctl is-active/is-enabled`, `ip ... show`, and V7 checkers.

## Registry Hashes

```text
users.registry  4b8ac23f01f8a6f5857500115bac6b401b824502648272ccaae234f76bd37908
egress.registry 67ac7afbac42b452f6d5be0ff1e3fc3cf3b3fae63ed72a7c18c6363a8e354d2f
```

## Authority Snapshot

```text
v7-health.service                 active enabled
v7-autoswitch-planner.timer       active enabled
v7-autoswitch-planner.service     inactive static
v7-users-autoswitch.timer         active enabled
v7-users-autoswitch.service       inactive static
```

The read-only process guard did not show a live `v7-user-switch` or `v7-routing-sync` process. It did show only the inspection shell command itself matching the process pattern during the first broad snapshot.

## Candidate Registry Evidence

```text
ip=10.7.0.15 current=vless table=1013 enabled=1
```

Candidate route evidence:

```text
USER=10.7.0.15 TABLE=1013 REGISTRY_EGRESS=vless ASSIGN_EGRESS=vless EXPECTED_DEV=tun0
OK: user=10.7.0.15 registry matches assignment
OK: user=10.7.0.15 table=1013 default dev tun0
OK: user=10.7.0.15 route_get uses tun0
```

Candidate switch history tail shows the last movement for `10.7.0.15` at `2026-05-25T07:54:40Z`, from `1` to `vless`. No candidate movement appeared in the latest 13:29-13:45 autoswitch burst.

## Target Egress Evidence

Selected target:

```text
id=1 protocol=amneziawg type=interface interface=v7e356a192b79 enabled=1 role=GLOBAL_FAST manual_only=0 reserve_only=0 exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
```

Load summary at capture time:

```text
1:     users=10 soft_limit=19 hard_limit=24 failover_hard_limit=32 status=OK
vless: users=6  soft_limit=19 hard_limit=24 failover_hard_limit=32 status=OK
```

Quality/stability signals:

```text
1:     avg_mbps=59.4437 min_mbps=43.24 stability=0.727411 samples=30
vless: avg_mbps=45.118  min_mbps=28.25 stability=0.626136 samples=30
```

## Runtime Check Results

```text
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

## Selection Verdict

Candidate `10.7.0.15 -> 1` is the least bad current approval-packet candidate found in this pass:

- enabled user;
- explicit current egress `vless`;
- explicit route table `1013`;
- target egress `1` is enabled and load summary says `OK`;
- target `1` excludes `TRUSTED_RU_SENSITIVE,DIRECT_RU`, reducing Trusted RU/Gosuslugi coupling for the canary packet;
- rollback target is the current egress `vless`;
- no routing/user mutation was executed.

This is not execution approval. Autoswitch must be held again inside the future canary window, and all pre-gates must be rechecked immediately before any live action.
