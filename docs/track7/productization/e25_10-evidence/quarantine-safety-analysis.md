# E25.10 Quarantine And Safety Analysis

## Result

`safe_for_normalization=true`

`endpoint_self_reference=false`

`unsafe_hooks_detected=false`

`raw_profile_executed=false`

## VPS Import

- host: `v3119922.hosted-by-vdsina.ru`
- checked_at_utc: `2026-05-28T14:31:04Z`
- imported_profile: `/root/v7-execution-profile-import/e25_10_operator_amnezia_for_awg.conf`
- mode_owner: `600 root:root`
- size: `462`
- sha256: `d6029f2b6e4d33afd458d3b9a4bd18ad436c1b4de4a6ee78b4194213f8448ce8`

## Tooling

- `awg-quick`: `/usr/bin/awg-quick`
- `awg`: `/usr/bin/awg`
- `wg-quick`: `/usr/bin/wg-quick`
- `wg`: `/usr/bin/wg`

## Profile Classification

- protocol: `amneziawg`
- route/nft hooks: `absent`
- DNS side effect: `present`
- IPv4 full tunnel: `present`
- IPv6 full tunnel: `present`
- `Table=` setting: `absent`

The raw profile is not safe for direct startup. It is safe to normalize because it has no route/firewall hooks and can be wrapped with `Table=off` plus DNS removal.

## Endpoint Check

- endpoint_port: `34403`
- endpoint_host_sha256: `b89a5f0aa892457a9ffc47fa76e2338d188090b92df54235f158c3d1126505f0`
- endpoint route: external route via `ens3`
- self/local endpoint detected: `false`

The endpoint is not routed via `lo`, unlike the known-dead self-referential profile from E25.7.

## Runtime Baseline

- `v7execwg0_absent=true`
- `v7execawg0_absent=true`
- `users.registry` SHA256: `bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- `egress.registry` SHA256: `a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`
- candidate row: `ip=10.7.0.11 current=1 table=1009 enabled=1`

## Decision

Proceed to V7 normalization only. Raw unsafe profile execution remains forbidden.
