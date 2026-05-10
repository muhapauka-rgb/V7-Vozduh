# V7 Admin Redesign Analysis Plan

Date: 2026-05-10

Design source:

- `/Users/ponch/Documents/New project/design/Норм 3 v7-admin-alternative-dashboard — копия 2.html`

Current live admin source:

- `admin/v7-admin-api`

## What The New Design Already Gets Right

The design moves V7 Admin from a long technical control page toward an operator console.

Main structure:

- `Overview`
- `Users`
- `Channels`
- `Routing`
- `Identity`
- `Checks`
- `Security`
- `Logs`

Strong patterns to keep:

- top status bar;
- compact summary cards;
- operational tables;
- drawer/details workspace for heavy actions;
- `Advanced technical mode` for raw output;
- contextual logs/details rather than global noise;
- Russian/English text layer;
- responsive layout;
- route and channel status expressed in human language first.

## Fresh Comparison Notes

The provided HTML design was reviewed visually and structurally against the live `/admin-v2` template.

The design is stronger than the current live admin in these areas:

- clearer top-level command center;
- richer topology block with a visible egress pool;
- clearer alerts list;
- better compact row density for users/channels;
- stronger idea of "summary first, details in drawer";
- contextual action buttons in rows;
- built-in language/theme/layout controls as future UI affordances;
- explicit Advanced/raw mode for technical detail.

The current live admin is stronger than the design in these areas:

- real `Add Channel` wizard endpoints are already wired;
- policy domain editor is already live;
- identity access controls are already live;
- profile issuing and delivery are already live;
- backups, cleanup, rollback and safe mode are already live;
- settings/policy controls exist as a dedicated page;
- event filters are already live;
- channel and user drawers already load live details.

Conclusion: the redesign must not replace the current admin with the static design. It should absorb the design language and navigation model while preserving current live actions.

## Current Feature Coverage

### Covered Well

These existing V7 areas have a clear place in the new design:

- system overview;
- users table;
- channel/egress table;
- route classes;
- direct RU and sensitive RU state;
- checks/diagnostics;
- backups;
- events/logs;
- identity/onboarding overview;
- admin accounts;
- kill switch and security posture.

### Partially Covered

These exist in the current backend/admin, but need a better home in the redesigned UI:

- egress draft wizard stages;
- runtime profile provisioning;
- enable readiness;
- service matrix per channel;
- channel speed comparison: V7 speed, client direct speed, drop percent;
- user smart profile generation;
- one-time delivery links;
- profile delivery history;
- identity device quality;
- proxy runtime refresh and public proxy inlet controls;
- policy domain group editing;
- backup restore preview and rollback;
- log/disk retention controls;
- safe mode;
- installer preflight;
- service recommendations.

### Missing Or Not Clear In The New Design

The design does not yet give a first-class, intuitive place for:

1. Full `Add Channel` wizard:
   upload/link/QR/manual -> detect -> preflight -> runtime test -> quarantine/ready -> add disabled -> provision -> enable.

2. Identity user detail as the operator workspace:
   devices, issued profiles, delivery links, lifecycle, device quality, action history.

3. Route policy domain editor:
   add/remove domains by group, backups, rollback, test domain.

4. Channel service matrix:
   channels vertically, traffic/service groups horizontally, with status and speed when already measured.

5. Proxy inbound / happ / Karing public access runtime:
   this is not an egress channel; it is a client ingress/runtime support layer.

6. Settings:
   cooldowns, thresholds, service preferences, systemd intervals, route mode defaults.

7. Safe mode:
   should be always visible because it changes whether actions can mutate state.

8. Backup and log limits:
   not just backup list, but retention, cleanup preview, journal/log size control.

9. User-facing `/connect` page:
   needs a place in admin as "User Portal / Connect Page" settings and diagnostics.

10. Rebalance:
    preview/apply one move/manual-only controls are not prominent enough.

## Proposed Integration Into The New Design

### Overview

Keep it as command center:

- system status;
- users online/readiness;
- channels health;
- routing health;
- kill switch;
- action needed;
- recent meaningful activity only.

Do not put raw tables here.

### Users

Make it the main workspace for VPN users and devices.

Rows:

- user/device;
- VPN IP;
- assigned channel;
- readiness;
- last seen;
- speed sample;
- one primary action.

Drawer:

- Connection Readiness;
- Device Quality;
- Smart Profiles;
- Profile Delivery;
- Route Reality;
- Speed request;
- History/logs;
- disable/enable/switch/reissue/rotate key.

### Identity

Make it the workspace for admission and lifecycle:

- allowed phones;
- organizations;
- groups;
- device limits;
- onboarding attempts;
- issue profile wizard;
- user lifecycle filters;
- import/export allowed phones.

Identity should manage "who may connect"; Users should manage "how this person's VPN actually works".

### Channels

Make it the workspace for egress tunnels.

Rows:

- channel;
- status;
- role;
- users;
- service matrix summary;
- V7 speed;
- client direct speed;
- drop percent;
- load;
- readiness.

Drawer:

- redacted config;
- health;
- service matrix;
- speed history;
- users on channel;
- maintenance/disable/quarantine;
- logs;
- runtime profile;
- enable readiness.

Add Channel should open a proper staged wizard, not a raw JSON section.

### Routing

Make it the workspace for policy and service-aware routing.

Sections:

- route classes;
- RU routing state;
- domain groups;
- policy matrix;
- route preview;
- rebalance preview;
- direct/sensitive RU tools;
- safe apply/rollback.

Domain group editing belongs here, not in a generic Actions block.

### Checks

Make it focused diagnostics:

- system health;
- leak protection;
- IPAM/capacity;
- routing checks;
- trusted RU diagnostics;
- installer preflight.

Checks should explain what failed and where to go next.

### Security

Make it operational safety:

- admin accounts;
- safe mode;
- kill switch;
- backups;
- restore preview;
- rollback;
- log retention;
- disk cleanup preview;
- password controls;
- security audit export.

### Logs

Make it event stream, not raw spam:

- audit events;
- switch events;
- backup events;
- user/device events;
- route events;
- filters;
- object details drawer.

Contextual logs should also appear from Users, Channels, Routing, and Security drawers.

### Settings

There is no Settings tab in the design yet.

Recommended option:

- add a small `Settings` entry in the top nav or user menu;
- keep low-frequency controls there:
  thresholds, cooldowns, health intervals, service preferences, default route modes, language/theme.

If we avoid a separate Settings tab, these controls will overload Security and Routing.

## Design Decisions Needed

1. Settings location:
   add separate `Settings` tab, or hide settings under the admin/user menu?

2. Add Channel wizard:
   should it open as a full-page wizard inside `Channels`, or as a large drawer/modal from `Channels`?

3. Proxy inbound / happ runtime:
   should it live under `Identity` as client access infrastructure, or under `Security` as runtime/proxy control?

4. Layout editor:
   the design has edit/reset layout controls. For production-like admin, this should probably be postponed or limited to column visibility only.

## Decisions Adopted For Implementation

To avoid stopping at every fork, these decisions are now adopted:

1. Keep `Settings` as a top-level tab.
2. Keep `Add Channel` as a full in-page wizard under `Channels`.
3. Put public client runtime controls (`happ`, `Karing`, proxy inlet, delivery links) under `Identity` and user drawers.
4. Postpone free-form layout editing; implement safer column visibility and saved filters first.
5. Keep raw logs out of root dashboards; show contextual logs in drawers and full history in `Logs`.
6. Keep technical/raw detail collapsed by default.

If later we build a separate polished frontend, these decisions become product navigation rules.

## Implementation Plan

### Phase A — Preserve and prepare

1. Keep current admin API endpoints unchanged.
2. Introduce the new shell layout behind a safe flag or alternate route first.
3. Do not delete the old admin page until the new one passes parity checks.

### Phase B — New static shell

1. Move the provided design into the admin template.
2. Replace hardcoded sample values with empty live containers.
3. Keep `Advanced technical mode` as a compatibility bridge.

Current status: partially complete. `/admin-v2` already has the shell, live tabs, drawers and most operator sections. The next pass is not a rewrite; it is a design convergence pass.

### Phase C — Live data binding

1. Bind `/api/session`.
2. Bind `/api/overview`.
3. Bind Users, Channels, Routing, Identity, Checks, Security, Logs from existing API.
4. Keep current actions wired to existing endpoints.

Current status: mostly complete for existing backend coverage. The remaining work is visual/ergonomic consolidation, not API invention.

### Phase D — First-class drawers

1. User drawer.
2. Channel drawer.
3. Routing/policy drawer.
4. Identity user drawer.
5. Security/backup drawer.
6. Log event drawer.

### Phase E — Missing feature placement

1. Add Channel wizard in Channels.
2. Device Quality in Users/Identity drawer.
3. Domain group editor in Routing.
4. Backup/log retention in Security.
5. Safe mode in top bar and Security.
6. Rebalance preview in Routing.

### Phase G — Design Convergence Pass

1. Replace the simple topology block with the richer egress-pool topology from the provided design.
2. Make overview tables more compact and add search/column affordances where they do not create risk.
3. Make channel rows show role, service coverage, speed, load and action in the same visual rhythm as the design.
4. Keep Add Channel visible under `Channels`, but make the staged flow read like the design cards.
5. Move noisy policy/domain tooling into a clearer `Routing` hierarchy:
   route classes, RU routing state, domain groups, matrix, guarded apply.
6. Turn `Checks` into grouped diagnostic cards with clear next actions.
7. Turn `Security` into a safety console:
   safe mode, backups, rollback, cleanup, admin accounts, audit.
8. Keep `Settings` for low-frequency tuning:
   thresholds, cooldowns, route modes, systemd intervals.
9. Keep contextual logs inside drawers, with full filters in `Logs`.
10. Browser-smoke-test every primary tab after each pass.

### Phase H — Parity Checklist

Before making redesigned admin the only admin route, verify all of these are reachable:

- user create/issue profile;
- user enable/disable/switch;
- Karing/Hiddify/happ profile generation or delivery;
- user route reality and logs;
- channel speed/manual matrix/logs/state changes;
- Add Channel draft/preflight/runtime/add-disabled/provision/readiness;
- policy domain add/remove/test/backup;
- service-aware dry run/apply preview;
- safe mode;
- backup create/list/cleanup/rollback;
- admin password/account controls;
- event filters;
- settings policy/systemd preview/apply.

### Phase F — Verification

1. Local Python syntax check.
2. Local HTML smoke check.
3. Deploy to VPS with backup.
4. Check `v7-admin-api` service.
5. Check `/login`, `/`, `/api/overview`, `/api/session`.
6. Manual UI pass through all tabs.
7. Keep rollback path to old admin.

## Recommendation

Adopt the provided design as the new primary admin direction, but implement it as a live redesign incrementally:

- first new shell;
- then live data;
- then drawers;
- then staged dangerous actions;
- then polish.

Do not make the design-only prototype the only admin until all existing actions are reachable.
