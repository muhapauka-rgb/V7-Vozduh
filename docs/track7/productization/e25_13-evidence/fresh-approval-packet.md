# E25.13 Fresh Approval Packet

`fresh_approval_packet_created=true`

`packet_non_expired=true`

`packet_id=packet-6cda2c9e4c42133eedfebd5b`

`approval_id=approval-4602f4946f57be3bf9212b03`

`operation_id=e25-13-first-movement-20260528T181306Z`

`packet_hash=b5b9484ff1ccd1f78b3eded361dce38348327518f36c657c2ea3087a2dc2b939`

## Movement

- runtime action: `BOUNDED_USER_MOVEMENT`
- execution method: `APPROVED_RAW_FALLBACK_PREPARED`
- UI execution allowed: `false`
- execution allowed now: `false`
- candidate user: `10.7.0.11`
- from egress: `1`
- to egress: `amneziawg-exec-20260528-10-8-1-14`
- rollback target: `1`
- movement budget: `1`
- blast radius: `1 user`

## Runtime Truth

- users.registry hash: `bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- egress.registry hash: `43dbba0e138d9ee33556801640e15968cebe5b58e6866802e0538d98b72af380`
- selected moves hash: `NONE`
- runtime snapshot hash: `53fcacea440df3c90025980003fb7d1bb8f6e836f89be2c844b5f5b4f1303435`
- target readiness: `GO`
- restore-settle: `GO`
- avg Mbps: `27.12`
- min Mbps: `10.67`
- stability: `1.0`

## Approval Lifetime

- created at: `2026-05-28T18:13:06Z`
- expires at: `2026-05-28T22:13:06Z`

## Approved Raw Fallback For Next Execution Block Only

Forward command, allowed only after fresh execution-time recheck in the next block:

```bash
v7-user-switch 10.7.0.11 amneziawg-exec-20260528-10-8-1-14
```

Rollback command:

```bash
v7-user-switch 10.7.0.11 1
```

## Fail-Closed Requirements

The packet must deny execution if any of these change: candidate current egress, registry hashes without accepted fresh recheck, selected moves, hidden movers, readiness, restore-settle, rollback target, execution-only isolation, approval expiry, replay state, movement budget, allowed user, or allowed target.
