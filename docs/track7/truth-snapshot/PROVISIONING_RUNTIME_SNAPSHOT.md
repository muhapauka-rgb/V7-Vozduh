# Provisioning Runtime Snapshot

Evidence source:

```text
docs/track7/truth-snapshot/evidence/section-provisioning-state.txt
docs/track7/truth-snapshot/evidence/section-routing-datapath.txt
```

## Users Registry

Observed users:

```text
17 registry rows
16 enabled users
1 disabled user: 10.7.0.7
all current=vless in snapshot
tables=100,101,104,1000-1013 with 1005 disabled
```

## Egress Registry

Enabled egresses:

```text
vless interface=tun0
awg0 interface=awg0
awg3 interface=awg3
1 interface=v7e356a192b79
openvpn-1779388847-d2ad7c interface=v7edb0c189291
wireguard-1779454504-c43409 interface=v7e06a394c478
```

## Reconcile

```text
V7_PROVISIONING_RECONCILE_CHECK=OK
```

## Backups / Rollback Material

Many registry, egress flag, assignment, and state backups exist. That improves recovery visibility, but rollback is still dangerous because restore/apply tools can touch configs, routing, nftables, and services.

## Verdict

Provisioning state is currently coherent enough for operations. It is not safe to run provisioning apply, IP allocation, user enable/disable/create, or user reconcile apply without a separate bounded approval.
