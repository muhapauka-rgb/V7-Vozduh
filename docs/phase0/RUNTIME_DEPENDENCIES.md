# V7 Phase 0 Runtime Dependencies

Purpose: map external commands and runtime dependencies referenced by the repository.

## Dependency Categories

- Runtime-critical: required for production routing or safety.
- Operational: required for admin/operator actions.
- Diagnostic: required for checks and visibility.
- Optional/helper: used when installed or in specific flows.
- Missing-from-repo: referenced but not implemented in this repository.

## System Dependencies

| Command | Category | Used By | Notes |
| --- | --- | --- | --- |
| `ip` | runtime-critical | hardening, benchmark, egress state | Linux routing/interface inspection. |
| `nft` | runtime-critical | kill switch, benchmark, direct diagnostics | nftables kill switch and direct/RU sets. |
| `systemctl` | runtime-critical | systemd install, OpenVPN lifecycle, admin actions | Linux service control. |
| `wg` | runtime-critical | admin API handshake/readiness flows | WireGuard peer/runtime inspection. |
| `wg-quick` | runtime-critical | `v7-egress-set-state` | WireGuard egress up/down. |
| `awg-quick` | runtime-critical | `v7-egress-set-state` | AmneziaWG egress up/down. |
| `openvpn` | runtime-critical | OpenVPN egress runtime | OpenVPN egress process. |
| `sing-box` | runtime-critical/operational | admin smart profile checks | Config check/runtime profile ecosystem. |
| `curl` | diagnostic/runtime | service matrix, direct diagnostics, benchmark | Service reachability and speed. |
| `ping` | diagnostic | MTU probe, benchmark | MTU/DF probing. |
| `dig` | diagnostic | direct/RU diagnostics | DNS classification diagnostics. |
| `dnsmasq` | runtime-critical for direct/RU MVP | direct render docs/scripts | Local DNS classification path. |
| `flock` | operational | path guard repair | Locking repair runs. |

## V7 Commands Referenced But Not Fully Present In Repo

These commands are expected to exist in production runtime, usually under `/usr/local/bin`.

| Command | Category | Referenced By | Notes |
| --- | --- | --- | --- |
| `v7-safe-run` | operational safety | admin diagnostics | Wrapper for safe diagnostic command execution. |
| `v7-system-check` | diagnostic | admin diagnostics/docs | System health aggregate. |
| `v7-user-route-check` | diagnostic | admin diagnostics/docs | Per-user route verification. |
| `v7-state-stale-check` | diagnostic | admin overview | State freshness check. |
| `v7-killswitch-check` | runtime safety | admin, hardening, docs | Repo has hardening source. |
| `v7-killswitch-status` | runtime safety | admin API | Status command referenced; source not present. |
| `v7-killswitch-enable` | runtime safety | `v7-egress-set-state`, hardening | Repo has hardening source. |
| `v7-user-create` | provisioning | admin API | Production provisioning command, not in repo. |
| `v7-user-create-from-ipam` | provisioning | admin API | Production provisioning command, not in repo. |
| `v7-user-disable` | provisioning | admin API | Production command, not in repo. |
| `v7-user-enable` | provisioning | admin API | Production command, not in repo. |
| `v7-user-switch` | runtime-critical | admin API, autoswitch | Core per-user egress switch command, not in repo. |
| `v7-user-reissue-config` | provisioning | admin API | Production command, not in repo. |
| `v7-user-reconcile-apply` | provisioning | admin API | Production repair command, not in repo. |
| `v7-user-rotate-key` | provisioning | admin API | Sensitive production command, not in repo. |
| `v7-users-rebalance-dry-run` | autoswitch/ops | admin API | Dry-run command, not in repo. |
| `v7-egress-speedtest` | diagnostics | admin API | Per-egress speed test, not in repo. |
| `v7-service-matrix-test` | diagnostics | admin API/systemd | Repo has source in `tools/`. |
| `v7-service-matrix-refresh-all` | diagnostics | systemd | Repo has source in `tools/`. |
| `v7-egress-set-state` | lifecycle | admin API | Repo has source in `tools/`. |
| `v7-audit-log` | audit | admin API/tools | Production audit writer, not in repo. |
| `v7-backup-create` | operational | admin API | Production command, not in repo. |
| `v7-backup-verify` | operational | admin API | Production command, not in repo. |
| `v7-backup-restore-preview` | operational | admin API | Production command, not in repo. |
| `v7-rollback-last-change` | operational | admin API | Production command, not in repo. |
| `v7-direct-add-domain` | direct/RU | admin API | Production command, not in repo. |
| `v7-direct-remove-domain` | direct/RU | admin API | Production command, not in repo. |
| `v7-direct-refresh-domains` | direct/RU | admin API | Production command, not in repo. |
| `v7-policy-*` | policy | admin API | Multiple policy helpers referenced, not all present. |
| `v7-proxy-*` | proxy runtime | admin API | Proxy runtime helpers referenced, not in repo. |
| `v7-trusted-ru-*` | trusted RU | admin API | Trusted RU diagnostic/decision helpers referenced, not in repo. |
| `v7-path-sample-ingest` | measurement | admin/client speed | Repo has source in `tools/`. |

## Dependency Risk

The repository is not self-contained for production. That is acceptable for the current shell-core architecture, but Phase 1/2 should document or import missing command contracts before refactoring callers.

## Phase 0 Rule

Do not replace these dependencies in Phase 0. Only document them.

