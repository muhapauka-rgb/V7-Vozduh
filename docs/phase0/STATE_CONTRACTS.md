# V7 Phase 0 State Contracts

Purpose: document critical state files, readers, writers, and schema expectations.

## Contract Rules

- State contracts must remain backward-compatible unless a migration is staged.
- Writers must use atomic writes where practical.
- Runtime state and UI state must not silently diverge.
- Contract changes must include validation, rollback, and operator-facing notes.

## Critical Contracts

| State | Kind | Main Readers | Main Writers | Contract Notes |
| --- | --- | --- | --- | --- |
| `/opt/v7/egress/state/users.registry` | line registry | admin API, autoswitch, reconciliation, client speed, benchmark | external provisioning commands, admin delete helpers | `key=value` rows. Critical fields include `ip`, `current`, `enabled`, table/identity metadata. |
| `/opt/v7/egress/state/egress.registry` | line registry | admin API, autoswitch, matrix, benchmark, hardening, egress state | egress lifecycle tools/admin helpers | Critical fields include `id`, `interface`, `protocol`, `config`, `enabled`, role/capacity metadata. |
| `/opt/v7/egress/state/egress-flags.state` | line state | admin API, egress detail | `v7-egress-set-state`, admin delete helpers | Tracks maintenance/disabled style lifecycle flags. |
| `/opt/v7/egress/state/v7-state.json` | JSON snapshot | admin overview, autoswitch, quality compactor | external state builder | Contains live users/egress health. Must be freshness-checked. |
| `/opt/v7/egress/state/service-matrix.json` | JSON | admin API, autoswitch, quality compactor | `v7-service-matrix-test`, `v7-telegram-sentinel` | Per-egress service status, route class fitness, Telegram status. |
| `/opt/v7/egress/state/egress-speed.json` | JSON | admin API, autoswitch, quality compactor | speed benchmark external/runtime tools | Per-egress speed and health metrics. |
| `/opt/v7/egress/state/egress-quality-summary.json` | JSON | autoswitch, admin API | `v7-egress-quality-compact` | Bounded EMA-style windows. Used for stability gates. |
| `/opt/v7/egress/state/egress-quality-ring.json` | JSON | diagnostics | `v7-egress-quality-compact` | Bounded sample ring; not authoritative routing policy. |
| `/opt/v7/egress/state/autoswitch-safety.json` | JSON | autoswitch | `v7-users-autoswitch` | Anti-flapping counters, target blocks, quarantine memory. |
| `/opt/v7/egress/state/telegram-sentinel.json` | JSON | autoswitch, admin API | `v7-telegram-sentinel` | Fast Telegram-specific degradation state. |
| `/opt/v7/egress/state/client-speed.json` | JSON | admin API, autoswitch | `v7-client-speed-api`, admin public sample handler | Client-side speed samples by user/path. |
| `/opt/v7/egress/state/client-agents.json` | JSON | admin API | `v7-client-speed-api` | Last seen client agent metadata. |
| `/opt/v7/egress/state/client-commands.json` | JSON | public client speed API, admin API | admin API, `v7-client-speed-api` | Pending/complete speed-test commands. |
| `/opt/v7/egress/state/path-samples.json` | JSON | benchmark, optimizer | `v7-path-sample-ingest` | Latest/history path samples keyed by ingress and egress. |
| `/etc/v7/policy.json` | JSON | admin API, autoswitch | admin policy update | Platform policy: switch, quality, load, reconnect, safety, intervals. |
| `/etc/v7/org-egress-policy.json` | JSON | admin API, autoswitch | admin org policy update | Organization isolation and per-egress group/capacity metadata. |
| `/etc/v7/admin/auth.json` | JSON | admin API | admin account/password actions | Admin users, password hashes, roles, legacy compatibility. |
| `/etc/v7/admin/safe-mode.json` | JSON | admin API | safe-mode action | Blocks dangerous actions when enabled. |
| `/opt/v7/admin/v7-identity.db` | SQLite | admin API | admin API | Identity, organizations, devices, pending profiles, connect sessions. |
| `/opt/v7/traffic/traffic.sqlite` | SQLite | admin API | external traffic snapshot/runtime | Traffic summaries and live views. |

## Registry Format Contract

Registry rows are parsed as whitespace-separated `key=value` pairs. Consumers tend to ignore unknown keys, which makes additive fields safer than renames.

Unsafe changes:

- renaming `ip`, `id`, `current`, `interface`, `enabled`;
- changing boolean encoding without compatibility;
- changing file location without wrappers;
- introducing multiline values.

## JSON Contract Pattern

Most JSON state files are dictionaries with schema-ish keys such as:

- `updated`;
- `items`;
- `users`;
- `summary`;
- `history`;
- `latest`.

Readers commonly tolerate missing files by using defaults. That tolerance must not be confused with schema freedom; silent defaults can hide runtime drift.

