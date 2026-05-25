# V7 Track 4 - Sensitive-State Hardening Plan

Purpose: reduce sensitive-state exposure without breaking admin/API access, onboarding, profile delivery, routing, or autoswitch.

No chmod/chown changes were applied in Track 4.

## Live Sensitive-State Inventory

Collected read-only on 2026-05-23.

| Path | Exists | Mode | Owner | Size | Risk |
|---|---:|---|---|---:|---|
| `/opt/v7/egress/state/profile-delivery-tokens.json` | yes | `0644` | `root:root` | `34217` | High |
| `/opt/v7/admin/v7-identity.db` | yes | `0600` | `root:root` | `200704` | Controlled |
| `/opt/v7/identity/v7-identity.db` | no | n/a | n/a | n/a | Contract mismatch historical risk |
| `/etc/v7/policy.json` | yes | `0644` | `root:root` | `896` | Medium |
| `/etc/v7/org-egress-policy.json` | yes | `0644` | `root:root` | `280` | Medium |
| `/opt/v7/egress/state/users.registry` | yes | `0644` | `root:root` | `787` | Medium |
| `/opt/v7/egress/state/egress.registry` | yes | `0644` | `root:root` | `1707` | Medium |
| `/opt/v7/egress/state/service-matrix.json` | yes | `0644` | `root:root` | `102449` | Low/medium |
| `/opt/v7/egress/state/autoswitch-safety.json` | yes | `0644` | `root:root` | `37394` | Medium |
| `/opt/v7/egress/state/telegram-sentinel.json` | yes | `0644` | `root:root` | `10850` | Low/medium |
| `/opt/v7/egress/state/egress-quality-summary.json` | yes | `0644` | `root:root` | `10342` | Low/medium |
| `/opt/v7/egress/state/egress-load-summary.json` | yes | `0644` | `root:root` | `2031` | Low |
| `/opt/v7/egress/state/client-reconnect-state.json` | yes | `0644` | `root:root` | `4756` | Medium |
| `/opt/v7/egress/state/v7-state.json` | yes | `0644` | `root:root` | `10088` | Medium |

## Identity DB Status

Canonical live path:

```text
/opt/v7/admin/v7-identity.db
```

Read-only open status: OK.

Tables observed:

- `access_settings`
- `admin_table_settings`
- `allowed_users`
- `connect_sessions`
- `devices`
- `groups`
- `identity_users`
- `onboarding_attempts`
- `organizations`
- `pending_profiles`
- `provisioning_jobs`
- `user_metadata`

Observed counts:

| Table | Count |
|---|---:|
| `access_settings` | 1 |
| `admin_table_settings` | 0 |
| `allowed_users` | 7 |
| `connect_sessions` | 8 |
| `devices` | 21 |
| `groups` | 1 |
| `identity_users` | 12 |
| `onboarding_attempts` | 42 |
| `organizations` | 3 |
| `pending_profiles` | 3 |
| `provisioning_jobs` | 8 |
| `user_metadata` | 2 |

## Risk Map

### High Risk

`/opt/v7/egress/state/profile-delivery-tokens.json`

Reason:

- token-related state;
- mode `0644`;
- likely profile/onboarding sensitive;
- should not be world-readable unless explicitly required.

### Medium Risk

Policy and registry files:

- `/etc/v7/policy.json`
- `/etc/v7/org-egress-policy.json`
- `/opt/v7/egress/state/users.registry`
- `/opt/v7/egress/state/egress.registry`
- `/opt/v7/egress/state/autoswitch-safety.json`
- `/opt/v7/egress/state/client-reconnect-state.json`
- `/opt/v7/egress/state/v7-state.json`

Reason:

- may reveal routing policy, user assignment, safety/freeze state, or platform topology.

### Controlled

`/opt/v7/admin/v7-identity.db`

Reason:

- mode `0600`;
- canonical path works;
- no immediate permission hardening needed.

## Hardening Strategy

Do not chmod blindly.

Stage 1 - access mapping:

- identify service users for:
  - `v7-admin-api.service`;
  - `v7-public-gateway.service`;
  - profile delivery;
  - onboarding/profile token readers;
  - autoswitch and observability writers.
- map read/write needs per file.

Stage 2 - dry-run permission proposal:

- propose target modes:
  - token state: likely `0600` or `0640`;
  - identity DB: keep `0600`;
  - policy/registry: likely `0640` if non-root service group exists;
  - summaries: can remain `0644` if they contain no secrets.
- validate service access before apply.

Stage 3 - tiny apply:

- change one file class at a time;
- backup metadata first;
- verify API/profile delivery after each change;
- run mandatory safety checks.

Stage 4 - contract update:

- document canonical permissions in `STATE_CONTRACTS.md`;
- add a read-only permission validator;
- show compact operator warning, not a noisy file-permission dashboard.

## Hardening Non-Negotiables

- Do not break onboarding.
- Do not break profile delivery.
- Do not break admin API.
- Do not block autoswitch/sentinel state writes.
- Do not make state unreadable to required services.
- Do not expose token contents in reports.

