# Runtime Identity Snapshot

Evidence source:

```text
docs/track7/truth-snapshot/evidence/section-runtime-identity.txt
docs/track7/truth-snapshot/evidence/section-systemd-v7.txt
docs/track7/truth-snapshot/evidence/section-processes.txt
```

## Host

```text
hostname=v3119922.hosted-by-vdsina.ru
os=Ubuntu 26.04 LTS
kernel=Linux 7.0.0-14-generic
virtualization=kvm
uptime=18 days, 22:12 at 2026-05-25T11:08:23Z snapshot
```

## Interfaces

Observed interfaces:

```text
ens3 public interface
wg0 client WireGuard subnet
tun0 VLESS/sing-box egress
awg0
awg3
v7e356a192b79
v7edb0c189291
v7e06a394c478
```

## Active V7 Services

Active/running or active/exited V7 services include:

```text
v7-admin-api.service active/running
v7-api.service active/running
v7-benchmark.service active/running
v7-client-speed-api.service active/running
v7-egress-openvpn@v7edb0c189291.service active/running
v7-health.service active/running
v7-killswitch.service active/exited
v7-mss-clamp.service active/exited
v7-proxy-inbound-happ-test.service active/running
v7-public-gateway.service active/running
v7-routing-sync.service active/exited
```

## Active Timers

Observed V7 timers:

```text
v7-telegram-sentinel.timer
v7-users-autoswitch.timer
v7-egress-quality-compact.timer
v7-path-sanity.timer
v7-path-guard-repair.timer
v7-direct-autosync.timer
v7-service-matrix-refresh-all.timer
v7-traffic-collector.timer
```

## Runtime Manifests

Runtime baseline marker found:

```text
/opt/v7/ops/deploy-baseline/20260523T122251Z/manifest.json
```

Local release object check still reports the local runtime manifest path as not supplied/available locally, so release provenance remains incomplete from repo perspective.

## Identity Verdict

Runtime is alive and service-rich. V7 has multiple active service surfaces and multiple egress interfaces. The host is not quiet: autoswitch, telemetry, public gateway, admin API, and path/proxy components are active.
