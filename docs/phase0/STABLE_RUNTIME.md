# V7 Phase 0 Stable Runtime

Purpose: identify currently stable operational areas that should be protected from casual refactor.

## Stable Runtime Areas

### Admin Control Plane

Path: `admin/v7-admin-api`

Role:

- admin UI;
- HTTP API;
- auth/RBAC/safe mode;
- identity/onboarding;
- egress lifecycle;
- policy/direct/RU views;
- diagnostics and audit views.

Phase 0 status: stable operational monolith. Document boundaries only. Do not split now.

### Autoswitch Runtime

Paths:

- `tools/v7-users-autoswitch`
- `tools/v7-egress-quality-compact`
- `tools/v7-telegram-sentinel`
- `tools/v7-service-matrix-refresh-all`
- `systemd/v7-users-autoswitch.*`
- `systemd/v7-egress-quality-compact.*`
- `systemd/v7-telegram-sentinel.*`
- `systemd/v7-service-matrix-refresh.*`

Role:

- cautious self-healing;
- quality history compaction;
- service matrix refresh;
- Telegram degradation sentinel.

Phase 0 status: stable but runtime-critical.

### Hardening Runtime

Paths:

- `hardening/v7-killswitch-enable`
- `hardening/v7-killswitch-check`
- `hardening/v7-provisioning-reconcile-check`
- `hardening/v7-path-guard-repair`
- `hardening/v7-egress-mtu-probe`
- `hardening/v7-direct-*`

Role:

- kill switch;
- direct/RU diagnostics;
- MTU checks;
- provisioning/routing reconciliation.

Phase 0 status: runtime-critical. Do not alter behavior.

### Egress Lifecycle Runtime

Paths:

- `tools/v7-egress-set-state`
- `systemd/v7-egress-openvpn@.service`
- `admin/v7-admin-api` egress draft/lifecycle blocks

Role:

- staged egress enable/disable/maintenance;
- OpenVPN runtime management;
- draft/preflight/runtime/provision flows.

Phase 0 status: stable operational path; high risk.

## Stable Runtime Protection Rules

- No path moves without wrappers.
- No command renames.
- No state schema changes.
- No default path changes.
- No timer interval changes in Phase 0.
- No direct datapath behavior changes.

