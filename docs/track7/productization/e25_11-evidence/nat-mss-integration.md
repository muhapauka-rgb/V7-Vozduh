# E25.11 NAT/MSS Integration

## Result

`nat_integration_ok=true`

`mss_integration_ok=true`

`runtime_checkers_ok_after_nat=true`

`routing_mutation_for_users=false`

## Rules Added

One interface-specific NAT rule was added:

```text
ip saddr @v7_client_src oifname "v7execwg0" counter masquerade comment "V7 NAT users via v7execwg0"
```

Two interface-specific forward rules were added:

```text
ip saddr @v7_client_src oifname "v7execwg0" tcp flags syn tcp option maxseg size set rt mtu counter comment "V7 MSS clamp users via v7execwg0"
ip saddr @v7_client_src oifname "v7execwg0" counter accept comment "V7 allow users via v7execwg0"
```

No broad NAT reset was run. Existing egress rules were left intact.

## Checker Results

After the rules were added and execution-only metadata was active:

- `v7-killswitch-check`: `OK`
- `v7-provisioning-reconcile-check`: `OK`

The previous E25.10 blockers were cleared:

- `nat_v7execwg0=missing`: resolved
- `mss_clamp_v7execwg0=missing`: resolved

## Scope

The NAT/MSS rules are inert until a governed execution explicitly routes an approved user to `v7execwg0`. E25.11 did not move any user and did not mutate any user route table.
