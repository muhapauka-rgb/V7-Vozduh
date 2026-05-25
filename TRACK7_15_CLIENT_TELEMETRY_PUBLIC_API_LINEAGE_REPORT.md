# V7 Vozduh Track 7.15 Report

## Client Telemetry & Public Speed API Lineage Batch

Track 7.15 resolved repo-side lineage for the narrow client telemetry/public speed-token API layer. No VPS runtime mutation, live public API execution, telemetry ingestion, service start/stop, deploy, token rotation, profile delivery, routing/datapath/autoswitch/policy change, chmod/chown, delete/archive, or restart was performed.

## 1. Tools Resolved

```text
v7-client-speed-api
v7-path-sample-ingest
```

Resolution basis:

- Both tools are present in `runtime-enumeration.json`.
- Both have exact-hash repo-side representations.
- No runtime source copy was needed.

Runtime evidence:

```text
v7-client-speed-api
  runtime path: /usr/local/bin/v7-client-speed-api
  sha256: 2d12e7f45f7e905a9b1d27abc1b3760b9edf347d5cbef007d87e58952c6531f0
  mode: 0755
  size: 20387
  mtime epoch: 1779379648
  systemd: v7-client-speed-api.service

v7-path-sample-ingest
  runtime path: /usr/local/bin/v7-path-sample-ingest
  sha256: 8032c394d888cc079d13db6d19eff91d62bdba8505df9b37c165bae1ebfd8224
  mode: 0755
  size: 5771
  mtime epoch: 1779379081
  systemd: none
```

## 2. Tools Skipped

No in-scope recommended tools were skipped.

Optional tools were not present in runtime enumeration:

```text
v7-path-sample-summary
v7-client-speed-summary
v7-client-speed-report
```

## 3. Repo Paths Created / Updated

Created:

```text
docs/track7/lineage/client-telemetry-public-api-tools.json
TRACK7_15_CLIENT_TELEMETRY_PUBLIC_API_LINEAGE_REPORT.md
```

Updated:

```text
docs/track7/PRODUCTION_ONLY_TOOL_GOVERNANCE.md
```

Repo-side runtime representations already existed unchanged:

```text
tools/v7-client-speed-api
tools/v7-path-sample-ingest
```

## 4. Lineage Metadata File

```text
docs/track7/lineage/client-telemetry-public-api-tools.json
```

The metadata records:

- runtime path, sha256, size, mode, mtime;
- systemd/reference evidence;
- governance class, criticality, release relevance, provenance confidence;
- repo path;
- owner/purpose/mutation classification;
- public API behavior;
- token behavior;
- telemetry/client-data reads and writes;
- logging/redaction behavior;
- audit behavior;
- verification requirements.

## 5. Public Telemetry Safety Review

`v7-client-speed-api`:

- Starts a `ThreadingHTTPServer`.
- Serves `/`, `/health`, `/api/my-speed`, `/api/agent/poll`.
- Accepts POST `/api/sample`.
- Reads `users.registry` and `egress.registry`.
- Writes `client-speed.json`, `client-agents.json`, and `client-commands.json`.
- Calls `v7-path-sample-ingest` as a subprocess for V7-mode samples.
- Suppresses default request logging.
- Stores client IP and User-Agent in telemetry state.
- Does not read or write `profile-delivery-tokens.json`.
- Does not print private keys or profile delivery tokens.

`v7-path-sample-ingest`:

- Reads sample JSON from stdin or file.
- Validates user IP, ingress, egress, mbps, and sample fields.
- Writes `path-samples.json` unless `--dry-run` is used.
- Emits JSON output that may include client IP and target URL.
- Does not parse profile delivery tokens.
- Does not call routing/proxy/policy/apply tools.

Safety verdict:

```text
lineage-only safe: yes
live execution safe in this track: no
telemetry privacy proven: no
runtime mutation if executed normally: yes
```

## 6. Owner / Purpose / Mutation Classification

```text
v7-client-speed-api
owner: client-telemetry
purpose: public/client speed-test API and agent polling endpoint
mutation level: public-api-service telemetry-write client-data-write
release relevance: must_be_release_owned
runtime criticality: runtime-critical
provenance confidence: high

v7-path-sample-ingest
owner: path-quality
purpose: validate and persist bounded client path benchmark samples
mutation level: telemetry-ingest telemetry-write
release relevance: runtime_local_allowed
runtime criticality: operator-convenience
provenance confidence: medium
```

## 7. Static Verification Results

```text
tools/v7-run-tests
Ran 28 tests
OK

python3 -m json.tool docs/track7/lineage/client-telemetry-public-api-tools.json
OK

PYTHONPYCACHEPREFIX=/private/tmp python3 -m py_compile admin/v7-admin-api admin_core/*.py tools/v7-release-lineage-check tools/v7-runtime-repo-diff tools/v7-client-speed-api tools/v7-path-sample-ingest
OK
```

No service was started and no telemetry sample was ingested.

## 8. Updated Governance Counts

Before Track 7.15:

```text
Runtime-only unresolved tools: 78
Critical unresolved lineage: 52
Total lineage resolved in metadata: 49
```

After Track 7.15:

```text
Runtime-only unresolved tools by basename: 78
Critical unresolved lineage by basename: 52
Total lineage resolved in metadata: 51
Remaining known unresolved by lineage metadata: 67
```

Note:

Both resolved tools already had exact repo-side representations, so this batch improves lineage metadata and release ownership without reducing the evidence-level runtime-only unresolved diff count.

## 9. Runtime / Repo Diff Result

```text
V7 runtime/repo governance diff (read-only)
Runtime governance: partial
Authoritative runtime tools: 24
Production-only tools: 78
Named lineage gaps: 78
Critical lineage gaps (known): 52
Unlisted lineage gaps: 0
Safe convergence candidates (known): 4
warnings:
  - runtime_manifest_not_supplied
```

## 10. Release Object Warning Status

```text
V7 release lineage check (read-only)
lineage_resolved_tools=51
remaining_known_unresolved=67
runtime_lineage=partial
release_provenance=incomplete
```

Warnings remain:

- runtime manifest is not locally available at the default live path;
- source worktree is dirty;
- 67 known production-only tools still require lineage;
- archive manifests are not locally available at default live paths.

## 11. Remaining Public Telemetry / Privacy Blockers

- Public speed telemetry writes client IP, User-Agent, route/egress context, and measurement samples.
- Token-scoped public access is mediated by `v7-public-gateway`, but telemetry privacy has not been audited end-to-end.
- Public speed API is runtime-critical and systemd-bound; no live service behavior was tested in this track.
- Path sample writes are state mutation and require dedicated safe test fixtures before behavioral tests.

## 12. Next Bounded Batch Safety

Next bounded batch is safe only if it remains lineage-only and avoids routing/autoswitch/policy apply behavior.

Recommended next candidate class:

```text
policy/direct/proxy preview or guard-readiness tooling only
```

Do not include apply tools, routing sync, user switching, autoswitch mutation, or Trusted RU/Gosuslugi changes without a separate high-risk review.
