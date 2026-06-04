# Service Intelligence Reality Map

## Existing Service Data

| Data | Owner / Producer | Storage | Consumer | Status |
|---|---|---|---|---|
| Service catalog and service checks | `tools/v7-service-matrix-test` | per-run output and `service-matrix.json` | service matrix refresh, autoswitch, admin views, RI models | EXISTS |
| Full service matrix refresh | `tools/v7-service-matrix-refresh-all`, `systemd/v7-service-matrix-refresh.*` | `/opt/v7/egress/state/service-matrix.json` and refresh summary/event | autoswitch, admin API, RI, snapshot workers | EXISTS |
| Service recommendations | `admin_core/service_views.py` and admin API wrappers | read-only derived payload | Admin API/UI | EXISTS |
| Service history read model | `ServiceHistoryStore` | derived in memory or saved if caller chooses | Routing Brain, workers, shadow CLI | EXISTS, non-authoritative |
| Service scores | `ServiceIntelligenceEngine` and `build_service_score_snapshots` | `service-scores.json`, `channel-service-scores.json` | runtime fast path and admin/overview | EXISTS |
| User service weights | `UserServiceWeights` from `service-preferences.json` | in-memory model; snapshot contract exists | Routing Brain advisory, future user-service snapshot | PARTIAL |
| Service snapshot production | `admin_core/intelligence_workers.py` | `/opt/v7/egress/state/intelligence` | runtime planner fast path | EXISTS for six production-confirmed files |

## Service Scores Already Existing

- RI.1 service score per service/target/window.
- RI.2/RI.3 weighted service score and candidate advisory score.
- PERF.3 `service-scores.json`.
- PERF.3 `channel-service-scores.json`.
- Autoswitch native `service_suitability.aggregate_score`.

## Truth Source

Canonical mutable service truth:

- `/opt/v7/egress/state/service-matrix.json`
- `/opt/v7/egress/state/egress-quality-summary.json`
- `/opt/v7/egress/state/service-preferences.json`
- `/opt/v7/egress/state/egress.registry`

Derived service truth:

- `/opt/v7/egress/state/intelligence/service-scores.json`
- `/opt/v7/egress/state/intelligence/channel-service-scores.json`

RI.4 must not create a parallel service matrix, service history store, or service score authority.

## Reuse / Extend Verdict

| RI.4 Need | Verdict |
|---|---|
| Service catalog | REUSE `tools/v7-service-matrix-test` |
| Service observations | REUSE `service-matrix.json` |
| Service history | EXTEND `ServiceHistoryStore`; do not create new store |
| Service scores | EXTEND `ServiceIntelligenceEngine` and snapshot workers |
| User-specific service weights | EXTEND `UserServiceWeights` and optionally implement existing `user-service-scores` snapshot contract |
| Service recommendations UI | REUSE admin/service read views |

