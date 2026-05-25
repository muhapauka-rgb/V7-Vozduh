# Routing Sync Governance

This document is static governance only. `v7-routing-sync` was read for analysis but not executed.

## Role

`v7-routing-sync` is the tool that applies the current user assignment registry to Linux routing tables. It does not decide where users should go; it makes existing registry decisions real in `ip route` and `ip rule`.

## Reads

```text
/opt/v7/egress/state/users.registry
/usr/local/lib/v7-egress-lib
node environment through v7_load_node_env when available
egress interface mapping through v7_egress_interface
```

## Writes / Mutates

For each enabled user row:

```text
ip route replace default dev <egress-interface> table <user-table>
ip rule del from <user-ip> table <user-table>
ip rule add pref <user-table> from <user-ip> table <user-table>
```

It prints current rules and route tables after mutation.

## What It Does Not Do Directly

No direct file writes were observed in the script. No direct `nft` writes, WireGuard config writes, service restart, or audit write were observed.

That said, it changes live routing state for every enabled user in `users.registry`. Its blast radius is therefore registry-wide.

## Blast Radius

| Input Scope | Runtime Effect |
|---|---|
| One changed user row | One user's table/rule can change |
| Many changed user rows | Many user tables/rules can change |
| Corrupt `users.registry` table/current/interface mapping | Broad routing misconfiguration |
| Missing/disabled egress interface | User is skipped, potentially leaving stale live rules |

## Kill Switch Interaction

`v7-routing-sync` does not rebuild kill switch rules. It relies on the existing kill switch table and reverse-route protections to block direct leakage. If user rules point to public/default routing or stale tables remain, `v7-killswitch-check` is the required post-check.

Required before future execution:

```text
tools/v7-route-movement-preview routing-sync ...
v7-killswitch-check
users.registry parse validation
egress.registry/interface validation
route table uniqueness validation
one-user canary if registry changed
```

Required after future execution:

```text
v7-killswitch-check
v7-user-route-check
sample ip route get per changed user
```

## Approval Model

`v7-routing-sync` must be treated as datapath mutation. It needs explicit approval and rollback readiness. It is not a dry-run tool.

Routing-sync cannot be the first live mutation after this governance work. It must come only after one-user canary success, registry backup, route snapshot, and a non-mutating preview showing the full registry-wide blast radius.
