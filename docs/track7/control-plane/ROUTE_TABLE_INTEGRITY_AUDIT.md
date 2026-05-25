# Route Table Integrity Audit

This audit is read-only. No route table was created, replaced, deleted, or repaired.

## Registry State

At the 2026-05-25 sample, all enabled users were assigned to:

```text
current=vless
expected_interface=tun0
```

Enabled route tables:

```text
100, 101, 104, 1000, 1001, 1002, 1003, 1004, 1006, 1007, 1008, 1009, 1010, 1011, 1012, 1013
```

Disabled route table:

```text
1005
```

## Duplicate / Invalid Table Usage

- Duplicate enabled-user tables: none observed.
- Invalid table IDs: none observed.
- Missing enabled route tables: none observed in `ip -4 route show table all`.
- Disabled user table `1005`: no required route table expectation.

## Table / Interface Match

For every enabled user table, `ip -4 route show table all` showed:

```text
default dev tun0 table <table> scope link
```

`v7-user-route-check` and `v7-provisioning-reconcile-check` also reported table defaults OK.

## Orphan / Drift Notes

No user-table orphan with an unknown enabled user was identified from the sampled table set. Table `70` is the direct/fwmark table and is not a user table.

## Would Routing-Sync Be Dangerous Now?

Yes, as a first action. Even though the route table state looks aligned, `v7-routing-sync` would be registry-wide mutation and the current control plane is not quiet. It should not be used as a canary precondition or automatic repair.

## Integrity Status

```text
route_table_integrity=OK_AT_SNAPSHOT
routing_drift_level=low_for_tables
routing_sync_safe_as_first_action=false
```
