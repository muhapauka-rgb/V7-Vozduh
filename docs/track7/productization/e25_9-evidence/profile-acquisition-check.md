# E25.9 Profile Acquisition Check

## Result

`new_profile_provided=false`

`profile_path=NONE`

No new operator-provided external execution profile was found.

## Locations Checked

Expected import/upload locations were checked on the VPS:

- `/root/v7-execution-profile-import`
- `/root/v7-execution-profile-upload`
- `/root/v7-external-execution-profile`
- `/opt/v7/operator-import`
- `/opt/v7/egress/import`
- `/tmp/v7-execution-profile-import`
- `/root/v7-new-profile`
- `/root/v7-import`

All were absent.

## Recent Profile-Like Files

Files modified after E25.8 were runtime state JSON files under `/opt/v7/egress/state`, for example:

- `egress-load-summary.json`
- `telegram-sentinel.json`
- `egress-quality-summary.json`
- `v7-state.json`
- `service-matrix.json`

These are not operator-provided outbound profiles.

## Known Dead Profiles

The known dead/invalid profiles remain present but were not reused:

- `/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.conf`
- `/etc/wireguard/vps.conf`

They require server-side peer repair and proof of handshake/RX before any future reuse.

## Runtime Safety Snapshot

- `v7execwg0` absent;
- `/etc/wireguard/v7execwg0.conf` absent;
- `users.registry` hash unchanged from prior E25 line;
- `egress.registry` hash unchanged from prior E25 line;
- candidate `10.7.0.11` remained on egress `1`;
- route table `1009` unchanged;
- selected moves absent;
- hidden movers absent;
- runtime checkers OK.

## Decision

The block stops at acquisition:

`operator_input_required=true`

No quarantine, normalization, activation, metadata creation, or long-window validation is allowed without a new profile.

## Raw Evidence

See `profile-acquisition-check.raw.md`.
