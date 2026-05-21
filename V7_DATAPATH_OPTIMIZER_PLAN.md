# V7 Datapath Optimizer Plan

Date: 2026-05-21
Status: active plan

## Goal

V7 must treat WG/AWG egress channels as first-class high-speed production
paths. A VLESS client routed to a WG/AWG egress should keep throughput close to
the egress baseline measured directly from the V7 server.

Direct client-to-egress profiles are not the product target. The product target
is:

```text
client -> V7 ingress -> optimized V7 datapath -> selected egress
```

## Current Finding

The live VPS showed a registry/datapath mismatch:

- enabled egresses include `tun0`, `v7e356a192b79`, `awg0`, and `awg3`;
- live kill switch NAT/allow rules still referenced `tun0` and old `awg2`;
- `awg2` no longer exists;
- MSS clamp existed only for `wg0 -> tun0`, `wg0 -> awg2`, and `wg0 -> ens3`;
- fast channel `1` uses `v7e356a192b79` and was not covered by the live
  optimized datapath rules.

Server-side throughput baseline on 2026-05-21:

```text
tun0:           35-93 Mbps
v7e356a192b79: 189-199 Mbps
awg0:          0.86-2.09 Mbps
awg3:          1.59-2.46 Mbps
```

The fast WG/AWG egress exists; the next task is to make client-through-V7 paths
preserve that speed.

## Phase 1: Registry-Driven Datapath

Every enabled egress in `/opt/v7/egress/state/egress.registry` with an
`interface=` value must receive:

- NAT/MASQUERADE for V7 client subnets;
- forward allow rules;
- TCP MSS clamp rules;
- health/reconcile checks that fail when any enabled egress is missing coverage.

This removes hardcoded `awg2/tun0` assumptions.

## Phase 2: MTU/MSS Probe

For each enabled egress interface, V7 probes DF payload sizes and computes:

- safe payload;
- safe path MTU;
- recommended TCP MSS;
- conservative fallback profile.

Initial profile ladder:

```text
performance:  MTU 1420, MSS route-derived
balanced:     MTU 1380, MSS 1340/1320
safe:         MTU 1280, MSS 1240
ultra-safe:   MTU 1240, MSS 1200
```

## Phase 3: Path Matrix Benchmark

V7 must benchmark pairs, not just channels:

```text
VLESS ingress -> VLESS egress
VLESS ingress -> WG/AWG egress
WG/AWG ingress -> VLESS egress
WG/AWG ingress -> WG/AWG egress
```

Each row stores throughput, latency, loss, retry symptoms, selected MTU/MSS
profile, and freshness.

Initial implementation:

- `v7-path-benchmark` builds `/opt/v7/egress/state/path-benchmark.json`;
- server-side rows are measured immediately with `curl --interface`;
- MTU rows are measured with DF ping payload probes;
- NAT/MSS datapath coverage is read from `nft`;
- `v7-client-speed-api` keeps saving normal client speed results and also
  mirrors successful `mode=v7` measurements into
  `/opt/v7/egress/state/path-samples.json`;
- client ingress rows remain pending until a VLESS/WG client path sample is
  posted.

The first JSON schema is:

```text
v7-path-benchmark/v1
```

The important distinction is deliberate:

```text
server_to_egress: measured by V7 itself
vless_ingress_to_egress: requires client/agent sample
wg_ingress_to_egress: requires client/agent sample
```

The path-sample ingestion is additive: if it fails, `/api/sample` still returns
success after the original client speed result is saved. This keeps the rollout
safe for the running server.

Admin-triggered client speed commands now carry `ingress_type` metadata, so
samples are routed into the right matrix row instead of being mixed together.

## Phase 4: Auto Optimization Loop

If a path is below target, V7 tries profiles in order and saves the fastest
stable one.

Suggested gates:

- production target: at least 85-95% of server-side egress baseline;
- warning: 60-85%;
- quarantine/manual-only: below 60% or unstable.

The goal is not to avoid WG egresses. The goal is to tune WG egress paths until
they can be selected automatically.

Initial guarded implementation:

- `v7-path-optimizer-advice` reads `path-benchmark.json`;
- compares client path samples to the server-side egress baseline;
- classifies each egress as `production_candidate`, `needs_tuning`,
  `manual_only`, `pending_client_samples`, `datapath_incomplete`, or
  `baseline_failed`;
- writes `/opt/v7/egress/state/path-optimizer-advice.json`;
- does not switch users, rewrite routes, or change MTU/MSS settings.

## Phase 5: Admin UX

The Admin UI should show:

```text
channel baseline speed
VLESS ingress path speed
WG ingress path speed
selected MTU/MSS profile
datapath coverage status
production/quarantine/manual-only decision
```

Operators should see whether a channel is slow because the provider is slow or
because V7 datapath tuning is incomplete.
