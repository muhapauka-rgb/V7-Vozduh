# PERF.1 Duplication Audit

## Duplicate Calculations

Observed patterns:

- Service suitability exists in planner logic and RI advisory logic.
- Route reality exists in admin live reads and route helper summaries.
- Traffic summaries mix SQLite reads with admin payload construction.
- Direct-routing checks can be called from diagnostics and quick status views.

Verdict:

- Acceptable today because extracted modules are pure builders and planner remains owner.
- Risk becomes HIGH if RI starts recomputing full service suitability per user instead of consuming shared snapshots.

## Duplicate Reads

Observed patterns:

- `admin/v7-admin-api` still has many `read_json`, `read_text`, `run_readonly`, SQLite, and JSONL references.
- Planner reads multiple state files during initialization.
- RI shadow and planner can both read service matrix, quality summary, preferences, and audit records.

Verdict:

- Runtime path must get a single request/run snapshot.
- Heavy Brain must own repeated history/service reads and publish compact outputs.

## Duplicate History Scans

Observed patterns:

- Planner reads recent switch history.
- RI shadow can read audit logs.
- Admin operator observability can search audit/evidence records.

Verdict:

- Full history scanning must not enter runtime.
- PERF.2 should define bounded aggregations and trust summaries.

## Duplicate Probes

Observed patterns:

- Service matrix tool performs curl/socket probes.
- Admin diagnostics can run direct route/domain checks.
- Traffic live endpoint can call external snapshot helper.

Verdict:

- Probes must be scheduled/adaptive and never hidden inside runtime decision path.

## Duplicate Summaries

Observed patterns:

- Overview, diagnostics, runtime read views, and performance summaries all describe health state from different angles.

Verdict:

- The single truth should be snapshot store schemas, not duplicated endpoint-specific recomputation.
