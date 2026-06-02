# P2.8.5 Blockers

Project: V7 Vozduh
Block: P2.8.5

## Open Blockers

| Blocker | Blocks branch work? | Blocks deploy/runtime work? | Status |
| --- | --- | --- | --- |
| Runtime Admin API source lineage UNKNOWN | no, if preserved as runtime patch evidence | yes | known |
| Local Admin API dirty and unreviewed | no, if treated as candidate package source | yes | known |
| `main` behind runtime/local | no, if not used as convergence base | yes, for release | known |
| Remote-only `codex/dynamic-load-autoswitch-pr` not locally materialized | no, if inspected before archive | no direct deploy blocker | known |
| Runtime-only execution read APIs not committed | no, they are Wave 1 | yes | known |
| No deploy manifest | no | yes | known |

## Unknowns

No new unclassified feature was discovered in P2.8.5. Remaining unknowns are lineage/provenance unknowns already documented.

## Decision

Blockers are sufficient to prevent deploy/runtime work. They do not prevent starting a constrained convergence branch preparation phase whose first wave preserves runtime-only behavior.

blockers_identified=true
