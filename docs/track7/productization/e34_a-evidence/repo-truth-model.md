# E34.A Repo Truth Model

repo_truth_model_defined=true

## Definition

repo_truth is the source-controlled intended state of code, documentation, manifests, schemas, tests, and release metadata.

## Repo Truth Components

| Component | Meaning |
| --- | --- |
| repository_version | Branch and HEAD commit. |
| commit_identity | Full commit SHA, commit timestamp, author, signed/verified status if available. |
| release_identity | Release id or tag that packages the commit. |
| repository_lineage | Parent commits, tag ancestry, branch relationship, PR/review references. |
| tracked_manifest | Files expected to be deployed or packaged. |
| expected_config_schema | Schemas and defaults expected by runtime. |

## Repository Snapshot

```text
repo_snapshot_id
branch
head_commit
dirty_worktree
tracked_file_manifest_hash
release_manifest_ref
schema_version
certification_refs
```

## Working Tree Rule

Uncommitted files may be architecture work in progress, but they are not release truth until committed and included in a release object.

## Fail-Closed Rule

If repo truth is dirty, unsigned, ambiguous, or missing release identity, production deployment may continue only as development/staging state, not certified commercial release.

repo_truth_model_defined=true
