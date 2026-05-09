# V7 Phase: Proxy Multi-User Identity Readiness

Date: 2026-05-09

## Goal

Prepare the happ/Karing proxy inbound for scale. One successful proxy identity is
not enough for the future 500-user model: V7 must detect duplicate UUIDs,
duplicate user bindings, runtime drift, route mismatches, and public candidate
fallback behavior before more users are added.

## Implemented

Added:

- `hardening/v7-proxy-multi-user-identity-dry-run`

Updated:

- `admin/v7-admin-api`

## What The Check Verifies

The dry-run checks:

- each binding has a unique user IP;
- each proxy UUID is unique;
- runtime `users[]` count matches binding count;
- every binding UUID exists in sing-box runtime users;
- every bound user exists and is enabled in `users.registry`;
- binding route table matches `users.registry`;
- assigned egress exists, is enabled, and its interface is live;
- per-user Linux `ip rule` exists as a reference route;
- public candidate contains per-user route rules;
- public candidate does not rely on inbound fallback for multi-user mode;
- service and candidate state are visible without exposing secrets.

## Important Current Limitation

The existing public candidate still has a single-user fallback that was useful
for the one-user canary. That is acceptable for the current `happ-test` identity,
but must not be treated as solved multi-user routing.

Before V7 uses this for many users, we need:

```text
two_identity_live_probe
```

That probe should create/use two disabled proxy identities, remove fallback in a
temporary candidate, and prove that each UUID maps to its intended user rule.

## Admin API

```text
POST /api/actions/proxy-multi-user-identity-dry-run
```

Role:

```text
viewer
```

## Safety

The action is read-only:

- no files written;
- no services started;
- no ports opened;
- no route changes;
- no kill-switch changes;
- no user movement;
- UUIDs are printed only redacted.
