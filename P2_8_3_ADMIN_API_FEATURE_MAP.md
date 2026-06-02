# P2.8.3 Admin API Feature Map

Project: V7 Vozduh
Block: P2.8.3

## Classification Key

- Runtime Only: present in live runtime but absent from committed GitHub baseline.
- Local Only: present in local dirty worktree but absent from live runtime.
- GitHub Only: present in GitHub but absent from runtime/local.
- Shared: present across relevant runtime/local/GitHub baseline.

## Feature Inventory

| Feature | Classification | Purpose | Owner | Storage | API | UI | Tests | Dependencies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Admin health/auth shell | Shared | serve admin UI and authenticated APIs | Admin API | auth/config files | `/health`, login/admin routes | admin shell | existing manual/runtime checks | `http.server`, auth helpers |
| Runtime execution summary | Runtime Only | read-only execution contract/event visibility | Runtime Admin API | `execution-contracts.json`, `execution-events.jsonl` | `/api/execution/summary` | execution summary drawer | not proven in Git | `json`, `jsonl`, sanitizers |
| Runtime execution contracts | Runtime Only | list/detail contracts already known to runtime | Runtime Admin API | execution contract store | `/api/execution/contracts`, `/api/execution/contracts/` | contract drawer | not proven in Git | execution normalization helpers |
| Runtime execution events | Runtime Only | read execution event timeline | Runtime Admin API | execution event store | `/api/execution/events`, `/api/execution/timeline` | timeline HTML | not proven in Git | event helpers |
| Runtime verification/rollback/explain | Runtime Only | read verification and rollback state | Runtime Admin API | contract/event derived read model | `/api/execution/verification`, `/api/execution/rollback`, `/api/execution/explain` | execution detail drawer | not proven in Git | read-only derivation |
| Execution draft contracts | Local Only | create non-executable contract drafts from proposals | Local P2.2 | proposal/evidence stores | `/api/execution/contracts/draft` | draft drawer | local test intent | proposal/evidence readers |
| Validation preview | Local Only | preview validation gates without execution | Local P2.3 | adapter-derived read models | `/api/execution/validation-preview`, `/api/execution/gates` | gate drawer | local test intent | readiness adapters |
| Verification preview | Local Only | preview verification checks | Local P2.3/P2.4 | derived read model | `/api/execution/verification-preview` | detail panels | local test intent | validation model |
| Rollback preview/impact | Local Only | preview rollback readiness and blast radius | Local P2.4/P2.5 | derived from draft/contract | `/api/execution/rollback-preview`, `/api/execution/rollback-impact` | rollback panels | local test intent | rollback manifests |
| Outcome simulation | Local Only | non-executable simulation and service impact | Local P2.5 | derived read model | `/api/execution/outcome-preview`, `/api/execution/blast-radius`, `/api/execution/service-impact`, `/api/execution/readiness-forecast` | simulation panels | local test intent | service matrix/readiness |
| Candidate pipeline | Local Only | candidate review and risk/readiness views | Local P2.6 | derived from drafts/proposals | `/api/execution/candidates`, `/api/execution/candidates/*` | candidate drawer/list | local test intent | candidate helpers |
| Candidate approval center | Local Only | approval/governance/rehearsal/workflow views | Local P2.7 | derived candidate models | `/api/execution/candidate-approval`, `/api/execution/candidate-governance`, `/api/execution/candidate-rehearsal`, `/api/execution/candidate-workflow` | candidate workflow UI | `tests/unit/test_p2_7_candidate_workflow.py` local/untracked | P2.7 bridge helpers |
| Operator overview/timeline/evidence | Shared | operator read-only observability | Runtime/Local/Updatesystem | evidence/proposal/runtime trust stores | `/api/operator/*`, `/api/evidence/*`, `/api/proposals/*` | operator panels | existing local/manual | `admin_core.events`, evidence/proposal helpers |
| Runtime/release trust | Shared | convergence and release trust visibility | Runtime/Local/Updatesystem | trust JSONL stores | `/api/runtime/*`, `/api/release/*` | trust cards/drawers | existing local/manual | trust store readers |
| Governance preview | Shared | preview operator governance without execution | Runtime/Local/Updatesystem | derived read model | `/api/operator/execution-governance-preview` | governance drawer | existing local/manual | operator helpers |
| Rehearsal preview | Shared | preview execution rehearsal without execution | Runtime/Local/Updatesystem | derived read model | `/api/operator/execution-rehearsal-preview` | rehearsal drawer | existing local/manual | operator helpers |
| Main branch admin baseline | GitHub Only relative to release policy | default branch history | GitHub `main` | committed Git object | older route set | older UI | historical | GitHub branch |

feature_map_complete=true
