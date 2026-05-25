# V7 Vozduh — Track 7.6 Observability & Capacity Support Lineage Batch

## 1. Tools Resolved

Resolved recommended observability/capacity batch:

```text
v7-observability-summary
v7-capacity-check
v7-capacity-readiness
v7-service-matrix-test
v7-egress-quality-compact
v7-path-benchmark
v7-path-optimizer-advice
```

Five tools were already exact-hash present in the repo:

```text
tools/v7-observability-summary
tools/v7-service-matrix-test
tools/v7-egress-quality-compact
tools/v7-path-benchmark
tools/v7-path-optimizer-advice
```

Two tools were copied read-only from live VPS `/usr/local/bin` into repo-side lineage location:

```text
tools/runtime-support/v7-capacity-check
tools/runtime-support/v7-capacity-readiness
```

No VPS runtime files were modified.

## 2. Tools Skipped

No recommended tool was skipped.

Optional tools intentionally skipped to keep this batch bounded:

```text
v7-egress-speedtest
v7-egress-history
v7-egress-load
v7-egress-stability
v7-recent-performance
v7-state-stale-check
v7-system-check
```

These are good candidates for a later observability/runtime-health batch, but importing them now would expand the scope too far.

## 3. Repo Paths Created / Updated

New repo-side runtime-support copies:

```text
tools/runtime-support/v7-capacity-check
tools/runtime-support/v7-capacity-readiness
```

Existing exact-hash repo paths used for lineage:

```text
tools/v7-observability-summary
tools/v7-service-matrix-test
tools/v7-egress-quality-compact
tools/v7-path-benchmark
tools/v7-path-optimizer-advice
```

## 4. Lineage Metadata File

Created:

```text
docs/track7/lineage/observability-capacity-support-tools.json
```

Metadata includes:

- basename;
- batch name;
- runtime path;
- sha256;
- size;
- mode;
- mtime epoch;
- governance class;
- runtime criticality;
- release relevance;
- provenance confidence;
- reference count and samples;
- repo path;
- owner;
- purpose;
- mutation level;
- state reads/writes;
- verification requirement;
- lineage status.

## 5. Owner / Purpose / Mutation Classification

| Tool | Owner | Mutation Level | Purpose |
|---|---|---|---|
| `v7-observability-summary` | `observability` | `state-read` | Build calm operator-facing health summary |
| `v7-capacity-check` | `capacity` | `runtime-check` | Check subnet/user capacity and legacy references |
| `v7-capacity-readiness` | `capacity` | `runtime-check` | Check staged IPAM/capacity readiness |
| `v7-service-matrix-test` | `service-matrix` | `summary-write` | Run service probes and update service matrix |
| `v7-egress-quality-compact` | `path-quality` | `metric-write` | Compact egress quality summaries/rings |
| `v7-path-benchmark` | `path-quality` | `runtime-check` | Benchmark path quality; writes only with `--write` |
| `v7-path-optimizer-advice` | `path-quality` | `summary-write` | Convert benchmark data to operator advice; writes only with `--write` |

None of these tools was executed against live state in Track 7.6.

## 6. Static Verification Results

Static checks:

```text
python3 -m py_compile tools/v7-observability-summary
python3 -m py_compile tools/v7-service-matrix-test
python3 -m py_compile tools/v7-egress-quality-compact
python3 -m py_compile tools/v7-path-benchmark
python3 -m py_compile tools/v7-path-optimizer-advice
bash -n tools/runtime-support/v7-capacity-check
bash -n tools/runtime-support/v7-capacity-readiness
```

Result:

```text
OK
```

The full local gate also passed:

```text
tools/v7-run-tests
Ran 28 tests
OK
```

## 7. Updated Governance Counts

Before Track 7.6:

```text
Runtime-only unresolved tools: 112
Critical unresolved lineage: 70
Lineage resolved in repo: 6
```

After Track 7.6:

```text
Tools resolved in this batch: 7
Runtime-only unresolved tools by basename: 110
Critical unresolved lineage by basename: 70
Total lineage resolved in metadata: 13
Remaining known unresolved by lineage metadata: 105
```

Why only two fewer runtime-only tools:

- five recommended tools were already exact-hash present in repo before this batch;
- two capacity tools were newly added to `tools/runtime-support/`.

Why critical unresolved did not drop:

- the two newly added capacity tools were classified as `runtime_local_allowed`;
- the release-critical recommended tools were already present in repo by basename before Track 7.6.

## 8. Runtime / Repo Diff Result

After Track 7.6:

```text
Runtime governance: partial
Authoritative runtime tools: 24
Production-only tools: 110
Named lineage gaps: 110
Critical lineage gaps (known): 70
Unlisted lineage gaps: 0
Safe convergence candidates (known): 4
warnings:
  - runtime_manifest_not_supplied
```

## 9. Release Object Warning Status

Release lineage checker:

```text
production_only_tools=118
lineage_resolved_tools=13
remaining_known_unresolved=105
runtime_lineage=partial
release_provenance=incomplete
```

Warnings remain:

```text
runtime_manifest_missing_locally_or_not_supplied
source_worktree_dirty
known_105_production_only_tools_require_lineage
archive_manifest_missing_locally_or_not_supplied
```

The platform is still not commercially reproducible.

## 10. Remaining Lineage Blockers

Still unresolved:

- 110 runtime-only tools by basename;
- 70 critical/release-relevant runtime-only tools by basename;
- 105 remaining tools by lineage metadata model;
- runtime manifest and archive manifests remain linked by VPS path, not local artifact;
- optional observability/runtime-health tools are still pending;
- no deployment convergence has happened.

## 11. Next Batch Safety

Next batch is safe if it stays bounded.

Recommended next batch:

```text
v7-egress-history
v7-egress-load
v7-egress-stability
v7-recent-performance
v7-state-stale-check
v7-system-check
```

`v7-egress-speedtest` should be handled carefully because it is classified as provisioning-critical and may run external network checks.
