# Convergence B Package Preparation

Project: V7 Vozduh
Block: Convergence B

| Package | Dependencies | Risks | Verification requirements |
| --- | --- | --- | --- |
| Package 1: Runtime Read APIs | execution stores, normalization helpers, auth/role map, UI drawer hooks | losing runtime behavior, copying state into Git | route inventory, API tests, read-only assertions |
| Package 2: Execution Draft + Validation | proposal/evidence readers, readiness adapters, Package 1 contract IDs | accidental execution semantics, duplicate readiness model | fail-closed tests, no mutation tests |
| Package 3: Simulation + Rollback | draft model, service matrix, rollback manifests | overlap with rehearsal/rollback read APIs | deterministic fixtures, impact preview tests |
| Package 4: Candidate Workflow | draft/simulation/readiness outputs, P2.7 candidate helpers | duplicate approval/workflow concepts | candidate state tests, retention/archive tests |
| Package 5: UI Integration | API packages 1-4, `/admin-v2` existing patterns | dead UI hooks, route mismatch | static JS hook scan, browser smoke in future local env |
| Package 6: Tests + Docs | all packages, reports, route inventory | noisy docs, missing proof | curated docs, unit/API tests, final package report |

package_preparation_complete=true
