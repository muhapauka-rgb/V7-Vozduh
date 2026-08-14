# V7 Repository Reports and Evidence Retention Reality Audit

Status: `AUDIT_COMPLETE_CLEANUP_NOT_EXECUTED`

Date: `2026-08-14`

Scope: operator-requested read-only repository/report/evidence retention audit,
consumed as input to the existing Responsibility Realignment/System Simplification
cleanup phases; no new Program or cleanup authority.

## Executive verdict

The repository needs material cleanup, but direct deletion or immediate Git-history
rewrite is unsafe. The dominant surface is not source code: the current HEAD contains
approximately `1,212.4 MiB` of logical file content, of which approximately
`1,168.7 MiB` is evidence/report/snapshot/trace/audit-like content. The safe route is
consumer-backed disposition, external archival of raw evidence with hashes and
manifests, future-generation prevention, then ordinary tracked deletion. History
rewrite is a separate last-resort decision.

The Reset Program is already recorded complete in fresh CPS. This audit does not
reopen Reset, complete an RS phase or grant deletion authority.

## Measured current reality

| Surface | Files | Logical size |
| --- | ---: | ---: |
| Complete HEAD | `8,857` | `1,212.4 MiB` |
| Evidence/report/snapshot/trace/audit-like HEAD | `7,659` | `1,168.7 MiB` |
| `docs/reports/**` | `1,283` | `215.8 MiB` |
| `docs/reports/*_EVIDENCE/**` raw evidence | `293` | `129.0 MiB` |
| `docs/reports/engineering/**` | `882` | `68.5 MiB` |
| `docs/reports/research/**` | `56` | `17.9 MiB` |
| Root-level evidence directories | `198` directories / `2,508` files | `630.7 MiB` |
| `docs/track7/**` | `3,522` | `312.7 MiB` |
| `.understand-anything/**` tracked generated analysis | `7` | approximately `4.2 MiB` |

Git object storage is much smaller than the logical checkout: the current packed Git
objects occupy approximately `58.39 MiB`. Large JSON/text snapshots compress well.
Therefore rewriting history now has high coordination risk and limited demonstrated
benefit compared with cleaning the active tree and preventing future accumulation.

## Largest confirmed surfaces

- `docs/track7/control-plane/e11_16-evidence/pre-ttl-snapshot.txt` — about `57 MiB`;
- `docs/reports/engineering/final_consumer_audit_2026-06-30/xref.tsv` — about `24 MiB`;
- `docs/track7/control-plane/e12-evidence/full-orchestration-snapshot-corrected.txt`
  — about `19 MiB`;
- `xref_important.tsv` — about `15 MiB`;
- `V7_AUTONOMOUS_MODEL_FUNCTION_GRAPH_APPENDIX.json` — about `10 MiB`;
- many Planner/Matrix/runtime observation JSON files are approximately `4.5-5.3 MiB`
  each.

The two cross-reference TSV files are referenced by one compact Engineering Report.
They are high-priority `ARCHIVE_EXTERNAL_OR_REGENERABLE` candidates after their
generation method, hash and required conclusions are preserved. The function graph
appendix has many Program/report consumers and cannot be deleted before those
references are reconciled. Large production observations participate in truth,
convergence or provenance chains and require evidence-class-specific review.

## Duplicate finding

Exact duplicate Git blobs inside `docs/reports/**` account for only approximately
`0.2 MiB` of redundant content. The problem is not exact byte duplication. It is
unbounded retention of distinct or near-distinct raw snapshots and complete
observation outputs. A checksum-only duplicate cleanup would produce negligible
shrink and would not solve the lifecycle defect.

## Required artifact dispositions

Every report/evidence artifact must receive one of:

| Disposition | Meaning |
| --- | --- |
| `KEEP_CANONICAL` | Existing canonical owner or permanent decision record. |
| `KEEP_COMPACT_REPORT` | Concise historical report with unique decision/provenance value. |
| `KEEP_TEST_FIXTURE` | Minimal deterministic fixture consumed by current tests/replay. |
| `KEEP_LOCAL_GENERATED_EXCLUDED_FROM_GIT` | Useful generated analysis retained locally but reproducible and untracked. |
| `ARCHIVE_EXTERNAL` | Raw evidence retained outside Git with immutable hash, owner and pointer. |
| `REGENERABLE_DELETE` | Output reproducible from retained source/tool/version and safe to remove. |
| `DUPLICATE_DELETE` | Semantically and evidentially redundant after consumer proof. |
| `OBSOLETE_DELETE` | No current/canonical/test/legal/Authority/rollback consumer and no unique knowledge. |
| `UNKNOWN_REQUIRES_OWNER_REVIEW` | Deletion blocked until exact consumer/provenance is resolved. |

Age, name, directory, size or lack of a static reference is not sufficient deletion
evidence.

## What should remain in Git

- source code and deployment/configuration schemas;
- current Programs, CPS/OMP and canonical owners;
- ADRs and permanent decisions;
- compact Engineering Reports preserving unique historical conclusions;
- minimum current test/replay fixtures;
- small evidence manifests with `evidence_id`, purpose, producer, timestamp,
  evidence class, content hash, storage pointer, retention and canonical conclusions.

## What should leave active Git after proof

- raw runtime/Planner/Matrix snapshots;
- full repeated before/after observations;
- generated cross-reference TSV and regenerable graphs;
- temporary audit outputs and local analysis caches;
- large journal/runtime dumps;
- superseded evidence bundles whose unique conclusion is already preserved by a
  compact report and canonical owner;
- historical program machinery with no current Runtime/test/exception consumer.

Raw evidence should use an approved external artifact/archive owner. Temporary CI
evidence may use bounded-retention workflow artifacts; immutable release evidence may
use release/object storage. Git LFS is appropriate only when a large artifact must
remain versioned with source, not as a default evidence dump.

## Safe execution sequence

1. Consume this audit as a bounded delta in the existing RS responsibility/package/
   cleanup evidence; do not reopen the completed Reset audit.
2. In the admitted RS6/RS7A/RS8/RS9 sequence, build one report/evidence
   consumer-disposition projection; do not create a new registry/framework.
3. Resolve Program/CPS/OMP/canonical/test/CI/tool/runtime references for each candidate.
4. Promote any durable knowledge that exists only in a report/evidence file.
5. Archive retained raw evidence with immutable hash, owner, location and restoration
   check.
6. Verify manifests restore the exact evidence and compact reports preserve all
   required conclusions.
7. Apply tracked deletion/relocation only in the later admitted cleanup phase with
   focused tests, reference validation and rollback/restoration path.
8. Add future-generation controls to `.gitignore`, report tooling and CI only after
   the exact retained/generated paths are classified.
9. Measure `BEFORE / AFTER / DELTA` for logical checkout, tracked paths, Git pack,
   reports, evidence directories and restored evidence coverage.
10. Consider `git filter-repo` only if active-tree cleanup is complete and measured
    clone/history cost still justifies a coordinated history rewrite with backup,
    tag/branch reconciliation and force-push approval.

## Safety boundaries

- Files deleted: `0`
- Files archived: `0`
- Git history rewritten: `NO`
- `.gitignore` changed: `NO`
- Runtime/production/routing/user/Authority effects: `NONE`
- Reset or RS phase completion claimed: `NO`

## Exact next frontier

Fresh CPS records the completed Reset Program and the active
`V7_RESPONSIBILITY_REALIGNMENT_AND_SYSTEM_SIMPLIFICATION_PROGRAM_V1`. Its detailed
execution fields remain at `RS6_RUNTIME_PACKAGE_MINIMIZATION` with exact safe action
`EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`; RS7 physical mutation is not admitted.
The same CPS Section 0 also contains contradictory high-level
`PRIMARY_ENGINEERING_FRONTIER=PROGRAM_COMPLETE` and
`PRIMARY_ENGINEERING_NEXT_ACTION=NONE_RESET_PROGRAM_TERMINAL` fields. This audit does
not choose between contradictory projections or mutate CPS.

The retention result is a bounded input to the existing RS6 package disposition and,
after separate admission, RS7A/RS8 consumer migration, archival/deletion and RS9
physical shrink closure. Cleanup begins only after existing owners reconcile the CPS
projection, prove consumers and admit exact archive/delete candidates.

Final terminal:

`REPORT_EVIDENCE_RETENTION_REALITY_AUDITED_DISPOSITION_AND_ARCHIVE_PROOF_REQUIRED`

## Cleanup execution update — Batch 3

Batch 1 removed two generated cross-reference TSVs after preserving their
producer, hashes and compact conclusions. Batch 2 stopped tracking the
regenerable Understand Anything fingerprints/intermediate scan while retaining
the consumed `knowledge-graph.json` owner. Batch 3 resolved the two largest raw
Track 7 snapshots rather than deleting around their active consumer.

| Artifact | Before | After | Disposition |
| --- | ---: | ---: | --- |
| `e11_16-evidence/pre-ttl-snapshot.txt` | `59,566,997` bytes | `840` bytes | compact receipt at the same existing path; exact TTL field preserved |
| `e12-evidence/full-orchestration-snapshot-corrected.txt` | `20,284,392` bytes | `875` bytes | compact receipt at the same existing path; consumer needs presence only |

Original hashes are recorded in the receipts. Both originals are restorable
from Git history and from the ignored local archive
`.v7/evidence-archive/2026-08-14-batch3/track7-large-raw-snapshots.tar.gz`
with SHA-256
`7d42f9dee7ecd3bd45b787eb829e30d157a065df141dfd2e32e03406ea9df46a`.

Fresh before/after execution of the existing
`tools/v7-control-plane-governance-check` compared all `34` E11.16/E12 output
fields and produced `0` semantic differences. The E11 TTL remains `81917`;
both artifact-completeness projections remain true. No tool, owner, registry,
truth source or parallel archive system was added.

Measured active-tree reduction in this batch: `79,849,674` bytes. Runtime,
Production, routing, user, policy and Authority effects: `NONE`.

## Cleanup execution update — Batch 4

Five additional raw historical Track 7 snapshots were archived locally and
replaced in place by compact receipts bound to their existing consumers:

| Artifact | Original bytes | Consumer contract retained |
| --- | ---: | --- |
| E9.4.4 runtime journal | `13,643,090` | presence only; bounded extract/report owns semantics |
| E11.14 full Runtime snapshot | `12,221,984` | historical timeline pointer only |
| E11.2 WireGuard truth | `10,333,049` | presence only; approval report owns semantics |
| E9.3.9 Planner observation | `10,080,389` | `selected_moves=[]` |
| E9.4.1 post-policy snapshot | `8,937,424` | four safety PASS markers plus `selected_moves=[]` |

The ignored recovery archive is
`.v7/evidence-archive/2026-08-14-batch4/track7-raw-snapshots.tar.gz`,
SHA-256
`973703a481424b21657e60ac0200c7a77e2de74ee26be3d5258d3d65f9cf586e`.
Every receipt preserves the original content hash, byte/line count, existing
consumer and exact minimal contract.

Full before/after output comparison of
`tools/v7-control-plane-governance-check` found no semantic difference. The
only JSON delta was the expected volatile `generated_at` timestamp. Measured
active-tree reduction: `55,213,419` bytes. Runtime, Production, routing, user,
policy and Authority effects: `NONE`.

## Cleanup execution update — Batch 5

Eleven more large Track 7 runtime/planner snapshots were reduced to compact
receipts after their real consumers were checked by meaning, not by filename.
The batch includes the E11.3 execution/pre-gate context, E9.4/E9.4.2 restore
observations, E10/E10.3 runtime truth, E11.9/E11.10 drain/closeout context,
E9.3.6 autoswitch snapshot, E11.1 governance snapshot and E11.3 switch-history
context.

Original total: `72,291,046` bytes. Compact receipts: `6,335` bytes. Measured
active-tree reduction: `72,284,711` bytes. Every receipt records its original
path, SHA-256, byte/line count and archive hash. The ignored restorable archive
is `.v7/evidence-archive/2026-08-14-batch5/track7-raw-snapshots.tar.gz`,
SHA-256
`424d691b6ee96004caa84f41b2a87dd786731fcad54f8b64fd99808b70208edf`.

The E9.3.6 receipt additionally preserves the four exact safety markers
consumed by the governance checker. Full before/after checker comparison has
`0` semantic differences after excluding only the volatile `generated_at`
timestamp. Runtime, Production, routing, user, policy and Authority effects:
`NONE`.
