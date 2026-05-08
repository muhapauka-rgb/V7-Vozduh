# V7 Phase 62: Smart Client Profiles And Abroad RU Routing

Date: 2026-05-08

## Goal

Add a client-side policy layer to V7 so the system can generate profiles for real user apps, not only raw WireGuard configs.

Target clients:

- iPhone: Karing, Happ
- Android: Hiddify, Happ
- Desktop: Clash Verge Rev, Karing, with room for more adapters later

## Why This Is Needed

Karing proved an important pattern:

```text
ifconfig.me -> proxy/VLESS
gosuslugi.ru / esia / gu-st.ru -> DIRECT from phone by ru[geosite]
```

This works because the client itself can route by domain/geosite before traffic reaches V7.

Plain iOS WireGuard cannot do this by domain. WireGuard can split by IP ranges via `AllowedIPs`, but it cannot say:

```text
gosuslugi.ru -> DIRECT
youtube.com -> V7
```

Therefore V7 needs Smart Client Profiles for clients that support domain rules.

## Product Model

V7 becomes two coordinated layers:

```text
V7 Server Core
  - users
  - egress pool
  - health
  - sticky assignment
  - failover
  - server-side DIRECT_RU
  - server-side TRUSTED_RU_SENSITIVE

V7 Smart Client Profiles
  - Karing
  - Hiddify
  - Happ
  - Clash Verge Rev
  - client-side ru/geosite rules
  - location mode
  - profile selectors
```

## New Files

Added:

- `client/v7-client-adapters.registry`
- `client/v7-client-route-modes.registry`

These are metadata registries for the future profile generator/admin UI.

They contain no secrets.

## Adapter Priorities

Initial adapter strategy:

```text
iPhone:
  primary: Karing
  secondary: Happ

Android:
  primary: Hiddify
  secondary: Happ

Desktop:
  primary: Clash Verge Rev
  secondary: Karing
```

Each adapter records whether it supports:

- domain rules;
- geosite rules;
- selectors;
- QR/profile import;
- profile format.

## Route Modes

### RU_LOCAL

For a user physically in Russia or on a network accepted by RU services.

```text
RU public domains      -> DIRECT_CLIENT
RU sensitive domains   -> DIRECT_CLIENT
global/video/default   -> V7_GLOBAL
```

This is the Karing-like mode.

It is fast and solves Gosuslugi/banks only when the user's local network is accepted by those services.

### ABROAD_RU_VIA_V7

For a user travelling or living outside Russia.

```text
RU public domains      -> V7_DIRECT_RU
RU sensitive domains   -> V7_TRUSTED_RU_ABROAD
global/video/default   -> V7_GLOBAL
```

This requires a separate tested route for government/sensitive services.

Important:

`V7_TRUSTED_RU_ABROAD` must not mean "any Russian VPS". It must be a route candidate that passes real service tests:

```text
gosuslugi.ru TCP OK
gosuslugi.ru TLS OK
esia.gosuslugi.ru OK
nalog.gov.ru OK
major government portals OK
```

Until that route exists, the admin must show:

```text
ABROAD_RU_VIA_V7: RU sensitive unavailable / not guaranteed
```

### AUTO_TRAVEL

For users who move between Russia and abroad.

The generated client profile should include selectors:

```text
RU Mode:
  - Direct from phone
  - Via V7 Russia
  - Trusted RU Abroad
```

This lets an operator or user switch mode without regenerating the whole profile.

### STRICT_V7

For untrusted Wi-Fi or users who want everything to pass through V7.

```text
RU public domains      -> V7_DIRECT_RU
RU sensitive domains   -> V7_TRUSTED_RU_ABROAD
global/video/default   -> V7_GLOBAL
```

This mode gives more server-side control, but depends completely on V7 route health.

## Government Portal Route Class

We should split sensitive RU into clearer sub-classes:

```text
RU_PUBLIC
  yandex.ru, vk.com, ok.ru, lamoda.ru, ozon.ru, ordinary .ru

RU_BANKING
  alfabank.ru and other banks

RU_GOV
  gosuslugi.ru, esia.gosuslugi.ru, nalog.gov.ru, mos.ru, government portals

RU_GOV_ABROAD
  same target domains, but using a dedicated trusted path for users outside Russia
```

Current `TRUSTED_RU_SENSITIVE` remains valid as a safe umbrella until we split it.

## Important Rule

For client-side direct:

```text
DIRECT_CLIENT means V7 does not see or control that traffic.
```

So admin must show this clearly:

- client-side direct is faster;
- client-side direct can make Gosuslugi work in Russia;
- client-side direct may fail abroad;
- server-side diagnostics cannot fully validate client-side direct;
- leak protection for direct traffic is delegated to the client profile.

## Admin UX Requirement

Each user should eventually have:

```text
Client app: Karing / Hiddify / Happ / Clash Verge Rev
Platform: iOS / Android / Windows / macOS
Location mode: RU_LOCAL / ABROAD_RU_VIA_V7 / AUTO_TRAVEL / STRICT_V7
RU public route: ...
RU sensitive route: ...
Global route: ...
Profile version: ...
Last generated: ...
```

Operator actions:

- Generate profile
- Regenerate QR
- Switch location mode
- Show active route policy
- Explain why a service goes direct/V7/trusted path

## Immediate Next Implementation

1. Add smart client adapter metadata to admin.
2. Add route mode selector to user profile model.
3. Generate first Karing profile draft for one test user.
4. Add `RU_LOCAL` rules:
   - RU/geosite -> direct
   - global/video -> V7
5. Add `ABROAD_RU_VIA_V7` as a visible mode, but mark `RU_GOV_ABROAD` as unavailable until a tested route candidate exists.
6. Later generate Hiddify/Happ/Clash profiles from the same policy model.

## Decision

Yes, V7 should be optimized around these client apps.

This makes the project more realistic:

- simple for users;
- flexible for travel;
- better performance;
- closer to successful production VPN products;
- still keeps V7 server-core as the orchestration authority.

