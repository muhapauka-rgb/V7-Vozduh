# API.1 Performance Foundation Audit

Mode: static performance audit. No live profiling and no runtime changes were performed.

## Largest Hotspots

| Component | Lines | Risk | Performance concern |
|---|---:|---|---|
| `html_page_v2` | 12,370 | MEDIUM/HIGH | Large in-process HTML/CSS/JS string construction and hard-to-review UI coupling. |
| `Handler` | 4,005 | HIGH | Large endpoint dispatch body; auth, routing, JSON/file responses, actions, and redirects share one class. |
| `overview` and related builders | 163+ direct lines plus many helper calls | HIGH | Aggregates many registries, policies, diagnostics, events, traffic, service matrix, and identity summaries. |
| egress draft/runtime helpers | 300+ line functions | HIGH | Parse, validate, test, run commands, and prepare runtime artifacts in one area. |
| service/policy/trusted RU helpers | scattered | MEDIUM/HIGH | Can repeat registry and policy reads across request paths. |

## Repeated Work Patterns

Static scan found many repeated references to:

- `read_text`;
- `read_json`;
- `write_json_atomic`;
- `append_jsonl`;
- `parse_registry`;
- `run_readonly`;
- `run_action`;
- `sqlite3`;
- `urllib.request`;
- traffic snapshot commands;
- service matrix checks;
- policy matrix/route tests.

The risk is not simply file size. The risk is request-time recomputation across independent helpers without a shared request snapshot.

## Calculations That Should Not Stay In Hot Request Paths

| Calculation | Target strategy |
|---|---|
| Full overview aggregation | request-scoped snapshot plus short TTL cache |
| service matrix freshness and route fitness | background refresh/cache producer plus cheap summary read |
| traffic SQLite live summaries | cached summary or explicit refresh endpoint |
| Trusted RU diagnostics | async/background result with read-only status endpoint |
| egress speed tests and route probes | explicit action/preflight endpoint, not automatic overview recompute |
| backup verification | explicit verify endpoint or cached latest verification result |
| registry cross-joins for recommendations | precomputed summary or request snapshot |
| profile/client artifact inspection | lazy detail endpoint |

## Calculations That Can Be Cached

| Data | Cache form | Invalidated by |
|---|---|---|
| registry snapshot | request-local and small TTL | registry mtime/hash change |
| overview summary | short TTL JSON snapshot | state/registry/policy/audit/event mtime |
| service matrix summary | file-backed latest result | service matrix refresh tool |
| route-class metadata | mtime/hash cache | route class registry/policy change |
| audit/event page reads | bounded page cache | audit/event file growth |
| identity read model | SQLite mtime and query cache | identity action write |

## Async Or Background Candidates

| Candidate | Reason |
|---|---|
| Trusted RU diagnostic and decision refresh | command may be slow and network-sensitive |
| service matrix refresh | probes are external and potentially slow |
| traffic live snapshots | can involve SQLite and external helper |
| backup verify latest | disk/archive work should not block overview |
| egress draft runtime tests | command-heavy; explicit operation history is better |
| proxy public canary checks | network/proxy-sensitive and should be explicit |

## Runtime Path Map

| Request class | Allowed work | Avoid |
|---|---|---|
| GET read APIs | cheap file reads, cached summaries, pure serialization | network probes, runtime mutations, full recompute cascades |
| GET UI pages | render static shell and boot data references | heavy embedded dynamic recomputation |
| POST preview/dry-run | explicit bounded helper calls, no apply | hidden writes, implicit movement |
| POST apply | guarded command execution only after auth/CSRF/confirm | moving logic outside audited route prematurely |
| audit/evidence detail | bounded file reads, pagination | unbounded JSONL scans without limit/compaction |

## Performance Verdict

The performance foundation should be built before or during API.2 by introducing snapshot/caching primitives around read-only builders. The first improvement should be structural and behavior-preserving: shared request snapshot, bounded reads, and extracted pure summary builders.
