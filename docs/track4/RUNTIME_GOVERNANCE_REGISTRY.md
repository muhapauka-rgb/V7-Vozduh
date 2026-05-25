# V7 Track 4 - Runtime Governance Registry

Purpose: make runtime tools governable without moving, deleting, or rewriting them.

This registry is a governance layer, not a cleanup instruction. A tool being listed here does not mean it is safe to archive. Cleanup requires a separate block, a manifest, and runtime verification.

## Registry Fields

Every runtime tool should eventually have:

| Field | Meaning |
|---|---|
| `tool` | Executable basename |
| `owner` | Runtime owner or module owner |
| `category` | Operational class |
| `mutation` | `read_only`, `writes_state`, `changes_runtime`, or `dangerous` |
| `safety_level` | `low`, `medium`, `high`, or `critical` |
| `rollback_sensitivity` | Whether mistakes need rollback context |
| `repo_lineage` | `repo_known`, `production_only`, `generated`, or `unknown` |
| `runtime_criticality` | `critical`, `support`, `operator`, `legacy`, or `unknown` |
| `cleanup_status` | `keep`, `deeper_inspection`, `archive_candidate`, or `forbidden_to_cleanup` |
| `verification_required` | Checks required after change |

## Current Runtime Tool Baseline

Source evidence:

- Block 3.1 deploy manifest: `/opt/v7/ops/deploy-baseline/20260523T122251Z/manifest.json`
- Block 3.2 archive: `/root/v7-backups/usr-local-bin-archive/20260523T122936Z/`
- Block 3.3 unknown classification
- Block 3.4 suspicious executable archive

Current PATH state after Block 3.4:

| Class | Count | Governance Verdict |
|---|---:|---|
| Active runtime executables | 24 | `forbidden_to_cleanup` unless replaced by a release process |
| Unknown active-like tools | 117 | Govern before cleanup |
| Known suspicious executables | 0 | Removed from PATH in Block 3.4 |
| Backup-like stale executables in PATH | 0 | Removed in Block 3.2 |
| Total `/usr/local/bin/v7*` | 141 | Cleaner but still not release-governed |

## Tool Category Registry

| Category | Count | Mutation Default | Safety Level | Cleanup Status |
|---|---:|---|---|---|
| `diagnostic_or_readonly_utility` | 26 | `read_only` | Low to medium | Keep unless owner confirms obsolete |
| `policy_or_direct_ru_utility` | 26 | Mixed | High | Forbidden to cleanup without direct/RU review |
| `operator_mutation_tool` | 22 | `changes_runtime` | High | Keep; needs audit and rollback context |
| `unknown_risk` | 20 | Unknown | Medium to high | Deeper inspection required |
| `provisioning_or_egress_utility` | 13 | Mixed | High | Keep until provisioning workflows are mapped |
| `identity_or_profile_utility` | 4 | Writes identity/profile state | High | Keep; identity-sensitive |
| `observability_or_measurement_tool` | 4 | Read-only/support | Low to medium | Keep as operator utilities |
| `review_setup_or_governance_tool` | 2 | Read-only/setup | Low | Keep or repo-govern later |

## Critical Named Tools

These tools are not necessarily systemd-bound, but they are operationally important.

| Tool | Owner | Mutation | Criticality | Cleanup Status |
|---|---|---|---|---|
| `v7-audit-log` | audit/runtime | `writes_state` | support-critical | keep; deeper inspect for repo lineage |
| `v7-user-switch` | routing/autoswitch | `changes_runtime` | critical | forbidden to cleanup |
| `v7-killswitch-check` | safety | `read_only` | critical verification | forbidden to cleanup |
| `v7-user-route-check` | routing safety | `read_only` | critical verification | forbidden to cleanup |
| `v7-provisioning-reconcile-check` | provisioning safety | `read_only` | critical verification | forbidden to cleanup |
| `v7-state-json` | state/runtime | `writes_state_or_cache` | support-critical | deeper inspection |
| `v7-user-desired-state` | state/routing | `writes_or_reads_state` | support-critical | deeper inspection |
| `v7-users-autoswitch` | autoswitch | `changes_runtime` | critical | forbidden to cleanup |
| `v7-users-rebalance` | routing operations | `changes_runtime` | high | keep; do not run broadly |
| `v7-users-rebalance-dry-run` | routing operations | `read_only/planning` | medium | keep as planning tool |
| `v7-policy-apply` | policy | `changes_runtime` | high | keep; audit required |
| `v7-egress-set-state` | provisioning | `writes_state` | high | keep; rollback required |

## Cleanup Rules

Allowed only in a dedicated cleanup block:

1. Build a fresh manifest before cleanup.
2. Only archive, never delete.
3. Do not touch active runtime executables.
4. Do not touch direct/RU, Trusted RU, policy, identity, user-switch, autoswitch, or provisioning tools without module owner review.
5. Preserve hash, mode, mtime, filename, original path, and reason.
6. Verify:
   - `systemctl --failed`
   - `v7-killswitch-check`
   - `v7-user-route-check`
   - `v7-provisioning-reconcile-check`
   - `v7-observability-summary --pretty`

## Ownership Model

| Owner | Scope |
|---|---|
| `safety` | kill switch, no-leak checks, route verification |
| `routing` | user route assignment, table/rule sanity, direct/RU isolation |
| `autoswitch` | guarded switching, anti-flap, capacity signal, switch history |
| `provisioning` | egress lifecycle, drafts, quarantine, enable gates, rollback |
| `identity` | identity DB, devices, onboarding, profile delivery |
| `policy` | global/org policy, route classes, direct/RU policy |
| `observability` | health summaries, service matrix, sentinel, operator truth |
| `admin` | admin API, UI, operator workflows |
| `audit` | actor/reason/before-after/rollback records |

## Governance Gate

Before adding a new runtime tool:

- define owner;
- declare whether it mutates runtime;
- declare exact state files it reads/writes;
- add rollback expectations;
- add audit expectations;
- add repo lineage;
- add verification checks;
- avoid putting temporary executables directly in PATH.

