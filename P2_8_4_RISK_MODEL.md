# P2.8.4 Risk Model

Project: V7 Vozduh
Block: P2.8.4

| Package | Risk | Blast Radius | Rollback Complexity | Verification Complexity | Approval Requirement |
| --- | --- | --- | --- | --- | --- |
| Runtime Read APIs | High | Admin API execution visibility | Medium | High | owner review |
| Draft + Validation Preview | High | execution preparation surfaces | Medium | High | code review plus tests |
| Simulation + Rollback Preview | Medium/High | preview/readiness surfaces | Medium | Medium/High | code review |
| Candidate Workflow | High | operator workflow and approval views | Medium | High | product/governance review |
| UI Integration | Medium | `/admin-v2` operator UX | Low/Medium | Medium | UI review |
| Tests + Documentation | Medium | release confidence | Low | Medium | reviewer signoff |
| Branch/Release Governance | High | release truth and deploy safety | Medium | Medium | repository owner approval |

## Critical Failure Modes

- Losing runtime-only execution read APIs.
- Deploying local-only preview code without review.
- Treating `main` as current Admin API source.
- Copying runtime config/state into Git.
- Creating convergence branch from the wrong base.
