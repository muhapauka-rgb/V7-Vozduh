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

## Cleanup execution update — Batch 6

The ignored local directory `.understand-anything/.trash-1786636987` was
classified as `KEEP_LOCAL_GENERATED_EXCLUDED_FROM_GIT` residue, not as a
knowledge-graph owner. It had no tracked files, no repository-visible
consumer references and is excluded by the existing
`.understand-anything/.gitignore` rule. The retained
`.understand-anything/knowledge-graph.json` remains present and non-empty.

The local trash directory was removed: `24,064 KiB -> 0 KiB`. This is a
workspace-cache reduction only: tracked-path delta `0`, Git-history delta
`0`, Runtime/Production/routing/user/Authority effects `NONE`, and no archive
was required because the data was regenerated trash rather than retained
evidence. The next Evidence Cleanup candidate must again prove its own
consumer, archive/restore and compact-knowledge disposition; Batch 6 creates
no deletion rule for other generated outputs.

## Cleanup execution update — Batch 7

`docs/channel_truth_1/evidence/autoswitch_planner_preview.json` was a
`6,753,352`-byte historical dry-run Planner observation. It has no current
source, test or Runtime consumer: its only direct consumers are three
historical reports that require the dry-run operation identity, aggregate
decision outcome and a historical user-level counterexample. It is therefore not
`OBSOLETE_DELETE`; it is `ARCHIVE_EXTERNAL` with a compact evidence projection
at the unchanged path.

The original is recoverable from the ignored local archive
`.v7/evidence-archive/2026-08-14-batch7/autoswitch-planner-preview.tar.gz`
(`SHA-256 2e26d2a20e64cf33d3eebc01c66f379abba1137a7d3ec54a3a5477618b2fa79e`)
and its source hash is
`c7d6d2a7cd89fff4ce8d40c5255494ee79b1acca2be821fb4d9d560928bbb05d`.
Archive extraction reproduced that source hash before replacement.

The compact receipt retains the operation and Planner generation identifiers,
terminal `DRY_RUN` outcome, the 26-user/18-selected-move summary and all
three route-group outcomes. Exact per-user historical observations remain
recoverable only from the hash-bound local archive; the compact Git receipt
does not replicate internal user addresses. The active-tree size changed
`6,753,352 -> 2,046` bytes, a `6,751,306`-byte reduction. Runtime,
Production, routing, user, policy and Authority effects: `NONE`.

## Cleanup execution update — Batch 8

`CTR_FINAL_EVIDENCE` contained nineteen intermediate historical observations:
nine `production_dry_run_02` through `_10` snapshots and ten API-wrapper
snapshots. Static reference reconciliation found no source, test, deploy or
Runtime consumer. Their only references were historical inventory listings;
the certification's decision-bearing inputs remain at their existing paths:
the primary dry-run (`_01`), `production_observation_window.json`, convergence
and truth evidence, and `CTR_FINAL_CERTIFICATION_REPORT.md`.

The nineteen intermediate files were moved out of active Git only after exact
archive restoration. Their original aggregate is `84,397,669` bytes and is
recoverable from the ignored archive
`.v7/evidence-archive/2026-08-14-batch8/ctr-final-intermediate-snapshots.tar.gz`
with SHA-256
`62187ca8d52cef254179965a33ffd3d07adaefcfbf0795be1a24352e64fa90cf`.
The colocated ignored `source-sha256sums.txt` passed for all nineteen files
after a clean extraction. This is `ARCHIVE_EXTERNAL`, not logical exclusion:
the active-tree physical reduction is exactly `84,397,669` bytes; no
conclusion, certification summary, source owner or archive/recovery path was
deleted. Runtime, Production, routing, user, policy and Authority effects:
`NONE`.

## Cleanup execution update — Batch 9

Nine large BA2 intermediate Planner, dry-run and policy-response snapshots
were `ARCHIVE_EXTERNAL` candidates. The two BA2 historical reports preserve
the decision-bearing facts (two-user selection, restore-barrier mismatch,
safety revert and final PASS), while the current source, tests, deployment and
Runtime have no consumer of these historical raw files. Existing compact BA2
summaries, truth/convergence gates and the certification report remain in Git.

The exact originals total `37,394,118` bytes. They were restored and checked
against all nine source SHA-256 records before active-tree removal. The
ignored archive is
`.v7/evidence-archive/2026-08-14-batch9/ba2-intermediate-runtime-snapshots.tar.gz`
with SHA-256
`15c1ad7011eab34f535fe509461fdd09fffabd5a31c3092ed5a99324d5fafe67`;
the associated ignored checksum file is the restoration manifest. This is a
physical active-tree reduction of `37,394,118` bytes, not a claim that the
underlying historical evidence was deleted. Runtime, Production, routing,
user, policy and Authority effects: `NONE`.

## Cleanup execution update — Batch 11

Seven `AUTONOMY_CANARY_1A` Planner observations were historical, no-mutation
`DRY_RUN` outputs. Each records the same Planner generation and structural
summary: `26` users, `7` egresses, `4` healthy egresses, `18` candidate moves,
`0` selected moves and `apply=false`. Their direct consumers are the
historical 1A report and xref index; there is no source, test, deploy or
Runtime consumer. Their referenced paths are retained unchanged as compact
JSON receipts, so those historical consumers keep the operation identity,
terminal reason, source hash, archive location and decision-bearing summary.

The originals total `33,783,083` bytes; compact receipts total `5,721` bytes,
for an active-tree reduction of `33,777,362` bytes. The ignored recovery
archive is
`.v7/evidence-archive/2026-08-14-batch11/autonomy-canary-1a-planner-observations.tar.gz`
with SHA-256
`f2c29f72f38073cc976ac6b2fd4288bb7a19d42f97a4fc0a06fb2930ab2a0559`.
All seven originals were byte-compared with a clean archive extraction before
replacement. This is `ARCHIVE_EXTERNAL`, not a claim that any historical
conclusion was deleted. Runtime, Production, routing, user movement, policy
and Authority effects: `NONE`.

## Cleanup execution update — Batch 12

Two `AUTONOMY_CANARY_1B` post-deploy Planner observations are historical
`DRY_RUN` evidence: both preserve the same generation, `26` users, `7`
egresses, `2` healthy egresses, `8` candidate moves, `0` selected moves and
`apply=false`. Their only consumers are later historical 1C inventory records
and the cross-reference index; no source, test, deploy or Runtime consumer
reads their full payload. The existing evidence paths now contain compact JSON
receipts with operation identity, terminal reason, source SHA-256 and summary.

The original total was `10,001,187` bytes; receipts total `1,633` bytes, for
an active-tree reduction of `9,999,554` bytes. Clean archive extraction was
byte-compared before replacement. The ignored recovery archive is
`.v7/evidence-archive/2026-08-14-batch12/autonomy-canary-1b-planner-observations.tar.gz`
with SHA-256
`611e1dbbe2b98f3b33528dce55e502f6c065dbfbbf9ec4800e6e8524bafe262d`.
Runtime, Production, routing, user movement, policy and Authority effects:
`NONE`.

## Cleanup execution update — Batch 13

The `AUTONOMY_TIER1_GOVERNED_CANARY_READINESS` observation from
`2026-06-24` is historical, no-mutation `DRY_RUN` evidence. The raw payload
records operation `runtime_autoswitch_0ec504cee56cd0936f0766e7`, its existing
`tools/v7-users-autoswitch` owner, a zero selected-move result, `apply=false`,
and terminal reason
`dry_run_restore_barrier_clearance_selected_moves_exceed_budget`. Its direct
consumers are historical `truth_final.json`, `convergence_final.json`, and
the cross-reference index; no source, test, deploy or Runtime consumer reads
the full 5,391,621-byte payload. Those references remain at the exact same
path as a compact JSON receipt, preserving the operation identity, decision,
source hash, archive location and decision-bearing summary.

The original has SHA-256
`f4660dbfcefd0f3efa31202d4cd98b453f88f88b3f3d875ac9141ceb47cf0930` and is
recoverable from the ignored existing archive lifecycle at
`.v7/evidence-archive/2026-08-14-batch13/autonomy-tier1-governed-canary-observation.tar.gz`
(archive SHA-256
`a12bda9bbbaee8ae9c8aa5a74cee8d6fe1a0e3ecfc0bdf5f4fcde59ec54bcd88`). A
clean extraction was byte-compared before replacement. The 1,501-byte receipt
reduces the active tree by `5,390,120` bytes. This is `ARCHIVE_EXTERNAL`, not
deletion or a claim that historical evidence disappeared; restoration is
possible through the recorded archive and source hash. Runtime, Production,
routing, user movement, policy and Authority effects: `NONE`.

## Cleanup execution update — Batch 14

Two related `AUTONOMY_TIER1_GOVERNED_CANARY_READINESS` observations are
historical, no-mutation `DRY_RUN` evidence. Both retain the existing
`tools/v7-users-autoswitch` owner, Planner generation, `observe` mode,
`apply=false`, zero selected moves and terminal reason
`dry_run_restore_barrier_clearance_generation_expired`. The ordinary canary
observation recorded `26` candidates; the WireGuard-target observation
recorded `0`. Their only consumers are historical `truth_final.json`,
`convergence_final.json` and the cross-reference index; no source, test,
deploy or Runtime consumer requires their full payloads. Existing references
remain unchanged at compact JSON receipts carrying the decision-bearing
operation and summary facts.

The originals total `10,778,977` bytes. They are recoverable from the ignored
existing archive lifecycle at
`.v7/evidence-archive/2026-08-14-batch14/autonomy-tier1-canary-observations.tar.gz`
(SHA-256
`6d31f1ad3d5a5d06d945773c17cfeedd6af32c1d07f2932e573e01cac0a23ae6`).
Their individual source hashes are recorded in their receipts; clean archive
extraction was byte-compared before replacement. Compact receipts total
`2,888` bytes, reducing the active tree by `10,776,089` bytes. This is
`ARCHIVE_EXTERNAL`, not deletion: restoration requires archive extraction and
source-hash verification. Runtime, Production, routing, user movement, policy
and Authority effects: `NONE`.

## Cleanup execution update — Batch 15

The post-deploy observation for `AUTONOMY_REAL_OUTCOME_COLLECTION` is historical
no-mutation evidence. It records operation
`runtime_autoswitch_ce4804d6deebc84aba227384`, the existing
`tools/v7-users-autoswitch` owner, `observe` mode, `apply=false`, `26`
candidates, zero selected moves and terminal reason
`dry_run_restore_barrier_clearance_generation_expired`. Its full raw payload
is referenced only by the historical mission report and cross-reference index;
that report already retains the decision-bearing outcome and confidence
conclusions. No source, test, deploy or Runtime consumer requires the full
payload. The existing evidence path therefore remains as a compact receipt
with its operation identity, conclusion-bearing summary, source hash and
recoverable archive pointer.

The original is `5,391,059` bytes with SHA-256
`baf5ba02eeabf18a076be0ff1712953a5ad65d44c588df46e59d92ef2fb783a7`.
The ignored archive is
`.v7/evidence-archive/2026-08-14-batch15/autonomy-real-outcome-observation.tar.gz`
with SHA-256
`b738970f36fdfb23fa86f602e9b3e788dd1efff329f65249358ba2b111b20b09`.
Clean extraction was byte-compared before replacement. The `1,331`-byte
receipt reduces the active tree by `5,389,728` bytes. This is
`ARCHIVE_EXTERNAL`, not deletion; restoration requires archive extraction and
source-hash verification. Runtime, Production, routing, user movement, policy
and Authority effects: `NONE`.

## Cleanup execution update — Batch 16

The two `AUTONOMY_SOURCE_CONFIDENCE_REALITY_AUDIT` Planner observations are
historical no-mutation `DRY_RUN` evidence. Both record the existing
`tools/v7-users-autoswitch` owner, `observe` mode, `apply=false`, `26` users,
`7` egresses, `2` healthy egresses, `10` candidates and zero selected moves.
Their distinct operation identities are retained in the receipts; both ended
with `dry_run_restore_barrier_clearance_generation_expired`. The historical
confidence-audit report already retains the decision-bearing conclusion about
forecast source confidence. Its only other consumer is the cross-reference
index; there is no source, test, deploy or Runtime consumer of the full raw
payload. Existing paths therefore remain compact receipts.

The originals total `10,752,120` bytes. They are recoverable from the ignored
existing archive lifecycle at
`.v7/evidence-archive/2026-08-14-batch16/autonomy-source-confidence-observations.tar.gz`
(SHA-256
`583b45f36dd9ef281e5d44d69dfa32ec569c767ef396cf99087f49f82ebde549`).
The individual source hashes are retained in the receipts and clean archive
extraction was byte-compared before replacement. Receipts total `2,434` bytes,
reducing the active tree by `10,749,686` bytes. This is `ARCHIVE_EXTERNAL`,
not deletion; restoration requires archive extraction and source-hash
verification. Runtime, Production, routing, user movement, policy and
Authority effects: `NONE`.

## Cleanup execution update — Batch 17

Two historical `tools/v7-users-autoswitch` dry-run wrapper payloads were
checked before compaction. Both had `apply_requested=false`, zero selected
moves, and a terminal dry-run reason. Their only path references are the
historical stability report and the existing cross-reference audit; no source,
test or Runtime consumer reads the full payload. The original paths remain as
compact receipts with operation identity, planner generation, terminal reason,
selected-move count, source hash and archive pointer.

| Receipt | Original bytes | Receipt bytes | Original SHA-256 |
|---|---:|---:|---|
| `POOL2_EVIDENCE/api_autoswitch_plan.json` | 5,270,640 | 992 | `7b28f5c7d81f9dd9aa64a6b4f21effdd369018510b0c9cf35f2fe0fe51ac26ef` |
| `EXEC1_EVIDENCE/autoswitch_plan_raw.json` | 5,256,361 | 1,003 | `3a6613cc1fc873a05a48602172e2d4f79f44ee6dd30860f889d784460b1f9baf` |

The originals are recoverable from the ignored existing archive lifecycle at
`.v7/evidence-archive/2026-08-14-batch17/planner-dry-run-wrappers.tar.gz`
(archive SHA-256
`38f476c9097ccaa6dfd5e8110fb664e48babd99a56f664f364f4429a28bbd466`).
Active-tree reduction: 10,525,006 bytes before
archive overhead). This is `ARCHIVE_EXTERNAL`, not deletion. Runtime,
production, routing, user movement, policy, Authority and Production Maturity
effects: `NONE`.

## Structural inventory — 2026-08-14

The repository was re-measured before any further deletion or relocation. The
inventory confirms that age alone is not a safe retention rule:

| Surface | Files | Bytes | Initial disposition |
|---|---:|---:|---|
| `docs/programs` | 17 | 1,847,959 | keep canonical |
| `docs/reference` | 34 | 1,514,163 | keep canonical |
| `docs/reports/engineering` | 906 | 33,984,016 | retain compact mission/closure reports; classify raw payloads |
| `docs/reports/research` | 57 | 18,770,954 | retain decision-bearing research; classify payloads |
| `docs/track7` | 3,539 | 121,148,577 | retain consumer-required receipts; archive raw outputs |
| root `*_EVIDENCE` directories | 180 | 542,284,642 | disposition by owner/reference/consumer, never by age alone |

The current Git tree contains 8,863 tracked files and 817,312,657 bytes. A
30-day mtime filter reports 999 old report files, but mtime is not evidence
age, lifecycle state, or consumer reachability. No mass deletion is therefore
admitted.

The next cleanup batch is restricted to root evidence payloads that satisfy all
of the following existing-owner checks: no source/test/Runtime consumer reads
the full payload; a decision-bearing report or receipt already preserves the
identity and conclusion; a byte-verifiable archive pointer can be created;
and the original path can remain as a compact receipt when a historical
consumer references it. Any item failing one check remains
`UNKNOWN_REQUIRES_OWNER_REVIEW`.

This inventory is a read-only disposition result. It authorizes neither
program deletion nor Git-history rewriting. The next safe action is a bounded
candidate scan of the 180 root evidence directories, followed by a separately
reviewable archive/compact-receipt batch. Runtime, production, routing, user,
Authority and Production Maturity effects: `NONE`.

## Cleanup execution update — Batch 18

An additional 18 historical planner JSON payloads were checked by semantics,
not by age. Every item had `apply_requested=false`,
`selected_move_count=0`, and no exact path reference from source, tests or
Runtime. Existing historical consumers can continue to read the original paths
because each path now contains a compact receipt preserving operation identity,
generation, terminal reason, source hash and archive pointer.

The originals total `90,124,919` bytes. They are recoverable from the ignored
archive
`.v7/evidence-archive/2026-08-14-batch18/zero-selection-dry-runs.tar.gz`
(SHA-256
`b435e04262a9468bb3f99290dd506a0cc66f5a09681e5a5a1839bec73cc9c83e`).
The receipts are approximately 20 KB in total. This is `ARCHIVE_EXTERNAL`,
not deletion. Runtime, production, routing, user movement, policy, Authority
and Production Maturity effects: `NONE`.

## Cleanup execution update — Batch 19

Nine historical planner dry-runs with available selected moves were checked
against the same owner/reference rule. They were all `apply_requested=false`,
had no active source/test/Runtime path reference, and their decision-bearing
counts and terminal reasons are now preserved in compact receipts. This is
not a certification invalidation and does not erase the archived selected-move
details.

The originals total `44,583,434` bytes. They are recoverable from
`.v7/evidence-archive/2026-08-14-batch19/selected-moves-dry-runs.tar.gz`
(SHA-256
`24e15a76673ed2fcdc0032f96479739f4664caab98cf5d19e543dd3160f08720`).
Active-tree reduction before archive overhead is approximately `44.56 MB`.
Disposition: `ARCHIVE_EXTERNAL`; runtime, production, routing, user movement,
policy, Authority and Production Maturity effects: `NONE`.

## Archive purge — 2026-08-14

Per explicit operator instruction, the local raw-evidence archives for cleanup
batches 3–5, 7–20 were permanently removed. The compact receipts and this
report remain; the archived raw payloads are no longer recoverable locally.
This purge affects repository evidence copies only and has no Runtime,
production, routing, user, policy, Authority or Production Maturity effect.

## Cleanup execution update — Batch 20

Fifteen additional historical zero-selection planner payloads were compacted.
Each had `apply_requested=false`, `selected_move_count=0`, and no direct
source/test/Runtime reference. Their terminal reasons and operation lineage
remain in receipts; full payloads remain recoverable in the archive.

Original total: `54,226,825` bytes. Archive:
`.v7/evidence-archive/2026-08-14-batch20/zero-selection-dry-runs-large.tar.gz`
(SHA-256
`c91760f1e9918c937dfe88860fcbbc9cc7d0b989bb84d4edc439f6a8b27520d6`).
Disposition: `ARCHIVE_EXTERNAL`; no Runtime, production, routing, user,
policy, Authority or Production Maturity effect.
