# V7 Vozduh Track 7.14 Report

## Profile Delivery & Token Tooling Lineage Batch

Track 7.14 resolved the repo-side lineage for the profile delivery public gateway layer. No VPS runtime mutation, live profile delivery, token rotation, onboarding execution, chmod/chown, restart, deploy, routing change, autoswitch change, or Trusted RU/Gosuslugi change was performed.

## 1. Tools Resolved

```text
v7-public-gateway
```

Resolution basis:

- Present in `runtime-enumeration.json`.
- Runtime path: `/usr/local/bin/v7-public-gateway`.
- Runtime sha256: `0ea593ad7bb8c79abe2fe3f1b3d518684b7211d571c994efbc481df9488bd123`.
- Exact repo-side representation already exists at `tools/v7-public-gateway`.
- Systemd referenced by `v7-public-gateway.service`.

## 2. Tools Skipped

```text
v7-client-speed-api
v7-path-sample-ingest
```

Skip reason:

- `v7-client-speed-api` is token-scoped public speed/client telemetry support, not profile delivery, token issuance, onboarding, or profile artifact publishing.
- `v7-path-sample-ingest` is a path-sample telemetry writer called by `v7-client-speed-api`.
- Both should be handled in a separate client telemetry/public API lineage batch.

Related tools already resolved:

```text
v7-smart-client-profile-generate -> Track 7.10
v7-user-reissue-config -> Track 7.10
v7-sensitive-state-check -> Track 7.9
```

## 3. Repo Paths Created / Updated

Created:

```text
docs/track7/lineage/profile-delivery-token-tools.json
TRACK7_14_PROFILE_DELIVERY_TOKEN_LINEAGE_REPORT.md
```

Updated:

```text
docs/track7/PRODUCTION_ONLY_TOOL_GOVERNANCE.md
```

Runtime tool source already existed unchanged:

```text
tools/v7-public-gateway
```

## 4. Lineage Metadata File

```text
docs/track7/lineage/profile-delivery-token-tools.json
```

The metadata records:

- runtime path, sha256, size, mode, mtime;
- systemd/reference evidence;
- governance class and release relevance;
- repo path;
- owner/purpose/mutation classification;
- token/profile/onboarding behavior;
- secret redaction behavior;
- explicit skipped/deferred tools.

## 5. Delivery / Token Safety Review

`v7-public-gateway` is a public allowlist proxy. It allows:

```text
/connect
/api/connect/start
/api/connect/status
/api/profile-delivery-qr
/api/profile-import-qr
/profile-delivery/<token>
/profile-import/<token>
/speed-test/<token>
/api/public-speed-sample/<token>
```

Safety findings:

- Does not create profile delivery tokens.
- Does not rotate profile delivery tokens.
- Does not persist delivery token state.
- Does not read `profile-delivery-tokens.json`.
- Does not print tokens through default request logging; `log_message` is suppressed.
- Strips `Cookie` and `Authorization` headers before proxying.
- Parses token values from URL paths and validates token-shaped path components.

Important boundary:

Profile delivery token lifecycle remains monolith-owned inside `admin/v7-admin-api`; this batch resolves the public ingress lineage, not end-to-end onboarding safety.

## 6. Owner / Purpose / Mutation Classification

```text
v7-public-gateway
owner: delivery
purpose: public allowlist gateway for connect/profile delivery/profile import/token-scoped public paths
mutation level: public-delivery-proxy
token reads: URL path token parsing only
token writes: none
profile artifact writes: none
onboarding behavior: forwards public connect requests to admin upstream
audit behavior: none observed
release relevance: must_be_release_owned
runtime criticality: runtime-critical
provenance confidence: high
```

## 7. Static Verification Results

```text
tools/v7-run-tests
Ran 28 tests
OK

PYTHONPYCACHEPREFIX=/private/tmp python3 -m py_compile admin/v7-admin-api admin_core/*.py tools/v7-release-lineage-check tools/v7-runtime-repo-diff tools/v7-public-gateway
OK

python3 -m json.tool docs/track7/lineage/profile-delivery-token-tools.json
OK
```

No live gateway execution was performed.

## 8. Updated Governance Counts

Before Track 7.14:

```text
Runtime-only unresolved tools by basename: 78
Critical unresolved lineage by basename: 52
Total lineage resolved in metadata: 48
```

After Track 7.14:

```text
Runtime-only unresolved tools by basename: 78
Critical unresolved lineage by basename: 52
Total lineage resolved in metadata: 49
Remaining known unresolved by lineage metadata: 69
```

Note:

`v7-public-gateway` already had an exact repo-side representation at `tools/v7-public-gateway`, so this batch improved lineage metadata and release ownership without reducing the runtime-only unresolved diff count.

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

The diff tool remains evidence-level: it reports the runtime/repo production-only set from `runtime-enumeration.json`, not lineage metadata completion.

## 10. Release Object Warning Status

```text
V7 release lineage check (read-only)
lineage_resolved_tools=49
remaining_known_unresolved=69
runtime_lineage=partial
release_provenance=incomplete
```

Warnings remain:

- runtime manifest is not locally available at the default live path;
- source worktree is dirty;
- 69 known production-only tools still require lineage;
- archive manifests are not locally available at default live paths.

Commercial reproducibility remains incomplete.

## 11. Remaining Onboarding / Profile Blockers

- Profile delivery token lifecycle remains inside `admin/v7-admin-api`.
- `profile-delivery-tokens.json` remains sensitive runtime state and should not be hardened blindly.
- Public connect onboarding invokes user creation/profile generation flows from the monolith.
- Client speed/token telemetry tooling remains unresolved in this specific lineage scope.
- No live onboarding/profile delivery behavior was verified or executed.

## 12. Next Bounded Batch Safety

Next batch is safe only if it remains narrow and does not execute runtime behavior.

Recommended next bounded batch:

```text
client telemetry / public speed-token support
```

Candidate tools:

```text
v7-client-speed-api
v7-path-sample-ingest
```

Do not combine that batch with routing, autoswitch, policy, Direct/RU, proxy apply, or user mutation tools.
