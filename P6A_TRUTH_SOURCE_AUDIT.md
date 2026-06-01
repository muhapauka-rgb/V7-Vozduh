# P6.A Truth Source Audit

Project: V7 Vozduh

Block: P6.A

## Truth Source Map

| Domain | Canonical source | Derived source | Presentation source |
| --- | --- | --- | --- |
| User | `/opt/v7/egress/state/users.registry` | route movement preview, readiness review | P6.A reports/admin view |
| Channel | `/opt/v7/egress/state/egress.registry` | capacity/quality/readiness summaries | P6.A reports/admin view |
| Candidate | selected row from `users.registry` plus readiness result | `v7-second-canary-target-readiness` | candidate review |
| Movement | fresh movement packet | `v7-route-movement-preview` | movement packet design |
| Approval | fresh dual-operator packet fields and TTL | validation/recheck results | approval report |
| Rollback | original `current` egress and route table before movement | rollback preview | rollback design |
| Verification | runtime checkers and registry/route hashes | observation samples | final verification |
| Observation | live registry hashes, route table/rule hashes, selected moves, checker results | observation report | final report |

## Conflict Review

Repository historical reports were used only for architecture and precedent.

The P6.A candidate design uses fresh runtime facts from `/opt/v7/egress/state`:

- user candidate current state
- destination channel state
- selected moves
- capacity
- trust
- route preview
- readiness output

No truth-source conflict was found.

## Verdict

- truth_source_audit_complete=true
- truth_sources_clean=true
- stale_report_used_as_runtime_truth=false
- runtime_truth_source=/opt/v7/egress/state
