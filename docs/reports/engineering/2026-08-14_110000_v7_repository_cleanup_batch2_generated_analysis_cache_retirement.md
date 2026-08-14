# V7 Repository Cleanup Batch 2 — Generated Analysis Cache Retirement

Status: `COMPLETE_BOUNDED_NON_RUNTIME_CLEANUP`

Date: `2026-08-14`

## Decision

The existing Understand Anything output was classified by meaning rather than
name. `knowledge-graph.json`, configuration, metadata and exclusion rules are
retained because the current RS6.2 audit contract may reuse the generated graph
as bounded relationship evidence. Two files are local incremental-analysis
caches, not Architecture Truth, Runtime Truth or unique evidence:

| Artifact | Bytes | SHA-256 | Consumer result | Disposition |
| --- | ---: | --- | --- | --- |
| `.understand-anything/fingerprints.json` | 1,030,118 | `289a29d326014024d6e7e1fc1f3f03c6dec4afadc43ba2bec0cfb43ed25b2495` | no project/Runtime/test/CI consumer | `REGENERABLE_DELETE` |
| `.understand-anything/intermediate/scan-result.json` | 246,460 | `c3b0a4eff9df3ea526b63f3702e59be3c7ef99c571bfe6518d1e425349bf6578` | no project/Runtime/test/CI consumer | `REGENERABLE_DELETE` |

The retained graph metadata says it was generated from commit
`97e651bb8b414b03d2b1de3b50acc0c9399f2e72`; therefore neither deleted cache
could honestly represent current live source truth. A future analysis run may
regenerate both locally. `.understand-anything/.gitignore` now prevents their
reintroduction while preserving the intentional graph artifact.

## Effects

- current tracked tree reduction: 1,276,578 bytes;
- Runtime/deploy/routing/user/Authority/Production Maturity effects: `NONE`;
- Git history rewrite: `NONE`;
- unique production evidence removed: `NONE`;
- existing RS6.2 graph consumer preserved: `YES`.

## Exact successor

Continue RS6 artifact disposition. Large Track 7 and production evidence
snapshots remain `UNKNOWN_REQUIRES_OWNER_REVIEW` until a compact owner-backed
manifest and retention/archive contract prove that raw evidence can be retired.
