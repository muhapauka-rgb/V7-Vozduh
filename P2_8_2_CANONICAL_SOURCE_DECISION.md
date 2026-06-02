# P2.8.2 Canonical Source Decision

Project: V7 Vozduh
Block: P2.8.2

## Decision Table

| Domain | Canonical decision | Reason |
| --- | --- | --- |
| Canonical Runtime Source | `/usr/local/bin/v7-admin-api` hash `8d7adc4d81f625c143ac4f227185c2b7e8708b511c01205c61b8905cbf3c1c04` for current live behavior only | runtime reality wins for deployed behavior |
| Canonical Development Source | `origin/Updatesystem` as committed baseline; local dirty `admin/v7-admin-api` as candidate patch only | local dirty work is not authoritative until reviewed/committed |
| Canonical GitHub Branch | `Updatesystem` for current V7 control-plane development | closest branch to runtime and active local upstream |
| Canonical Release Branch | `main` remains release/default branch until explicit branch governance changes it | GitHub default branch is `main` |
| Canonical Admin API Source Of Truth | not fully certified | runtime hash is not present in Git history |

## Practical Rule

- Use runtime file/hash to describe what Admin API is doing now.
- Use `origin/Updatesystem` to describe the last committed development baseline.
- Use local dirty file only as a candidate convergence patch.
- Use `main` only as release/default branch history, not as current Admin API implementation truth.

canonical_source_defined=true
safe_to_continue=false
