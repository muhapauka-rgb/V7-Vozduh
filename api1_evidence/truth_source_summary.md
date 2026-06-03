# API.1 Truth Source Summary

The generated `truth_source_map.json` records static state references per endpoint block. Static endpoint blocks often call helpers whose state files are outside the immediate branch body; this is why many endpoints appear under `no_static_state_ref`. The authoritative truth-source model below combines static endpoint data with named constants and helper ownership found in `admin/v7-admin-api`.

## Runtime And Admin Truth Sources

| Truth source | Current owner in admin API | Responsibility | Extraction safety |
|---|---|---|---|
| `/opt/v7/egress/state/users.registry` | registry/read models, user actions, planner previews | User runtime state and current egress assignment | Read-only wrappers only |
| `/opt/v7/egress/state/egress.registry` | registry/read models, egress lifecycle, service routing | Egress/channel inventory and lifecycle state | Read-only wrappers only |
| `/opt/v7/egress/state/v7-state.json` | state/overview helpers | Runtime summary state | Read-only summaries first |
| `/opt/v7/audit/audit.jsonl` | `audit_admin`, audit views | Admin/runtime audit stream | Read-only search/export first; writer stays |
| `/opt/v7/events` | event views | Event timeline files | Read-only extraction safe |
| `/etc/v7/admin/auth.json` | auth/session/account actions | Admin users, roles, password hashes, sessions | Do not extract first |
| `/etc/v7/admin/safe-mode.json` | safe-mode checks and action gates | Safe-mode policy state | Do not extract first |
| `/etc/v7/maintenance.conf` | maintenance settings endpoints | Maintenance cleanup/log policy | Do not extract first |
| `/etc/v7/egress-drafts` | egress draft lifecycle | Draft egress configs | Preview parsers only |
| `/opt/v7/admin/egress-draft-tests` | egress draft test history | Draft validation/test results | Read-only summary safe |
| `/etc/v7/egress-runtime` | runtime egress configs/backups | Runtime egress prepared configs | Read-only inventory only |
| `/opt/v7/admin/v7-identity.db` | identity/onboarding/device/org flows | Identity users, devices, groups, orgs, onboarding | Read-only query builders only |
| `/etc/v7/policy.json` | policy state/actions | Routing and policy config | Do not extract writes first |
| `/etc/v7/org-egress-policy.json` | org/group routing policy | Organization/group egress policy | Read-only model first |
| `/opt/v7/policy/route-classes.registry` | route-class/service-aware logic | Route class definitions | Read-only parser safe |
| `/opt/v7/egress/state/profile-delivery-tokens.json` | profile delivery/public import | Profile delivery token state | Do not extract first |
| `/opt/v7/egress/state/service-matrix.json` | service matrix summaries | Service health/cache matrix | Read-only summaries safe |
| `/opt/v7/egress/state/trusted-ru-diagnostic.state` | Trusted RU views/actions | Trusted RU diagnostic result state | Read-only summaries first |
| `/opt/v7/egress/state/trusted-ru-decision.state` | Trusted RU decision views/actions | Trusted RU decision state | Read-only summaries first |
| `/etc/v7/direct/domains.conf` | direct domain actions | Direct routing domain list | Do not extract writes first |
| `/etc/v7/policy` | policy domain files/backups | Policy domain stores | Read-only inventory only |
| `/opt/v7/traffic/traffic.sqlite` | traffic snapshots | Traffic history and live stats | Cached/background summary preferred |

## Generated Static Truth Source Buckets

| Static bucket | Endpoint count | Interpretation |
|---|---:|---|
| `no_static_state_ref` | 248 | Endpoint branch does not directly reference a tracked file constant; many call helpers. |
| `/opt/v7/egress/state` | 25 | Direct runtime state dependency in endpoint block. |
| `/etc/v7/maintenance.conf` | 2 | Direct maintenance config write/read endpoint dependency. |
| `/opt/v7/admin/v7-identity.db` | 2 | Direct identity DB endpoint dependency. |

## Truth Source Ownership Rules

1. Runtime registries remain authoritative in `/opt/v7/egress/state`.
2. Admin auth and safe mode remain authoritative in `/etc/v7/admin`.
3. Identity state remains authoritative in `/opt/v7/admin/v7-identity.db`.
4. Runtime action tools remain authoritative for actual movement, apply, rollback, and system changes.
5. `admin_core/operator_execution.py` remains canonical for operator execution packets and governance contract shape.
6. `admin_core/operator_observability.py` remains the preferred home for read-only timeline, audit, evidence, and operation-detail views.
7. `admin_core/routing_brain.py` and `admin_core/routing_intelligence.py` remain canonical for RI advisory scoring and explanation contracts.

## Extraction Implication

API.2 can safely begin only if it extracts read-only adapters that preserve these truth sources. It must not create new stores, mirror mutable state, or introduce a second admin/runtime authority.
