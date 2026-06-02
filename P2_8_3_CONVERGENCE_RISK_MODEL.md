# P2.8.3 Convergence Risk Model

Project: V7 Vozduh
Block: P2.8.3

| Candidate | Risk | Blast Radius | Rollback Complexity | Verification Requirement | Approval Requirement |
| --- | --- | --- | --- | --- | --- |
| Whole runtime file becomes repo source | High | entire Admin API | High | full route/UI/API diff and secret scan | explicit owner approval |
| Whole local file becomes repo source | High | entire Admin API and future deploy | High | full unit/API tests and runtime-only preservation check | explicit owner approval |
| Hybrid runtime read APIs plus local P2 work | Medium/High | Admin API execution/operator surfaces | Medium | route matrix, feature tests, fail-closed tests | review approval |
| Feature-by-feature migration | Medium | bounded per feature | Low/Medium | per-feature tests and diffs | staged approval |
| Direct deploy after convergence | Critical | live admin/runtime behavior | High | preflight, backup, deploy manifest, post-deploy hash | separate deploy block approval |
| Branch default switch | High | release governance | Medium | branch policy review | repository owner approval |

## Highest Risk

The highest risk is losing runtime-only execution read APIs by replacing runtime with a GitHub branch, or deploying unreviewed local preview code directly.
