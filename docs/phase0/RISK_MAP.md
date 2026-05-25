# V7 Phase 0 Risk Map

Purpose: classify repository areas by refactor and operational risk.

## Categories

- `SAFE_TO_REFACTOR`: low runtime risk if behavior is preserved.
- `RUNTIME_CRITICAL`: affects production behavior or state contracts.
- `HIGH_RISK`: can break routing, safety, provisioning, or operator trust.
- `EXPERIMENTAL`: not yet a stable architecture contract.
- `UNKNOWN`: needs more runtime evidence.

## Area Risk Table

| Area | Category | Why | Phase 0 Action |
| --- | --- | --- | --- |
| Governance/roadmap docs | SAFE_TO_REFACTOR | Documentation only. | Keep consistent names and references. |
| Phase reports | SAFE_TO_REFACTOR | Historical docs. | Archive later, do not delete. |
| `design/` snapshots | EXPERIMENTAL | Static prototypes/copies. | Preserve; consolidate later. |
| `artifacts/` test configs/QR | EXPERIMENTAL | Generated/test material. | Preserve; classify as fixtures later. |
| `admin/v7-admin-api` auth/session/RBAC | RUNTIME_CRITICAL | Controls access and dangerous actions. | Document boundaries only. |
| `admin/v7-admin-api` identity/onboarding | RUNTIME_CRITICAL | Writes SQLite and profiles. | No behavior changes in Phase 0. |
| `admin/v7-admin-api` egress lifecycle | HIGH_RISK | Can write runtime configs and registry. | Only document contracts. |
| `admin/v7-admin-api` embedded UI | RUNTIME_CRITICAL | Operator workflow and action trigger surface. | Preserve calm UX; no big redesign. |
| `tools/v7-users-autoswitch` | HIGH_RISK | Can switch users when applied. | No logic changes. |
| `tools/v7-egress-quality-compact` | RUNTIME_CRITICAL | Feeds autoswitch quality state. | Contract document only. |
| `tools/v7-telegram-sentinel` | RUNTIME_CRITICAL | Fast degradation input and optional autoswitch trigger. | No timer/logic changes. |
| `tools/v7-service-matrix-test` | RUNTIME_CRITICAL | Service health contract. | No schema changes. |
| `tools/v7-egress-set-state` | HIGH_RISK | Enables/disables egress runtime and rebuilds kill switch. | Do not modify in Phase 0. |
| `hardening/v7-killswitch-*` | HIGH_RISK | Safety foundation. | No behavior changes. |
| `hardening/v7-direct-*` | HIGH_RISK | Direct/RU route diagnostics and config. | No behavior changes. |
| `hardening/v7-provisioning-reconcile-check` | RUNTIME_CRITICAL | Detects runtime drift. | Preserve. |
| `systemd/` timers | RUNTIME_CRITICAL | Controls production cadence. | No interval changes. |
| Missing `/usr/local/bin/v7-*` commands | UNKNOWN | Runtime contracts not in repo. | Document dependencies. |
| Local DB `v7-v7-lab-speed-ru_local.db` | UNKNOWN | Untracked data file. | Do not add until classified. |

## High-Risk Themes

### Routing

Any change to `ip`, `nft`, marks, tables, interfaces, user assignment, or direct/RU policy is high risk.

### Kill Switch

Any change that can allow VPN subnet traffic to exit public interface without explicit direct policy is forbidden.

### Autoswitch

Any change that increases move rate, reduces cooldown, weakens safety, or hides explanation is high risk.

### Provisioning

Any change that auto-enables unknown egress, skips runtime verification, or silently edits registries is high risk.

### Direct/RU

Any fallback from `TRUSTED_RU_SENSITIVE` to unsafe direct/global routing is forbidden.

