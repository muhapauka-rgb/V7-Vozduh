# Block D2 Egress Certification

Date: 2026-06-01

## Enabled Egress Certified By Fixed Safety Review

Fixed safety-review detected these enabled egress IDs:

1. `vless`
2. `awg0`
3. `awg3`
4. `1`
5. `openvpn-1779388847-d2ad7c`
6. `wireguard-1779454504-c43409`
7. `amneziawg-exec-20260528-10-8-1-14`

## Planner View

Shadow planner summary:

- `egress_total=7`
- `healthy_egress_total=2`
- `users_total=18`
- `candidate_moves=12`
- `selected_moves=0`

The difference between enabled egress (`7`) and healthy egress (`2`) is expected: safety-review certifies registry availability; planner applies quality, route-class, reservation, and service fitness.

## Verdict

enabled_egress_certified=true

