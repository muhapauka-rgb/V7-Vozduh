# Kill Switch Dependency Analysis

This is static/read-only dependency analysis. The kill switch was checked but not rebuilt, disabled, or modified.

## Current Verified State

`v7-killswitch-check` reported:

```text
V7_KILLSWITCH_CHECK=OK
```

Observed protections included:

- client source set present;
- VPN subnets present;
- reverse route subnets present;
- direct leak drop rule present;
- direct whitelist rule present;
- direct fwmark rule present and ordered before user rules;
- DNS capture rules present;
- NAT and MSS clamp present for egress interfaces.

## Dependency On Routing-Sync

Kill switch protects leak boundaries, but it does not make user assignment decisions. It depends on user rules and route tables to send traffic through intended egresses. If user rules/tables are wrong, kill switch may still block direct leak while the user experiences wrong path or outage.

## Dependency On IP Rules

Missing user source rules can cause traffic to bypass a user-specific table. The kill switch may still prevent direct public leak, but it does not prove the traffic is on the intended egress.

## Dependency On Table Correctness

If table defaults point to the wrong egress, kill switch can still be OK while policy intent is wrong. This is why `v7-user-route-check` and route table audit remain required before canary.

## Missing Rules In Current Audit

Stable `ip rule show` snapshots did not prove missing enabled-user rules. `v7-reconcile-check` reported missing rules inconsistently, which is a control-plane integrity issue rather than proven kill-switch failure.

## Proxy Runtime Guard Overlap

Proxy runtime guard and kill switch overlap in leak-prevention goals but are not interchangeable. Proxy guard mutation is out of scope for canary preparation.

## Risk Status

```text
kill_switch_status=OK_AT_SNAPSHOT
direct_leak_risk=low_at_snapshot
intended_path_risk=controlled_by_route_tables_and_rules
canary_dependency=must_recheck_immediately_before_and_after
```
