# E25.12 Quality Root-Cause Snapshot

## Result

`quality_root_cause=MEASUREMENT_NOISE_AND_HOST_LOAD_CONTENTION`

`candidate_user=10.7.0.11`

`candidate_still_on_1=true`

`runtime_checkers_ok=true`

`selected_moves_zero=true`

`hidden_movers_absent=true`

## Target State

- target: `amneziawg-exec-20260528-10-8-1-14`
- interface: `v7execwg0`
- protocol: `amneziawg`
- MTU: `1280`
- endpoint route: external route via `ens3`
- endpoint ping: `5/5`, `0% packet loss`
- endpoint RTT: `min/avg/max/mdev = 18.930/31.039/46.893/9.328 ms`
- interface RX/TX errors: `0/0`
- interface RX/TX drops: `0/0`
- handshake: present
- target-local connectivity: present

## Readiness At Snapshot

Explicit execution readiness before recovery attempts:

- selected target: `NONE`
- approval status: `NO-GO`
- avg Mbps: `12.03`
- min Mbps: `5.08`
- stability: `0.737`
- rejection reason: `avg_mbps below floor (12.03); min_mbps below floor (5.08)`

## Runtime Safety

- default route unchanged
- DNS unchanged
- user table `1009`: `default dev v7e356a192b79 scope link`
- candidate route_get: `dev v7e356a192b79 table 1009`
- `users.registry` SHA256: `bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- `egress.registry` SHA256: `43dbba0e138d9ee33556801640e15968cebe5b58e6866802e0538d98b72af380`
- `v7-reconcile-check`: `OK`
- `v7-user-route-check`: `OK`
- `v7-killswitch-check`: `OK`
- `v7-provisioning-reconcile-check`: `OK`

## NAT/MSS

Existing E25.11 rules are present:

- `V7 NAT users via v7execwg0`
- `V7 MSS clamp users via v7execwg0`
- `V7 allow users via v7execwg0`

## Host Load

The VPS had non-trivial CPU pressure during the snapshot:

- load average: `2.42, 2.33, 2.07`
- CPU idle: `45.5%`
- process `python3` under `nobody`: approximately `109.1% CPU`

## Throughput Probe Shape

Target-local Cloudflare probes through `v7execwg0`:

| Bytes | HTTP | Speed B/s | Approx Mbps |
| ---: | ---: | ---: | ---: |
| 524288 | 200 | 846707 | 6.77 |
| 1048576 | 200 | 1343300 | 10.75 |
| 2097152 | 200 | 2206736 | 17.65 |

The larger probe performed substantially better than the smaller probes, which points toward measurement noise and connection warm-up effects rather than a simple hard connectivity failure.

## Classification

Primary classification:

`MEASUREMENT_NOISE_AND_HOST_LOAD_CONTENTION`

Secondary possibilities to test:

- `MTU_OR_MSS_LIMIT`
- `TEMPORARY_DEGRADATION`
- `ENDPOINT_CONGESTION`

Not supported by snapshot:

- hard packet loss
- interface RX/TX errors
- missing NAT/MSS
- route/DNS side effects
- dead peer
- runtime checker regression
