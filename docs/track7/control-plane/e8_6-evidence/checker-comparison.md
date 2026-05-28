# E8.6 Checker Comparison

Mode: read-only.

## Summary

```text
v7-reconcile-check=FAIL
v7-user-route-check=OK
v7-killswitch-check=OK
v7-provisioning-reconcile-check=OK
```

## Why Reconcile Fails

`v7-reconcile-check` fails on per-user rule presence checks:

```bash
ip -4 rule show 2>/dev/null | grep -q "from $ip lookup $table"
```

Because global `pipefail` is enabled and `grep -q` exits early after a match,
the pipeline can return `141` from upstream SIGPIPE even when the rule exists.

## Why User Route Check Passes

`v7-user-route-check` checks actual route reality:

- registry egress matches assignment file;
- table default points to expected egress device;
- `ip route get 8.8.8.8 from <user> iif wg0` uses expected device;
- leak to `ens3` would fail.

Fresh E8.6 output showed every enabled user OK.

## Why Kill Switch Check Passes

`v7-killswitch-check` validates:

- kill switch table;
- client source set;
- reverse route subnets;
- direct leak drop/whitelist rules;
- fwmark direct route table and ordering;
- DNS capture;
- NAT and MSS clamp across enabled egress interfaces;
- route reality for every enabled user.

Fresh E8.6 output ended:

```text
V7_KILLSWITCH_CHECK=OK
```

## Why Provisioning Reconcile Passes

`v7-provisioning-reconcile-check` validates:

- VPN source sets and reverse routes;
- NAT and MSS clamp per enabled egress interface;
- WireGuard peer presence;
- route reality does not leak to public interface;
- route table default matches expected egress interface.

Fresh E8.6 output ended:

```text
V7_PROVISIONING_RECONCILE_CHECK=OK
```

## Semantic Difference

| Checker | Primary model | Result | Interpretation |
|---|---|---|---|
| `v7-reconcile-check` | strict registry/assign/wg/rule/route spot check | FAIL | false-positive in rule presence pipeline |
| `v7-user-route-check` | per-user route reality | OK | datapath per user is operational |
| `v7-killswitch-check` | leak guard and route safety | OK | kill switch assumptions currently hold |
| `v7-provisioning-reconcile-check` | provisioning/runtime consistency | OK | registry/table/NAT/MSS/WG are consistent |

## Classification

```text
classification=CONFIRMED_FALSE_POSITIVE
affected_check=v7-reconcile-check missing ip rule lookup table
repair_runtime_before_canary=false for this failure class
fix_checker_before_using_reconcile_as_gate=true
bounded_waiver_possible=true
```
