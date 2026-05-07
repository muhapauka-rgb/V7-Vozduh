# V7 Phase 59: Karing Route Behavior Hypothesis

Date: 2026-05-07

## Context

The user confirmed that the iPhone app used for the direct VLESS test is Karing.

This matters because Karing is not only a simple VLESS client. It is a rule-based proxy utility that supports Clash/V2Ray/sing-box subscriptions, custom routing rule groups, and traffic splitting.

Public project/app descriptions indicate:

- Karing supports rule-based routing.
- Karing supports multiple subscription/config formats.
- Karing uses a sing-box kernel by default.

## Why This Changes The Diagnosis

The earlier assumption was:

```text
Karing direct VLESS opens Gosuslugi
therefore Gosuslugi works through VLESS exit 77.110.103.131
```

That is not yet proven.

The controlled V7 trace proves:

```text
iPhone -> V7 WireGuard -> tun0 -> VLESS -> Gosuslugi
```

and this path fails after TCP setup/TLS ClientHello.

The isolated server tests also prove:

```text
VPS -> sing-box VLESS -> Gosuslugi: timeout
VPS -> Xray VLESS -> Gosuslugi: timeout
```

But Karing may be doing:

```text
ifconfig.me -> VLESS
gosuslugi.ru -> DIRECT from phone/mobile/RU ISP
```

In that case both observations are true:

- `ifconfig.me` shows `77.110.103.131`;
- Gosuslugi opens;
- but Gosuslugi was not necessarily using the VLESS exit.

## Current Most Likely Explanation

Karing probably has routing/splitting behavior that sends sensitive RU or regional domains through a different path than generic global IP-check services.

This fits all observed facts:

- V7 routes Gosuslugi through VLESS and fails.
- Server-side sing-box VLESS fails for Gosuslugi.
- Server-side Xray VLESS fails for Gosuslugi.
- Karing opens Gosuslugi while generic IP checks show VLESS IP.
- Karing is rule-based and may route different domains differently.

## Required Proof

We need to inspect Karing's live connection/routing decision for `www.gosuslugi.ru`.

The proof should answer one question:

```text
When Karing opens Gosuslugi, is that connection using VLESS/proxy or DIRECT?
```

Useful evidence:

- Karing connection list / active connections screen while opening Gosuslugi.
- Karing route/rule match details for `gosuslugi.ru`.
- Exported Karing config ZIP/profile with secrets redacted.
- A screenshot showing the selected route/group for the Gosuslugi connection.

## V7 Decision

Do not change the V7 policy layer yet.

Current V7 policy is correct:

- `.ru` direct works for normal RU sites.
- sensitive RU is excluded from broad direct.
- sensitive RU currently prefers `vless`.
- no direct leak to `ens3` was observed.

Next implementation should add a diagnostic/admin concept:

```text
Observed Client Route
```

This lets V7 compare:

- what V7 thinks should happen;
- what the client app actually does;
- which route opened the target service.

## Future Product Direction

For sensitive RU services, V7 should support explicit route recipes:

- `DIRECT_RU_PUBLIC`
- `TRUSTED_RU_SENSITIVE`
- `GLOBAL_PROXY`
- `VIDEO_GLOBAL`

But the `TRUSTED_RU_SENSITIVE` path cannot be marked solved until we have a proven route that opens Gosuslugi from the V7 node, not only from a phone app with its own routing rules.

