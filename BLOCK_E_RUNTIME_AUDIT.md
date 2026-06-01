# Block E Runtime Audit

Date: 2026-06-01

## Runtime Health

- `v7-killswitch-check`: OK
- `v7-user-route-check`: OK for captured users
- `v7-runtime-contract-validate`: `status=ok`, critical `0`, warning `0`

## Capacity

Autoswitch shadow dynamic load:

- active users: `18`
- total channels: `7`
- healthy channels: `2`
- capacity status: `ok`
- candidate moves: `12`
- selected moves: `0`

Observability capacity group:

- status: healthy
- severity: ok

## Trust

Observability trust/routing notes:

- trusted/direct RU diagnostics: unknown
- direct routing: unknown
- services: blocked
- channels: unstable
- routing: degraded

These do not invalidate the one-user `vless -> awg3` proposal by themselves, but they block any wider autonomy or cohort movement.

## Selected Moves

Runtime shadow selected moves:

- selected moves: `0`
- reason: existing restore barrier zero-budget guard

Bounded proposal cap selected exactly one preview move:

- user: `10.7.0.16`
- from: `vless`
- to: `awg3`
- route class: `GLOBAL_STABLE`

## Target Readiness

Movement preview for `10.7.0.16 -> awg3`:

- errors: `[]`
- target interface: `awg3`
- blast radius: `one_user`
- table: `1014`
- rollback: `v7-user-switch 10.7.0.16 vless`

## Runtime Safety

- deploy performed: false
- systemd changed: false
- autoswitch apply run: false
- users moved: false
- routing changed: false

