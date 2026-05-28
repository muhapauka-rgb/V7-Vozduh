# E25.6 Offline Validation

## Result

- `offline_validation_pass=true`
- `safe_to_attempt_activation_next_block=true`
- `profile_activated=false`
- `raw_profile_started=false`

## Checks

| Check | Result |
| --- | --- |
| Candidate exists | `true` |
| Candidate hash captured | `true` |
| Protocol classification | `wireguard` |
| Required WireGuard fields present | `true` |
| Route hook scan | `PASS` |
| nft/iptables hook scan | `PASS` |
| DNS side effect detected | `true` |
| Full-tunnel semantics detected | `true` |
| Raw activation safe | `false` |
| V7 wrapper normalization possible | `true` |
| Interface conflict for `v7execwg0` | `false` |
| Route table conflict for `1250` | `false` |
| Secret leakage scan pending final tests | tracked in `tests.md` |

## wg-quick Note

`wg-quick strip` returned:

```text
wg-quick: The config file must be a valid interface name, followed by .conf
```

This is a filename/interface-name constraint, not a content execution failure. E25.6 did not copy the raw secret profile to `/tmp` or start it. The next activation block must validate the normalized profile at a proper interface path such as `v7execwg0.conf` before bringing it up.

## Normalized Wrapper Preview

See `offline-validation.raw.md` for the redacted normalized wrapper preview.

