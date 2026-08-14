# PERF.1 Static Measurement

## Static Counts

| File | Lines | Bytes | read_json | read_jsonl | read_text | sqlite3 | subprocess.run | run_readonly | curl refs | socket refs | writes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `tools/v7-users-autoswitch` | 2959 | 148165 | 16 | 0 | 3 | 0 | 3 | 0 | 0 | 0 | 6 |
| `admin_core/routing_intelligence.py` | 648 | 27298 | 4 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| `admin_core/routing_brain.py` | 377 | 17428 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `tools/v7-routing-intelligence-shadow` | 89 | 3471 | 7 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `tools/v7-service-matrix-test` | 554 | 21771 | 2 | 0 | 2 | 0 | 1 | 0 | 4 | 10 | 2 |
| `tools/v7-egress-quality-compact` | 229 | 8924 | 6 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 3 |
| `admin/v7-admin-api` | 35748 | 2093199 | 91 | 8 | 52 | 8 | 8 | 54 | 47 | 9 | 54 |
| `admin_core/runtime_read_views.py` | 121 | 4352 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `admin_core/route_reality_views.py` | 164 | 6393 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `admin_core/diagnostic_views.py` | 242 | 9820 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `admin_core/performance_summaries.py` | 181 | 6081 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Writes count combines `write_json_atomic` and append helpers where statically visible. The counts are static references, not live execution counts.

## Pure Routing Brain Synthetic Measurement

Synthetic local model:

- 50 candidate channels
- 10 required services
- 200 audit records
- 2000 total users supplied as model input
- no network
- no subprocess
- no runtime writes

Measured result:

- single call: about 46.5 ms
- 20 calls: about 945.5 ms total
- average call: about 47.3 ms

Interpretation:

Current RI.3 Brain cost is acceptable as a bounded advisory for small candidate sets, but it is too expensive to run per user across 2000 users in a hot runtime path. It must be precomputed or grouped before runtime.

## API.4 Prior Measurement

API.4 pure builder timing:

- overview summary builder: 0.035 ms
- egress health summary: 0.011 ms

Interpretation:

Pure payload builders are negligible compared with command probes, route checks, JSONL reads, SQLite summaries, and network tests.
