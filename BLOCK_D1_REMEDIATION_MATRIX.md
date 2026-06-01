# Block D1 Remediation Matrix

Project: V7 Vozduh

Block: D1 - Autoswitch Safety Remediation And Decision Tree

Date: 2026-06-01

| Issue | Root Cause | Severity | Fix | Risk | Next Action |
| --- | --- | --- | --- | --- | --- |
| Safety review critical | Registry parser expects two-column value format | High | Parse KV registry lines and read `enabled` | Low | Patch safety-review parser |
| No enabled egress detected | Safety review interpretation bug | High | Reuse shared KV parser style | Low | Add unit regression |
| Planner 12 failovers | Execution cohort current target is not autoswitch-eligible | Medium | Add governance hold/exclusion semantics | Medium | Shadow retry after cap |
| Planner too broad | Raw planner has no operator proposal cap | High | Add proposal cap and packet builder | Medium | Start budget=1 |
| Target full | Execution target at hard limit `10` | High | Create/certify second execution target | Medium | D2 target program |
| Admin API unavailable | Control-plane health down | Medium | Restore or explicitly decouple approval | Medium | Admin health remediation |
| Trust needs attention | Trusted RU path incomplete | Medium | Keep as blocker for sensitive routes | Medium | Separate trust remediation |
| Rollback all to egress 1 risky | Egress `1` hard limit low | Medium | Avoid rollback unless required | Medium | Keep current cohort held |

## Verdict

`remediation_matrix_complete=true`

