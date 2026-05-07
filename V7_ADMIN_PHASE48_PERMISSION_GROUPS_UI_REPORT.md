# V7 Admin Phase 48: Permission groups UI

Date: 2026-05-07

## Goal

Make service-aware policy domains manageable as expandable permission groups in
the admin panel.

The operator should be able to open a group such as:

```text
Direct RU
Sensitive RU
Video
Global Stable
```

and add/remove concrete domains inside it, for example:

```text
alfabank.ru
vk.com
ok.ru
```

## Admin UI

The `Service-aware Policy` section now renders policy domains as expandable
groups instead of one flat table.

Each group shows:

- clear label;
- internal route class id;
- domain count;
- plain-language purpose;
- permission/route behavior;
- add-domain field scoped to that group;
- remove button for each domain;
- backup/restore controls.

Important groups:

```text
Sensitive RU -> banks, Gosuslugi, ESIA, anti-fraud
Direct RU    -> ordinary Russian websites/apps that bypass external VPN
Video        -> video/media services
Global Stable -> messaging/push services
```

## Domain Defaults Added

The bootstrap default for `DIRECT_RU` now includes explicit VK/OK domains:

```text
vk.com
vk.ru
vkvideo.ru
vkuser.net
userapi.com
ok.ru
odnoklassniki.ru
okcdn.ru
mycdn.me
```

On the VPS these domains were added through the safe policy-domain commands,
not by manual file editing.

Alfa-Bank domains were already present in:

```text
TRUSTED_RU_SENSITIVE
```

## Validation

Commands run on VPS:

```bash
v7-policy-domain-list DIRECT_RU
v7-policy-test-domain vk.com 10.0.0.3
v7-policy-test-domain ok.ru 10.0.0.3
systemctl is-active v7-admin-api
curl -sS -I http://127.0.0.1:7080/login
v7-killswitch-check
v7-system-check
```

Results:

- `vk.com`: `DIRECT_RU`, desired path `ens3`, direct engine `DIRECT_READY`;
- `ok.ru`: `DIRECT_RU`, desired path `ens3`, direct engine `DIRECT_READY`;
- `v7-admin-api`: active;
- `HTTP /login`: `200 OK`;
- final `v7-killswitch-check`: `OK`;
- final `v7-system-check`: `OK`;
- live user routes stayed unchanged.

## Note

Immediately after sequential domain additions, a killswitch check can observe a
short rebuild window and report partial direct/DNS rule visibility. A follow-up
check returned `OK`; user route checks did not show public-interface leakage.

Next quality step:

```text
add a policy/dns/killswitch rebuild guard so checks and admin actions report
REBUILDING instead of transient FAIL during internal refresh windows.
```
