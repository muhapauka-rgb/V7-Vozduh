# V7 Phase: Proxy Multi-User Identity Sync

Date: 2026-05-09

## Goal

Prepare V7 proxy/happ ingress for real multi-user operation. Each V7 user must
have a separate proxy identity, so a future 500-user system does not depend on
one shared VLESS credential.

## Implemented

Added:

- `hardening/v7-proxy-identity-sync-users`

Updated:

- `admin/v7-admin-api`
- `hardening/v7-proxy-public-service-render`
- `hardening/v7-proxy-public-port-canary`
- `hardening/v7-proxy-public-enable`
- `hardening/v7-proxy-policy-runtime-adapter-dry-run`

## Safety Model

The sync step only writes disabled identity binding files:

- no service start;
- no public port open;
- no route change;
- no kill-switch change;
- no user movement;
- existing UUID values are preserved.

## VPS Result

Validated on the VPS:

- active V7 users selected for proxy identities: 3;
- bindings created/updated: 3;
- rendered runtime users: 3;
- public candidate auth rules: 3;
- candidate uses `auth_user`;
- candidate inbound fallback: disabled;
- two-identity live probe: OK;
- public-port canary: OK;
- public service restored: active/enabled;
- proxy public IP: `94.241.139.241`;
- direct `ens3` leak test: blocked;
- `v7-system-check`: `V7_RESULT=OK`.

## Current State

Current proxy identities:

- `10.0.0.2` -> `v7-10.0.0.2-happ`
- `10.0.0.3` -> `v7-10.0.0.3-happ`
- `10.0.0.6` -> `v7-10.0.0.6-happ`

`v7-proxy-multi-user-identity-dry-run --target-users 500` now reports:

- `multi_user_ready=yes`
- `bindings=3`
- `runtime_users=3`
- `candidate_auth_user_rules=yes`
- `candidate_inbound_fallback=no`

## Generated Profiles

Created happ profiles on the VPS without printing secrets:

- `/root/v7-smart-clients/user-10-0-0-3/happ-ru_local.txt`
- `/root/v7-smart-clients/user-10-0-0-6/happ-ru_local.txt`

## Remaining Work

The next scaling step is to connect user creation to proxy identity sync and
smart profile generation, so a new user can be created once and receive the
correct WireGuard/Karing/happ artifacts automatically.
