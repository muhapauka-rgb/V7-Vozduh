# E25.12 Quality Recovery Attempts

## Scope

Target-local quality recovery only.

- target: `amneziawg-exec-20260528-10-8-1-14`
- interface: `v7execwg0`
- candidate user: `10.7.0.11`
- user movement performed: `false`
- routing mutation for users performed: `false`
- autoswitch apply performed: `false`
- kill-switch control/toggle mutation performed: `false`

## Attempt 1: MTU Variant Probe

The first probe tested `MTU=1200`, `1280`, `1360`, and `1420` with target-local Cloudflare download probes through `v7execwg0`.

The first script had a parser bug in the computed `mbps` field, so the verdict uses the raw `curl speed_download` values. The raw data still showed the important shape:

| MTU | Avg Mbps | Min Mbps | Max Mbps | Notes |
| ---: | ---: | ---: | ---: | --- |
| 1200 | 38.25 | 27.24 | 45.87 | Best short-run min throughput. |
| 1280 | 27.77 | 9.58 | 50.76 | Repeated floor breaches around `9.6 Mbps`. |
| 1360 | 33.61 | 18.56 | 51.55 | Good short-run throughput. |
| 1420 | 31.34 | 14.04 | 45.67 | Passes short-run floor, but less conservative. |

## Attempt 2: Clean Comparison, 1200 vs 1360

Command:

`bash /tmp/e25_12_mtu_compare.sh`

The script changed only the target-local interface MTU during the probe, restored the original MTU at completion, and ran runtime checkers after each variant.

### MTU 1200

Ping:

`5 packets transmitted, 5 received, 0% packet loss, rtt min/avg/max/mdev = 26.740/31.430/40.056/5.048 ms`

Download samples:

| Sample | Mbps |
| ---: | ---: |
| 1 | 22.85 |
| 2 | 38.82 |
| 3 | 16.29 |
| 4 | 15.26 |
| 5 | 22.34 |
| 6 | 37.74 |
| 7 | 43.11 |
| 8 | 38.69 |

Verdict:

- avg Mbps: `29.39`
- min Mbps: `15.26`
- no sample below `10.0 Mbps`: `true`
- stable enough for sustained revalidation: `true`

### MTU 1360

Ping:

`5 packets transmitted, 5 received, 0% packet loss, rtt min/avg/max/mdev = 28.673/156.690/565.562/205.106 ms`

Download samples:

| Sample | Mbps |
| ---: | ---: |
| 1 | 3.67 |
| 2 | 27.09 |
| 3 | 43.87 |
| 4 | 42.21 |
| 5 | 13.48 |
| 6 | 10.68 |
| 7 | 18.42 |
| 8 | 21.68 |

Verdict:

- avg Mbps: `22.64`
- min Mbps: `3.67`
- no sample below `10.0 Mbps`: `false`
- jitter spike observed: `true`
- stable enough for sustained revalidation: `false`

## Selected Recovery

Selected MTU:

`1200`

Reason:

`MTU=1200` was the only tested value that passed both clean comparison requirements: every sample stayed above the `10.0 Mbps` min floor and ping jitter stayed bounded.

## Applied Change

Applied on VPS:

- backup: `/etc/amnezia/v7execwg0.conf.e25_12_mtu1280_backup`
- config: `/etc/amnezia/v7execwg0.conf`
- active interface: `v7execwg0`
- new MTU: `1200`

Verification output:

```text
mtu_recovery_applied=true
backup=/etc/amnezia/v7execwg0.conf.e25_12_mtu1280_backup
config_mtu=MTU = 1200
link=450: v7execwg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1200 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000\    link/none
default_route_unchanged=true
dns_unchanged=true
table_1009_unchanged=true
users_registry_unchanged=true
v7_reconcile_check=OK
v7_user_route_check=OK
v7_killswitch_check=OK
v7_provisioning_reconcile_check=OK
```

## Safety Verdict

- `quality_recovery_attempted=true`
- `unsafe_changes_made=false`
- `runtime_mutation_performed=true`
- `runtime_mutation_scope=target-local MTU recovery for v7execwg0 only`
- `user_movement_performed=false`
- `routing_mutation_for_users=false`
