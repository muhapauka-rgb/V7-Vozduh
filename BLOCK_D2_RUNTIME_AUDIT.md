# Block D2 Runtime Audit

Date: 2026-06-01

## Runtime Read-Only Checks

Commands were run read-only over SSH. No deploy, routing mutation, user movement, systemd change, or autoswitch apply was performed.

## Distribution

Enabled user distribution after D2 shadow retry:

| Egress | Enabled Users |
| --- | ---: |
| `amneziawg-exec-20260528-10-8-1-14` | 10 |
| `awg0` | 3 |
| `awg3` | 3 |
| `vless` | 2 |

Total enabled users: `18`

## Safety Review

Fixed repository safety-review, executed against live state through stdin:

- Status: `ok`
- Critical: `0`
- Warning: `0`
- Info: `1`
- Enabled egress: `7`
- Active users: `18`

## Runtime Guard Checks

- `v7-users-autoswitch.timer`: `inactive`
- No apply/movement/routing-sync process observed.
- Admin API health: unavailable on `127.0.0.1:8017`

## Verdict

runtime_unchanged=true

