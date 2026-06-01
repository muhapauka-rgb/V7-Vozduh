# Program F2 Runtime Audit

Date: 2026-06-01

## Runtime Guard

Captured runtime hashes:

- users registry: `ee71cdd73a5a9b03ff009b8c29fae194fbf97c4f956677028c3c1166c2e4dae4`
- egress registry: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- policy: `a610f6cd56a26fb360fdfee713bc49b0135608a3ed23f2d4892cf485ef4a0e24`
- org policy: `07bbb8c36af74cbb07a584a767d8b15f08f52cf169ac433c4740ae4d1d13d014`

`v7-users-autoswitch.timer`: `inactive`

No apply, user-switch, routing-sync, policy apply, or rebalance process was observed during preflight.

## Safety

Fixed safety review:

- status: `ok`
- critical: `0`
- warning: `0`
- enabled egress: `7`
- active users: `18`

## Capacity

Fresh shadow:

- users total: `18`
- egress total: `7`
- healthy egress total: `2`
- raw candidates: `12`
- selected moves: `0`

## Target Readiness

Approved target `awg3`:

- movement preview errors: `[]`
- target interface: `awg3`
- rollback command: `v7-user-switch 10.7.0.16 vless`

Fresh recommended target `awg0`:

- movement preview errors: `[]`
- target interface: `awg0`

## Runtime Verdict

Runtime can support a one-user movement after fresh packet approval. The current approved target is stale, so no movement was executed.

