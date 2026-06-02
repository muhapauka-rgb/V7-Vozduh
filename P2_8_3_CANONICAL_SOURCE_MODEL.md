# P2.8.3 Canonical Source Model

Project: V7 Vozduh
Block: P2.8.3

## Model

| Subsystem | Canonical Runtime Source | Canonical Development Source | Canonical GitHub Source | Canonical Future Source |
| --- | --- | --- | --- | --- |
| Live Admin API behavior | runtime hash `8d7adc...` | not local | not GitHub | signed release artifact from convergence branch |
| Admin API committed baseline | not runtime | `origin/Updatesystem` | `origin/Updatesystem` | protected development branch |
| Release/default history | not runtime | not local | `origin/main` | release branch after explicit governance |
| Execution read APIs | runtime file | runtime patch captured into review branch | absent from `Updatesystem` | reviewed commit preserving runtime behavior |
| Execution draft/validation/simulation/candidate work | not runtime | local dirty file | absent from `Updatesystem` | reviewed feature commits |
| Operator governance/rehearsal | runtime file | local/Updatesystem | `origin/Updatesystem` | shared source after convergence |
| Runtime state/config | `/opt/v7`, `/etc/v7`, live process state | not repository | not repository | runtime manifest plus secret-safe config policy |

## Canonical Direction

Recommended canonical direction: Hybrid, feature-by-feature convergence.

Runtime behavior must be preserved as evidence. Development should proceed from `origin/Updatesystem`, with local P2 work split into reviewable patches and runtime-only execution read APIs backported or superseded deliberately.

canonical_source_model_defined=true
recommended_canonical_direction_defined=true
