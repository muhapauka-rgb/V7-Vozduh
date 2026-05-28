# E25.7 Normalized Config Creation

## Result

- `normalized_config_written=true`
- `source_profile=/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.conf`
- `source_profile_hash=666cf51365f7e145726f7db7c503577ff2b5a872ae7351486cb41fd1316e0ff1`
- `normalized_interface=v7execwg0`
- `normalized_config_path=/etc/wireguard/v7execwg0.conf`
- `normalized_config_hash=c838438d6a6d5f82d8137c6d1aaa0682ccf52446c7bc563168009e2873ee16ed`
- `raw_profile_not_executed=true`
- `table_off_enforced=true`
- `dns_side_effect_blocked=true`
- `hooks_absent=true`

## Normalization

The normalized wrapper preserved cryptographic and peer settings, then removed or blocked unsafe behavior:

- removed DNS mutation;
- removed any possible hook directives;
- enforced `Table = off`;
- preserved `Address = 10.89.0.2/32`;
- preserved `MTU = 1280`;
- preserved peer `AllowedIPs = 0.0.0.0/0` only as a peer selector.

The raw profile was never started.

