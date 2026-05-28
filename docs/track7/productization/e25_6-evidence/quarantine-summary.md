# E25.6 Quarantine Summary

## Result

- `quarantine_created=true`
- `quarantine_type=redacted_evidence_only`
- `raw_secret_profile_copied_to_repo=false`
- `secrets_redacted_in_evidence=true`
- `no_profile_executed=true`
- `profile_activated=false`

## Quarantined Evidence Files

- `quarantine/v7-wg-client-test-direct-10.89.0.2.redacted.conf`
- `quarantine/v7-wg-client-test-v2-ipv6-mtu1200-10.89.0.2.redacted.conf`
- `quarantine/v7-awg-client-test-direct-10.88.0.2.redacted.conf`

The raw profile remains only at its original VPS path. The repository contains only redacted evidence copies and hashes.

## Secret Handling

Redacted fields:

- `PrivateKey`
- `PublicKey`
- `PresharedKey`
- `Endpoint`
- AWG-specific noise fields
- DNS values

No interface was brought up. No hooks were run. No routing or registry mutation occurred.

