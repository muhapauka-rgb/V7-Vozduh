# E25.8 V7 Normalization

## Normalized Wrapper

Source:

`/etc/wireguard/vps.conf`

Normalized interface:

`v7execwg0`

Normalized active config during test:

`/etc/wireguard/v7execwg0.conf`

## Applied Safety Rules

- `Table=off` enforced;
- DNS directives absent;
- route/firewall hooks absent;
- raw profile not executed;
- interface name isolated to `v7execwg0`;
- address narrowed to `10.10.0.2/32` for primary test to avoid broad connected-route side effects;
- MTU set to `1280` for primary test;
- peer endpoint and key material preserved.

## Normalized Hash

Primary normalized config SHA256:

`24c15c42b896808a28b78214a515df719be93159cb36f51b8f209add8aa8c522`

## Result

`normalized_config_written=true`

`table_off_enforced=true`

`dns_side_effect_blocked=true`

`hooks_absent=true`

`raw_profile_not_executed=true`

## Raw Evidence

See `target-local-activation-connectivity.raw.md`.
