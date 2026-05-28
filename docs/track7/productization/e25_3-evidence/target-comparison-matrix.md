# E25.3 Target Comparison Matrix

## Latest Live Readiness Comparison

Collected at final safety check around `2026-05-28T11:32:16Z`.

| Target | Users | Load | Diagnose | Avg Mbps | Min Mbps | Stability | Readiness | Main Blocker |
|---|---:|---|---|---:|---:|---:|---|---|
| `wireguard-1779454504-c43409` | 0 | OK | OK | 23.7843 | 19.54 | 0.821550 | GO | Spiky history |
| `openvpn-1779388847-d2ad7c` | 0 | OK | SUSPECT | 70.5033 | 64.04 | 0.908326 | NO-GO | diagnose SUSPECT / interface unknown |
| `awg0` | 3 | HARD_FULL | OK | 31.0617 | 9.16 | 0.294897 | NO-GO | occupied, hard full, quality below floor, route exclusions missing |
| `awg3` | 9 | HARD_FULL | OK | 39.9703 | 2.42 | 0.060545 | NO-GO | occupied, hard full, quality below floor, route exclusions missing |
| `vless` | 0 registry / 1 load | SOFT_FULL | SUSPECT | 49.61 | 44.21 | 0.891151 | NO-GO | interface unknown, load user, diagnose SUSPECT, exclusions missing |

## Historical Context

`wireguard-1779454504-c43409` is the only existing target that satisfies all movement-readiness gates when its quality metrics are above floor:

- zero registry users
- zero load users
- diagnose OK
- load OK
- required route exclusions present
- interface inferred healthy through WireGuard diagnose

But it also caused E25 and E25.2 aborts because quality fell below floor at execution time.

## Best Existing Candidate

`wireguard-1779454504-c43409`

Condition:

Only after a sustained GO pre-execution window and a fresh execution-time readiness GO.

## Dedicated Egress Need

No existing alternate target is cleaner than WireGuard. For a production-clean first operator-driven movement, a dedicated execution-only egress is recommended because the only eligible existing target is quality-spiky.

## Result

- `best_first_movement_target=wireguard-1779454504-c43409_CONDITIONAL`
- `dedicated_execution_egress_required=true`
