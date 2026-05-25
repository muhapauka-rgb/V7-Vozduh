# Trusted RU Decision Governance

This document is static governance only. It does not approve running Trusted RU diagnostics, refresh, decision writes, policy apply, routing sync, autoswitch, or Direct/RU mutation.

## Tools

| Tool | Reads | Writes | Network / Gosuslugi | Downstream Influence |
|---|---|---|---|---|
| `v7-trusted-ru-diagnostic` | Trusted RU domains, Direct/RU route evidence, DNS/probe results | `/opt/v7/egress/state/trusted-ru-diagnostic.state` | Yes. Probes Gosuslugi/Trusted RU domains over direct, browser-like direct, VLESS/SOCKS, AWG, TLS | Feeds decision and operator workflows |
| `v7-trusted-ru-decision` | `trusted-ru-diagnostic.state`, `/etc/v7/policy/trusted_ru_sensitive_domains.conf` if present | Only with `--write-state`: `/opt/v7/egress/state/trusted-ru-decision.state` | No direct probe observed | Emits `TRUSTED_RU_SENSITIVE` decisions and can persist them |
| `v7-trusted-ru-refresh-missing` | `trusted-ru-decision.state` | Indirectly diagnostic state, decision state, and state JSON through called tools | Yes, through `v7-trusted-ru-diagnostic` | Recomputes Trusted RU decision state |

## Decision Boundary

Trusted RU has three separate layers:

| Layer | Evidence | Mutation | Notes |
|---|---|---|---|
| Diagnostic observation | `trusted-ru-diagnostic.state` | diagnostic-state-write | Not read-only; live probes are Gosuslugi-sensitive |
| Decision preview/state | `v7-trusted-ru-decision` | optional decision-state-write | No route apply, but output can influence operators |
| Refresh missing | `v7-trusted-ru-refresh-missing` | diagnostic-state-write, decision-state-write | Calls live diagnostic for missing domains |

`v7-trusted-ru-decision` classifies domains into decisions such as `DIRECT_OK`, `BROWSER_LIKE_DIRECT_OK`, `USE_TEMP_VLESS`, `USE_AWG`, `MISSING_DIAGNOSTIC`, or `NO_SAFE_PATH`. That is a decision preview/state layer, not route application.

## Gosuslugi-Sensitive Behavior

Default decision domains include:

```text
www.gosuslugi.ru
gosuslugi.ru
esia.gosuslugi.ru
lk.gosuslugi.ru
alfa-mobile.alfabank.ru
```

If `/etc/v7/policy/trusted_ru_sensitive_domains.conf` exists, the decision tool reads it instead. The fallback defaults mean that even a simple Trusted RU decision report can expose sensitive routing status for public-service domains.

## Calls Not Observed

The inspected Trusted RU decision/refresh tools do not directly call:

```text
v7-policy-apply
v7-policy-resolve
v7-routing-sync
v7-users-autoswitch
nft
ip route
ip rule
```

This does not make them safe to run. Their state can influence downstream workflows and operator decisions.

## Risk

| Risk | Source | Control |
|---|---|---|
| Stale state interpreted as route truth | diagnostic/decision state files | Require freshness checks before any operator decision |
| Failed probes causing wrong path selection | diagnostic probes/timeouts | Separate probe failure from service blocking |
| Hidden mutation in refresh | `refresh-missing` calls diagnostic and decision write | Treat refresh as state mutation, never as read-only |
| Gosuslugi behavior change | downstream route/policy consumers | No route/policy execution without canary and rollback |

## Allowed Later

- Static inspection.
- Offline fixture tests for state parsing.
- Operator preview that clearly labels stale/missing/probe-failed state.

## Forbidden Without Separate Approval

- `v7-trusted-ru-diagnostic`
- `v7-trusted-ru-decision --write-state`
- `v7-trusted-ru-refresh-missing`
- Any policy/routing/autoswitch action derived from Trusted RU state.

