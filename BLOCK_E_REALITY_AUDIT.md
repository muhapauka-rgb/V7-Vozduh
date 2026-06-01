# Block E Reality Audit

Date: 2026-06-01
Branch: `v7-next`
Mode: bounded autonomy program, Stop Gate 1

## Repository State

- Current branch: `v7-next`
- Local HEAD: `d139c47d470055d8e61c3f40e7c4a2343d2538f4`
- `origin/v7-next`: `d139c47d470055d8e61c3f40e7c4a2343d2538f4`
- D2 remediation files are present locally and not pushed in this turn.

## Runtime Snapshot

Runtime files captured read-only into `/private/tmp/v7-block-e`:

- `users.registry`
- `egress.registry`
- `safety-fixed.json`
- `shadow.json`
- `proposal-cap.json`
- `move-preview.json`
- `rollback-preview.json`
- `killswitch.txt`
- `user-route-check.txt`
- `observability.txt`
- `runtime-contract.txt`

## Runtime Hashes

- users registry: `ee71cdd73a5a9b03ff009b8c29fae194fbf97c4f956677028c3c1166c2e4dae4`
- egress registry: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- policy: `a610f6cd56a26fb360fdfee713bc49b0135608a3ed23f2d4892cf485ef4a0e24`
- org policy: `07bbb8c36af74cbb07a584a767d8b15f08f52cf169ac433c4740ae4d1d13d014`

## Current User Distribution

- registry rows: `19`
- enabled users: `18`
- `amneziawg-exec-20260528-10-8-1-14`: `10`
- `awg0`: `3`
- `awg3`: `3`
- `vless`: `2`

## Fresh Shadow State

- `users_total=18`
- `egress_total=7`
- `healthy_egress_total=2`
- `candidate_moves=12`
- `selected_moves=0`
- `reconnect_rotation_candidates=0`
- `rebalance_candidates=0`

## Fresh Bounded Proposal

- budget: `1`
- raw candidates: `12`
- held candidates: `10`
- eligible candidates: `2`
- proposal count: `1`
- exact candidate: `10.7.0.16`
- exact movement: `vless -> awg3`

## Health And Trust

- `v7-killswitch-check`: `OK`
- `v7-user-route-check`: all checked users OK in captured output.
- `v7-runtime-contract-validate`: `status=ok`, critical `0`, warning `0`
- `v7-users-autoswitch.timer`: `inactive`
- no apply/movement/routing-sync process observed.
- observability groups:
  - autoswitch: healthy
  - capacity: healthy
  - users: healthy
  - security: healthy
  - channels: unstable
  - routing: degraded
  - services: blocked
  - trusted/direct routing: unknown

## Reality Verdict

Stage 1 proposal is valid enough for operator review, but execution is stopped at Stop Gate 1 pending explicit operator approval for the exact candidate and exact rollback.

