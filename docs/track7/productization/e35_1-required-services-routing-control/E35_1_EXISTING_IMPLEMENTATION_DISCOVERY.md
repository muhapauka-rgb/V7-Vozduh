# E35.1 Existing Implementation Discovery

Block: E35.1 Required Services & Routing Control Model
Mode: architecture + discovery + safe implementation planning
Runtime mutation: NO
User movement: NO
Routing/apply/autoswitch apply: NO

## Executive Verdict

existing_implementation_discovered=true

V7 already has a substantial routing-control substrate, but it is split across admin state, service preferences, service matrix, identity groups, org-egress policy, autoswitch gates and proposal/evidence surfaces.

What already exists:

- Service catalog and route-class service map in `admin/v7-admin-api`.
- Per-user service preferences stored in `SERVICE_PREFS_FILE` and edited via `/api/actions/service-preferences-update`.
- Service matrix normalization and route-class fitness in `normalize_service_matrix_row()` and `service_matrix_route_fitness()`.
- Service-aware recommendation and route dry-run logic in `service_recommendations()` and `service_aware_route_dry_run()`.
- Identity DB tables for `groups`, `organizations`, `allowed_users`, `identity_users`, and group route policy.
- Org/group egress policy file `/etc/v7/org-egress-policy.json`, exposed through `/api/org-egress-policy` and `/api/actions/org-egress-policy-update`.
- Autoswitch group gates in `tools/v7-users-autoswitch`: `allowed_egress`, `preferred_egress`, `excluded_egress`, `exclusive_group`, egress group ACL and isolation.
- Autoswitch suitability gates for basic health, reservation/canary, group policy, quality floors, required services, capacity/load and safety.
- Admin UI surfaces in `/admin-v2`: Users, Channels, Routing, Settings, Evidence, Proposals, Runtime Trust and Release Trust.

What can be reused:

- `SERVICE_CATALOG`, `KNOWN_SERVICES`, `DEFAULT_USER_PRIORITY_SERVICES`, `ROUTE_CLASS_SERVICE_MAP`.
- `service_preferences_state()`, `normalize_services()`, `user_priority_services_from_pref()`, `update_service_preferences()`.
- `service_matrix_state()`, `normalize_service_matrix_row()`, `service_matrix_route_fitness()`.
- `service_recommendations()` and proposal/evidence linkage.
- Identity DB group/organization tables and admin Users -> Organizations surface.
- `org_egress_policy_state()` and `sanitize_org_egress_policy()` as a starting point for group routing policy.
- Autoswitch gates `_gate_org()`, `_gate_quality()`, `_gate_service()`, `_gate_load()`, `_gate_safety()` as implementation evidence for the intended priority chain.
- Existing admin drawers/chips/cards and hardening search drawer.

What needs extension:

- A single read-only "effective routing controls" model per user.
- Explicit group model semantics that evolve Organizations -> Groups without duplicating identity truth.
- Group-level required services and allowed channels as first-class admin concepts.
- Routing mode semantics: `AUTO`, `OPERATOR_PINNED`, future-reserved `MANUAL`.
- Preferred channel field and pinned behavior; current `current` egress and sticky score are not enough.
- Channel suitability endpoint/summary that explains hard blocks vs soft preferences.
- Tests for required-service merge, group allowlist, routing modes and speed-not-overriding-hard-blocks.

What must not be touched in E35.1:

- `v7-user-switch`.
- `v7-routing-sync`.
- `v7-users-autoswitch --apply`.
- Direct RU refresh/apply.
- Trusted RU diagnostic/refresh mutations.
- Kill switch mutation.
- Production service restart.
- Runtime files under `/opt/v7`, `/etc/v7`, `/etc/wireguard`.

## Inventory Table

| Capability | Existing file/function/API/UI | Current behavior | Classification | Risk | Evidence |
|---|---|---|---|---|---|
| Service catalog | `admin/v7-admin-api` `SERVICE_CATALOG` | Defines Google, Google Auth, YouTube, Telegram, Apple, Instagram, WhatsApp, Facebook, Spotify, SoundCloud, ChatGPT, OpenAI Auth, Claude, Anthropic. | Reuse | Low | `admin/v7-admin-api:300` |
| Default user services | `DEFAULT_USER_PRIORITY_SERVICES` | Defaults to YouTube, Instagram, Telegram, Google, Google Auth. | Extend | Medium | `admin/v7-admin-api:316` |
| Route-class service map | `ROUTE_CLASS_SERVICE_MAP` | Maps services to `GLOBAL_FAST`, `GLOBAL_STABLE`, `VIDEO_OPTIMIZED`, `LOW_LATENCY`. | Reuse | Low | `admin/v7-admin-api:318` |
| User service preferences store | `SERVICE_PREFS_FILE` | Stores enabled flag and per-user services. | Extend | Medium | `admin/v7-admin-api:92`, `service_preferences_state()` |
| Service preferences API | `POST /api/actions/service-preferences-update` | Updates enabled/per-user services with auth, CSRF, admin role and audit. Does not move users. | Reuse | Low | `admin/v7-admin-api:32969` |
| Service preferences UI | Users drawer/settings surfaces | Operator can choose services for users and toggle service preference logic. | Extend | Medium | `admin/v7-admin-api:21222`, `28804` |
| Service matrix | `service_matrix_state()` | Normalizes service results, status and route-class fitness. | Reuse | Low | `admin/v7-admin-api:12661` |
| Route-class fitness | `service_matrix_route_fitness()` | Determines per-route-class status from required class services. | Reuse | Low | `admin/v7-admin-api:1552` |
| User service recommendation | `service_recommendations()` | Compares current egress with best egress per required services and creates manual-review recommendations. | Extend | Medium | `admin/v7-admin-api:12790` |
| Service-aware route dry run | `service_aware_route_dry_run()` | Scores route-class candidates and previews route changes. | Reuse | Low | `admin/v7-admin-api:13148` |
| Route candidate score | `egress_candidate_score()` | Rejects disabled/manual/strict-sensitive candidates; scores health, role, matrix, Telegram, priority, weight, speed and reserve penalty. | Refactor later | Medium | `admin/v7-admin-api:13140` |
| Group identity table | SQLite `groups` | Stores id, name, description, `route_policy`, timestamps. | Extend | Medium | `admin/v7-admin-api:1765` |
| Organization identity table | SQLite `organizations` | Stores org metadata and `group_id`. | Reuse | Low | `admin/v7-admin-api:1774` |
| Identity group upsert | `/api/actions/identity-group-upsert` | Creates/updates groups, admin role. | Extend | Medium | `admin/v7-admin-api:573`, `2278` |
| Identity organization upsert | `/api/actions/identity-organization-upsert` | Creates/updates organizations and group link. | Reuse | Low | `admin/v7-admin-api:574`, `2308` |
| Group route policy | `identity_effective_smart_mode()` | Uses group `route_policy` as smart client mode default. | Extend | Medium | `admin/v7-admin-api:2580` |
| Org-egress policy store | `ORG_POLICY_FILE` | JSON policy with default group/isolation, user_groups, groups and egress metadata. | Extend | Medium | `admin/v7-admin-api:67`, `12736` |
| Org-egress policy API | `/api/org-egress-policy`, `/api/actions/org-egress-policy-update` | Read/write policy with confirmation and audit. | Extend | Medium | `admin/v7-admin-api:29946`, `31960` |
| Autoswitch group assignment | `tools/v7-users-autoswitch` User.group | User group inferred from registry/org policy/user_groups/groups users. | Reuse | Medium | `tools/v7-users-autoswitch:652` |
| Autoswitch required services | `_required_services()`, `_important_services()` | Merges global policy/service prefs/defaults plus per-user prefs and CLI service. | Extend | Medium | `tools/v7-users-autoswitch:855` |
| Autoswitch group gates | `_gate_org()` | Hard-blocks not allowed, excluded, exclusive group, egress ACL and exclusive isolation; marks preferred. | Reuse | Low | `tools/v7-users-autoswitch:1356` |
| Autoswitch quality gates | `_gate_quality()` | Hard-blocks avg below 15, floor below 10, stability below 0.45. | Reuse | Low | `tools/v7-users-autoswitch:1379` |
| Autoswitch service gates | `_gate_service()` | Hard-blocks Trusted RU mismatch, Telegram hard states, persistent/multiple service failures and route-class FAIL. | Reuse | Low | `tools/v7-users-autoswitch:1428` |
| Autoswitch load gate | `_gate_load()` | Hard-blocks planned/failover target when hard/full. | Reuse | Low | `tools/v7-users-autoswitch:1335` |
| Autoswitch safety gate | `_gate_safety()` | Hard-blocks quarantine, failed verification limits, blocked target and pair reversal. | Reuse | Low | `tools/v7-users-autoswitch:1344` |
| Autoswitch scoring | `_score_parts()` | Scores health, service, Telegram, speed, stability, latency, load, quality history, priority, weight, sticky, org preference and reserve penalty. | Reuse | Medium | `tools/v7-users-autoswitch:1512` |
| Current-channel stickiness | `_score_parts()` sticky and `_score_without_sticky()` | Current route gets sticky score; rebalance uses score without sticky threshold. | Extend | Medium | `tools/v7-users-autoswitch:1245`, `1540` |
| Explicit pinned channel | none found | No separate `preferred_channel`/`pinned`/per-user `AUTO/PINNED/MANUAL` field. | Extend | Medium | `docs/track7/productization/e35_0-audit/user-pinning-audit.md` |
| Channel manual only | `manual_only`, role `MANUAL_ONLY` | Channel-level automation exclusion. Not a user routing mode. | Reuse | Low | `admin/v7-admin-api:390`, `tools/v7-users-autoswitch:1311` |
| Execution-only target | role `EXECUTION_ONLY` | Separate governed movement target; must not be autoswitch eligible. | Do Not Touch | High | `tools/v7-second-canary-target-readiness:276` |
| Evidence | `/api/evidence`, chips/drawer | Read-only explanation linked to objects. | Reuse | Low | `admin/v7-admin-api:29514`, `18551` |
| Proposal | `/api/proposals`, cards/drawer | Read-only recommendation linked to evidence; non-authoritative. | Reuse | Low | `admin/v7-admin-api:29540`, `18768` |
| Runtime Trust | `/api/runtime/convergence` | Read-only runtime trust/drift surface. | Reuse | Low | `admin/v7-admin-api:29566` |
| Release Trust | `/api/release/current` | Read-only release trust surface. | Reuse | Low | `admin/v7-admin-api:29585` |
| Approval packet governance | `admin_core/operator_execution.py` | Validates packet, runtime hashes, replay, selected moves and audit. | Do Not Touch | High | `admin_core/operator_execution.py:89` |

## Gap List

### Missing Group Model Pieces

- Current Organizations are identity/admin metadata, while Groups are partially present through identity DB and org policy.
- There is no single "Group Routing Control" object visible to operators with allowed channels, required services, default routing mode and audit history.
- `org-egress-policy.json` has useful mechanics, but its semantics are not yet formalized as the universal group constraint source for every routing/proposal/execution path.
- Group-level required services are not first-class in admin UX.

### Missing Hard Block Semantics

- Autoswitch implements many hard blocks, but admin/proposal surfaces do not expose a single hard-block matrix per user/channel.
- Required services are partially hard in autoswitch, but E35 needs explicit product semantics for when service failure is hard vs degraded/review-required.
- Execution-time recheck does not yet explicitly require group allowed channels and required-services suitability for future autonomous movements.

### Missing Routing Mode Semantics

- No explicit per-user `routing_mode=AUTO|OPERATOR_PINNED|MANUAL`.
- No explicit `preferred_channel` field for `OPERATOR_PINNED`.
- Current `current` egress is runtime state, not an operator preference.
- Current sticky score keeps the current route, but does not equal a pinned channel contract.

### Missing Admin Surface Pieces

- User drawer needs "Effective Required Services", "Routing Mode", "Preferred Channel", "Group", "Group allowed channels", "Suitability of current channel", and "Why this user is here".
- Channel drawer needs group allowlist summary and "users blocked from this channel and why".
- Settings needs a Groups routing-control editor that reuses existing Settings/Organizations areas.
- Routing needs explicit service-aware hard-block reasons.
- Main page should show only summary indicators: unsuitable users, restrictive groups, degraded required services.

### Missing Tests

- Required service merge: group baseline + user additions.
- No silent removal of group-required services.
- Unknown service rejected/quarantined.
- Allowed channels default all vs restricted list.
- Channel not allowed = hard block.
- OPERATOR_PINNED stays on preferred channel while suitable.
- Faster channel alone cannot move pinned user.
- Existing Evidence/Proposal/Trust remain non-authoritative.

## Safety Statement

runtime_mutation_performed=false
user_movement_performed=false
routing_changed=false
autoswitch_apply_run=false

Discovery used repository reads only. No runtime files, users, channels, routes, policies, autoswitch apply, Direct/Trusted RU refresh or kill switch controls were changed.
