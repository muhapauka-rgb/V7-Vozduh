# E25.15 Fresh Approval Packet

`fresh_approval_packet_created=true`

`packet_non_expired=true`

`packet_id=packet-0671c44ea5024978724e11e9`

`approval_id=approval-4bbbbf5f5d145367d490d523`

`operation_id=e25-15-first-movement-retry-20260528T205228Z`

`packet_hash=87726fe0ec4cfa1731868512f1557a0136399ca7349b2d7db012d185fbb529e1`

## Movement

- candidate: `10.7.0.11`
- from: `1`
- to: `amneziawg-exec-20260528-10-8-1-14`
- rollback: `1`
- movement budget: `1`
- blast radius: `1 user`
- out-of-scope users: `[10.7.0.16]`

## Runtime Truth

- users registry hash: `f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042`
- egress registry hash: `43dbba0e138d9ee33556801640e15968cebe5b58e6866802e0538d98b72af380`
- selected moves hash: `NONE`
- target readiness: `GO`
- restore-settle: `GO`

## Commands Approved For E25.15 Only After Fresh Recheck

```bash
v7-user-switch 10.7.0.11 amneziawg-exec-20260528-10-8-1-14
```

Rollback:

```bash
v7-user-switch 10.7.0.11 1
```

`execution_allowed_now=false` until E25.15 execution-time recheck passes.
