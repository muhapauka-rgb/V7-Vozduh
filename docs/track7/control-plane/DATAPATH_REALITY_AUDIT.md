# Datapath Reality Audit

This audit checks observed datapath behavior without changing routing, rules, nftables, kill switch, assignments, or services.

## Current Runtime Assignment Reality

At audit time, enabled users were assigned to `vless`, which maps to `tun0`.

## User Route Reality

`v7-user-route-check` reported:

```text
V7_USER_ROUTE_CHECK=OK
```

It showed registry assignment, assignment file, table default, and `route get` using `tun0` for enabled users.

## Kill Switch Reality

`v7-killswitch-check` reported:

```text
V7_KILLSWITCH_CHECK=OK
```

It also embedded user route checks and reported expected egress usage for 16 enabled users.

## Provisioning Reality

`v7-provisioning-reconcile-check` reported:

```text
V7_PROVISIONING_RECONCILE_CHECK=OK
```

NAT and MSS clamp were present for known egress interfaces, and user table defaults were OK.

## Leak Risk

No direct public-interface leak was observed in the read-only checks. The kill switch direct leak drop rule, direct fwmark rule, NAT, MSS clamp, and reverse route protections were present.

## Reality Status

```text
datapath_reality=OPERATIONAL_AT_SNAPSHOT
leak_evidence=none_observed
route_get_matches_registry=true
kill_switch_verified=true
provisioning_verified=true
```

## Remaining Concern

The datapath looks operational, but the control plane is not quiet. Autoswitch authority and reconcile inconsistency mean live canary remains NO-GO.
