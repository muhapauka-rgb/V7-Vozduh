# Runtime Governance Snapshot

Evidence source:

```text
runtime-enumeration.json
tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty
tools/v7-release-lineage-check --release-dir releases/v7-runtime-20260523T174503Z --pretty
docs/track7/truth-snapshot/evidence/section-governance-markers.txt
```

## Runtime Enumeration

```text
runtime_tools=141
authoritative_runtime=26
repo_missing_critical=59
runtime_local_pending_lineage=37
repo_missing_noncritical=19
runtime-critical=26
must_be_release_owned=93
runtime_local_allowed=48
```

## Runtime / Repo Diff

```text
Runtime governance: partial
Authoritative runtime tools: 24
Production-only tools: 56
Named lineage gaps: 56
Critical lineage gaps (known): 33
Unlisted lineage gaps: 0
Safe convergence candidates (known): 4
warning=runtime_manifest_not_supplied
```

## Release Lineage

```text
release_object_ready=true
runtime_lineage=partial
release_provenance=incomplete
production_only_tools=118
lineage_resolved_tools=75
remaining_known_unresolved=43
```

Warnings:

```text
runtime_manifest_missing_locally_or_not_supplied
source_worktree_dirty
known_43_production_only_tools_require_lineage
archive_manifest_missing_locally_or_not_supplied
```

## Governance Verdict

Governance is much better than at Track 7 start, but commercial reproducibility is not complete. Runtime is named and partially governed, while critical lineage and runtime-only drift remain material blockers.
