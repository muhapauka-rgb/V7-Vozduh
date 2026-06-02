# P2.8.3 Migration Package Design

Project: V7 Vozduh
Block: P2.8.3

## Runtime-Only Drift

| Drift | Preserve | Archive | Merge | Review | Reject |
| --- | --- | --- | --- | --- | --- |
| execution summary/contracts/events/timeline read APIs | yes | no | yes, into convergence branch | yes | no |
| execution verification/rollback/explain read APIs | yes | no | yes, or replace with local reviewed equivalent | yes | no |
| execution UI summary/contract drawers | yes | no | yes if still needed | yes | no |
| runtime file hash as behavior evidence | yes | yes as immutable evidence | no | yes | no |

## Local-Only Drift

| Drift | Preserve | Archive | Merge | Review | Reject |
| --- | --- | --- | --- | --- | --- |
| execution contract drafts | yes | no | after review | yes | no by default |
| validation/verification/rollback previews | yes | no | after review | yes | no by default |
| simulation/outcome/readiness forecast | yes | no | after review | yes | no by default |
| candidate approval/governance/rehearsal/workflow | yes | no | after review | yes | no by default |
| local untracked reports/evidence | yes | maybe later | docs package decision | yes | no by default |

## GitHub-Only Or Branch Drift

| Drift | Preserve | Archive | Merge | Review | Reject |
| --- | --- | --- | --- | --- | --- |
| `main` as default history | yes | no | not directly | yes | no |
| remote-only `codex/dynamic-load-autoswitch-pr` | preserve until inspected | likely after review | unlikely | yes | unknown |
| older feature branches | preserve until branch audit | likely | only if unique feature found | yes | unknown |

## Package Boundaries

1. Runtime read API preservation patch.
2. Execution draft and validation preview patch.
3. Simulation and rollback preview patch.
4. Candidate approval/workflow patch.
5. UI integration patch.
6. Tests and documentation patch.

migration_package_defined=true
