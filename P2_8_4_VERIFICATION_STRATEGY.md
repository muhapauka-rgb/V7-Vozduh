# P2.8.4 Verification Strategy

Project: V7 Vozduh
Block: P2.8.4

| Package | Verification Method | Success Criteria | Rollback Criteria | Proof Requirements |
| --- | --- | --- | --- | --- |
| Runtime Read APIs | route diff, unit/API read tests, non-executable assertion | all runtime read APIs preserved | any runtime-only API lost | route inventory, tests, hash diff |
| Draft + Validation Preview | unit tests for drafts/gates, fail-closed tests | preview-only outputs, no execution path | any mutating side effect | test logs, route inventory |
| Simulation + Rollback Preview | deterministic fixtures, retention checks | previews derive from read models only | non-deterministic or mutating output | fixture results, fail-closed proof |
| Candidate Workflow | P2.7 candidate tests, API consistency tests | states and timeline consistent | duplicate candidate store or execution hook | test output, schema examples |
| UI Integration | static JS hook scan, browser smoke in future non-runtime env | all drawers open, no missing API refs | dead route/UI hook | screenshots or smoke logs |
| Tests + Documentation | `git diff --check`, unit tests, report checklist | no whitespace drift, docs complete | missing verdict/safety flag | command outputs |

verification_strategy_defined=true
