# Program F Runtime Audit

Date: 2026-06-01

## Runtime Hashes

Captured from `runtime-guard.txt`:

- users registry: unchanged from Block E snapshot
- egress registry: unchanged from Block E snapshot
- policy: unchanged from Block E snapshot
- org policy: unchanged from Block E snapshot

## Health

- `v7-killswitch-check`: OK
- `v7-user-route-check`: OK in captured output
- `v7-runtime-contract-validate`: `status=ok`, critical `0`, warning `0`

## Capacity

Fresh shadow:

- `users_total=18`
- `egress_total=7`
- `healthy_egress_total=2`
- `candidate_moves=12`
- `selected_moves=0`
- `reconnect_rotation_candidates=0`
- `rebalance_candidates=0`

Proposal cap:

- raw candidates: `12`
- held candidates: `10`
- eligible candidates: `2`
- proposal count: `1`
- ready for operator review: true

## Trust

Observability groups:

- autoswitch: healthy
- capacity: healthy
- users: healthy
- security: healthy
- channels: unstable
- direct routing: unknown
- routing: degraded
- services: blocked
- trusted RU: unknown

These block autonomous certification, especially repeated autonomy and wider reliability claims.

## Target Readiness

Movement preview:

- user: `10.7.0.16`
- from: `vless`
- to: `awg3`
- target interface: `awg3`
- table: `1014`
- errors: `[]`

Rollback preview:

- rollback command: `v7-user-switch 10.7.0.16 vless`
- rollback ready: true

## Runtime Verdict

Runtime is ready for a one-user operator-approved movement, but not for execution without the missing approved packet.

