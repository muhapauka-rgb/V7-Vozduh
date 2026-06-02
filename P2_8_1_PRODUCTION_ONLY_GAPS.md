# P2.8.1 Production Only Gaps

Project: V7 Vozduh
Block: P2.8.1

## Production-Only Or Uncertified Artifacts

| Artifact | Evidence | Gap |
| --- | --- | --- |
| `/usr/local/bin/v7-admin-api` | runtime hash differs from local and GitHub audited hashes | origin commit/deploy source UNKNOWN |
| `/usr/local/bin/v7-api` | runtime hash exists; no exact local basename found | repository source UNKNOWN |
| `/usr/local/bin/v7-traffic-snapshot` | referenced by systemd; no exact local basename found during audit | repository source UNKNOWN |
| `/etc/systemd/system/v7-admin-api.service` | runtime unit exists; no local exact systemd source found | deployment lineage UNKNOWN |
| `/etc/systemd/system/v7-public-gateway.service` | runtime unit exists; no local exact systemd source found | deployment lineage UNKNOWN |
| `/etc/systemd/system/v7-api.service` | runtime unit exists; no local exact systemd source found | deployment lineage UNKNOWN |
| `/etc/systemd/system/v7-client-speed-api.service` | runtime unit exists; no local exact systemd source found | deployment lineage UNKNOWN |
| `/etc/v7` | 90 files at maxdepth 3 | config/state ownership requires separate secret-safe classification |
| `/opt/v7` | 512 files at maxdepth 3 | live state/event stores are production truth, not repository content |
| `codex/dynamic-load-autoswitch-pr` | remote branch exists live on GitHub but is not present as a local branch | branch purpose and merge state UNKNOWN |

## Non-Gaps Found

Several runtime tools match local/GitHub `origin/Updatesystem` hashes exactly: public gateway, client speed API, direct auto sync, users autoswitch, service matrix refresh, egress quality compactor, and telegram sentinel.

## Recommendation

Keep production-only artifacts quarantined as runtime truth until a signed deploy manifest maps runtime path, SHA256, source ref, deployment time, and deploy actor.
