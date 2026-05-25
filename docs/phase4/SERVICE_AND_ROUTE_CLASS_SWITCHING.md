# V7 Phase 4 - Service And Route-Class Aware Switching

## Purpose

Not every degradation is a global outage.

Autoswitch must understand affected service, route class, and user impact.

## Service-Aware Rules

Examples:

- Telegram degraded while YouTube is OK: consider `GLOBAL_STABLE`/Telegram-aware decision, not full platform reroute.
- YouTube degraded while general HTTPS is OK: treat as video/service class issue.
- Trusted RU unavailable: do not fallback unsafely to direct/global path.
- Direct routing broken: do not infer global egress failure.

## Route Classes

Decisions must respect:

- `GLOBAL_FAST`;
- `GLOBAL_STABLE`;
- `DIRECT_RU`;
- `TRUSTED_RU_SENSITIVE`.

## Current Implementation Alignment

Current autoswitch:

- derives route class from important services;
- can force `--service` and `--route-class`;
- gates Telegram specially;
- uses route class fitness from service matrix;
- blocks trusted RU unless candidate metadata marks trusted.

## Missing Future Work

Future phases should make direct/RU and trusted RU observability feed explicit autoswitch recommendations without enabling unsafe automatic fallback.
