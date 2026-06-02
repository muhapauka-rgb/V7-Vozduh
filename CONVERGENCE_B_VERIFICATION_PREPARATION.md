# Convergence B Verification Preparation

Project: V7 Vozduh
Block: Convergence B

| Package | Success criteria | Rollback criteria | Proof requirements |
| --- | --- | --- | --- |
| Runtime Read APIs | all eight runtime execution read routes present; all responses read-only | any missing runtime route or mutating behavior | route inventory, API tests, read-only assertions |
| Execution Draft + Validation | draft/validation APIs fail closed and do not execute | execution hook or mutation path found | unit tests, route diff, schema examples |
| Simulation + Rollback | simulation and rollback previews deterministic and preview-only | non-deterministic or mutating output | fixtures, output snapshots |
| Candidate Workflow | candidate states/timeline/approval/governance/rehearsal consistent | duplicate store or broken lifecycle | candidate tests, retention checks |
| UI Integration | UI hooks point to existing APIs and render safely | missing API route, JS error, dead drawer | static hook scan, browser/local smoke |
| Tests + Docs | tests/docs cover every package and safety verdict | missing package proof | test logs, reports, verdict checklist |

verification_preparation_complete=true
