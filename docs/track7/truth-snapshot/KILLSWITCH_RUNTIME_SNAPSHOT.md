# Kill Switch Runtime Snapshot

Evidence source:

```text
docs/track7/truth-snapshot/evidence/section-killswitch.txt
docs/track7/truth-snapshot/evidence/section-routing-datapath.txt
```

## Check Result

```text
V7_KILLSWITCH_CHECK=OK
```

Observed protections:

```text
client_source_set=present
reverse_route_subnet=10.0.0.0/24 present
reverse_route_subnet=10.7.0.0/22 present
direct_leak_drop_rule=present
direct_whitelist_rule=present
direct_fwmark_rule=present
direct_fwmark_precedes_user_rules=OK
nat_awg0=present
nat_awg3=present
nat_tun0=present
nat_v7e06a394c478=present
nat_v7e356a192b79=present
nat_v7edb0c189291=present
mss_clamp=present_nft for observed egresses
```

## Dependency

Kill switch appears healthy in current state. Its risk is dependency on future route/user/policy mutations: if autoswitch or routing-sync changes path state unexpectedly, kill switch checks must be repeated before trusting canary or apply results.

## Verdict

Kill switch is currently OK, but it is not a blanket approval for routing/autoswitch mutation.
