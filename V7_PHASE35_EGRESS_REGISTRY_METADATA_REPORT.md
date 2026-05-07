# V7 Phase 35: Egress registry metadata

Date: 2026-05-07

## Goal

Move egress metadata needed by checks/admin out of code and into
`/opt/v7/egress/state/egress.registry`.

This supports the larger V7 architecture: new egresses should be discoverable
from registry data instead of requiring code edits for every new tunnel.

## Changed

Updated `egress.registry` on the VPS:

```text
id=vless protocol=vless type=proxy interface=tun0 test=socks5://127.0.0.1:1080 enabled=1 expected_ip=77.110.103.131 config_path=/etc/sing-box/config.json
id=awg2 protocol=amneziawg type=interface interface=awg2 test=interface enabled=1 expected_ip=94.241.139.241 config_path=/etc/amnezia/amneziawg/awg2.conf
```

Updated `/usr/local/bin/v7-system-check`:

- Reads optional `expected_ip=...` from registry.
- Reports a warning when actual egress IP differs from expected IP.
- Keeps the existing OK behavior when external IP is reachable and matches.

## Backups

Created before changes:

- `/opt/v7/egress/state/egress.registry.backup.phase35-metadata.20260507-105825`
- `/root/v7-backups/v7-system-check.phase35.20260507-105824.bak`

## Validation

Commands run:

```bash
bash -n /usr/local/bin/v7-system-check
bash /tmp/v7-phase35-registry-metadata.sh
v7-system-check
v7-state-json-save
```

Result:

- Registry metadata updated successfully.
- `v7-system-check`: `V7_RESULT=OK`
- `vless_ip=77.110.103.131`
- `awg2_ip=94.241.139.241`
- User route tables still point to `tun0` for current users.
- No user routing mutation was performed.

## Next Implication

Future egress onboarding should write at least:

- `id`
- `protocol`
- `type`
- `interface`
- `test`
- `enabled`
- `expected_ip` after first successful validation
- `config_path`

This gives admin UI, health checks, speed tests, and diagnostics a common source
of truth.
