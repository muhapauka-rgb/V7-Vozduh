# P2.8.4 Package Classification

Project: V7 Vozduh
Block: P2.8.4

| Package | Runtime Source | Local Source | GitHub Source | Recommended Source | Status | Classification |
| --- | --- | --- | --- | --- | --- | --- |
| Runtime Read APIs | present and deployed | present as subset/superset | absent from `origin/Updatesystem` | runtime behavior preserved, reviewed into branch | production-only patch | Keep Runtime + Review + Merge |
| Execution Draft + Validation Preview | absent | present | absent | local after review | local-only candidate | Keep Local + Review |
| Simulation + Rollback Preview | partial rollback read model | present | partial/operator baseline | local plus runtime preservation | local-only/partial runtime | Merge + Review |
| Candidate Workflow | absent/partial | present | absent | local after review | local-only candidate | Keep Local + Review |
| UI Integration | runtime execution summary UI present | expanded local UI present | partial baseline | merged UI with runtime read API compatibility | split required | Merge + Review |
| Tests + Documentation | not runtime | local untracked | absent/uncommitted | curate into docs/test package | local-only | Review + Merge or Archive |
| Branch/Release Governance | runtime not branch authority | local planning docs | GitHub topology | policy docs only | planning-only | Review |

## Non-Recommended Classifications

- Replace runtime whole-file from GitHub: rejected for now because it would lose runtime-only execution read APIs.
- Replace runtime whole-file from local: rejected for now because it would deploy unreviewed P2 work.
- Archive runtime-only execution APIs: rejected unless a reviewed local equivalent replaces every API.

package_classification_complete=true
