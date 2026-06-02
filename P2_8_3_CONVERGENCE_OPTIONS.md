# P2.8.3 Convergence Options

Project: V7 Vozduh
Block: P2.8.3

## Option A: Runtime Becomes Source

Runtime Admin API is copied into repository as the source baseline.

| Dimension | Evaluation |
| --- | --- |
| Pros | preserves deployed behavior exactly; avoids losing production-only execution read APIs |
| Cons | imports UNKNOWN lineage; may overwrite reviewed local P2 work; risks committing runtime-specific assumptions |
| Risk | High |
| Required evidence | clean runtime capture, secret scan, diff review, owner approval |
| Verdict | Not recommended as whole-file strategy |

## Option B: Local Becomes Source

Local dirty `admin/v7-admin-api` becomes source baseline.

| Dimension | Evaluation |
| --- | --- |
| Pros | contains P2.2-P2.7 roadmap work; appears to be a superset of runtime route surface |
| Cons | uncommitted and unreviewed; not proven deployed; could alter runtime behavior if deployed directly |
| Risk | High |
| Required evidence | code review, tests, runtime-only feature preservation check |
| Verdict | Candidate only, not immediate canonical source |

## Option C: Hybrid Convergence

Preserve runtime-only execution read APIs and merge reviewed local P2 work onto `origin/Updatesystem`.

| Dimension | Evaluation |
| --- | --- |
| Pros | protects live runtime behavior while allowing P2 implementation to proceed; supports reviewable commits |
| Cons | requires careful manual diff reconciliation; more work than whole-file replacement |
| Risk | Medium/High |
| Required evidence | route/function matrix, tests, no-runtime-mutation review |
| Verdict | Recommended direction |

## Option D: Feature-by-Feature Convergence

Converge each subsystem independently: runtime read APIs, local previews, candidate workflow, UI, tests, docs.

| Dimension | Evaluation |
| --- | --- |
| Pros | smallest blast radius; best auditability; clean rollback per feature |
| Cons | longer roadmap; requires dependency ordering |
| Risk | Medium |
| Required evidence | feature packages and per-package tests |
| Verdict | Recommended execution method for Option C |

convergence_options_defined=true
