# V7 Admin Navigation Map

Date: 2026-05-10
Status: approved pre-navigation map

## Why This Exists

Before changing navigation, V7 needs a lossless map of where every current admin capability will live.

This document is the guardrail for the redesign:

- do not remove working functions;
- do not split one operator task across too many pages;
- keep technical depth in drawers/details;
- make the main navigation understandable for one person or one operator;
- keep RU/Gosuslugi/bank behavior tied to routing, not as a random special page.

## Confirmed Product Decisions

### Profile Delivery

Do not overbuild delivery links.

The intended behavior is simple:

1. User presses "Connect".
2. V7 creates/downloads the profile.
3. If the user gets distracted, they press again.
4. The newest link/profile flow replaces the previous active delivery.
5. Unused delivery links expire after one day.
6. Admin only needs simple states:
   - link issued;
   - downloaded;
   - expired;
   - issue again.

No heavy resend workflow is needed before navigation redesign.

### RU / Gosuslugi / Banks

For the normal Russia-based user mode, the preferred behavior is client-side smart routing:

- RU and sensitive RU traffic goes directly from the client device;
- global/video traffic goes through V7;
- V7 server-side sensitive RU path remains a separate future/abroad/strict-mode capability.

So the admin should describe this as a routing mode, not as a standalone "Gosuslugi module".

## Target Top Navigation

Recommended top-level navigation:

1. `Главная`
2. `Пользователи`
3. `Каналы`
4. `Маршруты`
5. `Проверки`
6. `Безопасность`
7. `Настройки`
8. `Логи`

Notes:

- Current `Users` and `Identity` should become one operator area: `Пользователи`.
- Identity concepts still exist internally: allowed phones, organizations, device limits, connect password.
- The operator should not need to understand the difference between "identity user" and "VPN user" on the main screen.

## Section Responsibilities

### 1. Главная

Purpose: answer "is V7 working right now?"

Show only:

- system freshness;
- active users;
- users needing operator action;
- egress/channel health;
- route health;
- kill switch status;
- RU client routing readiness;
- important alerts;
- recent meaningful events.

Do not show:

- raw JSON;
- full registry tables;
- long logs;
- all settings.

Current functions that move here:

- system status summary;
- alert summary;
- topology summary;
- active users preview;
- channels preview;
- "action needed" summary.

### 2. Пользователи

Purpose: one workspace for people, devices, profiles and connection readiness.

This section absorbs the useful parts of current `Users` and `Identity`.

Main sub-areas:

- Users table;
- Allowed phones;
- Organizations and groups;
- Device limits;
- Issue profile wizard;
- User/device lifecycle;
- Smart client profiles;
- One-time profile delivery;
- Route reality for a user;
- User speed request;
- User history/logs.

Rows should show:

- person or device label;
- phone if known;
- VPN IP;
- current channel;
- readiness;
- onboarding stage;
- last seen;
- speed sample;
- one primary action.

Drawer should show:

- profile state;
- RU_LOCAL smart profile;
- delivery state;
- downloaded/connected state;
- route reality;
- leak risk;
- speed samples;
- device history;
- contextual logs;
- actions: issue, reissue, switch, disable, enable, rotate key.

Current functions that move here:

- `user_create`;
- `user_create_from_ipam`;
- `user_reissue_config`;
- `user_rotate_key`;
- `user_switch`;
- `user_enable`;
- `user_disable`;
- smart profile generation/select/download;
- profile delivery create/revoke/status, but with simple UI;
- identity access allowed phones;
- groups/organizations;
- device issue/revoke;
- onboarding attempts;
- connect support.

### 3. Каналы

Purpose: manage external egress tunnels.

Rows should show:

- channel name;
- status;
- role;
- enabled/disabled/maintenance;
- users on channel;
- service matrix summary;
- server/V7 speed;
- client direct speed if measured;
- degradation percent if measured;
- load;
- enable readiness.

Drawer should show:

- redacted config;
- health;
- service matrix;
- speed samples;
- assigned users;
- runtime profile;
- enable readiness;
- maintenance/disable/quarantine controls;
- contextual logs.

Add Channel should stay here as a full staged section, not a tiny modal.

Current functions that move here:

- egress table;
- speed test button;
- service matrix button;
- egress config preview;
- egress QR preview;
- egress draft create;
- preflight;
- isolated runtime test;
- quarantine test;
- add disabled;
- runtime profile provisioning;
- enable readiness;
- enable/disable/maintenance;
- channel logs.

### 4. Маршруты

Purpose: decide where traffic goes.

This is where RU/Gosuslugi/bank behavior belongs.

Main sub-areas:

- Route classes;
- RU client modes;
- Domain groups;
- Service-aware policy;
- Policy matrix;
- Route preview;
- Rebalance preview;
- Sensitive RU abroad/strict readiness;
- Direct RU server-side diagnostics as secondary/future path.

Rows/cards should explain:

- `RU_LOCAL`: RU leaves directly from client device;
- `ABROAD_RU_VIA_V7`: RU goes through V7 when abroad mode is selected;
- `TRUSTED_RU_SENSITIVE`: government/bank path, not considered solved until a tested route exists;
- `GLOBAL_FAST`, `VIDEO_OPTIMIZED`, etc.

Current functions that move here:

- policy domain add/remove/test/backups/restore;
- policy matrix test;
- service-aware route dry-run;
- service-aware apply preview;
- guarded apply;
- direct domain add/remove/status;
- trusted RU diagnostic/readiness/decision;
- user flow trace;
- route classes;
- rebalance dry-run and manual one-move apply.

### 5. Проверки

Purpose: safe read-only diagnostics and focused checks.

Main sub-areas:

- full system check;
- kill switch check;
- capacity/IPAM check;
- route checks;
- policy checks;
- installer/preflight checks;
- stale state check;
- service matrix diagnostics.

Current functions that move here:

- diagnostics;
- killswitch check;
- installer;
- capacity readiness;
- route reality checks;
- service-aware dry-run;
- direct/trusted diagnostic results when used as diagnostics.

### 6. Безопасность

Purpose: safety controls and recovery.

Main sub-areas:

- admin password and accounts;
- roles/RBAC;
- safe mode;
- kill switch controls;
- backups;
- rollback;
- log/disk retention;
- cleanup preview/apply;
- security audit;
- SSH/key setup notes.

Current functions that move here:

- admin accounts;
- password rotate/change;
- safe mode;
- backup create/list/verify/download;
- restore preview;
- rollback preview/apply;
- maintenance settings;
- cleanup preview/apply;
- log maintenance status;
- security audit/export;
- kill switch enable/disable/status controls.

### 7. Настройки

Purpose: low-frequency configuration.

Keep this separate. Do not overload Security or Routing.

Main sub-areas:

- cooldown seconds;
- planned autoswitch limits;
- failover limits;
- health intervals;
- benchmark intervals;
- route mode defaults;
- service preferences;
- language/theme later;
- table column visibility later.

Current functions that move here:

- policy update;
- policy systemd preview/apply;
- service preferences update;
- route mode defaults;
- UI defaults later.

### 8. Логи

Purpose: global event stream and audit history.

Main rule:

- contextual logs stay next to objects;
- global logs remain here for search/filter/export.

Current functions that move here:

- events timeline;
- audit events;
- switch history summary;
- security audit export;
- filters by component, severity, user, channel.

## Current Tab Migration

| Current tab | Future location | Action |
|---|---|---|
| Overview | `Главная` | Keep, simplify and make more Russian/operator-first. |
| Users | `Пользователи` | Merge with Identity concepts. |
| Identity | `Пользователи` | Do not keep as top-level tab for normal operator view. |
| Channels | `Каналы` | Keep, strengthen Add Channel flow. |
| Routing | `Маршруты` | Keep, make RU/client-mode behavior clearer. |
| Checks | `Проверки` | Keep as diagnostics center. |
| Security | `Безопасность` | Keep. |
| Settings | `Настройки` | Keep. |
| Logs | `Логи` | Keep. |

## Dangerous Navigation Questions Answered

### Should `Identity` remain top-level?

No, not in the operator-facing navigation.

Reason: the system is for a concrete person/operator. Splitting `Users` and `Identity` forces the operator to understand backend concepts. Merge them into `Пользователи`, with internal subsections.

### Should delivery links get a big workflow?

No.

Reason: user presses connect, downloads profile, and if needed repeats. Keep one-day expiry and newest delivery wins. Show simple state only.

### Should Gosuslugi get a separate page?

No.

Reason: it is a traffic class and route behavior. Put it under `Маршруты`, with clear labels for `RU_LOCAL`, `ABROAD_RU_VIA_V7`, and future server-side sensitive path.

### Should Add Channel be a modal?

No.

Reason: safe channel onboarding is long and risky. It needs a full section inside `Каналы`.

### Should logs be everywhere?

No.

Reason: logs should appear contextually in drawers, with full search under `Логи`.

## Implementation Order

### Step 1: Navigation labels and grouping

Change top tabs to the target Russian/operator labels, without removing functions.

Expected result:

- `Identity` disappears as top-level;
- its panels move under `Пользователи`;
- all existing controls remain reachable.

### Step 2: Users page restructure

Make `Пользователи` the main operator workspace:

- users/device table first;
- profile issue wizard;
- allowed phones/groups/orgs below;
- lifecycle board;
- connect support.

### Step 3: Routing language cleanup

Make RU behavior clear:

- `RU_LOCAL` = direct on client;
- sensitive RU server path = future/abroad/strict mode;
- domain groups are editable but not scary.

### Step 4: Channels page polish

Keep Add Channel full flow and improve visual order:

- existing channels first;
- Add Channel wizard second;
- drafts/results third.

### Step 5: Security/settings/logs cleanup

Keep low-frequency controls out of daily operator path:

- Security for safety/recovery;
- Settings for tuning;
- Logs for global search.

## Verification Checklist For Each Navigation Change

After each change:

- `/admin-v2` loads without JavaScript errors;
- every top-level nav button opens a page;
- user create/profile issue still reachable;
- channel add wizard still reachable;
- route domain editor still reachable;
- kill switch and backup controls still reachable;
- logs/events still reachable;
- no raw secret appears in visible UI;
- local checks pass;
- VPS service restarts cleanly.

