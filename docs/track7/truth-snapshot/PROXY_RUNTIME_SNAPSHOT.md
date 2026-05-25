# Proxy Runtime Snapshot

Evidence source:

```text
docs/track7/truth-snapshot/evidence/section-proxy-telemetry-admin.txt
```

## Services

Active services:

```text
v7-admin-api.service active/running
v7-client-speed-api.service active/running
v7-proxy-inbound-happ-test.service active/running
v7-public-gateway.service active/running
```

Inactive service units:

```text
v7-path-guard-repair.service inactive/dead
v7-path-sanity.service inactive/dead
```

## Listening Surfaces

Observed listeners include:

```text
0.0.0.0:80 python3 public gateway
*:443 caddy
127.0.0.1:7080 admin API
10.0.0.1:7090 client speed API
127.0.0.1:1080 sing-box
0.0.0.0:1443 sing-box
0.0.0.0:1445 sing-box
```

## Runtime Guard / Exposure

Proxy runtime is active and publicly exposed through gateway/Caddy/sing-box surfaces. This is operationally necessary but high blast radius if proxy apply tools are used incorrectly.

## Verdict

Proxy runtime appears active and serving. It is not proven safe for mutation. Proxy apply/guard apply/public enable/disable remain forbidden without separate approval.
