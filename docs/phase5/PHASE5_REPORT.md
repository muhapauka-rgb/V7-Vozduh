# V7 Phase 5 Report

## Scope

Phase 5 inspected current identity, onboarding, profile delivery, user readiness, and organization policy foundations.

No runtime behavior, profile generation behavior, routing behavior, nftables behavior, systemd units, or admin endpoint behavior was changed.

## Current Strengths

The current platform already has substantial Phase 5 foundation:

- SQLite identity DB with groups, organizations, allowed users, identity users, devices, pending profiles, connect sessions, provisioning jobs, and onboarding attempts;
- public `/connect` flow through a narrow gateway allowlist;
- idempotent connect sessions;
- phone/organization/password onboarding gates;
- device limit enforcement;
- one-time profile delivery tokens with TTL and consumption tracking;
- delivery revocation on device revoke;
- user readiness and onboarding stage summaries;
- audited identity actions;
- explicit confirms for dangerous operations;
- org egress policy file used by control-plane logic.

## Main Gaps

### Lifecycle is implemented but not formalized

Current statuses exist, but target commercial lifecycle terms are not yet a stable contract.

### Identity/runtime drift needs a dedicated read-only review

Identity DB and `users.registry` can diverge. This is especially important for revoked devices, stale profiles, and orphan runtime rows.

### Organization isolation needs explicit policy semantics

Organizations and groups exist, but isolation boundaries and diagnostics visibility must be treated as formal architecture contracts before broader commercial use.

### Identity DB default path mismatch exists in documentation/tooling

The admin monolith defaults `V7_IDENTITY_DB_FILE` to `/opt/v7/admin/v7-identity.db`.

One earlier validator defaults to `/opt/v7/identity/v7-identity.db`. Future cleanup should align this carefully with migration notes, not by silently moving production DB files.

## Added Artifacts

- `MULTITENANT_MODEL.md`
- `ORGANIZATION_ISOLATION.md`
- `USER_LIFECYCLE.md`
- `DEVICE_LIFECYCLE.md`
- `PROFILE_DELIVERY_MODEL.md`
- `ONBOARDING_RECOVERY_UX.md`
- `POLICY_BASED_ACCESS.md`
- `SAFE_USER_OPERATIONS.md`
- `DEVICE_TRUST_FOUNDATION.md`
- `OPERATOR_IDENTITY_UX.md`
- `USER_READINESS_MODEL.md`
- `COMMERCIAL_ENTERPRISE_FOUNDATION.md`
- `IDENTITY_RUNTIME_CONSISTENCY.md`

## Added Tool

`tools/v7-identity-consistency-review` is a read-only consistency helper.

It checks:

- identity DB schema presence;
- organization/group references;
- user and device status compatibility;
- active device and runtime registry consistency;
- revoked device runtime leakage;
- pending profile expiration drift;
- profile delivery token consistency;
- org policy readability.

It does not write SQLite, registries, profile files, token files, routing state, nftables, or systemd.

## Phase Boundary

Phase 5 did not start Phase 6.

Admin platform split, new frontend architecture, and UI restructuring remain out of scope until a separate command.

